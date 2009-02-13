# -*- coding: utf-8 -*-
import misc
import re
import random

def main(bot, args):
    '''н€шорк'''
    rint = random.randint(0,3529)
    url = 'http://nya.sh/post/%s' %(rint)
    data = misc.readUrl(url)
    if not data: return 'can\'t get data', ''

    data = re.sub('\n', '', data)
    quote = re.findall('</i></div>(.*?)</div>', data)[0]
    
    quote = quote.decode('cp1251')
    quote = re.sub('<br />', '', quote)

    return quote,''
