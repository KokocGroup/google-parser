#! coding: utf-8
import json
import re
import unicodedata
import urllib
from urllib import quote, unquote
from urlparse import urlparse, urlunsplit, urlsplit
from HTMLParser import HTMLParser

from datetime import datetime
from pyquery import PyQuery
from lxml import etree


from google_parser.exceptions import SnippetsParserException, GoogleParserError, NoBodyInResponseError, \
    TemporaryGoogleParserError

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
    domain = re.sub(ur':.+', '' , parsed.netloc)
    return urlunsplit(('', domain, '', '', '')).replace('//', '')


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
        '<input.*?name=\"id\".*?value=\"([^\"]*)\".*?>',
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
        # with open('go.html', 'w') as f:
        #     f.write(self.content)

        self.xhtml_snippet = xhtml_snippet
        self.snippet_fields = snippet_fields

    def raise_if_temporary_error(self, html):
        if '<title>Error 502' in html:
            raise TemporaryGoogleParserError()

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

        q = ''
        q_match = re.search(ur"name=(?:'|\")q(?:'|\")\s*value=(?:'|\")([^'\"]*)(?:'|\")", self.content, re.I | re.M | re.S)
        if q_match:
            q = q_match.group(1)

        return {
            'url': 'https://www.google.com' + match_captcha[0].replace('&amp;', '&'),
            'captcha_id': match_captcha_id[0] if match_captcha_id else  '',
            'captcha_coninue': match_captcha_coninue[0].replace('&amp;', '&'),
            'q': q
        }

    @classmethod
    def is_before_search(cls, content):
        if u'<title>Прежде чем перейти к Google Поиску</title>' not in content:
            return

        match = re.search(ur'(<form\s*action="(https://consent.google.com/s[^"]*?)"\s*method="POST".*?</form>)', content, flags=re.I | re.M | re.S)
        if not match:
            raise GoogleParserError

        url = match.group(2)

        form = match.group(1)
        post = re.findall(ur'<input type="hidden" name="([^"]*?)" value="([^"]*?)">', form)
        if not post:
            raise GoogleParserError

        return {
            'url': url,
            'post': dict(post)
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
            ),
            re.compile(
                ur'<p>Your client does not have permission to get URL', re.I | re.M | re.S
            ),
        ]
        result = False
        for pattern in patterns:
            result |= bool(pattern.search(self.content))
            if result:
                break
        return result

    def is_recaptcha_suspicious_traffic(self):
        patterns = [
            re.compile(
                ur'Мы зарегистрировали подозрительный трафик, исходящий из вашей сети. С помощью', re.I | re.M | re.S
            ),
            re.compile(
                ur'<a href="//support\.google\.com/websearch/answer/86640">Подробнее\.\.\.</a>', re.I | re.M | re.S
            ),
            re.compile(
                ur'class="g-recaptcha"', re.I | re.M | re.S
            ),
        ]
        result = False
        for pattern in patterns:
            if bool(pattern.search(self.content)):
                return True
        return result

    def get_context_snippet_title(self, content):
        res = re.search(ur'<h3>\s*<a[^>]+?></a>\s*<a[^>]*?href="([^"]+?)"[^>]*?>\s*(.*?)\s*</a>\s*</h3>', content, re.I | re.M | re.S)
        if not res:
            raise GoogleParserError(u'Не удалось распарсить тайтл в сниппете: {0}'.format(content))
        return {'u': SnippetsParserDefault.format_context_link(res.group(1)), 't': res.group(2)}

    def get_context_visible_url(self, content):
        res = re.search(ur'<div\s*class="ads-visurl">.*?<cite\s*class="_WGk"[^>]*?>\s*(.*?)\s*</cite>', content, re.I | re.M | re.S)
        if not res:
            return
        return SnippetsParserDefault.strip_tags(res.group(1))

    def get_context_serp(self):
        snippets = re.findall(
            ur'(<li class="ads-ad"(?:\s*data-hveid="\d+")?>.*?(?:</ul>|</div>)\s*</li>)',
            self.content,
            re.I | re.M | re.S
        )
        sn = []
        for snippet in snippets:
            item = self.get_context_snippet_title(snippet)
            item['vu'] = self.get_context_visible_url(snippet)
            sn.append(item)

        return {'pc': len(sn), 'sn': sn}

    def get_serp(self):
        if self.is_not_found():
            return {'pc': 0, 'sn': []}

        pagecount = self.get_pagecount()
        snippets = self.get_snippets()

        for pos, snippet in enumerate(snippets, start=1):
            if snippet['p'] != pos:
                raise GoogleParserError('bad position')

            if not snippet['u']:
                raise GoogleParserError('bad url')

            if not snippet['d']:
                raise GoogleParserError('bad domain')

        return {'pc': pagecount, 'sn': snippets}

    @classmethod
    def pagination_exists(cls, content):
        res = re.search(
            ur'<td\s*class="b"\s*style="text-align:left">\s*<a\s*href="/search', content, re.I | re.M | re.S
        )
        if res:
            return True

        res = re.search(
            ur'<td>\s*<a[^>]+class="fl"\s*href="/search', content, re.I | re.M | re.S
        )
        if res:
            return True

        res = re.search(
            ur'<a\s*class="pn"\s*href="/search[^"]+"\s*id="pnnext"', content, re.I | re.M | re.S
        )
        if res:
            return True

        return False

    def get_pagecount(self):
        u"""Получить количество сниппетов результатов выдачи
        """

        pagecount = 0
        patterns = (
            ur'<div[^>]+resultStats(?:[^>]+)?>Результатов: примерно (.*?)<',
            ur'<div[^>]+resultStats(?:[^>]+)?>(.*?)<nobr>',
            ur'<div[^>]+result-stats(?:[^>]+)?>(.*?)<nobr>',
            ur'<div[^>]+resultStats(?:[^>]+)?>Результатов:(.*?)</div>',
            ur'<div>Результатов:\s*(.*?)</div>',
            ur'Результатов:\s*(.*?),.*?</div>',
            ur'из примерно <b>(.*?)</b>',
            ur'<div>Результаты:.*?из\s*<b>\s*(\d+)\s*</b>',
        )

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
            raise NoBodyInResponseError('no body in response')

        if '<div id="main">' in self.content and '<!-- cctlcm' in self.content and 'KP7LCb' in self.content:
            return SnippetsParserAfter_2022_02_14(self.snippet_fields).get_snippets(self.content)
        elif re.search('<div class="[^"]*?" id="res" role="main">.*?<div id="bottomads"', self.content, flags=re.S):
            return SnippetsParserAfter_2021_01_29(self.snippet_fields).get_snippets(self.content)
        elif re.search('<div class="[^"]*?" id="res" role="main">', self.content):
            return SnippetsParserAfter_2016_03_10(self.snippet_fields).get_snippets(self.content)
        elif '<body jsmodel="' in self.content:
            return MobileSnippetsParser(self.snippet_fields).get_snippets(self.content)
        elif '<div class="srg"' in self.content:
            return SnippetsParserDefault(self.snippet_fields).get_snippets(self.content)
        elif '<div id="search"><div id="ires">' in self.content:
            return SnippetsParserUnil_2015_07_23(self.snippet_fields).get_snippets(self.content)
        raise GoogleParserError('not found parser version')

    def is_not_found(self):
        patterns = [
            re.compile(ur'>\s*По\s*запросу\s*<(?:em|b|span)>.*?</(?:em|b|span)>\s*ничего\s*не\s*найдено\.', re.I | re.M | re.S),
            re.compile(ur'Извините,\s*у\s*нас\s*нет\s*информации\s*об\s*адресе\s*<(?:em|b)>.*?</(?:em|b)>', re.I | re.M | re.S),
            re.compile(ur'<div id="sbfrm_l"></div>', re.I | re.M | re.S),
            re.compile(ur'Результатов: примерно 0', re.I | re.M | re.S),
            re.compile(ur'<span class="[^"]+?">\s*ничего не найдено.', re.I | re.M | re.S),
            re.compile(ur'</a>\s*</div>\s*</div>\s*</div>\s*<footer', re.I | re.M | re.S),
        ]
        res = False
        for pattern in patterns:
            if pattern.search(self.content):
                return True

        pattern = re.compile(ur'<div class="hwc"></div>\s*</div>\s*</div>\s*</div>\s*<footer', re.I | re.M | re.S)
        match = pattern.search(self.content)
        if match:
            match = re.search(
                ur'Мы скрыли некоторые результаты, которые очень похожи на уже представленные выше \(0\)',
                self.content,
                flags=re.I | re.M | re.S
            )
            return bool(match)

        return res


