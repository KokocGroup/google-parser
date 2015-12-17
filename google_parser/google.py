#! coding: utf-8

import re
import unicodedata
import urllib
from urllib import quote, unquote
from urlparse import urlparse, urlunsplit, urlsplit
from HTMLParser import HTMLParser

from google_parser.exceptions import EmptySerp, NoBodyInResponseError, BadGoogleParserError, \
    SnippetsParserException, BadUrlError


__all__ = ['GoogleParser']


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
        'utf-8': 'utf8',
        'utf8': 'utf8',
        'cp1251': 'cp1251',
        'cp-1251': 'cp1251',
        'windows-1251': 'cp1251',
        'win-1251': 'cp1251',
        '1251': 'cp1251',
        'русdows-1251': 'cp1251',
        'koi8-r': 'koi8-r'
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

    query = "&".join(
        ["=".join([quote(_clean(t), "~:/?#[]@!$'()*+,;=") for t in q.split("=", 1)]) for q in query.split("&")])

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

    def __init__(self, content, xhtml_snippet=False, snippet_fields=('d', 'p', 'u', 't', 's', 'm')):
        self.content = to_unicode(content)
        self.xhtml_snippet = xhtml_snippet
        self.snippet_fields = snippet_fields

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

    def is_suspicious_traffic(self):
        patterns = [
            re.compile(
                ur'Мы зарегистрировали подозрительный трафик, исходящий из вашей сети. Повторите', re.I | re.M | re.S
            ),
            re.compile(
                ur'<a href="//support\.google\.com/websearch/answer/86640">Подробнее\.\.\.</a>', re.I | re.M | re.S
            )
        ]
        result = True
        for pattern in patterns:
            result &= bool(pattern.search(self.content))
        return result

    def get_serp(self):
        if self.is_not_found():
            return {'pc': 0, 'sn': []}

        pagecount = self.get_pagecount()
        snippets = self.get_snippets()

        if not snippets:
            raise EmptySerp()

        return {'pc': pagecount, 'sn': snippets}

    @classmethod
    def pagination_exists(cls, content):
        res = re.search(
            ur'<td\s*class="b"\s*style="text-align:left">\s*<a\s*href="/search', content, re.I | re.M | re.S
        )
        if res:
            return True

        res = re.search(
            ur'<td>\s*<a\s*class="fl"\s*href="/search', content, re.I | re.M | re.S
        )
        if res:
            return True

        return False

    def get_pagecount(self):
        u"""Получить количество сниппетов результатов выдачи
        """
        pagecount = 0
        patterns = (ur'<div[^>]+resultStats(?:[^>]+)?>Результатов: примерно (.*?)<',
        ur'<div[^>]+resultStats(?:[^>]+)?>(.*?)<nobr>',
        ur'<div[^>]+resultStats(?:[^>]+)?>Результатов:(.*?)</div>',
        ur'<div>Результатов:\s*(.*?)</div>',
        ur'Результатов:\s*(.*?),.*?</div>',
        ur'из примерно <b>(.*?)</b>',
        ur'<div>Результаты:.*?из\s*<b>\s*(\d+)\s*</b>')

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
        res = re.compile('<body.*?</body>', re.DOTALL).search(self.content)
        if not res:
            raise NoBodyInResponseError()

        pc = self.get_pagecount()
        if pc % 10 == 1 and '<div class="g"' in self.content:
            return [SnippetsParserDefault(self.snippet_fields).get_snippet(1, self.content)]
        elif '<div class="srg">' in self.content:
            return SnippetsParserDefault(self.snippet_fields).get_snippets(self.content)
        elif '<div id="search"><div id="ires">' in self.content:
            return SnippetsParserUnil_2015_07_23(self.snippet_fields).get_snippets(self.content)
        raise BadGoogleParserError()

    def is_not_found(self):
        patterns = [
            re.compile(ur'По\s*запросу\s*<(?:em|b)>.*?</(?:em|b)>\s*ничего\s*не\s*найдено\.', re.I | re.M | re.S),
            re.compile(ur'Извините,\s*у\s*нас\s*нет\s*информации\s*об\s*адресе\s*<(?:em|b)>.*?</(?:em|b)>', re.I | re.M | re.S),
        ]
        res = False
        for pattern in patterns:
            if pattern.search(self.content):
                return True
        return res


