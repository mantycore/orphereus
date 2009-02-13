# -*- coding: utf-8 -*-
import re
import misc

def main(bot, args):
    """link\nShows active broadcasting streams."""

    if args: return
    info, list = getRadioState()
    return '%s %s' %(info, list)

def getRadioState():
    server = 'http://fm.anoma.ch'
    data = misc.readUrl(server)
    if not data: return 'нет данных от сервера, мб айскаст лежит?', ''

    try:
        data, count = re.subn('streamheader', 'streamheader', data, 100)
        data = re.sub('\n', '', data)
        print 'Stream count: ',count
        if count == 0:
            return 'Никто не вещает, извините.',''

        link = '';
        bitrate = '';
        code = '';
        links = '';

        for i in range(count):
           link = re.findall('<a href="(.{1,15}?)">M3U</a>', data)[i]
           code = re.findall('Content Type.*?<td class="streamdata">[^/]*?/(.*?)</td>', data)[i]
           bitrate = re.findall('Bitrate.*?<td class="streamdata">(.*?)</td>', data)[i]
           print link, code, bitrate
           links = links + '%s%s | Encoder: %s | Quality: %s\n' %(server,link,code,bitrate)

        info = 'Active broadcast links: \n%s' %(links)
        return info,''
    except:
        return 'can\'t parse data', ''
