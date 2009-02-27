import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta, Picture
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
    def __init__(self):
        self.date = datetime.datetime.now()

    @staticmethod
    def create(postParams):
        post = Post()
        post.message = postParams.message
        post.messageShort = postParams.messageShort
        post.messageRaw = postParams.messageRaw
        post.messageInfo = postParams.messageInfo
        post.title = postParams.title
        post.spoiler = postParams.spoiler
        post.uidNumber = postParams.uidNumber
        if postParams.removemd5:
            post.removemd5 = postParams.removemd5

        thread = postParams.thread
        if thread:
            post.parentid = thread.id
            thread.replyCount += 1
            post.sage = postParams.postSage
            if not postParams.postSage:
                thread.bumpDate = datetime.datetime.now()
        else:
            post.parentid = -1
            post.replyCount = 0
            post.bumpDate = datetime.datetime.now()
            post.tags = postParams.tags

        if not postParams.existentPic:
            picInfo = postParams.picInfo
            if picInfo:
                post.file = Picture.create(picInfo.relativeFilePath,
                                     picInfo.thumbFilePath,
                                     picInfo.fileSize,
                                     picInfo.sizes,
                                     picInfo.extId,
                                     picInfo.md5)
        else:
            post.picid = existentPic.id

        meta.Session.add(post)
        meta.Session.commit()

    def incrementStats(self):
        taglist = self.tags

        newThread = True
        if not taglist:
            taglist = self.parentPost.tags
            newThread = False

        for tag in taglist:
            tag.replyCount += 1
            if newThread:
                tag.threadCount += 1

    def selfModeratable(self):
        if getattr(self, 'smCached', None) == None:
            self.smCached = False
            for tag in self.tags:
                if tag.options and tag.options.selfModeration:
                    self.smCached = True
                    break
        return self.smCached

    @staticmethod
    def getPost(id):
        return Post.query.filter(Post.id==id).one()

    @staticmethod
    def pictureRefCount(picid):
        return Post.query.filter(Post.picid==picid).count()

    @staticmethod
    def getByUid(uidNumber):
        return Post.query.filter(Post.uidNumber == uidNumber).all()
