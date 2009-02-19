import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_extlist = sa.Table("extlist", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("thwidth"  , sa.types.Integer, nullable=False),
    sa.Column("thheight" , sa.types.Integer, nullable=False),
    sa.Column("ext"      , sa.types.String(16), nullable=False),
    sa.Column("type"     , sa.types.String(16), nullable=False),
    sa.Column("enabled"  , sa.types.Boolean, server_default='1'),
    sa.Column("newWindow", sa.types.Boolean, server_default='1'),
    )

class Extension(object):
    pass