################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config, request
from pylons.i18n import get_lang, set_lang
import miscUtils as utils
from routes.util import url_for

import datetime
import os
import socket, struct, sys

import logging
log = logging.getLogger(__name__)

try:
    try:
        import cmemcache as memcache
        log.info('Using cmemcache')
    except:
        import memcache
        log.info('Using memcache, cmemcache not found. Consider installing')
    mc = None
except:
    log.warning('memcached interface not found, install memcache or cmemcache (recommended)')

def doFastRender(post, thread, controller):
    return controller.fastRender('wakaba/wakaba.postReply.mako', disableFiltering=True, thread=thread, post=post)

def repliesProxy(thread, controller):
    if mc:
        g = config['pylons.app_globals']
        postsDict = dict([(post.id, post) for post in thread.Replies])
        postsRender = mc.get_multi(postsDict.iterkeys(), key_prefix = g.OPT.cachePrefix)
        absentPosts = list(set(postsDict.iterkeys()) - set(postsRender.keys()))
        log.debug('NOT found: %s' % absentPosts)
        if absentPosts:
            absentPostsRender = dict([(post, doFastRender(postsDict[post], thread, controller)) for post in absentPosts])
            mc.set_multi(absentPostsRender, key_prefix = g.OPT.cachePrefix)
            postsRender.update(absentPostsRender)
        sortedPostsRender = list([postsRender[id] for id in sorted(postsRender.iterkeys())])
        return ''.join(sortedPostsRender)
    else:
        return u'<b>memcached interface is not installed</b><br />\
                 either install it, or set core.memcachedPosts -&gt; false'

threadPanelCallbacks = []
def threadPanelCallback(thread, userInst):
    result = ''
    for cb in threadPanelCallbacks:
        result += cb(thread, userInst)
    return result

postPanelCallbacks = []
def postPanelCallback(thread, post, userInst):
    result = ''
    for cb in postPanelCallbacks:
        result += cb(thread, post, userInst)
    return result

threadInfoCallbacks = []
def threadInfoCallback(thread, userInst):
    result = ''
    for cb in threadInfoCallbacks:
        result += cb(thread, userInst)
    return result

headCallbacks = []
def headCallback(context):
    result = ''
    for cb in headCallbacks:
        result += cb(context)
    return result

def currentTime():
    import time
    return time.time()

def applyFilters(inp, glob = False):
    gvars = config['pylons.app_globals']
    if glob:
        filters = gvars.globalFilterStack
    else:
        filters = gvars.filterStack
    out = inp
    for filter in filters:
        out = filter(out)
    return out

def postKwargs(threadId, postId):
    return {'post' : threadId and threadId or postId, 'anchor' : "i%s" % postId}

def postUrl(threadId, postId):
    return url_for('thread', **postKwargs(threadId, postId))

def expandName(name):
    #log.debug("expanding: %s" % name)
    if name:
        parts = name.split('.')
        if parts and utils.isNumber(parts[-2].replace('s', '')): #TODO: is the second condition really needed?
            ext = parts[-1].lower()
            prefix = name[0:4]
            #log.debug('%s/%s/%s' % (ext, prefix, name))
            return '%s/%s/%s' % (ext, prefix, name)
    #log.debug('passed: %s' % name)
    return name

def modLink(filePath, secid, hidePrefixes = False):
    #log.debug("gen link %s for id %s" %(filePath,secid))
    if hidePrefixes:
         baseName = os.path.basename(filePath)
         if baseName:
            return baseName

    return filePath

def templateExists(relName):
    #log.debug(config['pylons.g'].OPT.templPath)
    #log.debug(relName)
    #log.debug(os.path.join(config['pylons.g'].OPT.templPath, relName))
    #log.debug(os.path.exists(os.path.join(config['pylons.g'].OPT.templPath, relName)))
    return os.path.exists(os.path.join(config['pylons.app_globals'].OPT.templPath, relName))

def staticFile(fileName):
    gv = config['pylons.app_globals']
    spw = gv.OPT.staticPathWeb
    spl = gv.OPT.staticPath
    ext = fileName.split('.')[-1]
    relFileName = "%s/%s" % (ext, fileName)
    localFileName = os.path.join(spl, relFileName)
    version = gv.caches.get(localFileName, False)
    if not version:
        version = os.path.getmtime(localFileName)
        gv.caches[localFileName] = version
    return u"%s%s?version=%s" % (spw, relFileName, str(version))

def ipToInt(ipStr):
    val = struct.unpack('!L', socket.inet_aton(ipStr))[0]
    if val>sys.maxint:
        val = -(sys.maxint+1)*2 + val
    return val

def intToIp(ipint):
    ipi = int(ipint)
    return str((ipi >> 24) & 0xff)+'.'+str((ipi>>16) & 0xff)+'.'+str((ipi>>8) & 0xff)+'.'+str(ipi & 0xff) 

def setLang(lang):
    oldLang = get_lang()
    if (lang and (len(lang) == 2)):
        set_lang(lang)
    else:
        g = config['pylons.app_globals']
        langToSet = g.OPT.defaultLang
        for lang in request.languages:
            lang = lang[0:2]
            if lang in g.OPT.languages:
                langToSet = lang
                break
        set_lang(lang)
    return oldLang[0]

def makeLangValid(lang):
    if lang:
        if (len(lang) == 2):
            return  lang
        else:
            return ''

def sectionName(str):
    #TODO: find a better solution
    return str.replace(' ', '')