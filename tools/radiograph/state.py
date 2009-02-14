#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib

def main(bot, args):
    """s\nreturns listeners - curr and max."""

    if args: return
    curr, max = getRadioState('http://fm.anoma.ch/')
    print "%s %s" %(curr,max)

def getRadioState(link):
    data = readUrl(link)
    if not data: return 'нет данных от сервера, мб айскаст лежит?', ''

    try:
        data, count = re.subn('streamheader', 'streamheader', data, 100)
        data = re.sub('\n', '', data)
        if count == 0:
            return 'Никто не вещает, извините.',''

        curr = 0;
        peak = 0;

        for i in range(count):
           curr2 = re.findall('Current Listeners.*?<td class="streamdata">(.*?)</td>', data)[i]
           peak2 = re.findall('Peak Listeners.*?<td class="streamdata">(.*?)</td>', data)[i]
           curr = curr + int(curr2);
           peak = peak + int(peak2);

        return curr,peak
    except:
#        return 'can\'t parse data', ''
        return 'Парсер лох. Извините, ошибочка вышла.', ''

def readUrl(url): #{{{
    try:
        u = urllib.urlopen(url)
        s = u.read()
        u.close()
    except:
        return None

    return s
#}}}

main('','')
