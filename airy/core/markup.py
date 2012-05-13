import copy
from airy.utils.html import strip_tags
from airy.utils.encoding import smart_unicode
import logging
import re

_URL_RE = re.compile(ur"""\b((?:([\w-]+):(/{1,3})|www[.])(?:(?:(?:[^\s&()]|&amp;|&quot;)*(?:[^!"#$%&'()*+,.:;<=>?@\[\]^`{|}~\s]))|(?:\((?:[^\s&()]|&amp;|&quot;)*\)))+)""")

_link_regexes = [
    re.compile(r'(?P<body>https?://(?P<host>[a-z0-9._-]+)(?:/[/\-_.,a-z0-9%&?;=~]*)?(?:\([/\-_.,a-z0-9%&?;=~]*\))?)', re.I),
    # This is conservative, but autolinking can be a bit conservative:
    re.compile(r'mailto:(?P<body>[a-z0-9._-]+@(?P<host>[a-z0-9_._]+[a-z]))', re.I),
    re.compile(r'(?P<body>www\.(?P<host>[a-z0-9._-]+)(?:/[/\-_.,a-z0-9%&?;=~]*)?(?:\([/\-_.,a-z0-9%&?;=~]*\))?)', re.I),
    ]

_avoid_elements = ['textarea', 'pre', 'code', 'head', 'select', 'a']

_force_update_params = ['a',]

_avoid_hosts = [
    re.compile(r'^localhost', re.I),
    re.compile(r'\bexample\.(?:com|org|net)$', re.I),
    re.compile(r'^127\.0\.0\.1$'),
    ]

_avoid_classes = ['nolink']


def _link_text(text, link_regexes, avoid_hosts, factory, extra_params={}):
    leading_text = ''
    links = []
    last_pos = 0
    while 1:
        best_match, best_pos = None, None
        for regex in link_regexes:
            regex_pos = last_pos
            while 1:
                match = regex.search(text, pos=regex_pos)
                if match is None:
                    break
                host = match.group('host')
                for host_regex in avoid_hosts:
                    if host_regex.search(host):
                        regex_pos = match.end()
                        break
                else:
                    break
            if match is None:
                continue
            if best_pos is None or match.start() < best_pos:
                best_match = match
                best_pos = match.start()
        if best_match is None:
            # No more matches
            if links:
                assert not links[-1].tail
                links[-1].tail = text
            else:
                assert not leading_text
                leading_text = text
            break
        link = best_match.group(0)
        end = best_match.end()
        if link.endswith('.') or link.endswith(','):
            # These punctuation marks shouldn't end a link
            end -= 1
            link = link[:-1]
        prev_text = text[:best_match.start()]
        if links:
            assert not links[-1].tail
            links[-1].tail = prev_text
        else:
            assert not leading_text
            leading_text = prev_text
        anchor = factory('a')
        anchor.set('href', link)
        body = best_match.group('body')
        if not body:
            body = link
        if body.endswith('.') or body.endswith(','):
            body = body[:-1]
        anchor.text = body
        if extra_params:
            anchor.attrib.update(extra_params)
        links.append(anchor)
        text = text[end:]
    return leading_text, links


def _autolink(el, link_regexes=_link_regexes,
             avoid_elements=_avoid_elements,
             avoid_hosts=_avoid_hosts,
             avoid_classes=_avoid_classes,
             extra_params={}):
    """
    Turn any URLs into links.

    It will search for links identified by the given regular
    expressions (by default mailto and http(s) links).

    It won't link text in an element in avoid_elements, or an element
    with a class in avoid_classes.  It won't link to anything with a
    host that matches one of the regular expressions in avoid_hosts
    (default localhost and 127.0.0.1).

    If you pass in an element, the element's tail will not be
    substituted, only the contents of the element.
    """
    if el.tag in avoid_elements:
        if extra_params and el.tag in _force_update_params:
            el.attrib.update(extra_params)
        return
    class_name = el.get('class')
    if class_name:
        class_name = class_name.split()
        for match_class in avoid_classes:
            if match_class in class_name:
                return
    for child in list(el):
        _autolink(child, link_regexes=link_regexes,
            avoid_elements=avoid_elements,
            avoid_hosts=avoid_hosts,
            avoid_classes=avoid_classes,
            extra_params=extra_params)
        if child.tail:
            text, tail_children = _link_text(
                child.tail, link_regexes, avoid_hosts, factory=el.makeelement, extra_params=extra_params)
            if tail_children:
                child.tail = text
                index = el.index(child)
                el[index+1:index+1] = tail_children
    if el.text:
        text, pre_children = _link_text(
            el.text, link_regexes, avoid_hosts, factory=el.makeelement, extra_params=extra_params)
        if pre_children:
            el.text = text
            el[:0] = pre_children


