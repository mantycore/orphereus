# -*- coding: utf-8 -*-
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

from Orphereus.lib.base import *
from Orphereus.model import *
import sqlalchemy
import time
import re
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from Orphereus.lib.interfaces.AbstractHomeExtension import AbstractHomeExtension
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.BasePlugin import BasePlugin

import logging
log = logging.getLogger(__name__)

class OrphieViewPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Threads and boards (Obligatory)'),
                  'deps' : ('base_public',)
                 }
        BasePlugin.__init__(self, 'base_view', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('makeFwdTo', '/makeFwdTo',
                    controller = 'Orphie_View',
                    action = 'makeFwdTo')
        map.connect('frameMenu', '/frameMenu',
                    controller = 'Orphie_View',
                    action = 'frameMenu')
        map.connect('viewLogBase', '/viewLog',
                     controller = 'Orphie_View',
                     action = 'viewLog', page = 0,
                     requirements = dict(page = r'\d+'))
        map.connect('viewLog', '/viewLog/page/{page}',
                    controller = 'Orphie_View',
                    action = 'viewLog',
                    requirements = dict(page = r'\d+'))
        map.connect('viewAnimation',
                    '/viewAnimation/{source}/{animid}',
                    controller = 'Orphie_View',
                    action = 'viewAnimation',
                    animid = '0',
                    requirements = dict(source = r'\d+', animid = r'\d+'))
        map.connect('static', '/static/{page}',
                    controller = 'Orphie_View',
                    action = 'showStatic',
                    page = 'rules')

class OrphieViewController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def showStatic(self, page):
        c.boardName = _(page)
        return self.render('static.%s' % page)

    def frameMenu(self):
        c.suppressMenu = True
        c.suppressFooter = True
        c.suppressJsTest = True
        return self.render('frameMenu')

    def showPosts(self, threadFilter, tempid = '', page = 0, board = '', tags = [], tagList = []):
        if not g.OPT.allowTagCreation:
            for tag in tagList:
                if not Tag.getTag(tag):
                    return self.error(_(u"Board creation denied: %s") % tag)
        if isNumber(page):
            page = int(page)
        else:
            page = 0

        c.board = board

        extensions = g.caches.setdefaultEx('extensions', Extension.getList, True)
        extList = (ext.ext for ext in extensions)
        c.extLine = ', '.join(extList)

        count = threadFilter.count()
        tpp = self.userInst.threadsPerPage
        if page * tpp >= count and count > 0:
            return self.error(_("Incorrect page"))
        self.paginate(count, page, tpp)

        if count > 1:
            if bool(g.OPT.newsSiteMode) ^ bool(self.userInst.invertSortingMode):
                sortClause = Post.date.desc()
            else:
                sortClause = Post.bumpDate.desc()
            c.threads = threadFilter.order_by(Post.pinned.desc(), sortClause)[page * tpp: (page + 1) * tpp]
            if g.OPT.mixOldThreads and self.userInst.mixOldThreads and not board == '@':
                if g.OPT.newsSiteMode:
                    filterClause = Post.date < c.threads[-1].date
                else:
                    filterClause = Post.bumpDate < c.threads[-1].bumpDate
                oldThread = threadFilter.filter(filterClause).order_by(sqlalchemy.func.random()).first()
                #log.debug(oldThread)
                if oldThread:
                    oldThread.mixed = True
                    c.threads.insert(1, oldThread)

        elif count == 1:
            c.threads = [threadFilter.one()]
        elif count == 0:
            c.threads = []

        if tagList and len(tagList) == 1 and tags:
            currentBoard = tags[0]
            c.boardName = currentBoard and currentBoard.comment or (u"/%s/" % currentBoard.tag)
            c.tagLine = currentBoard.tag
        elif tagList or tags:
            tagDescr = Post.tagLine(tags, tagList)
            c.boardName = tagDescr[1]
            c.tagLine = tagDescr[0]
        else:
            c.boardName = board
            c.tagLine = c.boardName
            if board == '~':
                c.boardName = _('Overview')
            elif board == '@':
                c.boardName = _('Related threads')
            elif board == '*':
                c.boardName = _('My threads')

        c.boardOptions = Tag.conjunctedOptionsDescript(tags)
        c.invisibleBumps = asbool(meta.globj.OPT.invisibleBump)
        c.tagList = ' '.join(tagList)

        hiddenThreads = self.userInst.hideThreads
        hiddenThreads = map(lambda x: int(x), hiddenThreads) # legacy support
        for thread in c.threads:
            thread.hideFromBoards = (thread.id in hiddenThreads)
            thread.hidden = thread.hideFromBoards
            if thread.hideFromBoards:
                tl = []
                for tag in thread.tags:
                    tl.append(tag.tag)
                thread.tagLine = ', '.join(tl)

            if count > 1:
                replyCount = thread.replyCount
                replyLim = replyCount - self.userInst.repliesPerThread
                if replyLim < 0:
                    replyLim = 0
                thread.omittedPosts = replyLim
                thread.Replies = thread.filterReplies()[replyLim:]
            else:
                thread.Replies = thread.filterReplies().all()
                thread.omittedPosts = 0
                thread.hideFromBoards = False

        if tempid:
            oekaki = Oekaki.get(tempid)
            c.oekaki = oekaki
        else:
            c.oekaki = False

        c.curPage = page
        return self.render('posts')


    def GetBoard(self, board, tempid, page = 0):
        if board == None:
            if (g.OPT.framedMain and self.userInst and self.userInst.useFrame):
                c.frameTarget = request.params.get('frameTarget', h.url_for('boardBase', board = g.OPT.defaultBoard)) or h.url_for('boardBase', board = g.OPT.defaultBoard)
                return self.render('frameMain')
            else:
                board = g.OPT.defaultBoard

        if board == '!':
            if g.OPT.devMode:
                ct = time.time()
            c.boardName = _('Home')
            c.hometemplates = []
            homeModules = g.implementationsOf(AbstractHomeExtension)
            homeModulesDict = {}
            for module in homeModules:
                homeModulesDict[module.pluginId()] = module

            for enabledModuleName in g.OPT.homeModules:
                if enabledModuleName in homeModulesDict:
                    enabledModule = homeModulesDict[enabledModuleName]
                    c.hometemplates.append(enabledModule.templateName)
                    enabledModule.prepareData(self, c)

            if g.OPT.devMode:
                c.log.append("home: " + str(time.time() - ct))
            return self.render('home')

        board = filterText(board)
        if not g.OPT.allowOverview and '~' in board:
            return self.error(_("Overview is disabled."))
        c.PostAction = h.url_for('postThread', board = board) #board
        c.currentRealm = board

        if isNumber(page):
            page = int(page)
        else:
            page = 0

        filter = Post.buildMetaboardFilter(board, self.userInst)
        tags = Tag.getAllByNames(filter[1])
        return self.showPosts(threadFilter = filter[0], tempid = tempid, page = int(page), board = board, tags = tags, tagList = filter[1])

    def GetThread(self, post, tempid):
        thePost = Post.getPost(post)
        #if thePost isn't op-post, redirect to op-post instead
        if thePost and thePost.parentPost:
            if isNumber(tempid) and not int(tempid) == 0:
                redirect_to('thread', post = thePost.parentid, tempid = int(tempid))
            else:
                redirect_to('thread', **h.postKwargs(thePost.parentid, thePost.id))

        if not thePost:
            return self.error(_("No such post exist."))

        c.PostAction = h.url_for('postReply', post = thePost.id) #thePost.id
        c.currentRealm = thePost.id
        filter = Post.buildThreadFilter(self.userInst, thePost.id)
        return self.showPosts(threadFilter = filter, tempid = tempid, page = 0, board = '', tags = thePost.tags)

    def makeFwdTo(self):
        tagsStr = request.POST.get('tags', '')
        if tagsStr:
            tags = tagsStr.split(' ')
            return redirect_to('boardBase', board = '%2B'.join(tags).encode('utf-8'))
        else:
            return self.error(_("You must specify post tagline."))

    def viewLog(self, page):
        if g.OPT.usersCanViewLogs:
            c.boardName = 'Logs'
            page = int(page)
            count = LogEntry.count(disabledEvents)
            tpp = 50
            self.paginate(count, page, tpp)
            c.logs = LogEntry.getRange(page * tpp, (page + 1) * tpp, disabledEvents)
            rv = re.compile('(\d+\.){3}\d+')
            for le in c.logs:
                le.entry = rv.sub('<font color="red">[IP REMOVED]</font>', le.entry)
            return self.render('logs')
        else:
            return redirect_to('boardBase')

    def oekakiDraw(self, url, selfy, anim, tool, sourceId):
        if not self.currentUserCanPost():
            return self.error(_("Posting is disabled"))

        c.url = url
        enablePicLoading = not (request.POST.get('oekaki_type', 'reply').lower() == 'new')

        selfy = request.POST.get('selfy', selfy)
        if selfy:
            c.selfy = (selfy == '+selfy') or (selfy == 'on')
        else:
            c.selfy = self.userInst.oekUseSelfy

        anim = request.POST.get('animation', anim)
        if anim:
            c.animation = (anim == '+anim') or (anim == 'on')
        else:
            c.animation = self.userInst.oekUseAnim

        oekType = ''
        tool = request.POST.get('oekaki_painter', tool)
        if (tool and tool.lower() == 'shipro') or (not tool and c.userInst.oekUsePro):
            oekType = 'Shi pro'
            c.oekakiToolString = 'pro'
        else:
            oekType = 'Shi normal'
            c.oekakiToolString = 'normal';

        c.canvas = False
        c.width = request.POST.get('oekaki_x', '300')
        c.height = request.POST.get('oekaki_y', '300')

        if not (isNumber(c.width) or isNumber(c.height)) or (int(c.width) <= 10 or int(c.height) <= 10):
            c.width = 300
            c.height = 300
        c.tempid = str(long(time.time() * 10 ** 7))

        oekSource = None
        sourceAttachment = request.POST.get('sourceAttachment', None) or sourceId
        if sourceAttachment and isNumber(url) and enablePicLoading:
            post = Post.getPost(url)
            if not post:
                return self.error(_("Post doesn't exists"))

            sourceAttachment = int(sourceAttachment)
            if sourceAttachment >= len(post.attachments):
                return self.error(_("Post doesn't have such many attachments"))

            attachment = post.attachments[sourceAttachment]
            pic = attachment.attachedFile
            if pic and pic.width:
                oekSource = post.id
                c.canvas = h.modLink(pic.path, c.userInst.secid())
                c.width = pic.width
                c.height = pic.height

                if attachment.animpath:
                    c.pchPath = h.modLink(attachment.animpath, c.userInst.secid())
            else:
                sourceAttachment = None
        else:
            sourceAttachment = None

        Oekaki.create(c.tempid, self.sessUid(), oekType, oekSource, sourceAttachment, c.selfy)
        return self.render('spainter')

    def viewAnimation(self, source, animid):
        post = Post.getPost(source)
        animid = int(animid)
        if not post or not post.attachments or animid >= len(post.attachments):
            return self.error(_("No animation associated with this post"))

        animpath = post.attachments[animid].animpath
        if not animpath:
            return self.error(_("Incorrect animation ID"))
        c.pchPath = h.modLink(animpath, c.userInst.secid())
        return self.render('shiAnimation')
