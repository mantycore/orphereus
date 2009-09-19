from html5lib.html5parser import HTMLParser

#todo: write plugin to regenerate, backgrounds
def codeHighlightCss(background):
    from pygments.formatters import HtmlFormatter
    return HtmlFormatter().get_style_defs('.sourcecode')

def generateHighlightCSS(path, background = None):
    f = open(path, 'w')
    f.write(codeHighlightCss(background))
    f.close()

def fixHtml(html):
    p = HTMLParser()
    return ''.join([token.toxml() for token in p.parseFragment(html).childNodes])

def replaceEntities(text):
    return text.replace('&', '&amp;') \
               .replace('<', '&lt;') \
               .replace('>', '&gt;') \
               .replace("'", '&#39;') \
               .replace('"', '&quot;')

def replaceAcromyns(text):
    return text.replace('(c)', '&copy;') \
               .replace('--', '&mdash;') \
               .replace('(tm)', '&#153;') \
               .replace('...', '&#8230;') \

def filterText(text):
    generateHighlightCSS('d:/highlight.css')
    return replaceAcromyns(replaceEntities(text))


