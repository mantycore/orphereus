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

log = logging.getLogger(__name__)

class Empty:
    pass

class FcmController(BaseController):
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
                mtnLog.append(self.createLogEntry('Info', "Deleted invite <b>#%d</b> from date <b>%s</b> with id <font size='-2'>%s</font>" % (invite.id, invite.date, invite.invite)))
                meta.Session.delete(invite)
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

    def mtnAction(self, actid, secid):
        secTestPassed = False    
        if not secid:
            self.userInst = FUser(session.get('uidNumber',-1))
            if not self.userInst.isAuthorized():
                c.currentURL = '/holySynod/'
                return redirect_to('/')
            initEnvironment()
            if not self.userInst.isAdmin():
                c.errorText = "No way! You aren't holy enough!"
                return redirect_to('/')
            c.userInst = self.userInst
            if not checkAdminIP():
                return redirect_to('/')
            secTestPassed = True
        else:
            secidFilePath = os.path.join(appPath, 'fc/secid')
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
            return render('/wakaba.mtnIndex.mako')        
        else:
            addLogEntry(LOG_EVENT_MTN_BEGIN, _('Maintenance runned'))
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
            elif actid == 'all':
                mtnLog = self.clearOekaki()
                mtnLog += self.destroyInvites()
                mtnLog += self.integrityChecks()
                mtnLog += self.banRotate()   
                
            c.mtnLog = mtnLog
            addLogEntry(LOG_EVENT_MTN_END, _('Maintenance ended'))
            return render('/wakaba.mtnLog.mako')