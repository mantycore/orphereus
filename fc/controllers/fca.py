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
hashSecret = 'paranoia' # We will hash it by sha512, so no need to have it huge
class FcaController(BaseController):
    def __before__(self):
        self.userInst = FUser(session.get('uid_number',-1))
        if not self.userInst.isAuthorized():
            c.currentURL = '/holySynod/'
            return render('/wakaba.login.mako')
        self.initEnvironment()
        if not self.userInst.isAdmin():
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
    def manageBoards(self):
        c.boardName = 'Boards management'
        return render('/wakaba.manageBoards.mako')
    def editBoard(self,tag):
        c.boardName = 'Edit board'
        c.message = ''
        c.tag = meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag==tag).first()
        if not c.tag:
        	c.tag = Tag()
        	c.tag.options = TagOptions()
			c.tag.options.comment = ''
			c.tag.options.section_id = 0
			c.tag.options.persistent = False
			c.tag.options.imageless_thread = True
			c.tag.options.imageless_post = True
			c.tag.options.images = True
			c.tag.options.max_fsize = 3145728
			c.tag.options.min_size = 0
			c.tag.options.thumb_size = 250
        if request.POST.get('tag',False):
        	newtag = request.POST.get('tag',False)
        	newtagre = re.compile(r"""([^,@~\+\-\&\s\/\\\(\)<>'"%\d][^,@~\+\-\&\s\/\\\(\)<>'"%]*)""").match(newtag)
        	if newtagre:
        		newtag = newtagre.groups()[0]
        		newtagRecord = meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag==newtag).first()
        		if not newtagRecord or newtagRecord.id == c.tag.id:
        			c.tag.tag = newtag
        			c.tag.options.comment = request.POST.get('comment','')
        			c.tag.options.section_id = request.POST.get('section_id',0)
        			c.tag.options.persistent = request.POST.get('persistent',False)
        			c.tag.options.imageless_thread = request.POST.get('imageless_thread',True)
        			c.tag.options.imageless_post = request.POST.get('imageless_post',True)
        			c.tag.options.images = request.POST.get('images',True)
        			c.tag.options.max_fsize = request.POST.get('max_fsize',3145728)
        			c.tag.options.min_size = request.POST.get('min_size',0)
        			c.tag.options.thumb_size = request.POST.get('thumb_size',250)
        			if not c.tag.id:
        				meta.Session.save(c.tag)
        			meta.Session.commit()
        		else:
        			c.message = _("Board %s already exists!") % newtag
        	else:
        		c.message = _("Board name should be non-empty and should contain only valid symbols")
        return render('/wakaba.editBoard.mako')
    def manageUsers(self):
        c.boardName = 'Users management'
        return render('/wakaba.manageUsers.mako')
    def manageQuestions(self):
        c.boardName = 'Questions management'
        return render('/wakaba.manageQuestions.mako')        
    def manageApplications(self):
        c.boardName = 'Applications management'
        return render('/wakaba.manageApplications.mako')        
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
