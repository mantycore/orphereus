import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_invites = sa.Table("invites", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("invite"   , sa.types.String(128), nullable=False),
    sa.Column("date"     , sa.types.DateTime,  nullable=False)
    )
    
#TODO: rewrite Invite
class Invite(object):
    pass