def _autolink_html(html, *args, **kw):
    import lxml.html
    result_type = type(html)
    if isinstance(html, basestring):
        doc = lxml.html.fromstring(html)
    else:
        doc = copy.deepcopy(html)
    _autolink(doc, *args, **kw)
    return lxml.html._transform_result(result_type, doc)


def linebreaks(text):
    """
    Turns every new-line ("\n") into a "<br />" HTML tag.
    """
    return smart_unicode(text).replace('\n', '<br />')


def linkify(text, shorten=False, extra_params={"target": "_blank", "rel": "nofollow"},
            require_protocol=False, permitted_protocols=["http", "https"]):
    """Converts plain text into HTML with links.

    For example: ``linkify("Hello http://tornadoweb.org!")`` would return
    ``Hello <a href="http://tornadoweb.org">http://tornadoweb.org</a>!``

    Parameters:

    shorten: Long urls will be shortened for display.

    extra_params: Extra text to include in the link tag,
        e.g. linkify(text, extra_params={'rel': "nofollow", 'class': "external"})

    require_protocol: Only linkify urls which include a protocol. If this is
        False, urls such as www.facebook.com will also be linkified.

    permitted_protocols: List (or set) of protocols which should be linkified,
        e.g. linkify(text, permitted_protocols=["http", "ftp", "mailto"]).
        It is very unsafe to include protocols such as "javascript".
    """

    def make_link(m):
        url = m.group(1)
        proto = m.group(2)
        if require_protocol and not proto:
            return url  # not protocol, no linkify

        if proto and proto not in permitted_protocols:
            return url  # bad protocol, no linkify

        href = m.group(1)
        if not proto:
            href = "http://" + href   # no proto specified, use http

        params = ' '
        if extra_params:
            params += ' '.join(['%s="%s"' % (key, value) for key, value in extra_params.iteritems()])

        # clip long urls. max_len is just an approximation
        max_len = 30
        if shorten and len(url) > max_len:
            before_clip = url
            if proto:
                proto_len = len(proto) + 1 + len(m.group(3) or "")  # +1 for :
            else:
                proto_len = 0

            parts = url[proto_len:].split("/")
            if len(parts) > 1:
                # Grab the whole host part plus the first bit of the path
                # The path is usually not that interesting once shortened
                # (no more slug, etc), so it really just provides a little
                # extra indication of shortening.
                url = url[:proto_len] + parts[0] + "/" +\
                      parts[1][:8].split('?')[0].split('.')[0]

            if len(url) > max_len * 1.5:  # still too long
                url = url[:max_len]

            if url != before_clip:
                amp = url.rfind('&')
                # avoid splitting html char entities
                if amp > max_len - 5:
                    url = url[:amp]
                url += "..."

                if len(url) >= len(before_clip):
                    url = before_clip
                else:
                    # full url is visible on mouse-over (for those who don't
                    # have a status bar, such as Safari by default)
                    params += ' title="%s"' % href

        return u'<a href="%s"%s>%s</a>' % (href, params, url)

    try:
        text = text.replace('http://www.', 'www.').replace('www.', 'http://www.')
        return _autolink_html(text, _link_regexes, extra_params=extra_params)
    except ImportError:
        pass

    splitted_text = re.split("""(<a.*?>.*?</a>)""", text)
    for i in range(0, len(splitted_text), 2):
        splitted_text[i] = _URL_RE.sub(make_link, splitted_text[i])

    # The regex is modified to avoid character entites other than &amp; so
    # that we won't pick up &quot;, etc.
#    return _URL_RE.sub(make_link, text)
    return smart_unicode(''.join(splitted_text))

def sanitize(text):
    """
    Cleans up user input from potentially dangerous things,
    such as <script>, <img src="javascript:..." />, <a href="javascript:.."> etc.

    Please note, this function is **not 100% safe**.

    If want to ensure the input is safe it's best to just escape all HTML.

    If you decide to use ``markup,sanitize()`` make sure you have html5lib available on your system/project.
    """
    try:
        from airy.core import sanitizer
        return smart_unicode(sanitizer.clean_html(text))
    except ImportError:
        logging.error("You need html5lib in order to use sanitize")
        return "ERROR: You need html5lib in order to use sanitize"

def truncate(text, limit=80):
    return text[:limit]+'...'
