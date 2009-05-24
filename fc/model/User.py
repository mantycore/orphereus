################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #  
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #                                                                         #
################################################################################

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import eagerload

from fc.model import meta
from fc.model.UserOptions import UserOptions
from fc.model.LogEntry import LogEntry
from fc.model.UserFilters import UserFilters
from fc.lib.miscUtils import isNumber, toLog, filterText
from fc.lib.constantValues import *

import fc.lib.helpers as h

import datetime
import hashlib
import re
import pickle
from pylons.i18n import _, ungettext, N_

import logging
log = logging.getLogger(__name__)

t_users = sa.Table("user", meta.metadata,
    sa.Column("uidNumber",sa.types.Integer, primary_key=True),
    sa.Column("uid"      , sa.types.String(128), nullable=False)
    )

#TODO: universal setter/getter, FakeUser-like
class User(object):
    def __init__(self, uid):
        self.uid = uid
        self.options = UserOptions()
        UserOptions.initDefaultOptions(self.options, meta.globj.OPT)

    @staticmethod
    def create(uid):
        user = User(uid)
        meta.Session.add(user)
        meta.Session.commit()
        return user

    # user ID
    @staticmethod
    def getUser(uidNumber):
        ret = User.query.options(eagerload('options')).filter(User.uidNumber==uidNumber).first()

        if ret:
            if meta.globj: #TODO: legacy code
                if ret and not ret.options:
                    ret.options = UserOptions()
                    UserOptions.initDefaultOptions(ret.options, meta.globj.OPT)
                    meta.Session.commit()

                if not ret.options.hideThreads:
                    ret.options.hideThreads = pickle.dumps([])
                    meta.Session.commit()
                if not ret.options.homeExclude:
                    ret.options.homeExclude = pickle.dumps([])
                    meta.Session.commit()

            ret.Anonymous = False
        return ret

    @staticmethod
    def getByUid(uid):
        ret = User.query.filter(User.uid==uid).first()
        if ret:
            ret.Anonymous = False
        return ret

    @staticmethod
    def genUid(key):
        return hashlib.sha512(key + hashlib.sha512(meta.globj.OPT.hashSecret).hexdigest()).hexdigest()

    def isValid(self):
        return True

    def setUid(self, value=None):
        if value != None and not User.query.options(eagerload('options')).filter(User.uid==value).first():
            self.uid = value
            meta.Session.commit()
        return self.uid

    def secid(self):
        return (2*self.uidNumber + 6) * (self.uidNumber + 5) * (self.uidNumber - 1)

    def authid(self):
        return (self.uidNumber + 10) * (2*self.uidNumber + 1) * (self.uidNumber + 1)
        #(2*x+3)*(x+10)*(x-1)=

    def ban(self, bantime, banreason, who = -1):
        if len(banreason)<=1 :
            return N_('You should specify ban reason')
        if not (isNumber(bantime) and int(bantime) > 0):
            return N_('You should specify ban time in days')
        bantime = int(bantime)
        if bantime > 10000:
            bantime = 10000
        self.options.bantime = bantime
        self.options.banreason = banreason
        self.options.banDate = datetime.datetime.now()
        meta.Session.commit()
        LogEntry.create(who, LOG_EVENT_USER_BAN, N_('Banned user %d for %s days for reason "%s"') % (self.uidNumber, bantime, banreason))
        return N_('User was banned')

    def passwd(self, key, key2, changeAnyway = False, currentKey = False):
        newuid = User.genUid(key)
        olduid = self.uid

        if key == key2 and newuid != olduid and len(key) >= meta.globj.OPT.minPassLength:
            if not (changeAnyway or User.genUid(currentKey) == olduid):
                return N_("You have entered incorrect current security code!")

            anotherUser = User.getByUid(newuid)
            if not anotherUser:
                self.setUid(newuid)
                return True
            else:
                if not changeAnyway:
                    userMsg  = N_("Your have entered already existing Security Code. Both accounts was banned. Contact administrator immediately please.")
                    self.ban(7777, userMsg, -1)
                    anotherUser.ban(7777, N_("Your Security Code was used during profile update by another user. Contact administrator immediately please."), -1)
                    return userMsg
                else:
                    return N_("You have entered already existing Security Code.")
        return False

    # Board customization
    def addFilter(self, filter):
        userFilter = UserFilters(self.uidNumber, filterText(filter))
        self.filters.append(userFilter)
        meta.Session.add(userFilter)
        meta.Session.commit()
        return userFilter

    def deleteFilter(self, fid):
        userFilter = UserFilters.query.get(fid)
        if not userFilter or userFilter.uidNumber != self.uidNumber:
            return False
        meta.Session.delete(userFilter)
        meta.Session.commit()
        return True

    def changeFilter(self, fid, filter):
        userFilter = UserFilters.query.get(fid)
        if not userFilter or userFilter.uidNumber != self.uidNumber:
            return False
        userFilter.filter = filter
        meta.Session.commit()
        return True

    def hideLongComments(self, value=None):
        if value != None:
            self.options.hideLongComments = value
        return self.options.hideLongComments

    def useFrame(self, value=None):
        if value != None:
            self.options.useFrame = value
        return self.options.useFrame

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

    def threadsPerPage(self, value = None):
        if value != None and isNumber(value) or value == 0:
            self.options.threadsPerPage = value
        return self.options.threadsPerPage

    def repliesPerThread(self, value = None):
        if value != None and isNumber(value) or value == 0:
            self.options.repliesPerThread = value
        return self.options.repliesPerThread

    def style(self, value = None):
        if value:
            self.options.style = value
        return self.options.style

    def lang(self, value = None):
        if value:
            self.options.lang = h.makeLangValid(value)
        return self.options.lang

    def cLang(self, value = None):
        if value:
            self.options.cLang = h.makeLangValid(value)
        return self.options.cLang

    def template(self, value = None):
        if value:
            self.options.template = value
        return self.options.template

    def defaultGoto(self, value = None):
        if value != None and isNumber(value) or value == 0:
            if (value < 0 or value >= len(destinations)):
                value = 0
            self.options.defaultGoto = value
        return self.options.defaultGoto

    def expandImages(self, value = None):
        if value != None:
            self.options.expandImages = value
        return self.options.expandImages

    def oekUseSelfy(self, value = None):
        if value != None:
            self.options.oekUseSelfy = value
        return self.options.oekUseSelfy

    def oekUseAnim(self, value = None):
        if value != None:
            self.options.oekUseAnim = value
        return self.options.oekUseAnim

    def oekUsePro(self, value = None):
        if value != None:
            self.options.oekUsePro = value
        return self.options.oekUsePro

    def maxExpandWidth(self, value = None):
        if value != None and isNumber(value) or value == 0:
            self.options.maxExpandWidth = value
        return self.options.maxExpandWidth

    def maxExpandHeight(self, value = None):
        if value != None and isNumber(value) or value == 0:
            self.options.maxExpandHeight = value
        return self.options.maxExpandHeight

    def useTitleCollapse(self, value = None):
        if value != None:
            self.options.useTitleCollapse = value
        return self.options.useTitleCollapse

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

    def canChangeSettings(self):
        return self.options.canChangeSettings

    def canManageBoards(self):
        return self.options.canManageBoards

    def canManageUsers(self):
        return self.options.canManageUsers or self.options.canChangeRights

    def canManageExtensions(self):
        return self.options.canManageExtensions

    def canManageMappings(self):
        return self.options.canManageMappings

    def canRunMaintenance(self):
        return self.options.canRunMaintenance
