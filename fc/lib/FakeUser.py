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

import pickle
import random

from fc.lib.base import *
from fc.lib.miscUtils import *
from fc.model import UserOptions

#it's not really needed to implement all User interface.

class FakeUser(object):
    def __init__(self):
        self.__valid = False
        self.Anonymous = False
        self.uidNumber = -1
        
        if g.OPT.allowAnonymous:
            self.__valid = True
            self.Anonymous = True
            self.uid = "Anonymous"
            self.filters = ()

            self.__user = empty()
            self.__user.uidNumber = -1
            self.__user.filters = ()

            self.__user.options = empty()
            UserOptions.initDefaultOptions(self.__user.options, g.OPT)

    def isValid(self):
        return self.__valid

    def setUid(self, value=None):
        return self.__user.uid

    def isBanned(self):
        return False

    def secid(self):
        return 0

    def authid(self):
        return random.randint(1000, 10000)

    def sessValue(self, name, value, default):
        if value != None:
            session[name] = value
            session.save()
        return session.get(name, default)

    def sessPickleValue(self, name, value, default):
        if value != None:
            session[name] = pickle.dumps(value)
            session.save()
        return  pickle.loads(session.get(name, default))

    #customizable options
    def defaultGoto(self, value = None):
        return self.sessValue('defaultGoto', value, self.__user.options.defaultGoto)

    def hideLongComments(self, value=None):
        return self.sessValue('hideLongComments', value, self.__user.options.hideLongComments)

    def useFrame(self, value=None):
        return self.sessValue('useFrame', value, self.__user.options.useFrame)

    def mixOldThreads(self, value=None):
        return self.sessValue('mixOldThreads', value, self.__user.options.mixOldThreads)

    def useAjax(self, value=None):
        return self.sessValue('useAjax', value, self.__user.options.useAjax)

    def oekUseSelfy(self, value = None):
        return self.sessValue('oekUseSelfy', value, self.__user.options.oekUseSelfy)

    def oekUseAnim(self, value = None):
        return self.sessValue('oekUseAnim', value, self.__user.options.oekUseAnim)

    def oekUsePro(self, value = None):
        return self.sessValue('oekUsePro', value, self.__user.options.oekUsePro)

    def threadsPerPage(self, value = None):
        return self.sessValue('threadsPerPage', value, self.__user.options.threadsPerPage)

    def repliesPerThread(self, value = None):
        return self.sessValue('repliesPerThread', value, self.__user.options.repliesPerThread)

    def style(self, value = None):
        return self.sessValue('style', value, self.__user.options.style)

    def template(self, value = None):
        return self.sessValue('template', value, self.__user.options.template)

    def expandImages(self, value = None):
        return self.sessValue('expandImages', value, self.__user.options.expandImages)

    def maxExpandWidth(self, value = None):
        return self.sessValue('maxExpandWidth', value, self.__user.options.maxExpandWidth)

    def maxExpandHeight(self, value = None):
        return self.sessValue('maxExpandHeight', value, self.__user.options.maxExpandHeight)

    def useTitleCollapse(self, value = None):
        return self.sessValue('useTitleCollapse',  value, self.__user.options.useTitleCollapse)

    def homeExclude(self, value = None):
        return self.sessPickleValue('homeExclude',  value, self.__user.options.homeExclude)

    def hideThreads(self, value = None):
        return self.sessPickleValue('hideThreads',  value, self.__user.options.hideThreads)

    # disable any dangerous action
    def isAdmin(self):
        return False

    def canDeleteAllPosts(self):
        return False

    def bantime(self):
        return 0

    def banreason(self):
        return u''

    def optionsDump(self):
        return UserOptions.optionsDump(self.options)

