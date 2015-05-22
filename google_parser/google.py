#! coding: utf-8
import re
import urllib
import unicodedata
from urllib import quote, unquote
from urlparse import urlparse, urlunsplit, urlsplit

from pyquery import PyQuery
import lxml.etree as ET


__all__ = ['Google']


RE_URL_PROTOCOL = re.compile(ur'^(?:http|https|ftp)://', re.X | re.I | re.U)
body_regexp = re.compile('(<body.*?</body>)', re.DOTALL)


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


class Google(object):
    def __init__(self, content, xhtml_snippet=False):
        self.content = content
        self.xhtml_snippet = xhtml_snippet

    def parse(self):
        body = body_regexp.findall(self.content)
        if not body:
            raise Exception('no body in response')

        dom = PyQuery(body[0])
        serp = dom('#ires').find('li')

        snippets = []
        position = 0
        for snippet in serp:
            parsed_snippet = self.parse_snippet(snippet)
            if not parsed_snippet:
                continue
            position += 1
            parsed_snippet['p'] = position
            snippets.append(parsed_snippet)

        return snippets

    def parse_title_snippet(self, snippet):
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

    def parse_snippet(self, snippet):
        position, title, url = self.parse_title_snippet(snippet)
        if not url:
            return {}
        try:
            domain = get_full_domain_without_scheme(url)
        except UnicodeError as e:
            raise e

        description = self._parse_description_snippet(snippet)
        return {
            'd': domain,  # domain
            'p': position,  # position
            'u': url,  # url
            't': unicode(title),  # title snippet
            's': unicode(description),  # body snippet
            'm': self.is_map_snippet(snippet)  # map
        }

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

    def _is_not_found(self, response):
        response = self._encode_respoonse(response)
        return bool(re.findall(u'ничего не найдено', response.decode('utf-8')))

    def _encode_respoonse(response):
        try:
            encodings = re.findall('content=.*?charset=(.*?)"', response,
                                   re.DOTALL | re.IGNORECASE | re.UNICODE | re.MULTILINE)
            if encodings:
                encoding = encodings[0]
                return response.decode(encoding).encode('utf8')
        except Exception:
            pass
        return response

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

    def is_map_snippet(self, snippet):
        pattern = u'maps.google'
        for s in snippet.iter():
            if s.tag == 'a' and s.get('href').find(pattern) != -1:
                return True
        return False