class SnippetsParserDefault(object):
    snippets_regexp = re.compile(ur'(<div class="g">.*?</div><!--n--></div>)', re.I | re.M | re.S)
    result_regexp = re.compile(ur'(<div( class="srg"|[^>]+?id="rso"[^>]*?)>.*?<hr class=")', re.I | re.M | re.S)

    def __init__(self, snippet_fields):
        self.snippet_fields = snippet_fields

    def get_snippets(self, body):
        res = self.result_regexp.findall(body)
        if not res:
            raise GoogleParserError('no body in response')

        result = []
        position = 0
        for body in res:
            snippets = self.snippets_regexp.findall(body)
            for snippet in snippets:

                # игнорим расписание
                if 'rrecc' in snippet:
                    continue

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
                if self._is_map_snippet(item['u']) or item['u'].startswith('/search') or item['u'].startswith('/images'):
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
            'h': self._get_html(snippet),
            'vu': self._get_vu(snippet),
        }

    @classmethod
    def get_html_descr(cls, snippet):
        res = re.compile(ur'(<span class="st">.*?</span>)\s*</?div', re.I | re.M | re.S).search(snippet)
        if res:
            return res.group(1)

    def _get_vu(self, snippet):
        match = re.search(ur'<cite class="(?:_Rm|iUh)[^"]*?">([^<]+?)</cite>', snippet, re.I | re.M | re.S)
        if not match:
            return None
        return HTMLParser().unescape(match.group(1))

    def _get_html(self, snippet):
        if 'h' in self.snippet_fields:
            return snippet

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
            raise GoogleParserError(u'некорректный урл: {0}'.format(url))

    def _is_empty_snippet(self, snippet):
        return '<h3 class="r"></h3>' in snippet

    def _parse_title_snippet(self, snippet, position):
        snippet = re.sub(ur'<div class="action-menu.*?</div>', '', snippet, flags=re.I | re.M | re.S)
        res = re.compile(ur'<(?:h3|div)(?: class="r")?[^>]+?>.*?<a[^>]+?href="([^"]+?)"[^>]*?>(.*?)</a>', re.I | re.M | re.S).search(snippet)
        if res:
            title = res.group(2)
            if '<cite' in title:
                title = re.sub(ur'<cite.*?</cite>', '', title)

            if title.startswith('<div'):
                title_res = re.search(ur'<h3[^>]*?>\s*(?:<div[^>]*?>)(.*?)(?:</div>)</h3>', title, flags=re.I | re.M | re.S)
                if title_res:
                    title = title_res.group(1)

            return SnippetsParserDefault.strip_tags(title), SnippetsParserDefault.format_link(res.group(1)),
        raise GoogleParserError(u'Parsing error. Broken snippet at {0}: {1}'.format(position, snippet))

    def _is_image_snippet(self, url):
        return url.startswith('/images?q=')

    def _is_map_snippet(self, url):
        return 'maps.google' in url

    @classmethod
    def format_link(cls, link):
        link = link.replace('&amp;', '&')

        patterns = [
            ur'/interstitial\?url=([^&]*)',
                ur'/url\?q=([^&]*)',
                ur'/url\?.*?url=([^&]*)',
                ur'/infected\?url=([^&]*)',
        ]

        for pattern in patterns:
            res = re.compile(pattern).search(urllib.unquote(link))
            if res:
                return res.group(1)
        return link

    @classmethod
    def format_context_link(cls, link):
        link = SnippetsParserDefault.format_link(link)

        if link.startswith('/aclk?'):
            link = 'https://www.google.ru' + link
        return link

    def _parse_description_img_snippet(self, snippet):
        res = re.compile(ur'<div>(.*?)</div>', re.I | re.M | re.S).search(snippet)
        if res:
            return SnippetsParserDefault.strip_tags(res.group(1))
        raise GoogleParserError(u'не удалось найти описание сниппета: {}'.format(snippet))

    def _parse_description_snippet(self, snippet):
        patterns = [
            ur'<span class="(?:st|aCOpRe)">(.*?)</span>\s*(?:<br>|</div>|<div|</a>)',
            ur'<div\s+class="[^"]+?">\s*<div\s+class="[^"]+?">\s*<span(?:\s+class="[^"]+?")?>\s*(.*?)</span>\s*</div>',
            ur'<div\s+class="IsZvec">\s*<div\s+[^>]+?>\s*<span(?:\s+class="[^"]+?")?>\s*(.*?)</span>\s*</div>',
            ur'<div\s+class="(?:IsZvec|VwiC3b\s+[^"]+)"[^>]*?>\s*(.*?)</div>',
            ur'<div\s+class="IsZvec">\s*<span\s+[^>]+?/>\s*(.*?)</div>',
            ur'<div\s+class="IsZvec"/>(.*?)',
            ur'<div class="FUUCsd CkcVWd RgAZAc"[^>]*?>(.*?)</div>',
            ur'<div\s+class="s">(.*?)</div>',
            ur'<span\s+class="f">(.*?)<cite>',
            ur'<div\s+class="Uroaid">(.*?)</div>',
            ur'<div\s+class="Uroaid"/?>()',
            ur'<table\s+class="NwNzde">(.*?)</table>',
            ur'</div>\s*</div>\s*</div>\s*(.*?)<div class="NJo7tc',
        ]
        for pattern in patterns:
            res = re.search(pattern, snippet, flags=re.I | re.M | re.S)
            if res:
                return SnippetsParserDefault.strip_tags(res.group(1))

        if snippet.count('NJo7tc Z26q7c uUuwM') == 0:
            return ''

        raise GoogleParserError()

    @classmethod
    def strip_tags(self, html):
        return re.sub(ur' {2,}', ' ', re.sub(ur'<[^>]*?>', '', html.replace('&nbsp;', ' '))).strip()

    def _get_host(self, html):
        res = re.compile(ur'"host":"([^"]+?)"').search(html)
        if res:
            return res.group(1)


