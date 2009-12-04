# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Hedger                                                   #
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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

import datetime

from pylons.i18n import N_
from webhelpers.html.tags import link_to
from string import *
from beaker.cache import CacheManager

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.miscUtils import *
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.interfaces.AbstractProfileExtension import AbstractProfileExtension
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class UserInviteData(object):
    def __init__(self, uidNumber):
        self.userId = uidNumber
        self.invitesCount = 0

    def increment(self, count = 1):
        self.lastIncrement = datetime.datetime.now()
        self.invitesCount += count
        meta.Session.commit()
        toLog(LOG_EVENT_INVITE + 1, _("Invite given to user %d") % (self.userId,))

    @staticmethod
    def get(userInst):
        inviteData = UserInviteData.query.filter(UserInviteData.userId == userInst.uidNumber).first()
        if not inviteData:
            inviteData = UserInviteData(userInst.uidNumber)
            meta.Session.add(inviteData)
            meta.Session.commit()
        return inviteData

    """
    @staticmethod
    def countFor(userInst):
        if userInst.Anonymous:
            return 0
        inviteData = UserInviteData.get(userInst)
        return inviteData.invitesCount
    """

    @staticmethod
    def generateInvite(userInst, reason):
        if userInst.Anonymous:
            return None
        inviteData = UserInviteData.get(userInst)
        if inviteData.invitesCount > 0:
            inviteData.invitesCount -= 1
            invite = Invite.create(meta.globj.OPT.hashSecret, userInst.uidNumber, reason)
            meta.Session.commit()
            toLog(LOG_EVENT_INVITE, _("User %d created invite %d for the following reason: %s") % (userInst.uidNumber, invite.id, reason))
            return invite
        return None

