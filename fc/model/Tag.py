import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_tags = sa.Table("tags", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tag"      , sa.types.UnicodeText, nullable=False),
    sa.Column("replyCount" , sa.types.Integer, nullable=False, server_default='0'),
    sa.Column("threadCount" , sa.types.Integer, nullable=False, server_default='0'),
    )

t_tagsToPostsMap = sa.Table("tagsToPostsMap", meta.metadata,
#    sa.Column("id"          , sa.types.Integer, primary_key=True),                            
    sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('posts.id')),
    sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('tags.id')),
    )

class Tag(object):
    def __init__(self, tag): # xxx???  Liebert
        self.tag = tag
        self.replyCount = 0
        self.threadCount = 0