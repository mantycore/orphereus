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
from pylons import config, request, c, g
from pylons.i18n import get_lang, set_lang
import miscUtils as utils
from routes.util import url_for

import time
import os
import socket, struct, sys

from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.lib.interfaces.AbstractPostOutputHook import AbstractPostOutputHook

import logging
log = logging.getLogger(__name__)

def overrideThumbnail(post, context, thumbnailId):
    outputHooks = g.implementationsOf(AbstractPostOutputHook)
    for hook in outputHooks:
        if hook.overrideThumbnail(post, context, thumbnailId):
            c.currentThumbnailHook = hook
            return True
    c.currentThumbnailHook = None
    return False

def doFastRender(post, thread, controller):
    return controller.fastRender('postReply', disableFiltering = True, thread = thread, post = post)

def repliesProxy(thread, controller):
    user = controller.userInst
    # flags = (isBoardView, showLongMessages)
    intFlags = (int(bool(c.board)) << 1) + int(not(user.hideLongComments) or (c.count == 1))
    tmplPrefix = (len(g.OPT.templates) > 1 and user.template) or ''
    keyPrefix = str('%s%d%s' % (tmplPrefix, intFlags, get_lang()[0]))
    postPairs = []
    prepareIdsForHighlight = (not c.userInst.Anonymous) and c.userInst.options.hlOwnPosts
    for post in thread.Replies:
        postPairs.append((post.id, post))
        if prepareIdsForHighlight and post.uidNumber == c.userInst.uidNumber:
            c.userPostsToHighlight.append(post.id)
    postsDict = dict(postPairs)
    postsRender = g.mc.get_multi(postsDict.keys(), key_prefix = keyPrefix)
    absentPosts = list(set(postsDict.keys()) - set(postsRender.keys()))
    if absentPosts:
        absentPostsRender = dict([(post, doFastRender(postsDict[post], thread, controller)) for post in absentPosts])
        g.mc.set_multi(absentPostsRender, key_prefix = keyPrefix)
        postsRender.update(absentPostsRender)
    sortedPostsRender = list([postsRender[id] for id in sorted(postsRender.keys())])
    return ''.join(sortedPostsRender)

def threadPanelCallback(thread, userInst):
    gvars = config['pylons.app_globals']
    callbacks = gvars.implementationsOf(AbstractPageHook)
    result = ''
    for cb in callbacks:
        ret = cb.threadPanelCallback(thread, userInst)
        if ret:
            result += ret
    return result

def postPanelCallback(thread, post, userInst):
    gvars = config['pylons.app_globals']
    callbacks = gvars.implementationsOf(AbstractPageHook)
    result = ''
    for cb in callbacks:
        ret = cb.postPanelCallback(thread, post, userInst)
        if ret:
            result += ret
    return result

def threadInfoCallback(thread, userInst):
    gvars = config['pylons.app_globals']
    callbacks = gvars.implementationsOf(AbstractPageHook)
    result = ''
    for cb in callbacks:
        ret = cb.threadInfoCallback(thread, userInst)
        if ret:
            result += ret
    return result

def headCallback(context):
    gvars = config['pylons.app_globals']
    callbacks = gvars.implementationsOf(AbstractPageHook)
    result = ''
    for cb in callbacks:
        ret = cb.headCallback(context)
        if ret:
            result += ret
    return result

def currentTime():
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

def renderSection(section):
    linkTemplate = (g.OPT.dvachStyleMenu and r'<a href="%s" title="%s"><b>%s</b></a>') \
                        or r'<a href="%s" title="%s"><b>/%s/</b></a>'
    joiner = (g.OPT.dvachStyleMenu and '/') or ''
    items = [linkTemplate % (link, title, name)
                    for (name, link, title) in section]
    return joiner.join(items)

def boardsSection(boardSection):
    uSection = [(board.tag, url_for('boardBase', board = board.tag), board.comment,)
                    for board in boardSection[0]]
    return renderSection(uSection)

def boardMenu(sections, sectionIsTags = True):
    if sectionIsTags:
        boardsRender = [boardsSection(section) for section in sections]
    else:
        boardsRender = [renderSection(section) for section in sections]
    joiner = (g.OPT.dvachStyleMenu and '//') or '] ['
    return '[%s]' % (joiner.join(boardsRender))

def itemsToSection(items):
    """
    #returns section-like list.
    #items: list of tuples: (name, url, testCase, hint)
    #each item is shown, if it's testCase is True. Rendered to
    #    <a hred="%(url)" title="%(hint)>
    """
    return [(url, hint, name,) for (name, url, testCase, hint) in items if testCase]

def templateExists(relName):
    #log.debug(os.path.join(g.OPT.templPath, relName))
    key = os.path.join(g.OPT.templPath, relName)
    return g.caches.setdefaultEx(key, os.path.exists, key)

def staticFile(fileName):
    spw, spl = g.OPT.staticPathWeb, g.OPT.staticPath
    ext = fileName.split('.')[-1]
    relFileName = "%s/%s" % (ext, fileName)
    localFileName = os.path.join(spl, relFileName)
    version = g.caches.setdefaultEx(localFileName, os.path.getmtime, localFileName)
    return u"%s%s?version=%s" % (spw, relFileName, str(version))

def ipToInt(ipStr):
    val = struct.unpack('!L', socket.inet_aton(ipStr.split(":")[-1]))[0]
    if val > sys.maxint:
        val = -(sys.maxint + 1) * 2 + val
    return val

def intToIp(ipint):
    ipi = int(ipint)
    return str((ipi >> 24) & 0xff) + '.' + str((ipi >> 16) & 0xff) + '.' + str((ipi >> 8) & 0xff) + '.' + str(ipi & 0xff)

def setLang(lang):
    oldLang = get_lang()
    if (lang and (len(lang) == 2)):
        set_lang(lang)
    else:
        langToSet = g.OPT.defaultLang
        for lang in request.languages:
            lang = lang[0:2]
            if lang in g.OPT.languages:
                langToSet = lang
                break
        set_lang(langToSet) # TODO: check
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

def postEnabledToShow(post, user):
    if user.isAdmin():
        return True

    if post.parentPost:
        post = post.parentPost

    for tag in post.tags:
        if tag.adminOnly:
            return False

    return True

def tsFormat(dt):
    # TODO: move format string to config ?
    return dt.strftime('%Y-%m-%d %H:%M:%S')
