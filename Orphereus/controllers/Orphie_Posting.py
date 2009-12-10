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

import logging
import sqlalchemy
import os
import datetime
import time
import Image
import hashlib
import re
import base64

from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_, or_, not_

from mutagen.easyid3 import EasyID3
from urllib import quote_plus, unquote

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.OrphieMark.OrphieParser import OrphieParser
from Orphereus.lib.fileHolder import AngryFileHolder
from Orphereus.lib.processFile import processFile
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)

class OrphiePostingPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Posting (Obligatory)'),
                 }
        BasePlugin.__init__(self, 'base_posting', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        # Oekaki
        map.connect('oekakiDraw',
                    '/oekakiDraw/{url}/{sourceId}/{selfy}/{anim}/{tool}',
                    controller = 'Orphie_Posting',
                    action = 'oekakiDraw',
                    selfy = None,
                    anim = None,
                    tool = None,
                    sourceId = '0',
                    requirements = dict(sourceId = r'\d+'))

        # Threads
        map.connect('postReply', '/{post}',
                    controller = 'Orphie_Posting',
                    action = 'PostReply',
                    conditions = dict(method = ['POST']),
                    requirements = dict(post = r'\d+'))
        map.connect('delete', '/{board}/delete',
                    controller = 'Orphie_Posting',
                    action = 'DeletePost',
                    conditions = dict(method = ['POST']))
        map.connect('postThread', '/{board}',
                    controller = 'Orphie_Posting',
                    action = 'PostThread',
                    conditions = dict(method = ['POST']))

class OrphiePostingController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    #parser callback
    def cbGetPostAndUser(self, id):
        return (Post.getPost(id), self.userInst.uidNumber)

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
                return redirect_to(controller = 'Orphie_View', action = 'GetThread', post = post.parentid, board = None, anchor = anchor)
            else:
                return redirect_to(controller = 'Orphie_View', action = 'GetThread', post = post.id, board = None, anchor = anchor)
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
                    tag.comment = tagdef

            if not tags:
                return errorHandler(_("You should specify at least one board"))

            maxTagsCount = g.OPT.maxTagsCount
            if len(tags) > maxTagsCount:
                return errorHandler(_("Too many tags. Maximum allowed: %s") % (maxTagsCount))

            usualTagsCC = 0
            svcTagsCC = 0
            permaTagsCC = 0
            for tag in tags:
                if not tag.service:
                    usualTagsCC += 1
                else:
                    svcTagsCC += 1
                if tag.persistent:
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
