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

try:
    import cPickle as pickle
except:
    import pickle

from Orphereus.lib.constantValues import *
import Orphereus.lib.helpers as h
from pylons import app_globals as g

class EAbstractFunctionCall(Exception):
    def __repr__(self):
        return "Call to abstract function"

def safeListUnpickle(val):
    try:
        return pickle.loads(str(val))
    except:
        return []

class AbstractUser(object):
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # These routines intended ONLY for options #
    # which user can change himself            #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    booleanValues = ('hideLongComments',
                          'useFrame',
                          'useAjax',
                          'mixOldThreads',
                          'expandImages',
                          'oekUseSelfy',
                          'oekUseAnim',
                          'oekUsePro',
                          'useTitleCollapse',
                          'hlOwnPosts',
                          'invertSortingMode',
                          'gotoCreatedPost'
                         )
    intValues = ('threadsPerPage',
                 'repliesPerThread',
                 'maxExpandWidth',
                 'maxExpandHeight',
                 'defaultGoto',
                 )
    stringValues = ('style',
                    'template',
                    'lang',
                    'cLang',
                    )
    pickleValues = ('homeExclude',
                    'hideThreads',
                    )
    restrictions = {'threadsPerPage' : lambda val: 0 < val < 30,
                    'repliesPerThread' : lambda val: 0 < val < 100,
                    'maxExpandWidth' : lambda val: 0 < val < 4096,
                    'maxExpandHeight' : lambda val: 0 < val < 4096,
                    'defaultGoto' : lambda val: val in destinations.keys(),

                    'style' : lambda val: val in g.OPT.styles,
                    'template' : lambda val: val in g.OPT.templates,
                    'lang' : lambda val: val in g.OPT.languages or val == "auto",
                    'cLang' : lambda val: val in g.OPT.languages or val == "auto",
                   }

    proxies = {'lang' : lambda val: h.makeLangValid(val),
               'cLang' : lambda val: h.makeLangValid(val),
               'homeExclude' : lambda val: pickle.dumps(val),
               'hideThreads' : lambda val: pickle.dumps(val),
              }

    preparators = {'homeExclude' : safeListUnpickle, #lambda val: pickle.loads(str(val)),
                   'hideThreads' : safeListUnpickle, #lambda val: pickle.loads(str(val)),
                  }
    simpleValues = booleanValues + intValues + stringValues + pickleValues

    def __getattr__(self, name):
        if name in self.simpleValues:
            val = self.simpleGetter(name)
            preparator = self.preparators.get(name, None)
            if preparator:
                val = preparator(val)
            return val
        else:
            return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if name in self.simpleValues:
            proxy = self.proxies.get(name, None)
            restriction = self.restrictions.get(name, None)
            if not restriction or restriction(value):
                if proxy:
                    value = proxy(value)
                self.simpleSetter(name, value)
        else:
            object.__setattr__(self, name, value)

    def isValid(self):
        raise EAbstractFunctionCall()

    def setUid(self, value = None):
        raise EAbstractFunctionCall()

    def secid(self):
        raise EAbstractFunctionCall()

    def authid(self):
        raise EAbstractFunctionCall()

    def postCreatedCallback(self, post):
        pass
    # bans
    def isBanned(self):
        raise EAbstractFunctionCall()

    def bantime(self):
        raise EAbstractFunctionCall()

    def banreason(self):
        raise EAbstractFunctionCall()

    #rights
    def readonly(self):
        raise EAbstractFunctionCall()

    def isAdmin(self):
        raise EAbstractFunctionCall()

    def canDeleteAllPosts(self):
        raise EAbstractFunctionCall()

    def canMakeInvite(self):
        raise EAbstractFunctionCall()

    def canChangeRights(self):
        raise EAbstractFunctionCall()

    def canChangeSettings(self):
        raise EAbstractFunctionCall()

    def canManageBoards(self):
        raise EAbstractFunctionCall()

    def canManageUsers(self):
        raise EAbstractFunctionCall()

    def canManageExtensions(self):
        raise EAbstractFunctionCall()

    def canManageMappings(self):
        raise EAbstractFunctionCall()

    def canRunMaintenance(self):
        raise EAbstractFunctionCall()

    def canViewLogs(self):
        raise EAbstractFunctionCall()