class MobileSnippetsParser(SnippetsParserDefault):
    snippets_regexp = re.compile(ur'(<div data-hveid="[^"]+?">.*?</div>\s*</div>\s*</div>\s*</div>)', re.I | re.M | re.S)

    def _parse_title(self, snippet):
        match = re.search(
            ur'<a class="(?:C8nzq|cz3goc)\s+[^"]*BmP5tf[^"]*"[^>]*href="([^"]+)".*?<div[^>]+class="[^"]*MUxGbd v0nnCb[^"]*"[^>]*>(.*?)</div>',
            snippet,
            flags=re.S
        )
        if not match:
            print(snippet)
            raise GoogleParserError(snippet)

        url = HTMLParser().unescape(match.group(1))
        url = self.format_link(url)

        title = HTMLParser().unescape(
            SnippetsParserDefault.strip_tags(
                match.group(2) or '')
        )
        return url, title

    @classmethod
    def strip_element_tags(cls, element):
        html = etree.tostring(element)
        return HTMLParser().unescape(SnippetsParserDefault.strip_tags(html))

    def _get_descr(self, snippet):
        if 's' not in self.snippet_fields:
            return

        match = re.search(ur'<div class="(?:VwiC3b )?MUxGbd[^"]*"[^>]*>(.*?)</div>', snippet, flags=re.I | re.M | re.S)
        if not match:
            return None

        return HTMLParser().unescape(
            SnippetsParserDefault.strip_tags(
                match.group(1) or ''
            )
        )

    def _get_html(self, snippet):
        if 'h' in self.snippet_fields:
            return etree.tostring(snippet)

    def _get_vu(self, snippet):
        return self._parse_vu(snippet)

    def _parse_vu(self, snippet):
        match = re.search(ur'<span class="dTe0Ie qzEoUe">(.*?)</span>', snippet)
        if not match:
            return

        res = match.group(1) or ''
        res = res.strip()
        res = re.sub(ur'<span[^>]+>', '', res)
        res = re.sub(ur'</span>', '', res)
        res = HTMLParser().unescape(res)
        return res

    def get_snippets(self, body):
        dom = PyQuery(body)
        rso_div = dom('#rso')
        if not rso_div:
            raise GoogleParserError()

        main_class = 'mnr-c xpd O9g5cc uUPGi'

        divs = rso_div.find('div.mnr-c')
        serp = []
        for div in divs:
            attrib_class = div.attrib.get('class', '')

            if main_class != attrib_class:
                continue

            is_dual = False
            for hveid_div in div.findall('div'):
                if 'data-hveid' in hveid_div.attrib:
                    serp.append(hveid_div)
                    is_dual = True

            if not is_dual:
                serp.append(div)

        result = []
        position = 0
        for snippet in serp:
            snippet_content = etree.tostring(snippet)

            if snippet_content.count(main_class) > 1:
                continue

            if 'class="pXvdUe">' in snippet_content:
                continue

            if 'class="TvV1fe"' in snippet_content:
                continue

            position += 1

            u, t = self._parse_title(snippet_content)
            result.append({
                    'p': position,
                    'u': u,
                    'd': self._get_domain(u),
                    'm': self._is_map_snippet(u),
                    't': self._get_title(t),
                    's': self._get_descr(snippet_content),
                    'h': self._get_html(snippet_content),
                    'vu': self._get_vu(snippet_content),
            })

        return result


