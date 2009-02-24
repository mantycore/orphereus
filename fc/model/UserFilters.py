import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_userFilters = sa.Table("userFilters", meta.metadata,
    sa.Column("id"        , sa.types.Integer    , primary_key=True),
    sa.Column("uidNumber" , sa.types.Integer    , sa.ForeignKey('users.uidNumber')),
    sa.Column("filter"    , sa.types.UnicodeText, nullable=False)
    )

#TODO: rewrite UserFilters
class UserFilters(object):
    def __init__(self, uidNumber, filter):
        self.uidNumber = uidNumber
        self.filter = filter
