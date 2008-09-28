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

class OrphieBaseController(BaseController):
    def __init__(self):
        settings = meta.Session.query(Setting).all()
        settingsMap = {}
        if settings:
            for s in settings:
                if s.name in settingsDef:
                    settingsMap[s.name] = s
        for s in settingsDef:
            if not s in settingsMap:
                settingsMap[s] = Setting()
                settingsMap[s].name = s
                settingsMap[s].value = settingsDef[s]
                meta.Session.save(settingsMap[s])
                meta.Session.commit()
        g.settingsMap = settingsMap
        
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
        response.set_cookie('fc', request.cookies['fc'], domain='.'+g.OPT.baseDomain)
               
    def shrink(html, in_tags = False):
      eol = re.compile('[\r\n]')
      spaces_between_tags = re.compile('>\s+<')
      spaces_in_tags = re.compile('\s+')
      html = eol.sub(' ', html)
      html = spaces_between_tags.sub('> <', html)
      if in_tags:
        html = spaces_in_tags.sub(' ', html)
      return html
                    
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
            return self.shrink(render('/'+tpath, **options))
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
                addLogEntry(LOG_EVENT_USER_BAN,_('Banned user %s for %s days for reason "%s"') % (user.uidNumber, bantime, banreason))
                meta.Session.commit()
                return _('User was banned')
            else:
                return _('You should specify ban time in days')
        else:
            return _('You should specify ban reason')  