class SnippetsParserUnil_2015_07_23(SnippetsParserDefault):
    snippets_regexp = re.compile(ur'(<(?:li|div) class="g">(?:<span|<h3|<table).*?(?:(?:<br>|</a>)\s*</div>|</table>)\s*</(?:li|div)>)', re.I | re.M | re.S)
    result_regexp = re.compile(ur'(<div id="ires">.*?</ol>\s*</div>)', re.I | re.M | re.S)

    def _parse_description_snippet(self, snippet):
        patterns = [
            ur'<span class="(?:st|aCOpRe)">(.*?)</span>\s*(?:<br>|</div>|<div|</a>)',
            ur'<div\s+class="[^"]+?">\s*<div\s+class="[^"]+?">\s*<span(?:\s+class="[^"]+?")?>\s*(.*?)</span>\s*</div>',
            ur'<div\s+class="IsZvec">\s*<div\s+[^>]+?>\s*<span(?:\s+class="[^"]+?")?>\s*(.*?)</span>\s*</div>',
            ur'<div\s+class="IsZvec">\s*(.*?)</div>',
            ur'<div\s+class="IsZvec">\s*<span\s+[^>]+?/>\s*(.*?)</div>',
            ur'<div\s+class="s">(.*?)</div>',
        ]
        for pattern in patterns:
            res = re.search(pattern, snippet, flags=re.I | re.M | re.S)
            if res:
                return SnippetsParserDefault.strip_tags(res.group(1))


