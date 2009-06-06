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

import sqlalchemy as sa
from sqlalchemy import orm

from Orphereus.model import meta
import datetime
import re
import pickle

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta

t_userOptions = sa.Table("userOptions", meta.metadata,
    sa.Column("optid"    , sa.types.Integer, primary_key = True),
    sa.Column("uidNumber", sa.types.Integer, sa.ForeignKey('user.uidNumber')),
    sa.Column("threadsPerPage", sa.types.Integer, nullable = False),
    sa.Column("repliesPerThread", sa.types.Integer, nullable = False),
    sa.Column("style"    , sa.types.String(32), nullable = False),
    sa.Column("template" , sa.types.String(32), nullable = False),
    sa.Column("homeExclude", sa.types.String(256), nullable = False),
    sa.Column("hideThreads", sa.types.Text, nullable = True),
    sa.Column("bantime"  , sa.types.Integer, nullable = False),
    sa.Column("banreason", sa.types.UnicodeText(256), nullable = True),
    sa.Column("banDate", sa.types.DateTime, nullable = True),
    sa.Column("useFrame", sa.types.Boolean, nullable = True),
    sa.Column("hideLongComments", sa.types.Boolean, nullable = True),
    sa.Column("useAjax", sa.types.Boolean, nullable = True),
    sa.Column("expandImages", sa.types.Boolean, nullable = True, server_default = '1'),
    sa.Column("maxExpandWidth", sa.types.Integer, nullable = True, server_default = '1024'),
    sa.Column("maxExpandHeight", sa.types.Integer, nullable = True, server_default = '768'),
    sa.Column("mixOldThreads", sa.types.Boolean, nullable = True),
    sa.Column("useTitleCollapse", sa.types.Boolean, nullable = True),
    sa.Column("hlOwnPosts", sa.types.Boolean, nullable = True, server_default = '0'),
    sa.Column("invertSortingMode", sa.types.Boolean, nullable = True, server_default = '0'),
    sa.Column("defaultGoto", sa.types.Integer, nullable = True),
    sa.Column("oekUseSelfy", sa.types.Boolean, nullable = True, server_default = '0'),
    sa.Column("oekUseAnim", sa.types.Boolean, nullable = True, server_default = '0'),
    sa.Column("oekUsePro", sa.types.Boolean, nullable = True, server_default = '0'),
    sa.Column("isAdmin"  , sa.types.Boolean, nullable = True),
    sa.Column("canDeleteAllPosts", sa.types.Boolean, nullable = True),
    sa.Column("canMakeInvite", sa.types.Boolean, nullable = True),
    sa.Column("canChangeRights", sa.types.Boolean, nullable = True),
    sa.Column("canChangeSettings", sa.types.Boolean, nullable = True),
    sa.Column("canManageBoards", sa.types.Boolean, nullable = True),
    sa.Column("canManageUsers", sa.types.Boolean, nullable = True),
    sa.Column("canManageExtensions", sa.types.Boolean, nullable = True),
    sa.Column("canManageMappings", sa.types.Boolean, nullable = True),
    sa.Column("canRunMaintenance", sa.types.Boolean, nullable = True),
    sa.Column("lang", sa.types.String(2), nullable = False),
    sa.Column("cLang", sa.types.String(2), nullable = False),
    )

class UserOptions(object):
    @staticmethod
    def optionsDump(optionsObject):
        optionsNames = dir(optionsObject)
        ret = {}
        retest = re.compile("^(<.*(at (0x){0,1}[0-9a-fA-F]+)+.*>)|(__.*__)$")
        for name in optionsNames:
            attr = str(getattr(optionsObject, name))
            if not (retest.match(name) or retest.match(attr)):
                ret[name] = attr
        return ret

    @staticmethod
    def initDefaultOptions(optionsObject, globalOptHolder):
        optionsObject.isAdmin = False
        optionsObject.canDeleteAllPosts = False
        optionsObject.canMakeInvite = False
        optionsObject.canChangeRights = False
        optionsObject.canChangeSettings = False
        optionsObject.canManageBoards = False
        optionsObject.canManageUsers = False
        optionsObject.canManageExtensions = False
        optionsObject.canManageMappings = False
        optionsObject.canRunMaintenance = False
        optionsObject.bantime = 0
        #
        optionsObject.style = globalOptHolder.styles[0]
        optionsObject.template = globalOptHolder.templates[0]
        optionsObject.lang = ''
        optionsObject.cLang = ''
        optionsObject.threadsPerPage = 10
        optionsObject.repliesPerThread = 10
        optionsObject.maxExpandWidth = 1024
        optionsObject.maxExpandHeight = 768
        optionsObject.defaultGoto = 0
        optionsObject.homeExclude = pickle.dumps([])
        optionsObject.hideThreads = pickle.dumps([])
        optionsObject.hideLongComments = True
        optionsObject.useFrame = True
        optionsObject.useAjax = True
        optionsObject.mixOldThreads = True
        optionsObject.expandImages = True
        optionsObject.oekUseSelfy = False
        optionsObject.oekUseAnim = False
        optionsObject.oekUsePro = False
        optionsObject.useTitleCollapse = False
        optionsObject.hlOwnPosts = False
        optionsObject.invertSortingMode = False


