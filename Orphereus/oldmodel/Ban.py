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

from Orphereus.oldmodel import meta
import datetime

import logging
log = logging.getLogger(__name__)

t_bans = sa.Table("bans", meta.metadata,
    sa.Column("id"          , sa.types.Integer, primary_key = True),
#    sa.Column("ip"          , sa.types.Integer, nullable=False),
#    sa.Column("mask"        , sa.types.Integer, nullable=False),
    sa.Column("ip"          , meta.UIntType, nullable = False),
    sa.Column("mask"        , meta.UIntType, nullable = False),
    sa.Column("type"        , sa.types.Integer, nullable = False),
    sa.Column("reason"      , sa.types.UnicodeText, nullable = True),
    sa.Column("date"        , sa.types.DateTime, nullable = False),
    sa.Column("period"      , sa.types.Integer, nullable = False),
    sa.Column("enabled"      , sa.types.Boolean, server_default = '1'),
    )

class Ban(object):
    def __init__(self, ip, mask, type, reason, date, period, enabled):
        self.id = 0
        self._setData(ip, mask, type, reason, date, period, enabled)

    def delete(self):
        meta.Session.delete(self)
        meta.Session.commit()
        return True

    def disable(self):
        self.enabled = False
        meta.Session.commit()

    @staticmethod
    def create(ip, mask, type, reason, date, period, enabled = 0):
        ban = Ban(ip, mask, type, reason, date, period, enabled)
        ban.id = None
        meta.Session.add(ban)
        meta.Session.commit()
        return ban

    def setData(self, ip, mask, type, reason, date, period, enabled):
        self._setData(ip, mask, type, reason, date, period, enabled)
        meta.Session.commit()

    def _setData(self, ip, mask, type, reason, date, period, enabled):
        self.ip = ip
        self.mask = mask
        self.type = type   # 0 for read-only access, 1 for full ban
        self.reason = reason
        self.date = date
        self.period = period
        self.enabled = enabled

    @staticmethod
    def getBans():
        return Ban.query.order_by(Ban.enabled.desc()).all()

    @staticmethod
    def getBanById(banId):
        return Ban.query.filter(banId == Ban.id).first()

    @staticmethod
    def _getBanByIp(userIp):
        return Ban.query.filter(Ban.mask.op('&')(userIp) == Ban.ip.op('&')(Ban.mask)).first() #OMGWTF

    @staticmethod
    def getBanByIp(userIp):
        if meta.globj.OPT.memcachedBans:
            (banInfo, isCached) = meta.globj.mc.get('ban%s' %userIp) or (None, False) 
            if not(isCached):
                banInfo = Ban._getBanByIp(userIp)
                meta.globj.mc.set('ban%s' %userIp, (banInfo, True,), time=meta.globj.OPT.banCacheSeconds)
            return banInfo
        return Ban._getBanByIp(userIp)