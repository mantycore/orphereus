# -*- coding: utf-8 -*-
import urllib
import re
import misc
from simplejson import loads

def main(bot, args):
    '''g [site] <query>\nSearch on google.\nSite:
v|в - ru.wikipedia.org
w|ев - en.wikipedia.org
lm|лм - lurkmore
wa|ва - world-art.ru
ad|ад - anidb.info
ed|ед - encyclopediadramatica'''

    if not args: return
    
    site = ''
    if (args[0] == 'v') or (args[0] == 'в'):
        site = 'ru.wikipedia.org'
    elif (args[0] == 'w') or (args[0] == 'ев'):
        site = 'en.wikipedia.org'
    elif (args[0] == 'lm') or (args[0] == 'лм'):
        site = 'lurkmore.ru'
    elif (args[0] == 'wa') or (args[0] == 'ва'):
        site = 'world-art.ru'
    elif (args[0] == 'ad') or (args[0] == 'ад'):
        site = 'anidb.info'
    elif (args[0] == 'ed') or (args[0] == 'ед'):
        site = 'encyclopediadramatica.com'

    if site:
        if len(args) == 1: return
        site = 'site:%s ' %site
        args = args[1:]
    query = site + ' '.join(args)
    return google(site + ' '.join(args))

def google(query):
#    query = urllib.quote(query.encode('utf-8'))
    query = urllib.quote(query)
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
