#! coding: utf-8
from HTMLParser import HTMLParser
import re
import unicodedata
from urllib import quote, unquote
import urllib
from urlparse import urlparse, urlunsplit, urlsplit

from pyquery import PyQuery

from google_parser.exceptions import EmptySerp
import lxml.etree as ET


__all__ = ['GoogleParser']


RE_URL_PROTOCOL = re.compile(ur'^(?:http|https|ftp)://', re.X | re.I | re.U)
body_regexp = re.compile('(<body.*?</body>)', re.DOTALL)


def to_unicode(content, from_charset=None):
    u"""Безопасное приведение к юникоду

    :type  content: str
    :param content: текст
    :type  from_charset: str
    :param from_charset: Кодировка исходного текста

    :rtype: unicode
    :returns: текст, преобразованный в юникод
    """
    if type(content) == unicode:
        return content

    charsets = {
        'utf-8' : 'utf8',
        'utf8' : 'utf8',
        'cp1251' : 'cp1251',
        'cp-1251' : 'cp1251',
        'windows-1251' : 'cp1251',
        'win-1251' : 'cp1251',
        '1251' : 'cp1251',
        'русdows-1251': 'cp1251',
        'koi8-r' : 'koi8-r'
    }
    if type(from_charset) in (str, unicode):
        from_charset = str(from_charset.lower())

    try:
        from_charset = charsets[from_charset]
        return unicode(content, encoding=from_charset)

    except KeyError:
        for from_charset in ('utf8', 'cp1251', 'koi8-r', None):
            try:
                if from_charset is not None:
                    return unicode(content, encoding=from_charset)
                else:
                    return unicode(content)
            except UnicodeError:
                continue

        raise UnicodeError('Can not be converted to Unicode')

    except UnicodeError:
        return unicode(content, encoding=from_charset, errors='ignore')

