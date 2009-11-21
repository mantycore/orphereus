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
from sqlalchemy.orm import eagerload

from Orphereus.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta
from Orphereus.lib.miscUtils import filterText

def t_log_init(dialectProps):
    return sa.Table("log", meta.metadata,
            sa.Column("id"    , sa.types.Integer, primary_key = True),
            sa.Column("uidNumber", sa.types.Integer, sa.ForeignKey('user.uidNumber')),
            sa.Column("date"  , sa.types.DateTime, nullable = False),
            sa.Column("event" , sa.types.Integer, nullable = False),
            sa.Column("entry" , sa.types.UnicodeText, nullable = False)
            )

class LogEntry(object):
    def __init__(self, uidNumber, event, text):
        self.date = datetime.datetime.now()
        self.event = event
        self.uidNumber = uidNumber
        self.entry = text

    @staticmethod
    def count(filterList = False):
        filter = LogEntry.query
        if filterList:
            filter = filter.filter(not_(LogEntry.event.in_(filterList)))
        return filter.count()

    @staticmethod
    def getRange(start, end, filterList = False):
        filter = LogEntry.query.options(eagerload('user')).order_by(LogEntry.date.desc())
        if filterList:
            filter = filter.filter(not_(LogEntry.event.in_(filterList)))
        return filter[start:end]

    @staticmethod
    def create(uidNumber, event, text, commit = True):
        logEntry = LogEntry(uidNumber, event, filterText(text))
        meta.Session.add(logEntry)
        if commit:
            meta.Session.commit()