class SnippetsParserDefault(object):
    snippets_regexp = re.compile(ur'<div class="g">(.*?)</div><!--n--></div>', re.I | re.M | re.S)
    result_regexp = re.compile(ur'(<div class="srg">.*?<hr class=")', re.I | re.M | re.S)

    def __init__(self, snippet_fields):
        self.snippet_fields = snippet_fields

    def get_snippets(self, body):
        res = self.result_regexp.findall(body)
        if not res:
            raise BadGoogleParserError()

        result = []
        position = 0
        for body in res:
            snippets = self.snippets_regexp.findall(body)
            for snippet in snippets:

                position += 1

                try:
                    item = self.get_snippet(position, snippet)
                except SnippetsParserException:
                    if self._is_empty_snippet(snippet):
                        position -= 1
                        continue
                    else:
                        raise

                # игнорим сниппет с картинками
                if self._is_map_snippet(item['u']) or item['u'].startswith('/search'):
                    position -= 1
                    continue

                result.append(item)
        return result

    def get_snippet(self, position, snippet):
        title, url = self._parse_title_snippet(snippet, position)
        return {
            'p': position,
            'u': url,
            'd': self._get_domain(url),
            'm': self._is_map_snippet(url),
            't': self._get_title(title),
            's': self._get_descr(snippet, url),
        }

    def _get_descr(self, snippet, url):
        if 's' in self.snippet_fields:
            if self._is_image_snippet(url):
                return self._parse_description_img_snippet(snippet)
            else:
                return self._parse_description_snippet(snippet)

    def _get_title(self, title):
        if 't' in self.snippet_fields:
            return title

    def _get_domain(self, url):
        try:
            return get_full_domain_without_scheme(url)
        except UnicodeError as e:
            raise BadUrlError(u'некорректный урл: {0}'.format(url))

    def _is_empty_snippet(self, snippet):
        return '<h3 class="r"></h3>' in snippet

    def _parse_title_snippet(self, snippet, position):
        res = re.compile(ur'<h3 class="r">.*?<a[^>]+?href="([^"]+?)"[^>]*?>(.*?)</a>', re.I | re.M | re.S).search(snippet)
        if res:
            return self._strip_tags(res.group(2)), self._format_link(res.group(1)),
        raise SnippetsParserException(u'Parsing error. Broken snippet at {0}: {1}'.format(position, snippet))

    def _is_image_snippet(self, url):
        return url.startswith('/images?q=')

    def _is_map_snippet(self, url):
        return 'maps.google' in url

    def _format_link(self, link):
        link = link.replace('&amp;', '&')

        patterns = [
            ur'/interstitial\?url=([^&]*)',
                ur'/url\?q=([^&]*)',
                ur'/url\?url=([^&]*)',
                ur'/infected\?url=([^&]*)',
        ]

        for pattern in patterns:
            res = re.compile(pattern).search(urllib.unquote(link))
            if res:
                return res.group(1)
        return link

    def _parse_description_img_snippet(self, snippet):
        res = re.compile(ur'<div>(.*?)</div>', re.I | re.M | re.S).search(snippet)
        if res:
            return self._strip_tags(res.group(1))
        raise BadGoogleParserError(u'не удалось найти описание сниппета: {}'.format(snippet))

    def _parse_description_snippet(self, snippet):
        res = re.compile(ur'<span class="st">(.*?)</span>', re.I | re.M | re.S).search(snippet)
        if res:
            return self._strip_tags(res.group(1))

    def _strip_tags(self, html):
        return re.sub(ur' {2,}', ' ', re.sub(ur'<[^>]*?>', '', html.replace('&nbsp;', ' '))).strip()

    def _get_host(self, html):
        res = re.compile(ur'"host":"([^"]+?)"').search(html)
        if res:
            return res.group(1)

class SnippetsParserUnil_2015_07_23(SnippetsParserDefault):
    snippets_regexp = re.compile(ur'<li class="g">((?:<span|<h3|<table).*?(?:</div>|</table>))\s*</li>', re.I | re.M | re.S)
    result_regexp = re.compile(ur'(<div id="ires">.*?</ol>\s*</div>)', re.I | re.M | re.S)
