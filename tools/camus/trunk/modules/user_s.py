# -*- coding: utf-8 -*-
import re
import misc

def main(bot, args):
    """s\nShow radio state."""

    if args: return
    info, list = getRadioState()
    return '%s %s' %(info, list)

def getRadioState():
    data = misc.readUrl('http://fm.anoma.ch')
#    if not data: return 'can\'t get data', ''
    if not data: return 'нет данных от сервера, мб айскаст лежит?', ''

    try:
        data, count = re.subn('streamheader', 'streamheader', data, 100)
        data = re.sub('\n', '', data)
        print 'Stream count: ',count
        if count == 0:
            return 'Никто не вещает, извините.',''

        descr = re.findall('Stream Description.*?<td class="streamdata">(.*?)</td>', data)[0  ]
        song  = re.findall('Current Song.*?<td class="streamdata">(.*?)</td>', data)[0]
        curr = '';
        peak = '';
        name = '';
        descr = '';

        for i in range(count):
           curr = re.findall('Current Listeners.*?<td class="streamdata">(.*?)</td>', data)[i]
           peak = re.findall('Peak Listeners.*?<td class="streamdata">(.*?)</td>', data)[i]
           name = re.findall('<h3>Mount Point /(.*?)</h3></td>', data)[i]
           descr = descr + '%s: %s[%s] | ' %(name, curr, peak)

        print descr
        info = 'AnomaFM: %s <- %s' %(song, descr)
        #list = '(%s/%s)' %(curr2, peak2)
        return info,''
    except:
#        return 'can\'t parse data', ''
        return 'Парсер лох. Извините, ошибочка вышла.', ''
