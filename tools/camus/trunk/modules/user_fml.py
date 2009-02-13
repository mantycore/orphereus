# -*- coding: utf-8 -*-
import misc
import re

def main(bot, args):
    '''fuck my life'''
    url = 'http://www.fmylife.com/random'
    data = misc.readUrl(url)
    if not data: return 'can\'t get data', ''

    data = re.sub('\n', '', data)
    quote = re.findall('<div class="post"><p>(.*?)</p>', data)[0]
    
#    quote = quote.decode('cp1251')
    quote = re.sub('<br />', '', quote)

    return quote,''
