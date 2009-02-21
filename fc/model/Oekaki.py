import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_oekaki = sa.Table("oekaki", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tempid"   , sa.types.String(20), nullable=False),
    sa.Column("picid"    , sa.types.Integer, nullable=False),
    sa.Column("time"     , sa.types.Integer, nullable=False),
    sa.Column("source"   , sa.types.Integer, nullable=False),
    sa.Column("uidNumber",sa.types.Integer, nullable=False),
    sa.Column("type"     , sa.types.String(255), nullable=False),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("timeStamp", sa.types.DateTime, nullable=False)
    )

#TODO: rewrite Oekaki
class Oekaki(object):
    pass