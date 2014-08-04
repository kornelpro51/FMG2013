from __future__ import unicode_literals
#This file is part of html2plaintext. The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer
import htmlentitydefs


def html2plaintext(html, body_id=None, encoding='ascii'):
    """Convert the HTML to plain text"""
    urls = []
    if body_id is not None:
        strainer = SoupStrainer(id=body_id)
    else:
        if html.count('<body'):
            strainer = SoupStrainer('body')
        strainer = None

    soup = BeautifulSoup(html, parseOnlyThese=strainer, fromEncoding=encoding)
    for link in soup.findAll('a'):
        title = unicode(link.renderContents(), encoding)
        for url in [x[1] for x in link.attrs if x[0] == 'href']:
            urls.append(dict(
                url=url,
                tag=unicode(str(link), encoding),
                title=title)
            )

    try:
        html = soup.renderContents(encoding=encoding)
    except AttributeError:
        html = soup.__str__(encoding)

    if isinstance(html, str) and encoding != 'ascii':
        html = unicode(html, encoding)

    url_index = []
    i = 0
    for d in urls:
        if d['title'] == d['url'] or u'http://' + d['title'] == d['url']:
            html = html.replace(d['tag'], d['url'])
        else:
            i += 1
            html = html.replace(d['tag'], u'%s [%s]' % (d['title'], i))
            url_index.append(d['url'])

    html = html.replace('<strong>', '*').replace('</strong>', '*')
    html = html.replace('<b>', '*').replace('</b>', '*')
    html = html.replace('<h3>', '*').replace('</h3>', '*')
    html = html.replace('<h2>', '**').replace('</h2>', '**')
    html = html.replace('<h1>', '**').replace('</h1>', '**')
    html = html.replace('<em>', '/').replace('</em>', '/')

    html = html.replace('\n', ' ')
    html = html.replace('<br>', '\n')
    html = html.replace('&nbsp;', ' ')
    html = html.replace('</p>', '\n\n')
    html = html.replace('</tr>', '\n\n')
    html = re.sub('<br\s*/>', '\n', html)
    html = html.replace(' ' * 2, ' ')

    def desperate_fixer(g):
        return ' '

    html = re.sub('<.*?>', desperate_fixer, html)
    html = u'\n'.join([x.lstrip() for x in html.splitlines()])  # lstrip lines

    for i, url in enumerate(url_index):
        if i == 0:
            html += u'\n\n'
        html += u'[%s] %s\n' % (i + 1, url)

    html = unescape(html)

    return html


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)