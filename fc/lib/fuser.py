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
import pickle
from fc.lib.constantValues import *
from fc.lib.miscUtils import *

import logging
log = logging.getLogger(__name__)

class FUser(object):
    def __init__(self, uidNumber = -1):
        self.__uidNumber = uidNumber
        self.__valid = False
        self.Anonymous = False

        if uidNumber>-1 or g.OPT.allowAnonymous:
            self.__user = None
            self.Anonymous = False
            if uidNumber>-1:
                self.__user = meta.Session.query(User).options(eagerload('options')).filter(User.uidNumber==uidNumber).first()

            if not self.__user and g.OPT.allowAnonymous:
                self.__user = empty()
                self.__user.options = None
                self.__user.uidNumber = -1
                self.__user.filters = ()
                self.Anonymous = True

            if self.__user:
                self.__valid = True

                if not self.__user.options:
                    if uidNumber>-1:
                        self.__user.options = UserOptions()
                    else:
                        self.__user.options = empty()
                    self.__user.options.threadsPerPage = 10
                    self.__user.options.repliesPerThread = 10
                    self.__user.options.style = config['pylons.app_globals'].OPT.styles[0]
                    self.__user.options.template = 'wakaba'
                    self.__user.options.bantime = 0
                    self.__user.options.canDeleteAllPosts = False
                    self.__user.options.canMakeInvite = False
                    self.__user.options.canChangeRights = False
                    self.__user.options.isAdmin = False
                    self.__user.options.hideLongComments = True
                    self.__user.options.useAjax = True
                    self.__user.options.mixOldThreads = True
                    self.__user.options.defaultGoto = 0
                    self.__user.options.homeExclude = pickle.dumps([])
                    self.__user.options.hideThreads = pickle.dumps([])
                    meta.Session.commit()

                if not self.__user.options.hideThreads:
                    self.__user.options.hideThreads = pickle.dumps([])
                    meta.Session.commit()
                if not self.__user.options.homeExclude:
                    self.__user.options.homeExclude = pickle.dumps([])
                    meta.Session.commit()

                self.__valid = True

    def isValid(self):
        return self.__valid

    def isAuthorized(self):
        return self.isValid() and (session.get('uidNumber', -1) == self.__uidNumber)

    def canPost(self):
        return g.OPT.allowPosting and ((self.Anonymous and g.OPT.allowAnonymousPosting) or not self.Anonymous)

    def uidNumber(self):
        return self.__user.getUidNumber()

    def uid(self, value=None):
        return self.__user.getUid(value)
#========================
    def defaultGoto(self, value = None):
        return self.__user.defaultGoto(destinations, value)

    def filters(self):
        return self.__user.getFilters()

    def isBanned(self):
        return self.__user.isBanned()

    def isAdmin(self):
        return self.__user.isAdmin()

    def secid(self):
        return self.__user.secid()

    def hideLongComments(self, value=None):
        return self.__user.hideLongComments(value)

    def mixOldThreads(self, value=None):
        return self.__user.mixOldThreads(value)

    def useAjax(self, value=None):
        return self.__user.useAjax(value)

    def homeExclude(self, value = None):
        return self.__user.homeExclude(value)

    def hideThreads(self, value = None):
        return self.__user.hideThreads(value)

    def threadsPerPage(self, value = False):
        return self.__user.threadsPerPage(value)

    def repliesPerThread(self, value = False):
        return self.__user.repliesPerThread(value)

    def style(self, value = False):
        return self.__user.style(value)

    def template(self, value = False):
        return self.__user.template(value)

    def canDeleteAllPosts(self):
        return self.__user.canDeleteAllPosts()

    def canMakeInvite(self):
        return self.__user.canMakeInvite()

    def canChangeRights(self):
        return self.__user.canChangeRights()

    def bantime(self):
        return self.__user.bantime()

    def banreason(self):
        return self.__user.banreason()

    def optionsDump(self):
        return self.__user.optionsDump()

    def canChangeSettings(self):
        return self.__user.canChangeSettings()

    def canManageBoards(self):
        return self.__user.canManageBoards()

    def canManageUsers(self):
        return self.__user.canManageBoards()

    def canManageExtensions(self):
        return self.__user.canManageExtensions()

    def canManageMappings(self):
        return self.__user.canManageMappings()

    def canRunMaintenance(self):
        return self.__user.canRunMaintenance()

    def expandImages(self):
        return self.__user.expandImages()

    def maxExpandWidth(self):
        return self.__user.maxExpandWidth()

    def maxExpandHeight(self):
        return self.__user.maxExpandHeight()
