import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.orm import eagerload

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_log = sa.Table("log", meta.metadata,
    sa.Column("id"    , sa.types.Integer, primary_key=True),
    sa.Column("uidNumber", sa.types.Integer, sa.ForeignKey('users.uidNumber')),
    sa.Column("date"  , sa.types.DateTime, nullable=False),
    sa.Column("event" , sa.types.Integer, nullable=False),
    sa.Column("entry" , sa.types.UnicodeText, nullable=False)
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
        log.debug(start)
        log.debug(end)
        filter = LogEntry.query.options(eagerload('user')).order_by(LogEntry.date.desc())
        if filterList:
            filter = filter.filter(not_(LogEntry.event.in_(filterList)))
        return filter[start:end]

    @staticmethod
    def create(uidNumber, event, text, commit = True):
        logEntry = LogEntry(uidNumber, event, text)
        meta.Session.add(logEntry)
        if commit:
            meta.Session.commit()
