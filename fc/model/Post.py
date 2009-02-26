import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_posts = sa.Table("posts", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("secondaryIndex",sa.types.Integer, nullable=True),
    sa.Column("parentid" , sa.types.Integer, sa.ForeignKey('posts.id'), index=True),
    sa.Column("message"  , sa.types.UnicodeText, nullable=True),
    sa.Column("messageShort", sa.types.UnicodeText, nullable=True),
    sa.Column("messageRaw"  , sa.types.UnicodeText, nullable=True),
    sa.Column("messageInfo"  , sa.types.UnicodeText, nullable=True),
    sa.Column("title"    , sa.types.UnicodeText, nullable=True),
    sa.Column("sage"     , sa.types.Boolean, nullable=True),
    sa.Column("uidNumber",sa.types.Integer,nullable=True),
    sa.Column("picid"    , sa.types.Integer, sa.ForeignKey('piclist.id')),
    sa.Column("date"     , sa.types.DateTime, nullable=False),
    sa.Column("bumpDate", sa.types.DateTime, nullable=True),
    sa.Column("spoiler"  , sa.types.Boolean, nullable=True),
    sa.Column("replyCount" , sa.types.Integer, nullable=False, server_default='0'),
    sa.Column("removemd5"  , sa.types.String(32), nullable=True),
    )

#TODO: rewrite Post
class Post(object):
    def selfModeratable(self):
        if getattr(self, 'smCached', None) == None:
            self.smCached = False
            for tag in self.tags:
                if tag.options and tag.options.selfModeration:
                    self.smCached = True
                    break
        return self.smCached

    @staticmethod
    def pictureRefCount(picid):
        return Post.query.filter(Post.picid==picid).count()
