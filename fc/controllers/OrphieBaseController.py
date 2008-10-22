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
import string
import re
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *

log = logging.getLogger(__name__)

class OrphieBaseController(BaseController):
    def __before__(self):
        self.userInst = FUser(session.get('uidNumber', -1))        
        #log.debug(session.get('uidNumber', -1))
        if g.OPT.checkUAs and self.userInst.isValid():
            for ua in g.OPT.badUAs:
                if filterText(request.headers.get('User-Agent', '?')).startswith(ua):
                    self.banUser(meta.Session.query(User).filter(User.uidNumber == self.userInst.uidNumber()).first(), 2, _("[AUTOMATIC BAN] Security alert type 1: %s") %  hashlib.md5(ua).hexdigest())
                    break
        
    def initEnvironment(self):
        c.title = g.settingsMap['title'].value   
        boards = meta.Session.query(Tag).join('options').filter(TagOptions.persistent==True).order_by(TagOptions.sectionId).all()
        c.boardlist = []
        sectionId = 0
        section = []
        for b in boards:
            if not sectionId:
                sectionId = b.options.sectionId
                section = []
            if sectionId != b.options.sectionId:
                c.boardlist.append(section)
                sectionId = b.options.sectionId
                section = []
            bc = empty()
            bc.tag = b.tag
            bc.comment = b.options.comment
            section.append(bc) #b.tag)
        if section:
            c.boardlist.append(section)
        response.set_cookie('fc', request.cookies.get('fc',''), domain='.'+g.OPT.baseDomain)
         
    def render(self, page, **options):
        #log.debug(options)
        #return
        tname = 'std'
        tpath = "%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        
        try:
            if self.userInst and not self.userInst.isBanned():
                tname = self.userInst.template()
                tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        except: #userInst not defined or user banned
            pass
        
        if page and os.path.isfile(os.path.join(g.OPT.templPath, tpath)):               
            return render('/'+tpath, **options)
        else:
            return _("Template problem: " + page)
            
    def showStatic(self, page):
        c.page = page
        c.boardName = page
        return self.render('static.%s' % page) #render('/%s.static.mako' % self.userInst.template())
        
    def genUid(self, key):
        return hashlib.sha512(key + hashlib.sha512(g.OPT.hashSecret).hexdigest()).hexdigest()    

    def genInviteId(self):
        return hashlib.sha512(str(long(time.time() * 10**7)) + hashlib.sha512(g.OPT.hashSecret).hexdigest()).hexdigest()  
        
    def banUser(self, user, bantime, banreason):
        if len(banreason)>1:
            if isNumber(bantime) and int(bantime) > 0:
                bantime = int(bantime)
                user.options.bantime = bantime
                user.options.banreason = banreason
                user.options.banDate = datetime.datetime.now() 
                addLogEntry(LOG_EVENT_USER_BAN, _('Banned user %s for %s days for reason "%s"') % (user.uidNumber, bantime, banreason))
                meta.Session.commit()
                return _('User was banned')
            else:
                return _('You should specify ban time in days')
        else:
            return _('You should specify ban reason')  
