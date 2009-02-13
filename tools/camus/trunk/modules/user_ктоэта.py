# -*- coding: utf-8 -*-
import urllib
import re
import misc
from simplejson import loads

def whoplays():
    data = misc.readUrl('http://fm.anoma.ch')
    if not data: return 'нет данных от сервера, мб айскаст лежит?', ''

    try:
        data, count = re.subn('streamheader', 'streamheader', data, 100)
        data = re.sub('\n', '', data)
        print 'Stream count: ',count
        if count == 0:
            return 'Никто не вещает, извините.'

        song  = re.findall('Current Song.*?<td class="streamdata">(.*?)</td>', data)[0]
        #song = song.encode('utf-8')
        pos = song.find(' - ')
        song2 = song[0:pos]
        print song2
        return song2
    except:
        return 'Парсер лох. Извините, ошибочка вышла.'



def main(bot, args):
    '''g [site] <query>\nSearch on google.\nSite:
v - ru.wikipedia.org
w - en.wikipedia.org
lm - lurkmore
wa - world-art.ru
ad - anidb.info
ed - encyclopediadramatica'''

    site = 'en.wikipedia.org'
    if site:
        if len(args) == 1: return
        site = 'site:%s ' %site
        args = args[1:]
        
    args = whoplays()
        
    query = site + ' ' + args
    return google(site + ' ' + args)

def google(query):
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
