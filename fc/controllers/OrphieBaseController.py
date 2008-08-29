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
    def render(self, page):
        tname = 'std'
        tpath = "%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        
        try:
            if self.userInst and not self.userInst.isBanned():
                tname = self.userInst.template()
                tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        except: #userInst not defined or user banned
            pass
        
        if page and os.path.isfile(os.path.join(templPath, tpath)):               
            return render('/' + tpath)
        else:
            return _("Template problem: " + page)
            
    def genUid(self, key):
        return hashlib.sha512(key + hashlib.sha512(hashSecret).hexdigest()).hexdigest()    
        
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
