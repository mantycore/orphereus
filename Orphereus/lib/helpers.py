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
from pylons import config, request, tmpl_context as c, app_globals as g, config
from pylons.i18n import get_lang, set_lang
from webhelpers.html.tags import link_to
import miscUtils as utils
import pylons as __pylons

def url_for(*args, **kwargs):
    return __pylons.url(*args, **kwargs)

import time
import os
import socket, struct, sys

from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.lib.interfaces.AbstractPostOutputHook import AbstractPostOutputHook
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook

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
    for post in thread.Replies:
        postPairs.append((post.id, post))
        if c.userInst.hlOwnPosts and c.userInst.ownPost(post): #post.uidNumber == c.userInst.uidNumber:
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

def universalStrCallback(methodName, interface, *args):
    gvars = config['pylons.app_globals']
    callbacks = gvars.implementationsOf(interface)
    result = ''
    for cb in callbacks:
        method = getattr(cb, methodName)
        ret = method(*args)
        if ret:
            result += ret
    return result

def universalListCallback(methodName, interface, *args):
    gvars = config['pylons.app_globals']
    callbacks = gvars.implementationsOf(interface)
    result = []
    for cb in callbacks:
        method = getattr(cb, methodName)
        ret = method(*args)
        if ret:
            result.extend(ret)
    return result

def threadPanelCallback(thread, userInst):
    return universalStrCallback("threadPanelCallback", AbstractPageHook, thread, userInst)

def threadInfoCallback(thread, userInst):
    return universalStrCallback("threadInfoCallback", AbstractPageHook, thread, userInst)

def postPanelCallback(thread, post, userInst):
    return universalStrCallback("postPanelCallback", AbstractPageHook, thread, post, userInst)

def postHeaderCallback(thread, post, userInst):
    return universalStrCallback("postHeaderCallback", AbstractPageHook, thread, post, userInst)

def threadHeaderCallback(thread, userInst):
    return universalStrCallback("threadHeaderCallback", AbstractPageHook, thread, userInst)

def headCallback(context):
    return universalStrCallback("headCallback", AbstractPageHook, context)

def boardInfoCallback(context):
    return universalStrCallback("boardInfoCallback", AbstractPageHook, context)

def extraPostingFields(context, atTop):
    return universalListCallback("extraPostingFields", AbstractPostingHook, context, atTop)

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

def renderTopLink(menuitem):
    return '<b>%s</b>' % link_to(menuitem.text,
                   menuitem.route or '#',
                   title = menuitem.hint,
                   onclick = menuitem.onclick,
                   target = menuitem.target)

def renderCollapsedLink(menuitem):
    return '%s' % link_to(menuitem.text,
                   menuitem.route or '#',
                   title = menuitem.hint,
                   onclick = menuitem.onclick,
                   target = menuitem.target)

def renderSubLink(menuitem):
    texttemplate = g.OPT.dvachStyleMenu and '%s' or '/%s/'
    return '<b>%s</b>' % link_to(texttemplate % menuitem.text,
                   menuitem.route or '#',
                   title = menuitem.hint,
                   onclick = menuitem.onclick,
                   target = menuitem.target)

def renderNCSection(section, splitter):
    return splitter.join([renderSubLink(subsubitem) for subsubitem in section])

def renderNCTop(items, source):
    ilen = len(items)
    elements = []
    splitter = (g.OPT.dvachStyleMenu and '/') or ''
    subSplitter = (g.OPT.dvachStyleMenu and '//') or '] ['
    for pos, item in enumerate(items):
        atBegin = (pos == 0)
        atEnd = (pos == (ilen - 1))
        subitems = source.get(item.id, None)
        if subitems:
            element = renderNCSection(subitems, splitter)
            if not atEnd:
                element += subSplitter
            elements.append(element)
        else:
            element = renderTopLink(item)
            if not atEnd:
                element += subSplitter
            elements.append(element)
    return ''.join(elements)

"""
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
"""

"""
def itemsToSection(items):
    "" "
    #returns section-like list.
    #items: list of tuples: (name, url, testCase, hint)
    #each item is shown, if it's testCase is True. Rendered to
    #    <a hred="%(url)" title="%(hint)>
    "" "
    return [(url, hint, name,) for (name, url, testCase, hint) in items if testCase]
"""
def templateExists(relName):
    #log.debug(os.path.join(g.OPT.templPath, relName))
    key = os.path.join(g.OPT.templPath, relName)
    return g.caches.setdefaultEx(key, os.path.exists, key)

def staticFile(fileName):
    spw, spl = g.OPT.staticPathWeb, g.OPT.staticPath
    ext = fileName.split('.')[-1]
    relFileName = "%s/%s" % (ext, fileName)
    localFileName = os.path.join(spl, relFileName)
    if not os.path.exists(localFileName):
        localFileName = os.path.join(spl, fileName)
        relFileName = fileName
    if os.path.exists(localFileName):
        version = g.caches.setdefaultEx(fileName, os.path.getmtime, localFileName)
        return u"%s%s?version=%s" % (spw, relFileName, str(version))
    log.error("Static file not found: %s" % localFileName)
    return u"fileNotFound"

def ipToInt(ipStr):
    val = struct.unpack('!L', socket.inet_aton(ipStr.split(":")[-1]))[0]
    if val > sys.maxint:
        val = -(sys.maxint + 1) * 2 + val
    return val

def intToIp(ipint):
    ipi = int(ipint)
    return str((ipi >> 24) & 0xff) + '.' + str((ipi >> 16) & 0xff) + '.' + str((ipi >> 8) & 0xff) + '.' + str(ipi & 0xff)

def langForCurrentRequest():
    langToSet = g.OPT.defaultLang
    for lang in request.languages:
        lang = lang[0:2]
        if lang in g.OPT.languages:
            langToSet = lang
            break
    return langToSet

def setLang(lang):
    oldLang = get_lang()
    if (lang and (len(lang) == 2)):
        set_lang(lang)
    else:
        langToSet = langForCurrentRequest()
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

    tocheck = post
    if post.parentPost:
        tocheck = post.parentPost

    for tag in tocheck.tags:
        if tag.adminOnly:
            return False

    return True

def tsFormat(dt):
    # TODO: move format string to config ?
    return dt.strftime('%Y-%m-%d %H:%M:%S')
