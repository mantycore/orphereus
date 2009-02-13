import urllib
import re
import misc
from simplejson import loads

def main(bot, args):
    '''g [site] <query>\nSearch on google.\nSite:
v - ru.wikipedia.org
w - en.wikipedia.org
lm - lurkmore
wa - world-art.ru
ad - anidb.info
ed - encyclopediadramatica'''

    site = 'site:www.world-art.ru inurl:animation.php'

    query = site + ' '+' '.join(args)
    print query
    return google(query)

def google(query):
    query = urllib.quote(query)
    print query
    data = misc.readUrl('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&hl=ru' %query)
    if not data: return 'can\'t get data'

    try:
        convert = loads(data)
        results = convert['responseData']['results']
        if not results: return 'not found'

        url = urllib.unquote(results[0]['url'])
        title = results[0]['titleNoFormatting']
        content = results[0]['content']
        text = '%s\n%s\n%s' %(title, content, url)

        text = re.sub('<b>|</b>', '', text)
        text = re.sub('   ', '\n', text)

        return text
    except:
        return 'error'
