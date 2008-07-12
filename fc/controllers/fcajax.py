import logging

from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
import sqlalchemy
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
from wakabaparse import WakabaParser
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from fc.lib.settings import *

log = logging.getLogger(__name__)

class FcajaxController(BaseController):
    def __before__(self):
        self.userInst = FUser(session.get('uidNumber',-1))
        c.userInst = self.userInst
        if not self.userInst.isAuthorized():
            abort(403)
    def getPost(self,post):
        postInst = meta.Session.query(Post).get(post)
        if postInst:
            if postInst.parentid == -1:
                parent = postInst
            else:
                parent = meta.Session.query(Post).get(postInst.parentid)
            settingsMap = getSettingsMap()
            forbiddenTags = getTagsListFromString(settingsMap['adminOnlyTags'].value)       
            for t in parent.tags:
                if t.id in forbiddenTags:
                    abort(403)
            return postInst.message
        else:
            abort(404)
