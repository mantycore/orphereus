import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_userOptions = sa.Table("userOptions", meta.metadata,
    sa.Column("optid"    ,sa.types.Integer, primary_key=True),
    sa.Column("uidNumber",sa.types.Integer, sa.ForeignKey('users.uidNumber')),
    sa.Column("threadsPerPage", sa.types.Integer, nullable=False),
    sa.Column("repliesPerThread", sa.types.Integer, nullable=False),
    sa.Column("style"    , sa.types.String(32), nullable=False),
    sa.Column("template" , sa.types.String(32), nullable=False),
    sa.Column("homeExclude", sa.types.String(256), nullable=False),
    sa.Column("hideThreads", sa.types.Text, nullable=True),
    sa.Column("bantime"  , sa.types.Integer, nullable=False),
    sa.Column("banreason", sa.types.UnicodeText(256), nullable=True),
    sa.Column("banDate", sa.types.DateTime, nullable=True),
    sa.Column("hideLongComments", sa.types.Boolean, nullable=True),
    sa.Column("useAjax", sa.types.Boolean, nullable=True),
    sa.Column("mixOldThreads", sa.types.Boolean, nullable=True),
    sa.Column("defaultGoto", sa.types.Integer, nullable=True),
    sa.Column("isAdmin"  , sa.types.Boolean, nullable=True),
    sa.Column("canDeleteAllPosts", sa.types.Boolean, nullable=True),
    sa.Column("canMakeInvite", sa.types.Boolean, nullable=True),
    sa.Column("canChangeRights", sa.types.Boolean, nullable=True)
    )

class UserOptions(object):
    pass