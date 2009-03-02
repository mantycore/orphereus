from fc.lib.base import *
from fc.model import *
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
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController
from wakabaparse import WakabaParser

import logging
log = logging.getLogger(__name__)

#TODO: totally rewrite this controller

class Empty:
    pass

class FcmController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)

    def createLogEntry(self, type, message):
        act = Empty()
        act.type = type
        act.message = message
        return act

    def clearOekaki(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Clearing old oekaki entries...'))
        oekakies = meta.Session.query(Oekaki).all()
        currentTime = datetime.datetime.now()
        for oekaki in oekakies:
            #oekaki.time==-1 and not oekaki.path and
            if oekaki.timeStamp < currentTime - datetime.timedelta(days=1):
                mtnLog.append(self.createLogEntry('Info', "Deleted oekaki with <b>#%d</b>" % (oekaki.id)))
                meta.Session.delete(oekaki)
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def destroyInvites(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Deleting old invites...'))
        currentTime = datetime.datetime.now()
        invites = meta.Session.query(Invite).all()
        for invite in invites:
            if invite.date < currentTime - datetime.timedelta(weeks=1):
                msg1 = "Deleted invite <b>#%d</b>" % (invite.id)
                msg2 = " from date <b>%s</b> with id <font size='-2'>%s</font>" % (invite.date, invite.invite)
                toLog(LOG_EVENT_MTN_DELINVITE, msg1)
                mtnLog.append(self.createLogEntry('Info', msg1+msg2))
                meta.Session.delete(invite)
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def destroyTrackers(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Deleting old trackers...'))
        currentTime = datetime.datetime.now()
        trackers = meta.Session.query(LoginTracker).all()
        for tracker in trackers:
            if tracker.lastAttempt < currentTime - datetime.timedelta(days=1):
                mtnLog.append(self.createLogEntry('Info', "Deleted ip tracker for <b>%s</b> with <b>%d</b> attempts" % (tracker.ip, tracker.attempts)))
                if tracker.cid:
                    captcha = meta.Session.query(Captcha).filter(Captcha.id==tracker.cid).first()
                    if captcha:
                        meta.Session.delete(captcha)
                        mtnLog.append(self.createLogEntry('Info', "Deleted captcha <b>#%d</b>" % (captcha.id)))

                meta.Session.delete(tracker)

        captchas = meta.Session.query(Captcha).all()
        for ct in captchas:
            tracker = meta.Session.query(LoginTracker).filter(LoginTracker.cid == ct.id).first()
            if not tracker:
                mtnLog.append(self.createLogEntry('Info', "Deleted captcha <b>#%d</b>" % (ct.id)))
                meta.Session.delete(ct)
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def banRotate(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Removing bans...'))
        currentTime = datetime.datetime.now()
        users = meta.Session.query(User).all()
        for user in users:
            bantime = user.options.bantime
            banDate = user.options.banDate
            if bantime > 10000:
                bantime = 10000
            if banDate and bantime>0 and banDate < currentTime - datetime.timedelta(days=bantime):
                unbanMessage = ("Automatic unban: user <b>#%d</b> (Reason was %s)") % (user.uidNumber, user.options.banreason)
                mtnLog.append(self.createLogEntry('Info', unbanMessage))
                toLog(LOG_EVENT_MTN_UNBAN, unbanMessage)
                user.options.bantime = 0
                user.options.banreason = u''
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def integrityChecks(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Doing integrity checks...'))

        mtnLog.append(self.createLogEntry('Task', 'Cheking for orphaned database entries...'))

        mtnLog.append(self.createLogEntry('Task', 'User options...'))
        userOpts = meta.Session.query(UserOptions).all()
        for opt in userOpts:
            user = meta.Session.query(User).filter(User.uidNumber==opt.uidNumber).first()
            if not user:
                msg = 'Orphaned userOptions %d for %s, removing' % (opt.optid, str(opt.uidNumber))
                mtnLog.append(self.createLogEntry('Warning', msg))
                toLog(LOG_EVENT_INTEGR, msg)
                meta.Session.delete(opt)

        mtnLog.append(self.createLogEntry('Task', 'User filters...'))
        userFl = meta.Session.query(UserFilters).all()
        for fl in userFl:
            user = meta.Session.query(User).filter(User.uidNumber==opt.uidNumber).first()
            if not user:
                msg = 'Orphaned userFilters %d for %s, removing' % (fl.id, str(fl.uidNumber))
                mtnLog.append(self.createLogEntry('Warning', msg))
                toLog(LOG_EVENT_INTEGR, msg)
                meta.Session.delete(fl)

        mtnLog.append(self.createLogEntry('Task', 'Tag options...'))
        tagOpts = meta.Session.query(TagOptions).all()
        for opt in tagOpts:
            tag = meta.Session.query(Tag).filter(Tag.id==opt.tagId).first()
            if not tag:
                msg = 'Orphaned tagOptions %d for %s, removing' % (opt.id, str(opt.tagId))
                mtnLog.append(self.createLogEntry('Warning', msg))
                toLog(LOG_EVENT_INTEGR, msg)
                meta.Session.delete(opt)

        mtnLog.append(self.createLogEntry('Task', 'Pictures...'))
        pictures = meta.Session.query(Picture).all()
        for pic in pictures:
            post = Post.query.filter(Post.picid == pic.id).first()
            if not post:
                msg = 'Orphaned picture with id == %s, fileName == %s, removing' % (str(pic.id), pic.path)
                mtnLog.append(self.createLogEntry('Warning', msg))
                toLog(LOG_EVENT_INTEGR, msg)
                meta.Session.delete(pic)

        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Orpaned database entries check completed'))

        mtnLog.append(self.createLogEntry('Task', 'Cheking for orphaned files...'))


        junkPath= os.path.join(g.OPT.uploadPath, 'junk')
        if not os.path.exists(junkPath):
            os.mkdir(junkPath)

        files = [] #os.listdir(g.OPT.uploadPath)
        for dir, subdirs, flist in os.walk(g.OPT.uploadPath):
            for file in flist:
                name = os.path.join(dir+'/'+file)
                if not '.svn' in dir and not 'junk' in name:
                    files.append(name)

        ccJunkFiles = 0
        ccJunkThumbnails = 0
        for fn in sorted(files):
            fullname = os.path.basename(fn)
            name = fullname.split('.')[0]
            log.debug(fn)
            if os.path.isfile(fn) and name and len(name) > 0:
                isThumb = (name[-1] == 's')

                if isThumb:
                    thumbIds = meta.Session.query(Picture).filter(Picture.thumpath.like('%%%s' % fullname)).all()
                    if not thumbIds:
                        msg = 'Orphaned thumbnail %s moved into junk directory' % fn
                        mtnLog.append(self.createLogEntry('Info', msg))
                        toLog(LOG_EVENT_INTEGR, msg)
                        shutil.move(fn, junkPath)
                        ccJunkThumbnails += 1
                else:
                    picIds = meta.Session.query(Picture).filter(Picture.path.like('%%%s' % fullname)).all()
                    if not picIds:
                        msg = 'Orphaned picture %s moved into junk directory' % fn
                        mtnLog.append(self.createLogEntry('Info', msg))
                        toLog(LOG_EVENT_INTEGR, msg)
                        shutil.move(fn, junkPath)
                        ccJunkFiles += 1

        if (ccJunkFiles > 0 or ccJunkThumbnails > 0):
            toLog(LOG_EVENT_INTEGR, "%d files and %d thumbnails moved into junk directory" % (ccJunkFiles, ccJunkThumbnails))

        mtnLog.append(self.createLogEntry('Task', 'Orpaned files check completed'))

        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def sortUploads(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Sorting uploads directory...'))

        def moveFile(fname):
            expanded = h.expandName(fname)
            if expanded != fname:
                source = os.path.join(g.OPT.uploadPath, fname)
                target = os.path.join(g.OPT.uploadPath, expanded)
                if not os.path.exists(source):
                    msg = 'Warning: %s not exists' % (source)
                    mtnLog.append(self.createLogEntry('Info', msg))
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
        posts = Post.query.options(eagerload('file')).all()
        for post in posts:
            if post.file:
                fname = post.file.path
                if moveFile(fname):
                    post.file.path = h.expandName(fname)
                    movedCC += 1
                tfname = post.file.thumpath
                #log.debug(tfname)
                if moveFile(tfname):
                    post.file.thumpath = h.expandName(tfname)
                    movedTCC += 1

        if movedCC or movedTCC:
            msg = '%d files and %d thumbnails moved' % (movedCC, movedTCC)
            mtnLog.append(self.createLogEntry('Info', msg))
            toLog(LOG_EVENT_INTEGR, msg)
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        meta.Session.commit()
        return mtnLog

    def updateCaches(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Updating caches...'))
        posts = Post.query.filter(Post.parentid == None).all()
        for post in posts:
            repliesCount = Post.query.filter(Post.parentid == post.id).count()
            if post.replyCount != repliesCount:
                msg = 'Invalid RC: %d (actual: %d, cached: %d), updating' % (post.id, repliesCount, post.replyCount)
                warnMsg = self.createLogEntry('Warning', msg)
                mtnLog.append(warnMsg)
                toLog(LOG_EVENT_INTEGR_RC, msg)
                post.replyCount = repliesCount
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def updateStats(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Updating statistics...'))
        tags = meta.Session.query(Tag).all()
        for tag in tags:
            condition = Post.tags.any(Tag.id == tag.id)
            threadCount = Post.query.filter(Post.parentid == None).filter(condition).count()
            #log.debug("%s:%s" % (tag.tag, threadCount))

            if tag.threadCount != threadCount:
                msg = 'Invalid tag TC: %s (actual: %d, cached: %d), updating' % (tag.tag, threadCount, tag.threadCount)
                warnMsg = self.createLogEntry('Warning', msg)
                mtnLog.append(warnMsg)
                toLog(LOG_EVENT_INTEGR_RC, msg)
                tag.threadCount = threadCount

            replyCount = Post.query.filter(or_(condition, Post.parentPost.has(condition))).count()
            #log.debug("%s:%s" % (tag.tag, replyCount))

            if tag.replyCount != replyCount:
                msg = 'Invalid tag RC: %s (actual: %d, cached: %d), updating' % (tag.tag, replyCount, tag.replyCount)
                warnMsg = self.createLogEntry('Warning', msg)
                mtnLog.append(warnMsg)
                toLog(LOG_EVENT_INTEGR_RC, msg)
                tag.replyCount = replyCount
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def banInactive(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Setting auto bans...'))
        currentTime = datetime.datetime.now()
        users = meta.Session.query(User).all()
        for user in users:
            postsCount = Post.query.filter(Post.uidNumber == user.uidNumber).count()
            if user.options:
                if postsCount == 0 and user.options.bantime == 0:
                    user.ban(10000, _("[AUTOMATIC BAN] You haven't any posts. Please, contact administration to get you access back"), -1)
                    mtnLog.append(self.createLogEntry('Info', "%d autobanned" % user.uidNumber))
            else:
                mtnLog.append(self.createLogEntry('Warning', "User %d haven't options object" % user.uidNumber))
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def removeEmptyTags(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Removing empty tags...'))
        tags = meta.Session.query(Tag).all()
        for tag in tags:
            log.debug(tag.tag)
            if not tag.options or not tag.options.persistent:
                threadCount = Post.query.filter(Post.parentid == None).filter(Post.tags.any(Tag.id == tag.id)).count()
                if threadCount == 0:
                    mtnLog.append(self.createLogEntry('Info', "Removed tag %s" % tag.tag))
                    meta.Session.delete(tag)

        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def reparse(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Reparsing...'))
        posts = Post.query.all()
        for post in posts:
            log.debug(post.id)
            if post.messageRaw:
               parser = WakabaParser(g.OPT.markupFile)
               maxLinesInPost = int(g.settingsMap['maxLinesInPost'].value)
               cutSymbols = int(g.settingsMap["cutSymbols"].value)
               parsedMessage = parser.parseWakaba(post.messageRaw, self, lines=maxLinesInPost,maxLen=cutSymbols)
               fullMessage = parsedMessage[0]
               #if painterMark:
               #    fullMessage += painterMark
               mtnLog.append(self.createLogEntry('Info', "Reparsed post %d" % post.id))
               post.message = fullMessage
               post.messageShort = parsedMessage[1]

        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog

    def mtnAction(self, actid, secid):
        secTestPassed = False
        if not secid:
            if not self.currentUserIsAuthorized():
                c.currentURL = u'/holySynod/'
                return redirect_to('/')
            self.initEnvironment()
            if not (self.userInst.isAdmin() and self.userInst.canRunMaintenance()):
                c.errorText = "No way! You aren't holy enough!"
                return redirect_to('/')
            c.userInst = self.userInst
            if not checkAdminIP():
                return redirect_to('/')
            secTestPassed = True
        else:
            secidFilePath = os.path.join(g.OPT.appPath, 'fc/secid')
            try:
                secidFile = open(secidFilePath)
                secidFile.seek(0)
                secTestPassed = (secidFile.read() == secid)
                c.serviceOut = secTestPassed
                secidFile.close()
                os.remove(secidFilePath)
            except IOError, err:
                pass

        if not secTestPassed:
            return redirect_to('/')

        if not actid:
            c.boardName = 'Index'
            return self.render('mtnIndex')
        else:
            toLog(LOG_EVENT_MTN_BEGIN, _('Maintenance started'))
            mtnLog = []
            c.boardName = 'Maintenance log'
            if actid == 'clearOekaki':
                mtnLog = self.clearOekaki()
            elif actid == 'destroyInvites':
                mtnLog = self.destroyInvites()
            elif actid == 'banRotate':
                mtnLog = self.banRotate()
            elif actid == 'integrityChecks':
                mtnLog = self.integrityChecks()
            elif actid == 'destroyTrackers':
                mtnLog = self.destroyTrackers()
            elif actid == 'updateCaches':
                mtnLog = self.updateCaches()
            elif actid == 'updateStats':
                mtnLog = self.updateStats()
            elif actid == 'banInactive':
                mtnLog = self.banInactive()
            elif actid == 'removeEmptyTags':
                mtnLog = self.removeEmptyTags()
            elif actid == 'reparse':
                mtnLog = self.reparse()
            elif actid == 'sortUploads':
                mtnLog = self.sortUploads()
            elif actid == 'all':
                try:
                    mtnLog = self.clearOekaki()
                except:
                    toLog(LOG_EVENT_MTN_ERROR, _('Critical error in clearOekaki()'))
                try:
                    mtnLog += self.destroyInvites()
                except:
                    toLog(LOG_EVENT_MTN_ERROR, _('Critical error in destroyInvites()'))
                try:
                    mtnLog += self.destroyTrackers()
                except:
                    toLog(LOG_EVENT_MTN_ERROR, _('Critical error in destroyTrackers()'))
                try:
                    mtnLog += self.integrityChecks()
                except:
                    toLog(LOG_EVENT_MTN_ERROR, _('Critical error in integrityChecks()'))
                try:
                    mtnLog += self.banRotate()
                except:
                    toLog(LOG_EVENT_MTN_ERROR, _('Critical error in banRotate()'))
                #try:
                #    mtnLog += self.updateCaches()
                #except:
                #    toLog(LOG_EVENT_MTN_ERROR, _('Critical error in updateCaches()'))

            #for entry in mtnLog:
            #    toLog(LOG_EVENT_MTN_ACT, entry.type + ': ' + entry.message)

            c.mtnLog = mtnLog
            toLog(LOG_EVENT_MTN_END, _('Maintenance ended'))
            return self.render('mtnLog')
