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

from Orphereus.model import meta
import datetime
import time
import hashlib

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta

def t_invite_init(dialectProps):
    return sa.Table("invite", meta.metadata,
            sa.Column("id"       , sa.types.Integer, sa.Sequence('invite_id_seq'), primary_key = True),
            sa.Column("invite"   , sa.types.String(128), nullable = False),
            sa.Column("date"     , sa.types.DateTime, nullable = False),
            sa.Column("issuer", sa.types.Integer, nullable = True),
            sa.Column("reason" , sa.types.UnicodeText, nullable = True)
            )

class Invite(object):
    def __init__(self, code, issuer = None, reason = None):
        self.date = datetime.datetime.now()
        self.invite = code
        self.issuer = issuer
        self.reason = reason

    @staticmethod
    def getId(code):
        invite = Invite.query.filter(Invite.invite == code).first()
        ret = False
        if invite:
            ret = invite.id
            meta.Session.delete(invite)
            meta.Session.commit()
        return ret

    @staticmethod
    def create(secret, issuer, reason):
        invite = Invite(Invite.generateId(secret), issuer, reason)
        meta.Session.add(invite)
        meta.Session.commit()
        return invite

    @staticmethod
    def generateId(secret):
        return hashlib.sha512(str(long(time.time() * 10 ** 7)) + hashlib.sha512(secret).hexdigest()).hexdigest()
