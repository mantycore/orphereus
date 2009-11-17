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
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
import os
import cgi
import datetime
import time
import Image
import os
import shutil
import hashlib
import re
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider

from Orphereus.lib.OrphieMark.OrphieParser import OrphieParser
from Orphereus.lib.OrphieMark.tools import fixHtml

import logging
log = logging.getLogger(__name__)

class LogElement(object):
    printAll = False

    @staticmethod
    def setPrintAll(value = True):
        LogElement.printAll = value

    def __init__(self, type, message):
        self.timestamp = datetime.datetime.now()
        self.type = type
        self.message = message
        if LogElement.printAll:
            print self

    def __repr__(self):
        return "[%s] %s: %s" % (self.timestamp, self.type, self.message)

class MaintenanceWorker(object):
    obligatoryActions = ['banRotate', 'destroyTrackers', 'destroyInvites', 'cleanOekaki']
    optionalActions = ['integrityChecks', 'updateCaches', 'updateStats', 'banInactive',
                       'removeEmptyTags', 'reparseAll', 'sortUploads',
                       'findOrphanedPosts'
                      ]
    descriptions = {'banRotate' : N_('Remove old bans'),
                    'destroyTrackers' : N_('Destroy IP trackers (older than one day)'),
                    'destroyInvites' : N_('Destroy unused invites (older than one week)'),
                    'cleanOekaki' : N_('Destroy unused oekaki IDs (older than one day)'),

                    'integrityChecks' : N_('Integrity checks'),
                    'updateCaches' : N_('Update caches'),
                    'updateStats' : N_('Update statistics'),
                    'banInactive' : N_('Ban ALL users without posts'),
                    'removeEmptyTags' : N_('Remove empty tags'),
                    'reparseAll' : N_('Reparse posts which can be reparsed and fix incorrect XHTML if any'),
                    'sortUploads' : N_('Sort uploads'),
                    'findOrphanedPosts' : N_('Search for orphaned posts and group them into thread #0'),
                    }

    def banRotate(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Removing bans...'))
        currentTime = datetime.datetime.now()
        def usersSearch(users):
            for user in users:
                if user.options:
                    bantime = user.options.bantime
                    banDate = user.options.banDate
                    if banDate and bantime > 0 and banDate < currentTime - datetime.timedelta(days = min(10000, bantime)):
                        unbanMessage = (u"Automatic unban: user <b>#%d</b> (Reason was %s)") % (user.uidNumber, user.options.banreason)
                        mtnLog.append(LogElement('Info', unbanMessage))
                        toLog(LOG_EVENT_MTN_UNBAN, unbanMessage)
                        user.unban()
                else:
                    mtnLog.append(LogElement('Error', u'Integrity error: user %d has no options object' % user.uidNumber))
        batchProcess(User.query, usersSearch)
        mtnLog.append(LogElement('Task', 'Done'))

        mtnLog.append(LogElement('Task', 'Removing IP bans...'))
        def bansSearch(bans):
            for ban in bans:
                bantime = ban.period
                banDate = ban.date
                if bantime > 10000:
                    bantime = 10000
                if banDate and bantime > 0 and banDate < (currentTime - datetime.timedelta(days = bantime)):
                    ban.disable()
                    unbanMessage = (u"Automatic unban: IP <b>%s</b> (Reason was %s)") % (h.intToIp(ban.ip), ban.reason)
                    mtnLog.append(LogElement('Info', unbanMessage))
                    toLog(LOG_EVENT_MTN_UNBAN, unbanMessage)
        batchProcess(Ban.query.filter(Ban.enabled == True), bansSearch)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def cleanOekaki(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Clearing old oekaki entries...'))
        currentTime = datetime.datetime.now()
        def searchRoutine(oekakies):
            for oekaki in oekakies:
                #oekaki.time==-1 and not oekaki.path and
                if oekaki.timeStamp < currentTime - datetime.timedelta(days = 1):
                    mtnLog.append(LogElement('Info', "Deleted oekaki with <b>#%d</b>" % (oekaki.id)))
                    meta.Session.delete(oekaki)
        batchProcess(Oekaki.query, searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def destroyInvites(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Deleting old invites...'))
        currentTime = datetime.datetime.now()
        def searchRoutine(invites):
            for invite in invites:
                if invite.date < currentTime - datetime.timedelta(weeks = 1):
                    msg1 = u"Deleted invite <b>#%d</b>" % (invite.id)
                    msg2 = u" from date <b>%s</b> with id <font size='-2'>%s</font>" % (invite.date, invite.invite)
                    toLog(LOG_EVENT_MTN_DELINVITE, msg1)
                    mtnLog.append(LogElement('Info', msg1 + msg2))
                    meta.Session.delete(invite)
        batchProcess(Invite.query, searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def destroyTrackers(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Deleting old trackers...'))
        currentTime = datetime.datetime.now()
        def searchRoutine(trackers):
            for tracker in trackers:
                if tracker.lastAttempt < currentTime - datetime.timedelta(days = 1):
                    mtnLog.append(LogElement('Info', "Deleted ip tracker for <b>%s</b> with <b>%d</b> attempts" % (tracker.ip, tracker.attempts)))
                    if tracker.cid:
                        captcha = Captcha.query.filter(Captcha.id == tracker.cid).first()
                        if captcha:
                            meta.Session.delete(captcha)
                            mtnLog.append(LogElement('Info', "Deleted captcha <b>#%d</b>" % (captcha.id)))
                    meta.Session.delete(tracker)
        batchProcess(LoginTracker.query, searchRoutine)

        def captchaSearch(captchas):
            for ct in captchas:
                if ct.timestamp < currentTime - datetime.timedelta(days = 1):
                    mtnLog.append(LogElement('Info', "Deleted old captcha <b>#%d</b>" % (ct.id)))
                    meta.Session.delete(ct)
        batchProcess(Captcha.query, captchaSearch)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def integrityChecks(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Doing integrity checks...'))

        mtnLog.append(LogElement('Task', 'Checking for orphaned database entries...'))

        mtnLog.append(LogElement('Task', 'User options...'))
        def userOptsSearch(userOpts):
            for opt in userOpts:
                user = User.query.filter(User.uidNumber == opt.uidNumber).first()
                if not user:
                    msg = u'Orphaned userOptions %d for %s, removing' % (opt.optid, str(opt.uidNumber))
                    mtnLog.append(LogElement('Warning', msg))
                    toLog(LOG_EVENT_INTEGR, msg)
                    meta.Session.delete(opt)
        batchProcess(UserOptions.query, userOptsSearch)

        mtnLog.append(LogElement('Task', 'User filters...'))
        def userFiltersSearch(userFl):
            for fl in userFl:
                user = User.query.filter(User.uidNumber == fl.uidNumber).first()
                if not user:
                    msg = u'Orphaned userFilters %d for %s, removing' % (fl.id, str(fl.uidNumber))
                    mtnLog.append(LogElement('Warning', msg))
                    toLog(LOG_EVENT_INTEGR, msg)
                    meta.Session.delete(fl)
        batchProcess(UserFilters.query, userFiltersSearch)

        """
        mtnLog.append(LogElement('Task', 'Tag options...'))
        def tagOptsSearch(tagOpts):
            for opt in tagOpts:
                tag = Tag.query.filter(Tag.id == opt.tagId).first()
                if not tag:
                    msg = u'Orphaned tagOptions %d for %s, removing' % (opt.id, str(opt.tagId))
                    mtnLog.append(LogElement('Warning', msg))
                    toLog(LOG_EVENT_INTEGR, msg)
                    meta.Session.delete(opt)
        batchProcess(TagOptions.query, tagOptsSearch)
        """

        mtnLog.append(LogElement('Task', 'Pictures...'))
        def picturesSearch(pictures):
            for pic in pictures:
                if pic.pictureRefCount() < 1:
                    msg = u'Orphaned picture with id == %s, fileName == %s, removing' % (str(pic.id), pic.path)
                    mtnLog.append(LogElement('Warning', msg))
                    toLog(LOG_EVENT_INTEGR, msg)
                    meta.Session.delete(pic)
        batchProcess(Picture.query, picturesSearch)

        meta.Session.commit()
        mtnLog.append(LogElement('Task', 'Orpaned database entries check completed'))

        mtnLog.append(LogElement('Task', 'Checking for orphaned files...'))


        junkPath = os.path.join(g.OPT.uploadPath, 'junk')
        if not os.path.exists(junkPath):
            os.mkdir(junkPath)

        files = [] #os.listdir(g.OPT.uploadPath)
        for dir, subdirs, flist in os.walk(g.OPT.uploadPath):
            for file in flist:
                name = os.path.join(dir + '/' + file)
                if not ('junk' in name or '.svn' in dir or 'pch' in name):
                    files.append(name)

        ccJunkFiles = 0
        ccJunkThumbnails = 0
        for fn in sorted(files):
            fullname = os.path.basename(fn)
            name = fullname.split('.')[0]
            #log.debug(fn)
            if os.path.isfile(fn) and name and len(name) > 0:
                isThumb = (name[-1] == 's')

                if isThumb:
                    thumbIds = Picture.query.filter(Picture.thumpath.like('%%%s' % fullname)).all()
                    if not thumbIds:
                        msg = u'Orphaned thumbnail %s moved into junk directory' % fn
                        mtnLog.append(LogElement('Info', msg))
                        toLog(LOG_EVENT_INTEGR, msg)
                        shutil.move(fn, junkPath)
                        ccJunkThumbnails += 1
                else:
                    picIds = Picture.query.filter(Picture.path.like('%%%s' % fullname)).all()
                    if not picIds:
                        msg = u'Orphaned picture %s moved into junk directory' % fn
                        mtnLog.append(LogElement('Info', msg))
                        toLog(LOG_EVENT_INTEGR, msg)
                        shutil.move(fn, junkPath)
                        ccJunkFiles += 1

        if (ccJunkFiles > 0 or ccJunkThumbnails > 0):
            toLog(LOG_EVENT_INTEGR, "%d files and %d thumbnails moved into junk directory" % (ccJunkFiles, ccJunkThumbnails))

        mtnLog.append(LogElement('Task', 'Orpaned files check completed'))

        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def sortUploads(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Sorting uploads directory...'))

        def moveFile(fname):
            expanded = h.expandName(fname)
            if expanded != fname:
                source = os.path.join(g.OPT.uploadPath, fname)
                target = os.path.join(g.OPT.uploadPath, expanded)
                if not os.path.exists(source):
                    msg = 'Warning: %s not exists' % (source)
                    mtnLog.append(LogElement('Info', msg))
                    toLog(LOG_EVENT_INTEGR, msg)
                    return False
                targetDir = os.path.dirname(target)
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)
                shutil.move(source, target)
                return True
            return False

        movedCC = 0
        movedTCC = 0
        posts = Post.query.options(eagerload('attachments')).all()
        for post in posts:
            for fileAssoc in post.attachments:
                file = fileAssoc.attachedFile
                if file:
                    fname = file.path
                    if moveFile(fname):
                        file.path = h.expandName(fname)
                        movedCC += 1
                    tfname = file.thumpath
                    #log.debug(tfname)
                    if moveFile(tfname):
                        file.thumpath = h.expandName(tfname)
                        movedTCC += 1

        if movedCC or movedTCC:
            msg = '%d files and %d thumbnails moved' % (movedCC, movedTCC)
            mtnLog.append(LogElement('Info', msg))
            toLog(LOG_EVENT_INTEGR, msg)
        mtnLog.append(LogElement('Task', 'Done'))
        meta.Session.commit()
        return mtnLog

    def updateCaches(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Updating caches...'))
        def searchRoutine(posts):
            for post in posts:
                repliesCount = Post.query.filter(Post.parentid == post.id).count()
                if post.replyCount != repliesCount:
                    msg = 'Invalid RC: %d (actual: %d, cached: %d), updating' % (post.id, repliesCount, post.replyCount)
                    warnMsg = LogElement('Warning', msg)
                    mtnLog.append(warnMsg)
                    toLog(LOG_EVENT_INTEGR_RC, msg)
                    post.replyCount = repliesCount
        batchProcess(Post.query.filter(Post.parentid == None), searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def updateStats(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Updating statistics...'))
        def searchRoutine(tags):
            for tag in tags:
                condition = Post.tags.any(Tag.id == tag.id)
                threadCount = Post.query.filter(Post.parentid == None).filter(condition).count()
                #log.debug("%s:%s" % (tag.tag, threadCount))

                if tag.threadCount != threadCount:
                    msg = 'Invalid tag TC: %s (actual: %d, cached: %d), updating' % (tag.tag, threadCount, tag.threadCount)
                    warnMsg = LogElement('Warning', msg)
                    mtnLog.append(warnMsg)
                    toLog(LOG_EVENT_INTEGR_RC, msg)
                    tag.threadCount = threadCount

                replyCount = Post.query.filter(or_(condition, Post.parentPost.has(condition))).count()
                #log.debug("%s:%s" % (tag.tag, replyCount))

                if tag.replyCount != replyCount:
                    msg = 'Invalid tag RC: %s (actual: %d, cached: %d), updating' % (tag.tag, replyCount, tag.replyCount)
                    warnMsg = LogElement('Warning', msg)
                    mtnLog.append(warnMsg)
                    toLog(LOG_EVENT_INTEGR_RC, msg)
                    tag.replyCount = replyCount

        batchProcess(Tag.query, searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def banInactive(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Setting auto bans...'))
        def searchRoutine(users):
            for user in users:
                postsCount = Post.query.filter(Post.uidNumber == user.uidNumber).count()
                if user.options:
                    if postsCount == 0 and user.options.bantime == 0:
                        user.ban(10000, "[AUTOMATIC BAN] You haven't any posts. Please, contact administration to get you access back", -1)
                        mtnLog.append(LogElement('Info', "%d autobanned" % user.uidNumber))
                else:
                    mtnLog.append(LogElement('Warning', "User %d haven't options object" % user.uidNumber))
        batchProcess(User.query, searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def removeEmptyTags(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Removing empty tags...'))
        def searchRoutine(tags):
            for tag in tags:
                if tag.persistent:
                    threadCount = Post.query.filter(Post.parentid == None).filter(Post.tags.any(Tag.id == tag.id)).count()
                    if threadCount == 0 and not tag.service:
                        mtnLog.append(LogElement('Info', "Removed tag %s" % tag.tag))
                        meta.Session.delete(tag)
        batchProcess(Tag.query, searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    #parser callback
    def cbGetPostAndUser(self, id):
        return (Post.getPost(id), self.currentUserId)

    def reparseAll(self):
        mtnLog = []
        mtnLog.append(LogElement('Task', 'Reparsing...'))
        self.formatPostReference = OrphieBaseController.formatPostReference
        def reparseRoutine(posts):
            for post in posts:
                #log.debug("Reparsing %d..." % post.id)
                if post.messageRaw:
                    self.currentUserId = post.uidNumber
                    #parser = WakabaParser(g.OPT, post.parentPost and post.parentPost.id or - 1)
                    maxLinesInPost = int(g.OPT.maxLinesInPost)
                    cutSymbols = g.OPT.cutSymbols
                    #parsedMessage = parser.parseWakaba(post.messageRaw, self, lines = maxLinesInPost, maxLen = cutSymbols)
                    parser = OrphieParser(g, self)
                    parsedMessage = parser.parseMessage(post.messageRaw, post.parentPost and post.parentPost.id or - 1, maxLinesInPost, cutSymbols)
                    fullMessage = parsedMessage[0]
                    #if painterMark:
                    #    fullMessage += painterMark
                    mtnLog.append(LogElement('Info', "Reparsed post %d" % post.id))
                    post.message = fullMessage
                    post.messageShort = parsedMessage[1]
                else:
                    if post.message:
                        post.message = fixHtml(post.message)
                        mtnLog.append(LogElement('Info', "Fixed message for post %d" % post.id))
                    if post.messageShort:
                        mtnLog.append(LogElement('Info', "Fixed short message for post %d" % post.id))
                        post.messageShort = fixHtml(post.messageShort)
        batchProcess(Post.query.order_by(Post.id.asc()), reparseRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

    def findOrphanedPosts(self):
        def createOrphanedThread():
            orphanedThread = Post()
            orphanedThread.message = u'Orphereus maintenance subsystem'
            orphanedThread.title = u'Orphaned posts'
            orphanedThread.date = datetime.datetime(1970, 1, 1)
            orphanedThread.bumpDate = orphanedThread.date

            orphanedThread.messageInfo = u'Service thread'
            meta.Session.commit()
            orphanedThread.id = 0
            meta.Session.commit()
            return orphanedThread

        mtnLog = []
        mtnLog.append(LogElement('Task', 'Searching for orphaned posts...'))

        def searchRoutine(posts):
            for post in posts:
                parent = None
                if post.parentid != None:
                    parent = Post.getPost(post.parentid)
                orphaned = post.parentid != None and not parent
                treelike = post.parentid != None and parent and parent.parentid != None
                if orphaned or treelike:
                    orphanedThread = Post.getPost(0)
                    if not orphanedThread:
                        orphanedThread = createOrphanedThread()
                        mtnLog.append(LogElement('Info', 'Thread #0 created'))
                    post.parentid = 0
                    if orphaned:
                        mtnLog.append(LogElement('Info', 'Orphaned post #%d moved into thread #0' % post.id))
                    if treelike:
                        mtnLog.append(LogElement('Info', 'Post #%d was tree-like reply to reply and moved into thread #0' % post.id))

        batchProcess(Post.query.order_by(Post.id.asc()), searchRoutine)
        mtnLog.append(LogElement('Task', 'Done'))
        return mtnLog

from paste.script import command
from Orphereus.config.environment import load_environment
from paste.deploy import appconfig
from pylons import config

class MaintenanceCommand(command.Command):
    #max_args = 0
    min_args = 1

    usage = "development.ini %s %s | RunAllObligatory" % (MaintenanceWorker.obligatoryActions, MaintenanceWorker.optionalActions)
    summary = "Runs maintenance routines"
    group_name = "Orphereus"

    parser = command.Command.standard_parser(verbose = True)
    parser.add_option('--config',
                      action = 'store',
                      dest = 'config',
                      help = 'config name (e.g. "development.ini")')

    parser.add_option('--path',
                      action = 'store',
                      dest = 'path',
                      help = 'working dir (e.g. ".")')

    @staticmethod
    def setup_config(filename, relative_to):
        if not relative_to or not os.path.exists(relative_to):
            relative_to = "."
        print 'Loading config "%s" at path "%s"...' % (filename, relative_to)
        conf = appconfig('config:' + filename, relative_to = relative_to)
        load_environment(conf.global_conf, conf.local_conf, False)
        g._push_object(meta.globj) #zomg teh h4x

    def command(self):
        #devIni = self.args[0]
        self.setup_config(self.options.config, self.options.path)

        LogElement.setPrintAll(True)
        if 'RunAllObligatory' in self.args:
            actions = {}.fromkeys(MaintenanceWorker.obligatoryActions).keys()
        else:
            actions = self.args
        self.process(actions)

    @staticmethod
    def process(actions, printMessages = True):
        log = []
        if actions:
            worker = MaintenanceWorker()
            toLog(LOG_EVENT_MTN_BEGIN, u'Maintenance started')
            for action in actions:
                if action in MaintenanceWorker.obligatoryActions or action in MaintenanceWorker.optionalActions:
                    if printMessages:
                        print "Running %s..." % action
                    try:
                        log += getattr(worker, action)()
                    except Exception, e:
                        errorMsg = u"Exception occured in %s: %s" % (action, str(e))
                        if printMessages:
                            print errorMsg
                        toLog(LOG_EVENT_MTN_ERROR, errorMsg)
                    if printMessages:
                        print "Completed"
            toLog(LOG_EVENT_MTN_END, u'Maintenance ended')
        elif printMessages:
            print "No work to do"
        return log

class MaintenancePlugin(BasePlugin, AbstractPostingHook, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Maintenance'),
                 }
        BasePlugin.__init__(self, 'maintenance', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('hsMaintenance', '/holySynod/service/:actid', controller = 'Orphie_Maintenance', actid = '', action = 'mtnAction')
        #map.connect('hsMaintenance', '/holySynod/service/:actid/:secid', controller = 'Orphie_Maintenance', actid = '', secid = '', action = 'mtnAction')

    def beforePostCallback(self, controller, request, **kwargs):
        thread = kwargs.get("thread", None)
        if thread and thread.id == 0:
            return _("Posting into service thread #0 is prohibited")
        return None

    def entryPointsList(self):
        return [('maintenance', "MaintenanceCommand"), ]

    # Implementing AbstractMenuProvider
    def MenuItemIsVisible(self, id, baseController):
        user = baseController.userInst
        if id == 'id_hsMaintenance':
            return user.canRunMaintenance()
        return True

    def menuItems(self, menuId):
        #          id        link       name                weight   parent
        menu = None
        if menuId == "managementMenu":
            menu = (MenuItem('id_hsMaintenance', _("Maintenance"), h.url_for('hsMaintenance'), 300, False),
                    )
        return menu

class OrphieMaintenanceController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.requestForMenu("managementMenu")

    def mtnAction(self, actid): #, secid):
        #secTestPassed = False
        #if not secid:
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canRunMaintenance()) or self.userInst.isBanned():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')
        secTestPassed = True

        #TODO: legacy code. But MAY BE usable on weak hostings with small modifications (constant secid from config)
        """
        else:
            secidFilePath = os.path.join(g.OPT.appRoot, 'Orphereus/secid')
            try:
                secidFile = open(secidFilePath)
                secidFile.seek(0)
                secTestPassed = (secidFile.read() == secid)
                c.serviceOut = secTestPassed
                secidFile.close()
                os.remove(secidFilePath)
            except IOError, err:
                pass
        """

        if not secTestPassed:
            return redirect_to('boardBase')

        c.currentItemId = 'id_hsMaintenance'
        if not actid:
            c.obligatoryActions = MaintenanceWorker.obligatoryActions
            c.optionalActions = MaintenanceWorker.optionalActions
            c.descriptions = MaintenanceWorker.descriptions
            c.boardName = _('Index')
            return self.render('mtnIndex')
        else:
            c.boardName = 'Maintenance log'
            actions = []
            if actid in MaintenanceWorker.optionalActions or actid in MaintenanceWorker.obligatoryActions:
                actions = [actid]
            elif actid == 'all':
                actions = {}.fromkeys(MaintenanceWorker.obligatoryActions).keys()

            mtnLog = MaintenanceCommand.process(actions, False)
            c.mtnLog = mtnLog
            return self.render('mtnLog')
