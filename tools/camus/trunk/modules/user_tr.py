# -*- coding: utf-8 -*-
import urllib
import misc
from simplejson import loads

def main(bot, args):
    '''tr <from_lang> <to_lang> <text>\nTranslate text.\nSee also: wtf'''

    if len(args) > 2:
        return translate(args[0], args[1], ' '.join(args[2:]))

def translate(from_l, to_l, text):
    text = urllib.quote(text.encode('utf-8'))
    data = misc.readUrl('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%%7C%s' %(text, from_l, to_l))
    if not data: return 'can\'t get data'
    
    try:
        convert = loads(data)
        status = convert['responseStatus']

        results = convert['responseData']['translatedText']
        if results: 
            return results
    except:
        pass

    return 'can\'t translate this shit!'