class SnippetsParserAfter_2016_03_10(SnippetsParserDefault):
    snippets_regexp = re.compile(ur'(<div class=(?:"g\s*(?:card-section)?"(?: data-hveid="[^"]+?")?(?: data-ved="[^"]+?")?>|"g\s+[^_"]*"[^>]*>)\s*(?:<h2[^>]+?>[^<]+?</h2>)?\s*(?:<div data-hveid="[^"]+?">|<div>)?<!--m-->\s*.*?</div><!--n-->\s*(?:</div>))', re.I | re.M | re.S)
    result_regexp = re.compile(ur'(<div class="[^"]*?" id="res" role="main">.*?<!--z-->)', re.I | re.M | re.S)

    def get_snippets(self, body):
        res = self.result_regexp.findall(body)
        if not res:
            raise GoogleParserError('no body in response')

        result = []
        position = 0
        for body in res:
            snippets = self.snippets_regexp.findall(body)
            for snippet in snippets:
                if re.search(ur'class="g[^"]+obcontainer\s*', snippet):
                    continue

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

        if len(result) >= 2 and result[0]['u'] == result[1]['u']:
            result = result[1:]
            for pos, snippet in enumerate(result, start=1):
                snippet['p'] = pos

        return result


class SnippetsParserAfter_2021_01_29(SnippetsParserAfter_2016_03_10):
    snippets_regexp = None
    result_regexp = re.compile(ur'(<div class="[^"]*?" id="res" role="main">.*?<div id="bottomads")', re.I | re.M | re.S)

    def get_snippet(self, position, snippet):
        title, url = self._parse_title_snippet(snippet, position)
        return {
            'p': position,
            'u': url,
            'd': self._get_domain(url),
            'm': self._is_map_snippet(url),
            't': self._get_title(title),
            's': self._get_descr(snippet, url),
            'h': self._get_html(snippet),
            'vu': self._get_vu(snippet),
        }

    def get_snippets(self, body):
        res = self.result_regexp.findall(body)
        if not res:
            raise GoogleParserError('no body in response')

        result = []
        position = 0
        for body in res:
            dom = PyQuery(body)
            snippets = dom('div.g')
            for snippet in snippets:
                html = HTMLParser().unescape(
                    etree.tostring(snippet)
                )

                if len(snippet.cssselect('div.g')) > 1:
                    continue

                if re.search(ur'class="g[^"]+(?:obcontainer|g-blk)\s*', html):
                    continue

                if re.search(ur'class="[^"]*?\s*obcontainer\s+', html):
                    continue

                # дополнительные элементы
                if re.search(ur'class="[^"]+?(?:__outer-card|-wholepage|g-blk|vk_c)', html):
                    continue

                # дополнительные элементы
                if re.search(ur'class="[^"]*?lu_map_section', html):
                    continue

                if re.search(ur'id="imagebox_bigimages"', html):
                    continue

                if re.search(ur'<div\s*class="[^"]*rrec[^"]*"', html):
                    continue

                if re.search(ur'<g-section-with-header', html):
                    continue

                position += 1
                try:
                    item = self.get_snippet(position, html)
                except SnippetsParserException:
                    if self._is_empty_snippet(snippet):
                        position -= 1
                        continue
                    else:
                        raise

                # игнорим сниппет с картинками и карты
                if self._is_map_snippet(item['u']) or item['u'].startswith('/search'):
                    position -= 1
                    continue

                result.append(item)

        if len(result) >= 2 and result[0]['u'] == result[1]['u']:
            result = result[1:]
            for i in range(len(result)):
                result[i]['p'] = i + 1

        return result


