import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_tagOptions = sa.Table("tagOptions", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tagId"   , sa.types.Integer,  sa.ForeignKey('tags.id')),
    sa.Column("comment"  , sa.types.UnicodeText, nullable=True),
    sa.Column("sectionId", sa.types.Integer, nullable=False),
    sa.Column("persistent", sa.types.Boolean, nullable=False),
    sa.Column("imagelessThread", sa.types.Boolean, nullable=False),
    sa.Column("imagelessPost", sa.types.Boolean, nullable=False),
    sa.Column("images"   , sa.types.Boolean, nullable=False),
    sa.Column("maxFileSize" , sa.types.Integer, nullable=False),
    sa.Column("minPicSize" , sa.types.Integer, nullable=False),
    sa.Column("thumbSize", sa.types.Integer, nullable=False),
    sa.Column("enableSpoilers", sa.types.Boolean, nullable=False),
    sa.Column("canDeleteOwnThreads", sa.types.Boolean, server_default='1'),
    sa.Column("specialRules"  , sa.types.UnicodeText, nullable=True),
    )

class TagOptions(object):
    def __init__(self):
        self.sectionId = 0
        self.persistent = False