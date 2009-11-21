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
from sqlalchemy.sql import and_, or_, not_

from Orphereus.model import meta
from Orphereus.model.Picture import Picture
import datetime

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta

__CONST_MAX_EXTENSION_LENGTH = 16
__CONST_MAX_EXTENSION_TYPE_LENGTH = 16
__CONST_MAX_EXTENSION_PATH_LENGTH = 255

def t_extension_init(dialectProps):
    return sa.Table("extension", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key = True),
    sa.Column("path"     , sa.types.String(__CONST_MAX_EXTENSION_PATH_LENGTH), nullable = False),
    sa.Column("thwidth"  , sa.types.Integer, nullable = False),
    sa.Column("thheight" , sa.types.Integer, nullable = False),
    sa.Column("ext"      , sa.types.String(__CONST_MAX_EXTENSION_LENGTH), nullable = False, unique = True, index = True),
    sa.Column("type"     , sa.types.String(__CONST_MAX_EXTENSION_TYPE_LENGTH), nullable = False),
    sa.Column("enabled"  , sa.types.Boolean, server_default = '1'),
    sa.Column("newWindow", sa.types.Boolean, server_default = '1'),
    )

class Extension(object):
    def __init__(self, name, enabled, newWindow, type, path, thwidth, thheight):
        self.ext = name
        self.setData(enabled, newWindow, type, path, thwidth, thheight)

    def setData(self, enabled, newWindow, type, path, thwidth, thheight):
        self.path = path
        self.enabled = enabled
        self.newWindow = newWindow
        self.type = type
        self.path = path
        self.thwidth = thwidth
        self.thheight = thheight
        meta.Session.commit()

    def count(self):
        return Picture.query.filter(Picture.extension.has(Extension.id == self.id)).count()

    def delete(self):
        if self.count() == 0:
            meta.Session.delete(self)
            meta.Session.commit()
            return True
        else:
            return False

    @staticmethod
    def getList(enabledOnly):
        filter = Extension.query.order_by(Extension.type)
        if enabledOnly:
            filter = filter.filter(Extension.enabled == True)
        return filter.all()

    @staticmethod
    def getExtension(ext):
        return Extension.query.filter(Extension.ext == ext).first()

    @staticmethod
    def create(name, enabled, newWindow, type, path, thwidth, thheight):
        if not Extension.getExtension(name):
            ext = Extension(name, enabled, newWindow, type, path, thwidth, thheight)
            meta.Session.add(ext)
            meta.Session.commit()
            return ext
        else:
            return False
