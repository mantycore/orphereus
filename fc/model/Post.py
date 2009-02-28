import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_, or_, not_

from fc.model import meta
from fc.model.Picture import Picture
from fc.model.Tag import Tag
from fc.lib.miscUtils import getRPN
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
            post.picid = postParams.existentPic.id

        meta.Session.add(post)
        meta.Session.commit()
        return post

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

    def getExactReplyCount(self):
        if self.parentPost:
            return False
        else:
            return Post.query.filter(Post.parentid == self.id).count()

    def getReplies(self):
        if self.parentPost:
            return False
        else:
            return Post.query.filter(Post.parentid == self.id).all()

    @staticmethod
    def getPost(id):
        return Post.query.get(id)
        #return Post.query.filter(Post.id==id).one()

    @staticmethod
    def pictureRefCount(picid):
        return Post.query.filter(Post.picid==picid).count()

    @staticmethod
    def filterByUid(uidNumber):
        return Post.query.filter(Post.uidNumber == uidNumber)

    @staticmethod
    def buildFilter(url, userInst):
        def buildMyPostsFilter():
            list  = []
            posts = Post.getByUid(userInst.uidNumber).all()

            for p in posts:
                if p.parentid == -1 and not p.id in list:
                    list.append(p.id)
                elif p.parentid > -1 and not p.parentid in list:
                    list.append(p.parentid)
            return Post.id.in_(list)

        def buildArgument(arg):
            if not isinstance(arg, sa.sql.expression.ClauseElement):
                if arg == '@':
                    return (buildMyPostsFilter(), [])
                elif arg == '~':
                    return (not_(Post.tags.any(Tag.id.in_(userInst.homeExclude()))), [])
                else:
                    return (Post.tags.any(tag=arg), [arg])
            else:
                return arg

        #log.debug(self.userInst.homeExclude())
        operators = {'+':1, '-':1, '^':2, '&':2}
        url = url.replace('&amp;', '&')
        filter = Post.query.options(eagerload('file')).filter(Post.parentid==-1)
        filteringExpression = False
        tagList = []
        RPN = getRPN(url,operators)
        stack = []
        for i in RPN:
            if i in operators:
                # If operator is not provided with 2 arguments, we silently ignore it. (for example '- b' will be just 'b')
                if len(stack)>= 2:
                    arg2 = stack.pop()
                    arg1 = stack.pop()
                    if i == '+':
                        f = or_(arg1[0],arg2[0])
                        for t in arg2[1]:
                            if not t in arg1[1]:
                                arg1[1].append(t)
                        stack.append((f,arg1[1]))
                    elif i == '&' or i == '^':
                        f = and_(arg1[0],arg2[0])
                        for t in arg2[1]:
                            if not t in arg1[1]:
                                arg1[1].append(t)
                        stack.append((f,arg1[1]))
                    elif i == '-':
                        f = and_(arg1[0],not_(arg2[0]))
                        for t in arg2[1]:
                            if t in arg1[1]:
                                arg1[1].remove(t)
                        stack.append((f,arg1[1]))
            else:
                stack.append(buildArgument(i))
        if stack and isinstance(stack[0][0],sa.sql.expression.ClauseElement):
            cl = stack.pop()
            filteringExpression = cl[0]
            filter = filter.filter(filteringExpression)
            tagList = cl[1]
        return (filter, tagList, filteringExpression)

    @staticmethod
    def excludeAdminTags(filter, userInst):
        if not userInst.isAdmin():
            blocker = Post.tags.any(Tag.id.in_(meta.globj.forbiddenTags))
            filter = filter.filter(not_(
                                   or_(blocker,
                                        Post.parentPost.has(blocker),
                                   )))
        return filter
