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

t_tagOptions = sa.Table("tagOptions", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key = True),
    sa.Column("tagId"   , sa.types.Integer, sa.ForeignKey('tag.id')),
    sa.Column("comment"  , sa.types.UnicodeText, nullable = True),
    sa.Column("sectionId", sa.types.Integer, nullable = False),
    sa.Column("persistent", sa.types.Boolean, nullable = False),
    sa.Column("service", sa.types.Boolean, nullable = False),
    sa.Column("imagelessThread", sa.types.Boolean, nullable = False),
    sa.Column("imagelessPost", sa.types.Boolean, nullable = False),
    sa.Column("images"   , sa.types.Boolean, nullable = False),
    sa.Column("maxFileSize" , sa.types.Integer, nullable = False),
    sa.Column("minPicSize", sa.types.Integer, nullable = False),
    sa.Column("thumbSize", sa.types.Integer, nullable = False),
    sa.Column("enableSpoilers", sa.types.Boolean, nullable = False),
    sa.Column("canDeleteOwnThreads", sa.types.Boolean, server_default = '1'),
    sa.Column("specialRules"  , sa.types.UnicodeText, nullable = True),
    sa.Column("selfModeration", sa.types.Boolean, nullable = False),
    sa.Column("showInOverview", sa.types.Boolean, server_default = '1'),
    sa.Column("bumplimit", sa.types.Integer, nullable = True),
    )

class TagOptions(object):
    def __init__(self):
        self.sectionId = 0
        self.persistent = False
        self.service = False
        self.comment = u''
        self.specialRules = u''
        self.imagelessThread = meta.globj.OPT.defImagelessThread
        self.imagelessPost = meta.globj.OPT.defImagelessPost
        self.images = meta.globj.OPT.defImages
        self.enableSpoilers = meta.globj.OPT.defEnableSpoilers
        self.canDeleteOwnThreads = meta.globj.OPT.defCanDeleteOwnThreads
        self.maxFileSize = meta.globj.OPT.defMaxFileSize
        self.minPicSize = meta.globj.OPT.defMinPicSize
        self.thumbSize = meta.globj.OPT.defThumbSize
        self.selfModeration = meta.globj.OPT.defSelfModeration
        self.showInOverview = meta.globj.OPT.defShowInOverview
        self.bumplimit = meta.globj.OPT.defBumplimit

