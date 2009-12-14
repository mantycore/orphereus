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

import random

from Orphereus.lib.base import *
from Orphereus.lib.miscUtils import *
from Orphereus.model import UserOptions
from Orphereus.lib.interfaces.AbstractUser import AbstractUser

#it's not really needed to implement all User interface.

class FakeUser(AbstractUser):
    #def __new__(typ, *args, **kwargs):
    #    obj = AbstractUser.__new__(typ, *args, **kwargs)
    #    obj.simpleSetter = FakeUser.sessValue
    #    obj.simpleGetter = FakeUser.sessGetValue
    #    return obj

    def __init__(self):
        self.__valid = False
        self.Anonymous = False
        self.uidNumber = -1

        self.__user = empty()
        self.__user.uidNumber = -1
        self.__user.filters = ()

        self.__user.options = empty()
        if g.OPT.allowAnonymous:
            self.__valid = True
            self.Anonymous = True
            self.uid = "Anonymous"
            self.filters = ()

            UserOptions.initDefaultOptions(self.__user.options, g.OPT)
            #self.__user.options.readonly = not g.OPT.allowAnonymousPosting

    def simpleGetter(self, name):
        return session.get(name, getattr(self.__user.options, name))

    def simpleSetter(self, name, value):
        if value != None:
            session[name] = value
            session.save()
        #return session.get(name, default)

    def optionsDump(self):
        return UserOptions.optionsDump(self.__user.options)

    def isValid(self):
        return self.__valid

    def setUid(self, value = None):
        return self.__user.uid

    # bans
    def bantime(self):
        return 0

    def banreason(self):
        return u''

    def isBanned(self):
        return False

    # auth stubs
    def secid(self):
        return 0

    def authid(self):
        return random.randint(1000, 10000)

    # disable any dangerous action
    def readonly(self):
        return not g.OPT.allowAnonymousPosting

    def isAdmin(self):
        return False

    def canDeleteAllPosts(self):
        return False
