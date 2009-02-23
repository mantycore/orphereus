import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import eagerload

from fc.model import meta
import datetime
import hashlib
import re
import pickle
from pylons import config

import logging
log = logging.getLogger(__name__)

from fc.model import meta
from fc.model.UserOptions import UserOptions
from fc.lib.miscUtils import isNumber
from fc.lib.constantValues import destinations

t_users = sa.Table("users", meta.metadata,
    sa.Column("uidNumber",sa.types.Integer, primary_key=True),
    sa.Column("uid"      , sa.types.String(128), nullable=False)
    )

#TODO: rewrite User
class User(object):
    # user ID
    @staticmethod
    def getUser(uidNumber, globalOptHolder = False):
        ret = User.query.options(eagerload('options')).filter(User.uidNumber==uidNumber).first()
        if globalOptHolder:
            if not ret.options:
                ret.options = UserOptions()
                UserOptions.initDefaultOptions(ret.options, globalOptHolder)
                meta.Session.commit()

            if not ret.options.hideThreads:
                ret.options.hideThreads = pickle.dumps([])
                meta.Session.commit()
            if not ret.options.homeExclude:
                ret.options.homeExclude = pickle.dumps([])
                meta.Session.commit()

        if ret:
            ret.Anonymous = False
        return ret

    @staticmethod
    def genUid(key):
        return hashlib.sha512(key + hashlib.sha512(config['pylons.app_globals'].OPT.hashSecret).hexdigest()).hexdigest()

    def isValid(self):
        return True

    def setUid(self, value=None):
        if value != None and not User.query.options(eagerload('options')).filter(User.uid==value).first():
            self.uid = value
        return self.uid

    def secid(self):
        return (2*self.uidNumber + 6) * (self.uidNumber + 5) * (self.uidNumber - 1)
        #(2*x+3)*(x+10)*(x-1)=

    # Board customization
    def hideLongComments(self, value=None):
        if value != None:
            self.options.hideLongComments = value
        return self.options.hideLongComments

    def mixOldThreads(self, value=None):
        if value != None:
            self.options.mixOldThreads = value
        return self.options.mixOldThreads

    def useAjax(self, value=None):
        if value != None:
            self.options.useAjax = value
        return self.options.useAjax

    def homeExclude(self, value = None):
        if value != None:
            self.options.homeExclude = pickle.dumps(value)
        return pickle.loads(self.options.homeExclude)

    def hideThreads(self, value = None):
        if value != None:
            self.options.hideThreads = pickle.dumps(value)
        return pickle.loads(self.options.hideThreads)

    def threadsPerPage(self, value = False):
        if value:
            self.options.threadsPerPage = value
        return self.options.threadsPerPage

    def repliesPerThread(self, value = False):
        if value:
            self.options.repliesPerThread = value
        return self.options.repliesPerThread

    def style(self, value = False):
        if value:
            self.options.style = value
        return self.options.style

    def template(self, value = False):
        if value:
            self.options.template = value
        return self.options.template

    def defaultGoto(self, value = None):
        if value != None and isNumber(value) or value == 0:
            if (value < 0 or value >= len(destinations)):
                value = 0
            self.options.defaultGoto = value
        return self.options.defaultGoto

    def expandImages(self):
        return True

    def maxExpandWidth(self):
        return 1024

    def maxExpandHeight(self):
        return 768

    def optionsDump(self):
        return UserOptions.optionsDump(self.options)

    # access
    def isBanned(self):
        return self.options.bantime > 0

    def bantime(self):
        return self.options.bantime

    def banreason(self):
        return self.options.banreason

    # admin rights
    @staticmethod
    def getAdmins():
        return User.query.options(eagerload('options')).filter(User.options.has(UserOptions.isAdmin==True)).all()

    def isAdmin(self):
        return self.options.isAdmin

    def canDeleteAllPosts(self):
        return self.options.canDeleteAllPosts

    def canMakeInvite(self):
        return self.options.canMakeInvite

    def canChangeRights(self):
        return self.options.canChangeRights

    #TODO: XXX: temporary code
    def canChangeSettings(self):
        return self.options.isAdmin

    def canManageBoards(self):
        return self.options.isAdmin

    def canManageUsers(self):
        return self.options.isAdmin

    def canManageExtensions(self):
        return self.options.isAdmin

    def canManageMappings(self):
        return self.options.isAdmin

    def canRunMaintenance(self):
        return self.options.isAdmin
