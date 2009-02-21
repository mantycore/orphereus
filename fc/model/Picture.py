import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_piclist = sa.Table("piclist", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("thumpath" , sa.types.String(255), nullable=False),
    sa.Column("width"    , sa.types.Integer, nullable=False),
    sa.Column("height"   , sa.types.Integer, nullable=False),    
    sa.Column("thwidth"  , sa.types.Integer, nullable=False),
    sa.Column("thheight" , sa.types.Integer, nullable=False),
    sa.Column("size"     , sa.types.Integer, nullable=False),
    sa.Column("md5"      , sa.types.String(32), nullable=False),
    sa.Column("extid"    , sa.types.Integer, sa.ForeignKey('extlist.id'))
    )

#TODO: rewrite Picture
class Picture(object):
    pass