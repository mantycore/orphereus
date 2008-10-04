#coding: utf8
import logging
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from fc.lib.settings import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class Empty:
    pass

class FcmController(OrphieBaseController):
    def __before__(self):
        pass
            
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
                addLogEntry(LOG_EVENT_MTN_DELINVITE, msg1)
                mtnLog.append(self.createLogEntry('Info', msg1+msg2))
                meta.Session.delete(invite)
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog;
        
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
                    meta.Session.delete(captcha)
                    mtnLog.append(self.createLogEntry('Info', "Deleted captcha <b>#%d</b>" % (captcha.id)))                
                    
                meta.Session.delete(tracker)
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog;        
        
    def banRotate(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Removing bans...'))
        currentTime = datetime.datetime.now()                
        users = meta.Session.query(User).all()
        for user in users:
            bantime = user.options.bantime
            banDate = user.options.banDate
            if banDate and bantime>0 and banDate < currentTime - datetime.timedelta(days=bantime):
                unbanMessage = ("Automatic unban: user <b>#%d</b> (Reason was %s)") % (user.uidNumber, user.options.banreason)
                mtnLog.append(self.createLogEntry('Info', unbanMessage))
                addLogEntry(LOG_EVENT_MTN_UNBAN, unbanMessage)
                user.options.bantime = 0
                user.options.banreason = ''
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog;        

    def integrityChecks(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Doing integrity checks.... NOT IMPLEMENTED.'))
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog;     
    
    def updateCaches(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Updating caches...'))        
        posts = meta.Session.query(Post).filter(Post.parentid == -1).all()
        for post in posts:
            repliesCount = meta.Session.query(Post).filter(Post.parentid == post.id).count()
            if post.replyCount != repliesCount:
                msg = 'Warning', _("Invalid RC: %d, updating") % post.id
                warnMsg = self.createLogEntry('Info', msg)
                mtnLog.append(warnMsg)
                addLogEntry(LOG_EVENT_INTEGR_RC, msg)                
                post.replyCount = repliesCount 
        meta.Session.commit()        
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog;     
    
    def banInactive(self):
        mtnLog = []
        mtnLog.append(self.createLogEntry('Task', 'Setting auto bans...'))
        currentTime = datetime.datetime.now()                
        users = meta.Session.query(User).all()
        for user in users:
            postsCount = meta.Session.query(Post).filter(Post.uidNumber == user.uidNumber).count()
            if postsCount == 0:
                self.banUser(user, 10000, ("[AUTOMATIC BAN] You haven't any posts. Please, contact johan.liebert@jabber.ru to get you access back"))
                mtnLog.append(self.createLogEntry('Info', "%d autobanned" % user.uidNumber))
                
        meta.Session.commit()
        mtnLog.append(self.createLogEntry('Task', 'Done'))
        return mtnLog;   
    
    def mtnAction(self, actid, secid):
        secTestPassed = False    
        if not secid:
            self.userInst = FUser(session.get('uidNumber',-1))
            if not self.userInst.isAuthorized():
                c.currentURL = '/holySynod/'
                return redirect_to('/')
            self.initEnvironment()
            if not self.userInst.isAdmin():
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
            addLogEntry(LOG_EVENT_MTN_BEGIN, _('Maintenance started'))
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
            elif actid == 'banInactive':
                mtnLog = self.banInactive()                                            
            elif actid == 'all':
                mtnLog = self.clearOekaki()
                mtnLog += self.destroyInvites()
                mtnLog += self.destroyTrackers()
                mtnLog += self.integrityChecks()
                mtnLog += self.banRotate()
                mtnLog += self.updateCaches()                   
            
            #for entry in mtnLog:
            #    addLogEntry(LOG_EVENT_MTN_ACT, entry.type + ': ' + entry.message)
                
            c.mtnLog = mtnLog
            addLogEntry(LOG_EVENT_MTN_END, _('Maintenance ended'))
            return self.render('mtnLog')