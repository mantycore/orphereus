import urllib
import re

def force_unicode(string, encoding='utf-8'): #{{{
    if type(string) is str:
        string = string.decode(encoding)
    if type(string) is not unicode:
        string = unicode(string)
    return string
#}}}

def readUrl(url): #{{{
    try:
        u = urllib.urlopen(url)
        s = u.read()
        u.close()
    except:
        return None

    return s
#}}}

def getImgXML(img_url, img_src): #{{{
    img_url = re.sub('"|\'|<|>', '', img_url)
    img_src = re.sub('"|\'|<|>', '', img_src)
    img_url = re.sub('&', '&amp;', img_url)
    img_src = re.sub('&', '&amp;', img_src)

    return '<html xmlns=\'http://jabber.org/protocol/xhtml-im\'>' +\
           '<body xml:lang=\'en-US\' xmlns=\'http://www.w3.org/1999/xhtml\'>' +\
           '<a href=\'%s\'><img src=\'%s\' /></a>' %(img_url, img_src) +\
           '</body>' +\
           '</html>'
#}}}