class SnippetsParserAfter_2022_02_14(SnippetsParserAfter_2021_01_29):
    snippets_regexp = None
    result_regexp = re.compile(ur'(<div id="main">.*?<!-- cctlcm)', re.I | re.M | re.S)

    def _parse_title_snippet(self, snippet, position):
        res = re.search(
            ur'<div\s*class="egMi0[^"]*">'
                ur'<a\s*href="([^"]+?)"[^>]*?>'
                    ur'(?:<div\s*class="DnJfK"><div\s*class="j039Wc">)?'
                    ur'<h3\s*class="[^"]*?">'
                        ur'<div\s*class="BNeawe[^"]*?"[^>]*?>\s*(.*?)\s*</div>',
            snippet,
            re.I | re.M | re.S | re.X
        )
        if res:
            return HTMLParser().unescape(SnippetsParserDefault.strip_tags(res.group(2))), SnippetsParserDefault.format_link(res.group(1)),
        raise GoogleParserError(u'Parsing error. Broken snippet at {0}: {1}'.format(position, snippet))

    def _parse_description_snippet(self, snippet):

        snippet = snippet.replace('<div><div class="BNeawe s3v9rd AP7Wnd"><div>', '')

        patterns = [
            ur'<div class="BNeawe s3v9rd AP7Wnd">(.*?)</div></div>',
        ]
        for pattern in patterns:
            res = re.findall(pattern, snippet, flags=re.I | re.M | re.S)
            if not res:
                continue

            result = res[0]
            if len(res) > 1:
                result = res[1]

            return HTMLParser().unescape(SnippetsParserDefault.strip_tags(result))

        raise GoogleParserError('Description not found')

    def get_snippet(self, position, snippet):
        title, url = self._parse_title_snippet(snippet, position)
        return {
            'p': position,
            'u': url,
            'd': self._get_domain(url),
            'm': self._is_map_snippet(url),
            't': self._get_title(title),
            's': self._get_descr(snippet, url),
            'h': self._get_html(snippet),
            'vu': self._get_vu(snippet),
        }

    def get_snippets(self, body):
        res = self.result_regexp.findall(body)
        if not res:
            raise GoogleParserError('no body in response')

        result = []
        position = 0
        for body in res:
            dom = PyQuery(body)
            snippets = dom('div.luh4tb')
            if not snippets:
                snippets = dom('div.fP1Qef')
            for snippet in snippets:
                html = etree.tostring(snippet)

                html_unescaped = HTMLParser().unescape(html)
                if re.search(ur'<span class="[^"]+?">Реклама</?span>?', html_unescaped, flags=re.I):
                    continue

                position += 1
                try:
                    item = self.get_snippet(position, html)
                except SnippetsParserException:
                    if self._is_empty_snippet(snippet):
                        position -= 1
                        continue
                    else:
                        raise

                # игнорим сниппет с картинками и карты
                if self._is_map_snippet(item['u']) or item['u'].startswith('/search'):
                    position -= 1
                    continue

                result.append(item)

        if len(result) >= 2 and result[0]['u'] == result[1]['u']:
            result = result[1:]
            for i in range(len(result)):
                result[i]['p'] = i + 1

        return result


