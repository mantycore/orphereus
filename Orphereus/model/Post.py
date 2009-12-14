################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_, or_, not_

from Orphereus.model import meta
from Orphereus.model.Picture import Picture, PictureAssociation
from Orphereus.model.Tag import Tag
#from Orphereus.model.TagOptions import TagOptions
from Orphereus.model.LogEntry import LogEntry
from Orphereus.lib.miscUtils import getRPN, empty
from Orphereus.lib.constantValues import *
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
import datetime
import os

from pylons.i18n import _, ungettext, N_
from paste.deploy.converters import asbool

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta

def t_posts_init(dialectProps):
    return sa.Table("post", meta.metadata,
    sa.Column("id"       , sa.types.Integer, sa.Sequence('post_id_seq'), primary_key = True, index = not meta.dialectProps['disableComplexIndexes']),
    sa.Column("secondaryIndex", sa.types.Integer, nullable = True),
    sa.Column("parentid" , sa.types.Integer, sa.ForeignKey('post.id'), nullable = True, index = True),
    sa.Column("message"  , sa.types.UnicodeText, nullable = True),
    sa.Column("messageShort", sa.types.UnicodeText, nullable = True),
    sa.Column("messageRaw"  , sa.types.UnicodeText, nullable = True),
    sa.Column("messageInfo"  , sa.types.UnicodeText, nullable = True),
    sa.Column("title"    , sa.types.UnicodeText, nullable = True),
    sa.Column("sage"     , sa.types.Boolean, nullable = True),
    sa.Column("uidNumber", sa.types.Integer, nullable = True, index = True),
    sa.Column("date"     , sa.types.DateTime, nullable = False, index = True),
    sa.Column("bumpDate", sa.types.DateTime, nullable = True, index = True),
    sa.Column("replyCount" , sa.types.Integer, nullable = False, server_default = '0'),
    sa.Column("removemd5"  , sa.types.String(32), nullable = True),
    sa.Column("ip"         , meta.UIntType, nullable = True),
    sa.Column("pinned"  , sa.types.Boolean, nullable = False, index = True),
    #sa.Column("spoiler"  , sa.types.Boolean, nullable = True),
    )
#sa.Index('idx_BumpPin', t_posts.c.bumpDate, t_posts.c.pinned)

