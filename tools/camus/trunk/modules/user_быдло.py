import misc
import re
import random

def main(bot, args):
    '''быдлобашорк'''
#    rint = random.randint(0,402422)
    url = 'http://bash.org.ru/random'
    data = misc.readUrl(url)
    if not data: return 'can\'t get data', ''
    
    data = re.sub('\n', '', data)
    quote = re.findall('</div>.{1,4}<div>(.*?)</div>', data)[0]
    quote = quote.decode('cp1251')
    quote = re.sub('<br>','\n', quote)
    quote = re.sub('<br />', "\n", quote)
    quote = re.sub('&quot;', '"', quote)

    return quote,''
