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
            if self.userInst:
                tname = self.userInst.template()
                tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        except: #userInst not defined
            pass
        
        if page and os.path.isfile(os.path.join(templPath, tpath)):               
            return render('/' + tpath)
        else:
            return _("Template problem")
