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
            
    def index(self):
        c.boardName = 'Index'
        return render('/wakaba.mtnIndex.mako')

    def clearOekaki(self):
        c.boardName = 'Clearing old oekaki entries...'
        c.boardName = 'Removing orphaned oekaki...'
        oekakies = meta.Session.query(Oekaki).all()
        c.mtnLog = []
        for oekaki in oekakies:
            if oekaki.time==-1 and not oekaki.path and oekaki.id<len(oekakies)-30:
                act = Empty()
                act.type="Info"
                act.message="Deleted oekaki with <b>#%d</b>" % (oekaki.id)
                c.mtnLog.append(act)
                meta.Session.delete(oekaki)
        meta.Session.commit()
        return render('/wakaba.mtnLog.mako')        

    def destroyInvites(self):
        c.boardName = 'Destroying all invites...'
        invites = meta.Session.query(Invite).all()
        c.mtnLog = []
        for invite in invites:
            act = Empty()
            act.type="Info"
            act.message="Deleted invite <b>#%d</b> from date <b>%s</b> with id <font size='-2'>%s</font>" % (invite.id, invite.date, invite.invite)
            c.mtnLog.append(act)
            meta.Session.delete(invite)
        meta.Session.commit()
        return render('/wakaba.mtnLog.mako')

    def integrityChecks(self):
        c.boardName = 'Doing integrity checks.... NOT IMPLEMENTED.'
        return render('/wakaba.mtnLog.mako')        
      