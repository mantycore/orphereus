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

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta

def t_oekaki_init(dialectProps):
    return sa.Table("oekaki", meta.metadata,
        sa.Column("id"       , sa.types.Integer, primary_key = True),
        sa.Column("tempid"   , sa.types.String(20), nullable = False),
        sa.Column("time"     , sa.types.Integer, nullable = False),
        sa.Column("sourcePost"   , sa.types.Integer, nullable = True),
        sa.Column("sourcePicIdx" , sa.types.Integer, nullable = True),
        sa.Column("uidNumber", sa.types.Integer, nullable = False),
        sa.Column("type"     , sa.types.String(255), nullable = False),
        sa.Column("path"     , sa.types.String(255), nullable = False),
        sa.Column("timeStamp", sa.types.DateTime, nullable = False),
        sa.Column("selfy", sa.types.Boolean, nullable = False),
        sa.Column("animPath", sa.types.String(255), nullable = True),
        )

class Oekaki(object):
    def __init__(self, tempid, uidNumber, type, sourcePost, sourcePicIdx, selfy):
        self.timeStamp = datetime.datetime.now()
        self.time = -1
        self.path = ''
        self.type = type
        self.uidNumber = uidNumber
        self.sourcePost = sourcePost
        self.sourcePicIdx = sourcePicIdx
        self.tempid = tempid
        self.selfy = selfy
        self.animPath = None

    @staticmethod
    def create(tempid, uidNumber, type, source, sourcePicIdx, selfy):
        oekaki = Oekaki(tempid, uidNumber, type, source, sourcePicIdx, selfy)
        meta.Session.add(oekaki)
        meta.Session.commit()

    @staticmethod
    def get(tempid):
        return Oekaki.query.filter(Oekaki.tempid == tempid).first()

    def setPathsAndTime(self, path, animPath, time):
        self.path = path
        self.animPath = animPath
        self.time = time
        meta.Session.commit()

    def delete(self):
        meta.Session.delete(self)
        meta.Session.commit()