class InvitesPlugin(BasePlugin, AbstractProfileExtension, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('Userspace invite generator'),
                  'deps' : ('adminpanel',)
                 }
        BasePlugin.__init__(self, 'invites', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('userInvitesManager', '/userProfile/invites/:act', controller = 'userinvites', action = 'manageInvites', act = 'show')
        map.connect('userInvitesGive', '/holySynod/giveInvite/:post', controller = 'userinvites', action = 'giveInvite', requirements = dict(post = '\d+'))

    def initORM(self, orm, engine, dialectProps, propDict):
        namespace = self.namespace()
        t_userinvites = sa.Table("userinvite", meta.metadata,
            sa.Column('userId'  , sa.types.Integer, sa.ForeignKey('user.uidNumber'), primary_key = True),
            sa.Column('invitesCount'  , sa.types.Integer, nullable = False),
            sa.Column("lastIncrement" , sa.types.DateTime, nullable = True),
            )

        #orm.mapper
        meta.mapper(namespace.UserInviteData, t_userinvites, properties = {'user' : orm.relation(User), })

    def updateGlobals(self, globj):
        intValues = [('invites',
                               ('minimalPostsCount', 'minimalRecentPostsCount',
                                'minimalAge', 'recentPostsPercentage',
                                'inviteIssuingInterval'
                               )
                              ),
                            ]
        boolValues = [('invites',
                               ('enableDirectInvitesGeneration',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(boolValues, CFG_BOOL)

    def additionalProfileLinks(self, userInst):
        links = []
        if not userInst.Anonymous:
            inviteData = self.incrementInvitesIfNeeded(userInst)
            links = (('userInvitesManager', {}, _('Invites (%d)') % inviteData.invitesCount),)
            return links

    def postPanelCallback(self, thread, post, userInst):
        result = ''
        if g.OPT.enableDirectInvitesGeneration and c.userInst.isAdmin() and c.userInst.canMakeInvite():
            result += link_to(_("[Give invite]"), h.url_for('userInvitesGive', post = post.id))
        return result

    def threadPanelCallback(self, thread, userInst):
        return self.postPanelCallback(thread, thread, userInst)

    def incrementInvitesIfNeeded(self, userInst):
        inviteData = self.namespace().UserInviteData.get(userInst)
        if self.checkCond(userInst):
            inviteData.increment()
        return inviteData

    def __getUserAge(self, userInst):
        ns = self.namespace()
        oldestPost = ns.Post.query.filter(ns.Post.uidNumber == userInst.uidNumber).order_by(ns.Post.id.asc()).first()
        if not oldestPost:
            return 0
        age = datetime.datetime.now() - oldestPost.date
        return age.days

    def __getAllPostsCount(self, userInst):
        ns = self.namespace()
        return ns.Post.query.filter(ns.Post.uidNumber == userInst.uidNumber).count()

    def __getRecentPostsCount(self, userInst):
        ns = self.namespace()
        timeback = datetime.datetime.now() - datetime.timedelta(days = 7)
        return ns.Post.query.filter(and_(ns.Post.uidNumber == userInst.uidNumber, ns.Post.date > timeback)).count()

    def __checkLastGivenInvite(self, userInst):
        ns = self.namespace()
        inviteData = self.namespace().UserInviteData.get(userInst)
        return (not inviteData.lastIncrement) or (datetime.datetime.now() - inviteData.lastIncrement).days > g.OPT.inviteIssuingInterval

    def checkCond(self, userInst):
        """
        print self.__getUserAge(userInst)
        print self.__getAllPostsCount(userInst)
        print self.__getRecentPostsCount(userInst)
        print self.__checkLastGivenInvite(userInst)
        """
        obligatoryCondition = not(userInst.Anonymous) and \
                (self.__getUserAge(userInst) >= g.OPT.minimalAge) and \
                (self.__getAllPostsCount(userInst) >= minimalPostsCount) and \
                (self.__checkLastGivenInvite(userInst))

        if obligatoryCondition:
            recentPostsCount = self.__getRecentPostsCount(userInst)
            cm = CacheManager(type = 'memory')
            cch = cm.get_cache('home_stats')
            cacheTime = getattr(g.OPT, 'statsCacheTime', 30)
            vts = cch.get_value(key = "vitalSigns", createfunc = Post.vitalSigns, expiretime = cacheTime)

            return (recentPostsCount >= g.OPT.minimalRecentPostsCount) and \
                   (100.0 * recentPostsCount) / vts.lastWeekMessages >= g.OPT.recentPostsPercentage
        return None

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import OrphieBaseController

class UserinvitesController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def manageInvites(self, act):
        if self.userInst.Anonymous:
            return self.error(_("Inivte creation allowed only for registered users"))
        c.boardName = _('My invites')

        if act == 'create':
            reason = filterText(request.params.get('invitereason', ''))
            invite = UserInviteData.generateInvite(self.userInst, reason)
            if not invite:
                return self.error(_("You can't create invites now"))
            else:
                c.message = _("Invite #%d successfully created") % invite.id

        inviteData = g.pluginsDict['invites'].incrementInvitesIfNeeded(self.userInst)
        c.invites = Invite.query.filter(Invite.issuer == self.userInst.uidNumber).order_by(Invite.date.desc()).all()
        c.invitesCount = inviteData.invitesCount #UserInviteData.countFor(self.userInst)
        return self.render('userInvites')

    def giveInvite(self, post):
        if not self.userInst.isAdmin() or self.userInst.isBanned() or not self.userInst.canMakeInvite():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')

        if not g.OPT.enableDirectInvitesGeneration:
            return self.error(_("This action disabled in config"))

        if not checkAdminIP():
            return redirect_to('boardBase')

        postInst = Post.getPost(int(post))
        if not postInst:
            return self.error(_("Post doesn't exists"))

        uid = postInst.uidNumber
        if not (uid > 0):
             return self.error(_("Can't give invite to anonymous user"))

        user = User.getUser(uid)
        if user.options.isAdmin and user.options.canMakeInvite:
            return self.error(_("Giving invites to superuser is meaningless"))

        inviteData = UserInviteData.get(user)
        inviteData.increment()

        return redirect_to('hsInvite')
