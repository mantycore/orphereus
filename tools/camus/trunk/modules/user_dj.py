# -*- coding: utf-8 -*-
import re
import misc

def main(bot, args):
    """s\nShows radio state."""

    if args: return
    info, list = getRadioState()
    return '%s %s' %(info, list)

def getRadioState():
    data = misc.readUrl('http://fm.anoma.ch')
    if not data: return 'can\'t get data', ''
    data = re.sub('\n', '', data)

    try:
        #descr = re.findall('Stream Description.*?<td class="streamdata">(.*?)</td>', data)[0]
        descr = re.findall('Stream Title.*?<td class="streamdata">(.*?)</td>', data)[0]
        print descr
        pos = descr.find('//')
        print pos
        if pos!=-1:
            descr2 = descr[pos:0]
            desrc = descr2
        else:
            descr = re.findall('Stream Description.*?<td class="streamdata">(.*?)</td>', data)[0]


        print descr
        #info = 'AnomaFM MJ: %s' %(descr)
        #list = '(%s/%s)' %(curr2, peak2)
        return descr,''
    except:
        return 'can\'t parse data', ''
