import sqlalchemy as sa
from sqlalchemy import orm

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
    pass