def normalize(url, charset='utf-8'):
    def _clean(string):
        string = unicode(unquote(string), 'utf-8', 'replace')
        return unicodedata.normalize('NFC', string).encode('utf-8')

    default_port = {
        'ftp': 21,
        'telnet': 23,
        'http': 80,
        'gopher': 70,
        'news': 119,
        'nntp': 119,
        'prospero': 191,
        'https': 443,
        'snews': 563,
        'snntp': 563,
    }

    if isinstance(url, unicode):
        url = url.encode(charset, 'ignore')

    if url[0] not in ['/', '-'] and ':' not in url[:7]:
        url = 'http://' + url

    url = url.replace('#!', '?_escaped_fragment_=')

    scheme, auth, path, query, fragment = urlsplit(url.strip())
    (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

    scheme = scheme.lower()

    host = host.lower()
    if host and host[-1] == '.':
        host = host[:-1]
        # take care about IDN domains
    try:
        host = host.decode(charset).encode('idna')  # IDN -> ACE
    except Exception:
        host = host.decode(charset)

    path = quote(_clean(path), "~:/?#[]@!$&'()*+,;=")
    fragment = quote(_clean(fragment), "~")

    query = "&".join(["=".join([quote(_clean(t), "~:/?#[]@!$'()*+,;=") for t in q.split("=", 1)]) for q in query.split("&")])

    if scheme in ["", "http", "https", "ftp", "file"]:
        output = []
        for part in path.split('/'):
            if part == "":
                if not output:
                    output.append(part)
            elif part == ".":
                pass
            elif part == "..":
                if len(output) > 1:
                    output.pop()
            else:
                output.append(part)
        if part in ["", ".", ".."]:
            output.append("")
        path = '/'.join(output)

    if userinfo in ["@", ":@"]:
        userinfo = ""

    if path == "" and scheme in ["http", "https", "ftp", "file"]:
        path = "/"

    if port and scheme in default_port.keys():
        if port.isdigit():
            port = str(int(port))
            if int(port) == default_port[scheme]:
                port = ''

    auth = (userinfo or "") + host
    if port:
        auth += ":" + port
    if url.endswith("#") and query == "" and fragment == "":
        path += "#"
    return urlunsplit((scheme, auth, path, query, fragment))


def get_absolute_url(url):
    return normalize(url).replace('//www.', '//')


def get_full_domain_without_scheme(url):
    parsed = urlparse(get_absolute_url(url))
    return urlunsplit(('', parsed.netloc, '', '', '')).replace('//', '')


class GoogleSerpCleaner(object):
    flags = re.U | re.I | re.M | re.S

    _patterns = (
        ur'<script.*?<\/script>',
        ur'<style.*?<\/style>',
        ur'onmousedown=".*?"',
        ur'onclick=".*?"',
        ur'class=".*?"',
        ur'target="_blank"',
        ur'title=".*?"',
        ur'ondblclick=".*?"',
        ur'style=".*?"',
        ur'<i\s+><\/i>',
        ur'\s+tabindex="\d+"',
        ur'<noscript>.*?<\/noscript>',
        ur'<link.*?/>',
        ur'><!--.*?-->',
        ur'<i\s+><\/i>',
    )
    patterns = []
    for p in _patterns:
        patterns.append(re.compile(p, flags=re.U | re.I | re.M | re.S))
    patterns = tuple(patterns)

    no_space = re.compile(ur'\s+', flags=flags)

    @classmethod
    def clean(cls, content):
        content = content
        for p in cls.patterns:
            content = p.sub('', content)

        content = cls.no_space.sub(' ', content)
        return content

class GoogleParser(object):
    # Адрес картинки (src)
    captcha_regexp = re.compile(
        '<img src=\"([^\"]+)\"',
        re.DOTALL | re.IGNORECASE | re.UNICODE | re.MULTILINE
    )
    # Ключ картинки
    captcha_id_regexp = re.compile(
        '<input.*?name=\"id\".*?value=\"([^\"]+)\".*?>',
        re.DOTALL | re.IGNORECASE | re.UNICODE | re.MULTILINE
    )
    # Путь куда редиректить
    captcha_continue_regexp = re.compile(
        '<input.*?name=\"continue\".*?value=\"([^\"]+)\".*?>',
        re.DOTALL | re.IGNORECASE | re.UNICODE | re.MULTILINE
    )

    sorry_page_regexp = re.compile(
        '<title>Sorry...</title>',
        re.DOTALL | re.IGNORECASE | re.UNICODE | re.MULTILINE
    )
    
    def __init__(self, content, xhtml_snippet=False, snippet_fileds=('d', 'p', 'u', 't', 's', 'm')):
        self.content = to_unicode(content)
        self.xhtml_snippet = xhtml_snippet
        self.snippet_fileds = snippet_fileds

    def get_clean_html(self):
        return GoogleSerpCleaner.clean(self.content)

    def get_captcha_data(self):
        u"""Проверить наличие капчи на странице
        """

        is_captcha = bool(re.findall(
            '^.*?(<img src="/sorry/image).*', self.content,
            re.DOTALL | re.UNICODE | re.IGNORECASE
        ))
        if not is_captcha:
            return

        match_captcha = self.captcha_regexp.findall(self.content)
        if not match_captcha:
            return

        match_captcha_id = self.captcha_id_regexp.findall(self.content)
        match_captcha_coninue = self.captcha_continue_regexp.findall(self.content)

        return {
            'url': 'https://www.google.com' + match_captcha[0].replace('&amp;', '&'),
            'captcha_id': match_captcha_id[0],
            'captcha_coninue': match_captcha_coninue[0].replace('&amp;', '&')
        }

    def is_blocked(self):
        return bool(self.sorry_page_regexp.search(self.content))

    def get_serp(self):
        if self.is_not_found():
            return {'pc': 0, 'sn': []}
        
        pagecount = self.get_pagecount()
        snippets = self.get_snippets()
        
        if not snippets:
            raise EmptySerp()
        
        return {'pc': pagecount, 'sn': snippets}

    def get_pagecount(self):
        u"""Получить количество сниппетов результатов выдачи
        """
        pagecount = 0
        patterns = (r'<div[^>]+resultStats(?:[^>]+)?>Результатов: примерно (.*?)</div>',
                    r'<div[^>]+resultStats(?:[^>]+)?>(.*?)<nobr>',
                    r'<div[^>]+resultStats(?:[^>]+)?>Результатов:(.*?)</div>',
                    r'<div>Результатов:\s*(.*?)</div>',
                    r'Результатов:\s*(.*?),.*?</div>',
                    r'из примерно <b>(.*?)</b>',
                    r'<div>Результаты:.*?из\s*<b>\s*(\d+)\s*</b>')

        response = self.content
        for pattern in patterns:
            res = re.findall(pattern, response, re.DOTALL | re.IGNORECASE | re.UNICODE | re.MULTILINE)
            if res:
                # html-символы могут встречаться в виде своих числовых кодов (например, &nbsp; = &#160;)
                # избавимся от закодированных последовательностей в результирующей строке
                res_str = HTMLParser().unescape(res[0])
                results_ints = re.findall(r'\d+', res_str.split(',')[0])
                if results_ints:
                    return int(''.join(results_ints))
        return pagecount

    def get_snippets(self):
        body = body_regexp.findall(self.content)
        if not body:
            raise Exception('no body in response')

        dom = PyQuery(body[0])
        serp = dom('#ires').find('li')

        snippets = []
        position = 0
        for snippet in serp:
            parsed_snippet = self._parse_snippet(snippet)
            if not parsed_snippet:
                continue
            position += 1
            parsed_snippet['p'] = position
            snippets.append(parsed_snippet)

        return snippets

    def _parse_snippet(self, raw_snippet):
        position, title, url = self._parse_title_snippet(raw_snippet)
        if not url:
            return {}
        
        try:
            domain = get_full_domain_without_scheme(url)
        except UnicodeError as e:
            raise e

        snippet = {
            'd': domain,  # domain
            'p': position,  # position
            'u': url,  # url
            'm': self._is_map_snippet(raw_snippet),  # map
            't': None,  # title snippet
            's': None,  # body snippet
        }
        if 't' in self.snippet_fileds:
            snippet['t'] = title
        if 's' in self.snippet_fileds:
            snippet['s'] = self._parse_description_snippet(raw_snippet)
            
        return snippet

    def _parse_title_snippet(self, snippet):
        elements_h3 = [el for el in snippet.iter() if el.tag == 'h3']
        empty_result = None, None, None
        if not elements_h3:
            return empty_result
        h3 = elements_h3[-1]
        if h3 is None:
            return empty_result
        a = h3.find('a')
        if a is None:
            return empty_result
        url = self._format_link(a.get('href'))
        if not RE_URL_PROTOCOL.match(url):
            return empty_result
        if self.xhtml_snippet:
            title = ' '.join([self._etree_to_string(el).strip() for el in a.iter() if el.tag != 'a'])
        else:
            title = ''.join(a.itertext()).strip()
        return None, title, url

    def _parse_description_snippet(self, snippet):
        description = u''
        div_description = snippet.find('div')
        if div_description is not None:
            span_description = div_description.find('span')
            if self.xhtml_snippet and span_description is not None:
                description = self._etree_to_string(span_description)
            else:
                description = u'' if span_description is None else ' '.join(span_description.itertext()).strip()
        return description

    def _etree_to_string(self, el):
        return ET.tostring(el, encoding='UTF-8')

    def is_not_found(self):
        return u'ничего не найдено' in self.content
#        return bool(re.findall(ur'ничего не найдено', self.content))


    def _format_link(self, link):
        _marker_1 = '/interstitial?url='
        _marker_2 = '/url?q='
        _marker_end = '&sa='
        if link.find(_marker_1) >= 0:
            pos_start = link.index(_marker_1)
            pos_start += len(_marker_1)
            try:
                pos_end = link.index(_marker_end)
                link = link[pos_start:pos_end]
            except Exception:
                link = link[pos_start:]
            return urllib.unquote(link)
        elif link.find(_marker_2) >= 0:
            pos_start = link.index(_marker_2)
            pos_start += len(_marker_2)
            pos_end = link.index(_marker_end)
            link = link[pos_start:pos_end]
            return urllib.unquote(link)
        else:
            return link

    def _is_map_snippet(self, snippet):
        pattern = u'maps.google'
        for s in snippet.iter():
            if s.tag == 'a' and s.get('href').find(pattern) != -1:
                return True
        return False