class Post(object):
    def __init__(self):
        self.date = datetime.datetime.now()
        self.pinned = False

    @staticmethod
    def create(postParams):
        post = Post()
        post.secondaryIndex = postParams.get('secondaryIndex', None)
        post.date = postParams.get('date', None)
        post.message = postParams.message
        post.messageShort = postParams.messageShort
        post.messageRaw = postParams.messageRaw
        post.messageInfo = postParams.messageInfo
        post.title = postParams.title
        #post.spoiler = postParams.spoiler
        post.uidNumber = postParams.uidNumber
        if postParams.removemd5:
            post.removemd5 = postParams.removemd5

        post.ip = postParams.ip

        thread = postParams.thread
        if thread:
            post.parentid = thread.id
            thread.replyCount += 1
            #log.debug(postParams.bumplimit)
            #log.debug(thread.replyCount)
            post.sage = postParams.postSage
            limitOk = not postParams.bumplimit or (postParams.bumplimit >= thread.replyCount)
            if (not postParams.postSage) and limitOk:
                thread.bumpDate = datetime.datetime.now()
        else:
            post.parentid = None
            post.replyCount = 0
            post.bumpDate = datetime.datetime.now()
            post.tags = postParams.tags

        recentlyCreated = {}
        for picInfo in postParams.picInfos:
            if picInfo:
                existent = recentlyCreated.get(picInfo.md5, picInfo.existentPic)
                if not existent: # in postParams.existentPics:
                    newPic = Picture.create(picInfo.relativeFilePath,
                                         picInfo.thumbFilePath,
                                         picInfo.fileSize,
                                         picInfo.sizes,
                                         picInfo.extension.id,
                                         picInfo.md5,
                                         picInfo.additionalInfo,
                                         )
                    assoc = PictureAssociation(picInfo.spoiler, picInfo.relationInfo, picInfo.animPath)
                    meta.Session.add(assoc)
                    assoc.attachedFile = newPic
                    post.attachments.append(assoc)
                    recentlyCreated[picInfo.md5] = newPic
                else:
                    alreadyAdded = None
                    for attachment in post.attachments:
                        if attachment.attachedFile == existent:
                            alreadyAdded = True
                            break
                    if not alreadyAdded:
                        assoc = PictureAssociation(picInfo.spoiler, None, None)
                        meta.Session.add(assoc)
                        assoc.attachedFile = existent
                        post.attachments.append(assoc)

        post.incrementStats()
        meta.Session.add(post)
        meta.Session.commit()
        return post
    
    # TODO: add file support
    @staticmethod
    def createDef(**params):
        defaultParams = {'message': u'',
                         'messageShort': u'',
                         'messageRaw': u'',
                         'messageInfo': u'',
                         'title': u'',
                         'uidNumber': u'',
                         'parentid': 1,
                         'ip': 0, 
                         'uidNumber': 0,
                         'date': datetime.datetime.now(),
                         'pinned': False,
                         'sage': False, 
                         }
        defaultParams.update(params)
        post = Post()
        for key in defaultParams.keys():
            setattr(post, key, defaultParams[key])
        meta.Session.add(post)
        meta.Session.commit()

    def removeTag(self, tag):
        if not self.parentid:
            if tag in self.tags:
                tag.threadCount -= 1
                tag.replyCount -= (self.replyCount + 1)
                self.tags.remove(tag)
        else:
            raise Exception("Can't remove tags from reply")

    def appendTag(self, tag):
        if not self.parentid:
            if not tag in self.tags:
                tag.threadCount += 1
                tag.replyCount += (self.replyCount + 1)
                self.tags.append(tag)
        else:
            raise Exception("Can't remove tags from reply")

    def incrementStats(self):
        taglist = self.tags

        newThread = True
        if not taglist:
            taglist = Post.getPost(self.parentid).tags
            newThread = False

        for tag in taglist:
            tag.replyCount += 1
            if newThread:
                tag.threadCount += 1

    def selfModeratable(self):
        if getattr(self, 'smCached', None) == None:
            self.smCached = False
            for tag in self.tags:
                if tag.selfModeration:
                    self.smCached = True
                    break
        return self.smCached

    @staticmethod
    def tagLine(tags, tagNames = None):
        names = []
        rawNames = []
        for t in tags:
            names.append(t.comment or (u"/%s/" % t.tag))
            rawNames.append(t.tag)
        if tagNames:
            for name in tagNames:
                if not name in rawNames:
                    rawNames.append(name)
                    names.append(u"/%s/" % name)
        return ("+".join(rawNames), " + ".join(names))

    def getExactReplyCount(self):
        if self.parentPost:
            return False
        else:
            return Post.query.filter(Post.parentid == self.id).count()

    def filterReplies(self):
        if self.parentPost:
            return []
        else:
            return Post.query.filter(Post.parentid == self.id).order_by(Post.id.asc())

    @staticmethod
    def getPost(id):
        return Post.query.get(id)
        #return Post.query.filter(Post.id==id).one()

    @staticmethod
    def filterByUid(uidNumber):
        return Post.query.filter(Post.uidNumber == uidNumber)

    @staticmethod
    def filter(filter):
        if filter is not None:
            return Post.query.filter(filter)
        return Post.query

    @staticmethod
    def buildMetaboardFilter(url, userInst):
        def buildMyPostsFilter(opOnly = False):
            list = []
            posts = Post.filterByUid(userInst.uidNumber).all()

            for p in posts:
                if not p.parentid and not p.id in list:
                    list.append(p.id)
                elif p.parentid and not (p.parentid in list) and not opOnly:
                    list.append(p.parentid)
            return Post.id.in_(list)

        def buildArgument(arg):
            if not isinstance(arg, sa.sql.expression.ClauseElement):
                if arg == '@':
                    return (buildMyPostsFilter(False), [])
                elif arg == "*":
                    return (buildMyPostsFilter(True), [])
                elif arg == '~':
                    #disableExclusions = Post.tags.any(Tag.id.in_(userInst.homeExclude))
                    #disableHidden = Post.tags.any(not_(Tag.showInOverview))
                    #return (not_(or_(disableExclusions, disableHidden)), [])
                    #inclusion = Post.tags.any(and_(Tag.showInOverview == True, not_(Tag.id.in_(userInst.homeExclude))))
                    if userInst.homeExclude:
                        return (not_(Post.tags.any(or_(Tag.showInOverview == False, Tag.id.in_(userInst.homeExclude)))), [])
                    else:
                        return (not_(Post.tags.any(Tag.showInOverview == False)), [])
                else:
                    retarg = [arg]
                    hooks = meta.globj.implementationsOf(AbstractPostingHook)
                    for handler in hooks:
                        clause, newName = handler.tagHandler(arg, userInst)
                        if (clause is not None) and newName:
                            return (clause, [newName])
                        elif newName:
                            retarg = [newName]
                    return (Post.tags.any(tag = arg), retarg)
            else:
                return arg

        filter = Post.query.options(eagerload('attachments')).filter(Post.parentid == None)
        filteringExpression = Post.excludeAdminOnlyThreads(userInst)
        tagList = []
        if url:
            operators = {'+':1, '-':1, '^':2, '&':2}
            url = url.replace('&amp;', '&')
            RPN = getRPN(url, operators)
            stack = []
            for i in RPN:
                if i in operators:
                    # If operator is not provided with 2 arguments, we silently ignore it. (for example '- b' will be just 'b')
                    if len(stack) >= 2:
                        arg2 = stack.pop()
                        arg1 = stack.pop()
                        if i == '+':
                            f = or_(arg1[0], arg2[0])
                            for t in arg2[1]:
                                if not t in arg1[1]:
                                    arg1[1].append(t)
                            stack.append((f, arg1[1]))
                        elif i == '&' or i == '^':
                            f = and_(arg1[0], arg2[0])
                            for t in arg2[1]:
                                if not t in arg1[1]:
                                    arg1[1].append(t)
                            stack.append((f, arg1[1]))
                        elif i == '-':
                            f = and_(arg1[0], not_(arg2[0]))
                            for t in arg2[1]:
                                if t in arg1[1]:
                                    arg1[1].remove(t)
                            stack.append((f, arg1[1]))
                else:
                    stack.append(buildArgument(i))
            if stack and isinstance(stack[0][0], sa.sql.expression.ClauseElement):
                cl = stack.pop()
                if filteringExpression is not None:
                    filteringExpression = and_(cl[0], filteringExpression)
                else:
                    filteringExpression = cl[0]
                tagList = cl[1]
        if filteringExpression is not None:
            filter = filter.filter(filteringExpression)
        return (filter, tagList, filteringExpression)

    @staticmethod
    def excludeAdminOnlyThreads(userInst):
        blockHidden = None #not_(Post.id == None)
        if not userInst.isAdmin():
            # Now excludeAdminOnlyThreads uses only for thread exclusion, so we shouldn't exclude children...
            blockHidden = not_(Post.tags.any(Tag.adminOnly == True))
            #blocker = Post.tags.any(Tag.adminOnly == True)
            #blockHidden = not_(or_(blocker, Post.parentPost.has(blocker)))
        return blockHidden

    @staticmethod
    def buildThreadFilter(userInst, threadId):
        exclusion = Post.excludeAdminOnlyThreads(userInst)
        if exclusion is not None:
            return Post.filter(exclusion).filter(Post.id == threadId).options(eagerload('attachments'))
        else:
            return Post.filter(Post.id == threadId).options(eagerload('attachments'))

    @staticmethod
    def getThread(threadId):
        return Post.filter(or_(Post.parentid == threadId, Post.id == threadId)).order_by(Post.id.asc()).all()

    def deletePost(self, userInst, fileonly = False, checkOwnage = True, reason = "???", rempPass = False):
        opPostDeleted = False

        if userInst.Anonymous and self.removemd5 != rempPass:
            return False

        threadRemove = True
        tags = self.tags
        parentp = self
        if self.parentPost:
            parentp = self.parentPost
            tags = parentp.tags
            threadRemove = False

        isOwner = userInst.uidNumber == self.uidNumber
        selfModEnabled = parentp.selfModeratable()
        canModerate = selfModEnabled and userInst.uidNumber == parentp.uidNumber
        postCanBeDeleted = (isOwner or canModerate or userInst.canDeleteAllPosts())

        if checkOwnage and not postCanBeDeleted:
            # print some error stuff here
            return False

        tagline = u''
        taglist = []
        for tag in tags:
            taglist.append(tag.tag)

            tag.replyCount -= 1
            if threadRemove:
                tag.threadCount -= 1
        tagline = ', '.join(taglist)

        postOptions = Tag.conjunctedOptionsDescript(self.parentid > 0 and parentp.tags or self.tags)
        if checkOwnage and not self.uidNumber == userInst.uidNumber:
            logEntry = u''
            uidNumber = userInst.uidNumber
            if not canModerate:
                if self.parentid:
                    logEntry = N_("Deleted post %s (owner %s); from thread: %s; tagline: %s; reason: %s") % (self.id, self.uidNumber, self.parentid, tagline, reason)
                else:
                    logEntry = N_("Deleted thread %s (owner %s); tagline: %s; reason: %s") % (self.id, self.uidNumber, tagline, reason)
            else:
                uidNumber = 0
                logEntry = N_("[self-moderation] Deleted post %s") % (self.id)
            if fileonly:
                logEntry += " %s" % N_("(file only)")
            LogEntry.create(uidNumber, LOG_EVENT_POSTS_DELETE, logEntry)

        if not self.parentPost and not fileonly:
            if not (postOptions.canDeleteOwnThreads or userInst.canDeleteAllPosts()):
                return False
            opPostDeleted = True
            for post in Post.query.filter(Post.parentid == self.id).all():
                post.deletePost(userInst, checkOwnage = False)

        if self.attachments:
            filesToDelete = []
            #TODO: ability for deletion separate files
            for picAssoc in self.attachments:
                filesToDelete.append(picAssoc.attachedFile)
                picAssoc.attachedFile = Picture.getPicture(0)
                picAssoc.spoiler = None
                picAssoc.relationInfo = None
                if picAssoc.animpath:
                    picAssoc.animpath = None
                    animPath = os.path.join(meta.globj.OPT.uploadPath, picAssoc.animpath)
                    if os.path.isfile(animPath):
                        os.unlink(animPath)

            meta.Session.commit()

            for picAssoc in filesToDelete:
                picAssoc.deletePicture(True)

        if not (fileonly and postOptions.imagelessPost):
            invisBumpDisabled = not(asbool(meta.globj.OPT.invisibleBump))
            parent = self.parentPost
            if parent:
                parent.replyCount -= 1

            if invisBumpDisabled and self.parentid and not self.sage:
                thread = Post.query.filter(Post.parentid == self.parentid).all()
                maxDate = parent.date
                for post in thread:
                    if (not post.sage) and (not post.id == self.id) and maxDate < post.date:
                        maxDate = post.date
                parent.bumpDate = maxDate

            meta.Session.delete(self)
        meta.Session.commit()
        return opPostDeleted

    @staticmethod
    def getPostsCount():
        return Post.query.count()

    @staticmethod
    def vitalSigns():
        ret = empty()
        tpc = Post.getPostsCount()
        uniqueUidsExpr = meta.Session.query(Post.uidNumber).distinct()
        ret.last1KUsersCount = uniqueUidsExpr.filter(and_(Post.id <= tpc, Post.id >= tpc - 1000)).count()
        ret.prev1KUsersCount = uniqueUidsExpr.filter(and_(Post.id <= tpc - 1000, Post.id >= tpc - 2000)).count()

        currentTime = datetime.datetime.now()
        firstBnd = currentTime - datetime.timedelta(days = 7)
        secondBnd = currentTime - datetime.timedelta(days = 14)
        ret.lastWeekMessages = meta.Session.query(Post.id).filter(Post.date >= firstBnd).count()
        ret.prevWeekMessages = meta.Session.query(Post.id).filter(and_(Post.date <= firstBnd, Post.date >= secondBnd)).count()
        return ret

    @staticmethod
    def normalizeHiddenThreadsList(userInst):
        userInst.hideThreads = map(lambda x: int(x), userInst.hideThreads) #legacy support
        hiddenTuples = meta.Session.query(Post.id).filter(Post.id.in_(userInst.hideThreads)).all()
        userInst.hideThreads = map(lambda x: x[0], hiddenTuples)
        meta.Session.commit()
