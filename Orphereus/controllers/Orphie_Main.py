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
from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.orm import class_mapper
import sqlalchemy
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
import base64
from Orphereus.lib.OrphieMark.OrphieParser import OrphieParser
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from Orphereus.lib.fileHolder import AngryFileHolder
from Orphereus.lib.processFile import processFile
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.lib.interfaces.AbstractProfileExtension import AbstractProfileExtension
from Orphereus.lib.interfaces.AbstractSearchModule import AbstractSearchModule
from Orphereus.lib.interfaces.AbstractHomeExtension import AbstractHomeExtension
from OrphieBaseController import OrphieBaseController
from mutagen.easyid3 import EasyID3
from urllib import quote_plus, unquote

import logging
log = logging.getLogger(__name__)

#TODO: new debug system. Don't forget about c.log and c.sum

class OrphieMainController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    #parser callback
    def cbGetPostAndUser(self, id):
        return (Post.getPost(id), self.userInst.uidNumber)

    def selfBan(self, confirm):
        if g.OPT.spiderTrap and not self.userInst.Anonymous:
            if confirm:
                self.userInst.ban(2, _("[AUTOMATIC BAN] Security alert type 2"), -1)
                redirect_to('boardBase')
            else:
                return self.render('selfBan')
        else:
            return redirect_to('boardBase')

    def frameMenu(self):
        c.disableMenu = True
        c.disableFooter = True
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
            c.boardName = currentBoard.options and currentBoard.options.comment or (u"/%s/" % currentBoard.tag)
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
        for thread in c.threads:
            thread.hideFromBoards = (str(thread.id) in hiddenThreads)
            thread.hidden = thread.hideFromBoards
            if thread.hideFromBoards:
                tl = []
                for tag in thread.tags:
                    tl.append(tag.tag)
                thread.tagLine = ', '.join(tl)

            if count > 1:
                replyCount = thread.replyCount
                #replyCount = Post.query.options(eagerload('file')).filter(Post.parentid==thread.id).count()
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

    def gotoDestination(self, post):
        taglineSource = post
        if post.parentid:
            taglineSource = post.parentPost
        postTagline = Post.tagLine(taglineSource.tags)[0]

        tagLine = request.POST.get('tagLine', postTagline)

        dest = int(request.POST.get('goto', 0))
        if isNumber(dest):
            dest = int(dest)
        else:
            dest = 0

        curPage = request.POST.get('curPage', 0)
        if isNumber(curPage):
            curPage = int(curPage)
        else:
            curPage = 0

        anchor = "i%d" % post.id

        if dest == 0: #current thread
            if post.parentid:
                return redirect_to(action = 'GetThread', post = post.parentid, board = None, anchor = anchor)
            else:
                return redirect_to(action = 'GetThread', post = post.id, board = None, anchor = anchor)
        elif dest == 1 or dest == 2: # current board
            if  tagLine:
                if dest == 1:
                    curPage = 0
                return redirect_to('board', board = tagLine, page = curPage, anchor = anchor)
        elif dest == 3: # overview
            pass
        elif dest == 4: # destination board
            return redirect_to('boardBase', board = postTagline)
        elif dest == 5: #referrer
            return redirect_to(request.headers.get('REFERER', tagLine.encode('utf-8')), anchor = anchor)

        # impossible with correct data
        return redirect_to('boardBase', board = g.OPT.allowOverview and '~' or postTagline, anchor = anchor)

    def showProfile(self):
        if self.userInst.Anonymous and not g.OPT.allowAnonProfile:
            return self.error(_("Profile is not avaiable to Anonymous users."))

        self.forceNoncachedUser()
        c.additionalProfileLinks = []
        linkGenerators = g.implementationsOf(AbstractProfileExtension)
        for generator in linkGenerators:
            linkslist = generator.additionalProfileLinks(self.userInst)
            if linkslist:
                c.additionalProfileLinks += linkslist

        c.templates = g.OPT.templates
        c.styles = g.OPT.cssFiles[self.userInst.template]
        c.languages = g.OPT.languages
        c.profileChanged = False
        c.boardName = _('Profile')
        if bool(request.POST.get('update', False)):
            lang = filterText(request.POST.get('lang', self.userInst.lang))
            c.reload = (h.makeLangValid(lang) != self.userInst.lang)

            for valueName in self.userInst.booleanValues:
                val = bool(request.POST.get(valueName, False))
                setattr(self.userInst, valueName, val)

            for valueName in self.userInst.intValues:
                val = request.POST.get(valueName, getattr(self.userInst, valueName))
                if isNumber(val):
                    setattr(self.userInst, valueName, int(val))

            for valueName in self.userInst.stringValues:
                val = filterText(request.POST.get(valueName, getattr(self.userInst, valueName)))
                setattr(self.userInst, valueName, val)

            homeExcludeTags = Tag.stringToTagLists(request.POST.get('homeExclude', u''), False)[0]
            #log.debug(homeExcludeTags)
            homeExcludeList = []
            for t in homeExcludeTags:
                homeExcludeList.append(t.id)
            self.userInst.homeExclude = homeExcludeList

            if not c.userInst.Anonymous:
                c.profileMsg = _('Password was NOT changed.')
                key = request.POST.get('key', '').encode('utf-8')
                key2 = request.POST.get('key2', '').encode('utf-8')
                currentKey = request.POST.get('currentKey', '').encode('utf-8')
                passwdRet = self.userInst.passwd(key, key2, False, currentKey)
                if passwdRet == True:
                    c.profileMsg = _('Password was successfully changed.')
                elif passwdRet == False:
                    c.message = _('Incorrect security codes')
                else:
                    return self.error(passwdRet)
                meta.Session.commit()

            c.profileChanged = True
            c.profileMsg += _(' Profile was updated.')
            if c.reload:
                c.profileMsg += _(' Reload page for language changes to take effect.')

        homeExcludeTags = Tag.getAllByIds(self.userInst.homeExclude)
        homeExcludeList = []
        for t in homeExcludeTags:
            homeExcludeList.append(t.tag)
        c.homeExclude = ', '.join(homeExcludeList)
        c.hiddenThreads = Post.filter(Post.id.in_(self.userInst.hideThreads)).options(eagerload('tags')).all()
        for t in c.hiddenThreads:
            tl = []
            for tag in t.tags:
                tl.append(tag.tag)
            t.tagLine = ', '.join(tl)
        c.userInst = self.userInst
        return self.render('profile')

    def DeletePost(self, board):
        if not self.currentUserCanPost():
            return self.error(_("Removing prohibited"))

        fileonly = 'fileonly' in request.POST
        redirectAddr = board

        opPostDeleted = False
        reason = filterText(request.POST.get('reason', '???'))

        remPass = ''
        if self.userInst.Anonymous:
            remPass = hashlib.md5(request.POST.get('remPass', '').encode('utf-8')).hexdigest()

        retest = re.compile("^\d+$")
        for i in request.POST:
            if retest.match(request.POST[i]):
                post = Post.getPost(request.POST[i])
                if post:
                    res = post.deletePost(self.userInst, fileonly, True, reason, remPass)
                opPostDeleted = opPostDeleted or res

        tagLine = request.POST.get('tagLine', g.OPT.allowOverview and '~' or '!')
        if opPostDeleted:
            redirectAddr = tagLine

        return redirect_to('boardBase', board = redirectAddr)

    def search(self, text, page = 0):
        rawtext = text
        if not text:
            rawtext = request.POST.get('query', u'')
        text = filterText(rawtext)

        if isNumber(page):
            page = int(page)
        else:
            page = 0

        pp = self.userInst.threadsPerPage
        c.boardName = _("Search")
        c.query = text

        tagfilter = False
        filteredQueryRe = re.compile("^(([^:]+):){1}(.+)$").match(text)
        if filteredQueryRe:
            groups = filteredQueryRe.groups()
            filterName = groups[1]
            text = groups[2]
            tagfilter = Post.buildMetaboardFilter(filterName, self.userInst)[2]

        if not tagfilter:
            tagfilter = Post.buildMetaboardFilter(False, self.userInst)[2]

        filteringClause = or_(tagfilter, Post.parentPost.has(tagfilter))

        searchModules = g.implementationsOf(AbstractSearchModule)
        searchPlugin = None
        for sm in searchModules:
            if sm.pluginId() == g.OPT.searchPluginId:
                searchPlugin = sm

        if not searchPlugin:
            return self.error(_("Search plugin isn't configured"))

        #searchRoutine = searchPlugin.config.get('searchRoutine', None)
        #if not searchRoutine:
        #    return self.error(_("The plugin selected to search doesn't provide search features"))

        posts, count, failInfo, highlights, warnings = searchPlugin.search(filteringClause, text, page, pp)
        if failInfo:
            return self.error(failInfo)
        self.paginate(count, page, pp)

        c.warnings = warnings
        c.highlights = highlights
        c.posts = posts
        return self.render('search')

    def Anonimyze(self, post):
        postid = request.POST.get('postId', False)
        batch = request.POST.get('batchFA', False)
        if postid and isNumber(postid):
            c.FAResult = self.processAnomymize(int(postid), batch)
        else:
            c.boardName = _('Final Anonymization')
            c.FAResult = False
            c.postId = post
        return self.render('finalAnonymization')

    def processAnomymize(self, postid, batch):
        if not g.OPT.enableFinalAnonymity:
            return [_("Final Anonymity is disabled")]

        if self.userInst.Anonymous:
            return [_("Final Anonymity available only for registered users")]

        result = []
        post = Post.getPost(postid)
        if post:
            posts = []
            if not batch:
                posts = [post]
            else:
                posts = Post.filter(and_(Post.uidNumber == self.userInst.uidNumber, Post.date <= post.date)).all()
            for post in posts:
                if post.uidNumber != self.userInst.uidNumber:
                    result.append(_("You are not author of post #%s") % post.id)
                else:
                    delay = g.OPT.finalAHoursDelay
                    timeDelta = datetime.timedelta(hours = delay)
                    if post.date < datetime.datetime.now() - timeDelta:
                        post.uidNumber = 0
                        post.ip = None
                        result.append(_("Post #%d successfully anonymized") % post.id)
                    else:
                        params = (post.id, str(post.date + timeDelta), str(datetime.datetime.now()))
                        result.append(_("Can't anomymize post #%d now, it will be allowed after %s (now: %s)" % params))
            meta.Session.commit()
        else:
            result = [_("Nothing to anonymize")]

        return result

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
        enablePicLoading = not (request.POST.get('oekaki_type', 'Reply').lower() == 'new')
        c.selfy = bool(request.POST.get('selfy', False)) or selfy == '+selfy'
        c.animation = bool(request.POST.get('animation', False)) or anim == '+anim'

        oekType = ''
        if request.POST.get('oekaki_painter', False).lower() == 'shipro' or tool.lower() == 'shipro':
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

    def PostReply(self, post):
        return self.processPost(postid = post)

    def PostThread(self, board):
        return self.processPost(board = board)

    def ajaxPostReply(self, post):
        return self.processPost(postid = post, ajaxRequest = True)

    def ajaxPostThread(self, board):
        return self.processPost(board = board, ajaxRequest = True)

    @staticmethod
    def getTagDescription(tagName, textFilter):
        rex = re.compile(r"^tagname_(\d+)$")
        for name in request.POST.keys():
            matcher = rex.match(name)
            if matcher and request.POST[name] == tagName:
                return textFilter(request.POST.get('tagdef_%s' % matcher.group(1), ''))

    def processPost(self, postid = None, board = u'', ajaxRequest = False):
        def ajaxError(message):
            return message
        def usualError(message):
            return self.error(message)

        postingHooks = g.implementationsOf(AbstractPostingHook)

        errorHandler = usualError
        if ajaxRequest:
            errorHandler = ajaxError

        if c.ban and c.ban.enabled:
            if ajaxRequest:
                return errorHandler(_("IP banned"))
            else:
                redirect_to('ipBanned')

        if not self.currentUserCanPost():
            return errorHandler(_("Posting is disabled"))

        if isNumber(postid):
            postid = int(postid)
        else:
            postid = None

        baseEncoded = 'baseAndUrlEncoded' in request.POST
        def normalFilter(text):
            return filterText(text)
        def base64TextFilter(text):
            tmp = unquote(text)
            if '%u' in tmp:
                tmp = tmp.replace('%u', '\\u').decode('unicode_escape')
            return filterText(tmp)
        textFilter = normalFilter
        if baseEncoded:
            textFilter = base64TextFilter

        postMessage = request.POST.get('message', u'')
        c.postMessage = textFilter(postMessage)

        postTitle = textFilter(request.POST.get('title', u''))
        c.postTitle = postTitle

        tagstr = request.POST.get('tags', False)
        if tagstr:
            c.postTagLine = textFilter(tagstr)

        response.set_cookie('orphie-postingCompleted', 'no')
        #response.set_cookie('orphie-lastPost', quote_plus(c.postMessage.encode('utf-8')))
        response.set_cookie('orphie-lastTitle', quote_plus(c.postTitle.encode('utf-8')))
        if tagstr:
            response.set_cookie('orphie-lastTagLine', quote_plus(c.postTagLine.encode('utf-8')))

        postRemovemd5 = None
        if self.userInst.Anonymous:
            captchaOk = (g.OPT.allowAnswersWithoutCaptcha and postid) or g.OPT.forbidCaptcha
            if not captchaOk:
                anonCaptId = session.get('anonCaptId', False)
                captcha = Captcha.getCaptcha(anonCaptId)
                #log.debug("captcha: id == %s, object == %s " %(str(anonCaptId), str(captcha)))
                if captcha:
                    captchaOk = captcha.test(request.POST.get('captcha', False))

            if not captchaOk:
                return errorHandler(_("Incorrect Captcha value"))

            remPass = request.POST.get('remPass', False)
            if remPass:
                postRemovemd5 = hashlib.md5(remPass.encode('utf-8')).hexdigest()
                response.set_cookie('orhpieRemPass', unicode(remPass), max_age = 3600)
                #log.debug('setting pass cookie in post proc: %s' %str(remPass.encode('utf-8')))

        afterPostCallbackParams = {}
        thread = None
        tags = []
        if postid != None:
            thePost = Post.getPost(postid)

            if not thePost:
                return errorHandler(_("Can't post into non-existent thread"))

            if thePost.parentid != None:
                thread = thePost.parentPost
            else:
                thread = thePost
            tags = thread.tags
        else:
            for hook in postingHooks:
                tagstr, afterPostCallbackParams[hook.pluginId()] = hook.tagCreationHandler(tagstr, self.userInst, textFilter)

            tags, createdTags, dummy = Tag.stringToTagLists(tagstr, g.OPT.allowTagCreation)
            for tag in createdTags:
                tagdef = self.getTagDescription(tag.tag, textFilter)
                if tagdef:
                    tag.options.comment = tagdef

            if not tags:
                return errorHandler(_("You should specify at least one board"))

            maxTagsCount = g.OPT.maxTagsCount
            if len(tags) > maxTagsCount:
                return errorHandler(_("Too many tags. Maximum allowed: %s") % (maxTagsCount))

            usualTagsCC = 0
            svcTagsCC = 0
            permaTagsCC = 0
            for tag in tags:
                if not (tag.options and tag.options.service):
                    usualTagsCC += 1
                else:
                    svcTagsCC += 1
                if tag.options and tag.options.persistent:
                    permaTagsCC += 1

            if len(tags) > 1 and not g.OPT.allowCrossposting:
                if not g.OPT.allowCrosspostingSvc:
                    return errorHandler(_("Crossposting disabled"))
                else:
                    if usualTagsCC > 1:
                        return errorHandler(_("Crossposting allowed only for service tags"))

            if not g.OPT.allowPureSvcTagline and usualTagsCC == 0:
                return errorHandler(_("Can't post with service tags only"))

            #TODO: this check should be done before Tag() constructors
            #In other cases only Autocommit=False will be correct
            permCheckRes = Tag.checkForConfilcts(tags)
            if not permCheckRes[0]:
                return errorHandler(_("Tags restrictions violations:<br/> %s") % ('<br/>'.join(permCheckRes[1])))

        for hook in postingHooks:
            prohibition = hook.beforePostCallback(self, request, thread = thread, tags = tags)
            if prohibition:
                return errorHandler(prohibition)

        options = Tag.conjunctedOptionsDescript(tags)
        if Tag.tagsInConflict(options, postid): #not options.images and ((not options.imagelessThread and not postid) or (postid and not options.imagelessPost)):
            return errorHandler(_("Unacceptable combination of tags"))

        files = []
        postMessageInfo = None # TODO: Reserved for future. It may be used for "USER WAS BANNED FOR THIS POST" messages
        tempid = request.POST.get('tempid', False)
        animPath = None
        oekakiInfo = None
        if tempid:
            oekaki = Oekaki.get(tempid)
            if oekaki:
                animPath = oekaki.animPath
                files = [(FieldStorageLike(oekaki.path, os.path.join(g.OPT.uploadPath, oekaki.path)), -1)]
                oekakiInfo = u'<span class="postInfo">Drawn with <b>%s%s</b> in %s seconds' \
                                 % (oekaki.type, oekaki.selfy and "+selfy" or "", str(int(oekaki.time / 1000)))
                if oekaki.sourcePost:
                    oekakiInfo += ", picture %d from post %s was used as source" % (oekaki.sourcePicIdx + 1, self.formatPostReference(oekaki.sourcePost))
                oekakiInfo += u'</span>'
                oekaki.delete()
        #else:
        retest = re.compile("^file_(\d+)$")
        fileIds = []
        for i in request.POST.keys():
            matcher = retest.match(i)
            if matcher:
                fileIds.append(int(matcher.group(1)))
        fileIds = list(set(fileIds))
        fileIds.sort()
        for fileId in fileIds:
            file = request.POST.get('file_%d' % fileId, None)
            if file is not None:
                files.append((file, fileId))

        postMessageShort = None
        postMessageRaw = None
        if postMessage:
            if len(postMessage) <= 15000:
                #parser = WakabaParser(g.OPT, thread and thread.id or - 1)
                parser = OrphieParser(g, self)
                maxLinesInPost = int(g.OPT.maxLinesInPost)
                cutSymbols = g.OPT.cutSymbols
                #parsedMessage = parser.parseWakaba(postMessage, self, lines = maxLinesInPost, maxLen = cutSymbols)
                parsedMessage = parser.parseMessage(postMessage, thread and thread.id or - 1, maxLinesInPost, cutSymbols)
                fullMessage = parsedMessage[0]
                postMessageShort = parsedMessage[1]

                #FIXME: not best solution
                #if not fullMessage[5:].startswith(post.message):
                if (not postMessage in fullMessage) or postMessageShort:
                    postMessageRaw = postMessage

                postMessage = fullMessage
            else:
                return errorHandler(_('Message is too long'))

        picInfos = [] #TODO: class PicInfo instead of Empty
        for file, fileId in files:
            assert len(picInfos) <= options.allowedAdditionalFiles + 1
            if len(picInfos) == options.allowedAdditionalFiles + 1:
                break

            fileDescriptors = processFile(file, options.thumbSize, baseEncoded = baseEncoded)
            #log.debug(fileDescriptors)
            fileHolder = False
            #existentPic = False
            picInfo = False
            if fileDescriptors:
                fileHolder = fileDescriptors[0] # Object for file auto-removing
                picInfo = fileDescriptors[1]
                existentPic = fileDescriptors[2]
                errorMessage = fileDescriptors[3]
                if errorMessage:
                    return self.error(errorMessage)

                picInfo.existentPic = existentPic
                picInfo.fileHolder = fileHolder
                picInfo.additionalInfo = ''

            if picInfo:
                if not options.images:
                    return errorHandler(_("Files are not allowed on this board"))
                if picInfo.fileSize > options.maxFileSize:
                    return errorHandler(_("File size (%d) exceeds the limit (%d)") % (picInfo.fileSize, options.maxFileSize))
                if picInfo.sizes and picInfo.sizes[0] and picInfo.sizes[1] and (picInfo.sizes[0] < options.minPicSize or picInfo.sizes[1] < options.minPicSize):
                    return errorHandler(_("Image is too small. At least one side should be %d or more pixels.") % (options.minPicSize))

                if fileId == -1: # Oekaki
                    picInfo.relationInfo = oekakiInfo
                    picInfo.animPath = animPath
                else:
                    picInfo.relationInfo = None
                    picInfo.animPath = None

                if picInfo.extension.type == 'music':
                    try:
                        audio = EasyID3(picInfo.localFilePath)
                        taglist = sorted(audio.keys())
                        taglist.reverse()
                        tagsToShow = taglist
                        if tagsToShow:
                            trackInfo = '<span class="postInfo">ID3 info:</span><br/>'
                            for tag in tagsToShow:
                                #log.debug(tag)
                                #log.debug(audio[tag])
                                value = audio[tag]
                                if value and isinstance(value, list) and tag in id3FieldsNames.keys():
                                    value = ' '.join(value)
                                    trackInfo += u'<b>%s</b>: %s<br/>' % (filterText(id3FieldsNames[tag]), filterText(value))
                            picInfo.additionalInfo = trackInfo
                            #if not postMessageInfo:
                            #    postMessageInfo = trackInfo
                            #else:
                            #    postMessageInfo += '<br/>%s' % trackInfo
                    except:
                        log.debug("Can't load ID3 from %s" % picInfo.localFilePath)

                #TODO: move tags here
                picInfo.spoiler = None
                if options.enableSpoilers:
                    picInfo.spoiler = bool(request.POST.get('spoiler_%d' % fileId, None))

                if len(picInfos) < options.allowedAdditionalFiles + 1:
                    picInfos.append(picInfo)

        if not postMessage and not picInfos and not postMessageInfo:
            return errorHandler(_("At least message or file should be specified"))

        postSage = bool(request.POST.get('sage', False))
        if postid:
            if not picInfos and not options.imagelessPost:
                return errorHandler(_("Replies without image are not allowed"))
        else:
            if not picInfos and not options.imagelessThread:
                return errorHandler(_("Threads without image are not allowed"))

        postParams = empty()
        postParams.message = postMessage
        postParams.messageShort = postMessageShort
        postParams.messageRaw = postMessageRaw
        postParams.messageInfo = postMessageInfo
        postParams.title = postTitle
        #postParams.spoiler = postSpoiler
        postParams.uidNumber = self.userInst.uidNumber
        postParams.removemd5 = postRemovemd5
        postParams.postSage = postSage
        #postParams.replyTo = postid
        postParams.thread = thread
        postParams.tags = tags
        #postParams.existentPics = [existentPic, existentPic]
        postParams.picInfos = picInfos
        postParams.bumplimit = options.bumplimit

        #if animPath and postParams.picInfos:
        #    assert len(postParams.picInfos) == 1
        #    for picInfo in postParams.picInfos:
        #        picInfo.animPath = animPath
        #        picInfo.additionalInfo = None

        postParams.ip = None
        if self.userInst.Anonymous or g.OPT.saveAnyIP:
            postParams.ip = self.userIp

        post = Post.create(postParams)

        for picInfo in postParams.picInfos:
            if picInfo.fileHolder:
                picInfo.fileHolder.disableDeletion()

        for hook in postingHooks:
            hook.afterPostCallback(post, self.userInst, afterPostCallbackParams.get(hook.pluginId(), None))

        response.set_cookie('orphie-postingCompleted', 'yes')

        if ajaxRequest:
            return 'completed'
        else:
            return self.gotoDestination(post)
