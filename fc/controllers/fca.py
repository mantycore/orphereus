import logging
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
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

log = logging.getLogger(__name__)

class FcaController(BaseController):
    def __before__(self):
        self.userInst = FUser(session.get('uid_number',-1))
        if not self.userInst.isAuthorized():
            c.currentURL = '/holySynod/'
            return render('/wakaba.login.mako')
        self.initEnvironment()
        if not self.isAdmin():
            c.errorText = "No way! You aren't holy enough!"
            return render('/wakaba.error.mako')
        c.userInst = self.userInst
        
    def initEnvironment(self):
        c.title = 'FailChan'
        boards = meta.Session.query(Tag).join('options').filter(TagOptions.persistent==True).order_by(TagOptions.section_id).all()
        c.boardlist = []
        section_id = 0
        section = []
        for b in boards:
            if not section_id:
                section_id = b.options.section_id
                section = []
            if section_id != b.options.section_id:
                c.boardlist.append(section)
                section_id = b.options.section_id
                section = []
            section.append(b.tag)
        if section:
            c.boardlist.append(section)
    def index(self):
        c.boardName = 'Index'
        return render('/wakaba.adminIndex.mako')
    def boardsManagement(self):
        c.boardName = 'Boards management'
        return render('/wakaba.boardsManage.mako')
    def makeInvite(self):         
        if not self.userInst.canMakeInvite():
            c.errorText = "No way! You aren't holy enough!"
            return render('/wakaba.error.mako') 
        c.boardName = 'Invites'
        invite = Invite()
        invite.date = datetime.datetime.now()
        invite.invite = hashlib.sha512(str(long(time.time() * 10**7)) + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
        meta.Session.save(invite)
        meta.Session.commit()
        c.message = "<a href='/register/%s'>INVITE</a>" % invite.invite
        return render('/wakaba.adminMessage.mako')
