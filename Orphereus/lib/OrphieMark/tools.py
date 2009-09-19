from html5lib.html5parser import HTMLParser

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
    return replaceAcromyns(replaceEntities(text))