class GoogleJsonParser(GoogleParser):
    def __init__(self, content, xhtml_snippet=False, snippet_fields=('d', 'p', 'u', 't', 's', 'm')):

        self.raise_if_temporary_error(content)

        content = self._prepare_content(content)
        super(GoogleJsonParser, self).__init__(content, xhtml_snippet=False, snippet_fields=snippet_fields)


    def _get_need_blocks(self, content):
        ret = ''

        blocks = content.split('/*""*/')
        for block in blocks:

            block = block.strip()
            if not block:
                continue

            d = json.loads(block).get('d', '')
            if '"i":"search"' in d or '"i":"appbar"' in d or '"i":"xjs"' in d or '"i":"topstuff"' in d or not self._is_je_api(d):
                ret += d
        return ret

    def _is_je_api(self, content):
        return u'<script>je.api' in content

    def _prepare_content(self, content):
        try:
            self.content = content
            if self.is_suspicious_traffic():
                return content

            need_blocks = self._get_need_blocks(content)

            # second and other pages
            if not self._is_je_api(need_blocks):
                return need_blocks

            je_apis = re.findall(ur'<script>je.api\((.*?)\);</script>', need_blocks, re.I | re.M | re.S)

            ret = '<body><div class="med" id="res" role="main"><div class="srg">'
            for je_api in je_apis:
                if '"i":"search"' not in je_api and '"i":"appbar"' not in je_api and '"i":"xjs"' not in je_api and '"i":"topstuff"' not in je_api:
                    continue

                match = re.search(ur'"h":"(.*?)"', je_api, re.I | re.M | re.S)
                if not match:
                    continue

                ret += match.group(1).decode('string_escape').decode('raw_unicode_escape', 'ignore')
            ret += '<hr class=""></div></body>'
            return ret
        except Exception as e:
            raise GoogleParserError('{}: {}'.format(type(e), str(e)))


class GoogleMobileParser(GoogleParser):
    def get_snippets(self):
        res = re.compile('<body.*?</body>', re.DOTALL).search(self.content)
        if not res:
            raise GoogleParserError('no body in response')

        if '<div class="srg"' in self.content:
            return SnippetsMobileParserDefault(self.snippet_fields).get_snippets(self.content)
        raise GoogleParserError()


    @classmethod
    def pagination_exists(cls, content):
        res = re.search(
            ur'<a[^>]+?id="pnnext"', content, re.I | re.M | re.S
        )
        if res:
            return True

        return False

    def get_pagecount(self):
        return None

class SnippetsMobileParserDefault(SnippetsParserDefault):
    snippets_regexp = re.compile(ur'<div class="g card-section">(.*?)</div>\s*<!--n-->\s*</div>', re.I | re.M | re.S)
    result_regexp = re.compile(ur'(<div class="srg".*?(?:</div>\s*</div>\s*</div>\s*</div>\s*<div class))', re.I | re.M | re.S)

    def _parse_description_snippet(self, snippet):
        res = re.compile(ur'<span class="st">(.*?)</span>\s*</div>', re.I | re.M | re.S).search(snippet)
        if res:
            return SnippetsParserDefault.strip_tags(res.group(1))
