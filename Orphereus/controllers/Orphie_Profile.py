# -*- coding: utf-8 -*-
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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

import logging
import sqlalchemy

from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_, or_, not_

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.interfaces.AbstractProfileExtension import AbstractProfileExtension
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)

class OrphieProfilePlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('User profile (Obligatory)'),
                 }
        BasePlugin.__init__(self, 'base_profile', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('userProfile', '/userProfile',
                    controller = 'Orphie_Profile',
                    action = 'showProfile')

class OrphieProfileController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def showProfile(self):
        if self.userInst.Anonymous and not g.OPT.allowAnonProfile:
            return self.error(_("Profile is not avaiable to Anonymous users."))

        self.forceNoncachedUser()
        Post.normalizeHiddenThreadsList(self.userInst)
        c.additionalProfileLinks = []
        linkGenerators = g.implementationsOf(AbstractProfileExtension)
        for generator in linkGenerators:
            linkslist = generator.additionalProfileLinks(self.userInst)
            if linkslist:
                c.additionalProfileLinks += linkslist

        c.templates = g.OPT.templates
        c.styles = g.OPT.cssFiles[self.userInst.template]
        c.languages = g.OPT.languages
        c.profileChanged = False
        c.boardName = _('Profile')
        if bool(request.POST.get('update', False)):
            lang = filterText(request.POST.get('lang', self.userInst.lang))
            c.reload = (h.makeLangValid(lang) != self.userInst.lang)

            oldUseFrame = self.userInst.useFrame
            for valueName in self.userInst.booleanValues:
                val = bool(request.POST.get(valueName, False))
                setattr(self.userInst, valueName, val)

            for valueName in self.userInst.intValues:
                val = request.POST.get(valueName, getattr(self.userInst, valueName))
                if isNumber(val):
                    setattr(self.userInst, valueName, int(val))

            for valueName in self.userInst.stringValues:
                val = filterText(request.POST.get(valueName, getattr(self.userInst, valueName)))
                setattr(self.userInst, valueName, val)

            if oldUseFrame != self.userInst.useFrame:
                c.proceedRedirect = True
                if self.userInst.useFrame:
                    c.frameTargetToRedir = h.url_for('userProfile')
                    c.currentURL = None
                else:
                    c.currentURL = h.url_for('userProfile')
            homeExcludeTags = Tag.stringToTagLists(request.POST.get('homeExclude', u''), False)[0]
            #log.debug(homeExcludeTags)
            homeExcludeList = []
            for t in homeExcludeTags:
                homeExcludeList.append(t.id)
            self.userInst.homeExclude = homeExcludeList

            if not c.userInst.Anonymous:
                c.profileMsg = _('Password was NOT changed.')
                key = request.POST.get('key', '').encode('utf-8')
                key2 = request.POST.get('key2', '').encode('utf-8')
                currentKey = request.POST.get('currentKey', '').encode('utf-8')
                passwdRet = self.userInst.passwd(key, key2, False, currentKey)
                if passwdRet == True:
                    c.profileMsg = _('Password was successfully changed.')
                elif passwdRet == False:
                    c.message = _('Incorrect security codes')
                else:
                    return self.error(passwdRet)
                meta.Session.commit()

            c.profileChanged = True
            c.profileMsg += _(' Profile was updated.')
            if c.reload:
                c.profileMsg += _(' Reload page for language changes to take effect.')

        homeExcludeTags = Tag.getAllByIds(self.userInst.homeExclude)
        homeExcludeList = []
        for t in homeExcludeTags:
            homeExcludeList.append(t.tag)
        c.homeExclude = ', '.join(homeExcludeList)
        c.hiddenThreads = Post.filter(Post.id.in_(self.userInst.hideThreads)).options(eagerload('tags')).all()
        for t in c.hiddenThreads:
            tl = []
            for tag in t.tags:
                tl.append(tag.tag)
            t.tagLine = ', '.join(tl)
        c.userInst = self.userInst
        return self.render('profile')
