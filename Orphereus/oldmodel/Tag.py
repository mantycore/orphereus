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

from Orphereus.oldmodel import meta
from Orphereus.oldmodel.TagOptions import TagOptions
from Orphereus.lib.miscUtils import empty
import datetime
import re

from pylons.i18n import _, ungettext, N_

import logging
log = logging.getLogger(__name__)

from Orphereus.oldmodel import meta

t_tags = sa.Table("tag", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key = True),
    sa.Column("tag"      , sa.types.UnicodeText, nullable = False),
    sa.Column("replyCount" , sa.types.Integer, nullable = False, server_default = '0'),
    sa.Column("threadCount" , sa.types.Integer, nullable = False, server_default = '0'),
    )

t_tagsToPostsMap = sa.Table("tagsToPostsMap", meta.metadata,
#    sa.Column("id"          , sa.types.Integer, primary_key=True),
    sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id')),
    sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('tag.id')),
    )


t_usertags = sa.Table("usertag", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key = True),
    sa.Column('userId'  , sa.types.Integer, sa.ForeignKey('user.uidNumber')),
    sa.Column("tag"      , sa.types.UnicodeText, nullable = False),
    sa.Column("comment"  , sa.types.UnicodeText, nullable = True),
    )

t_userTagsToPostsMappingTable = sa.Table("usertagsToPostsMap", meta.metadata,
    sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id')),
    sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('usertag.id')),
    )

class UserTag(object):
    def __init__(self, name, comment, uidNumber):
        self.tag = name
        self.comment = comment
        self.userId = uidNumber

    @staticmethod
    def get(tagName, userInst):
        return UserTag.query.filter(and_(UserTag.tag == tagName, UserTag.userId == userInst.uidNumber)).first()

    @staticmethod
    def getById(tagid, userInst):
        return UserTag.query.filter(and_(UserTag.id == int(tagid), UserTag.userId == userInst.uidNumber)).first()

    @staticmethod
    def getPostTags(postid, userId):
        from Orphereus.oldmodel.Post import Post
        return UserTag.query.filter(and_(UserTag.userId == userId, UserTag.posts.any(Post.id == postid))).all()

    def addToThread(self, thread):
        if not thread in self.posts:
            self.posts.append(thread)
            meta.Session.commit()
            return True
        return False

class Tag(object):
    def __repr__(self):
        return u"%s (#%d)" % (self.tag, self.id)

    def __init__(self, tag):
        self.tag = tag
        self.replyCount = 0
        self.threadCount = 0
        self.options = TagOptions()

    def save(self):
        meta.Session.commit()

    def getExactThreadCount(self):
        from Orphereus.oldmodel.Post import Post
        return Post.query.filter(Post.tags.any(Tag.id == self.id)).count()
    """
    def __le__(self, other):
        return cmp(self.tag, other.tag)

    def __ge__(self, other):
        return ncmp(other.tag, self.tag)
    """
    @staticmethod
    def getBoards():
        return Tag.query.join('options').filter(TagOptions.persistent == True).order_by(TagOptions.sectionId).all()

    @staticmethod
    def getTag(tagName):
        return Tag.query.options(eagerload('options')).filter(Tag.tag == tagName).first()

    @staticmethod
    def getById(tagId):
        return Tag.query.options(eagerload('options')).filter(Tag.id == tagId).first()

    @staticmethod
    def getAll():
        return Tag.query.options(eagerload('options')).all()

    @staticmethod
    def getAllByIds(idList):
        return Tag.query.options(eagerload('options')).filter(Tag.id.in_(idList)).all()

    @staticmethod
    def getAllByNames(names):
        return Tag.query.options(eagerload('options')).filter(Tag.tag.in_(names)).all()

    @staticmethod
    def getAllByThreadCount(tc):
        return Tag.query.filter(Tag.threadCount == tc).all()

    @staticmethod
    def splitTagString(tagstr):
        if tagstr:
            tagstr = tagstr.replace('&amp;', '&')
            regex = re.compile(r"""([^,@~\#\+\-\&\s\/\\\(\)<>'"%\d][^,@~\#\+\-\&\s\/\\\(\)<>'"%]*)""")
            return regex.findall(tagstr)
        return []

    @staticmethod
    def stringToTagLists(tagstr, createNewTags = True):
        processedTags = []
        existentTags = []
        nonExistentTagNames = []
        createdTags = []
        for t in Tag.splitTagString(tagstr):
            if not t in processedTags:
                tag = Tag.getTag(t)
                if tag:
                    existentTags.append(tag)
                elif createNewTags:
                    tag = Tag(t)
                    existentTags.append(tag)
                    createdTags.append(tag)
                if tag or createNewTags:
                    processedTags.append(t)
                else:
                    nonExistentTagNames.append(t)
        return (existentTags, createdTags, nonExistentTagNames)

    @staticmethod
    def csStringToExTagIdList(string):
        result = []
        tags = string #.split('|')
        for tag in tags:
            aTag = Tag.query.options(eagerload('options')).filter(Tag.tag == tag).first()
            if aTag:
                result.append(aTag.id)
        return result

    @staticmethod
    def conjunctedOptionsDescript(tags):
        options = empty()
        optionsFlag = True
        rulesList = []
        for t in tags:
            if t.options:
                if optionsFlag:
                    options.imagelessThread = t.options.imagelessThread
                    options.imagelessPost = t.options.imagelessPost
                    options.images = t.options.images
                    options.enableSpoilers = t.options.enableSpoilers
                    options.maxFileSize = t.options.maxFileSize
                    options.minPicSize = t.options.minPicSize
                    options.thumbSize = t.options.thumbSize
                    options.canDeleteOwnThreads = t.options.canDeleteOwnThreads
                    options.selfModeration = t.options.selfModeration
                    options.showInOverview = t.options.showInOverview
                    options.bumplimit = t.options.bumplimit
                    optionsFlag = False
                else:
                    options.imagelessThread = options.imagelessThread & t.options.imagelessThread
                    options.imagelessPost = options.imagelessPost & t.options.imagelessPost
                    options.enableSpoilers = options.enableSpoilers & t.options.enableSpoilers
                    options.canDeleteOwnThreads = options.canDeleteOwnThreads & t.options.canDeleteOwnThreads
                    options.images = options.images & t.options.images
                    options.selfModeration = options.selfModeration | t.options.selfModeration
                    options.showInOverview = options.showInOverview & t.options.showInOverview

                    if t.options.bumplimit and (not options.bumplimit or (t.options.bumplimit < options.bumplimit)):
                        options.bumplimit = t.options.bumplimit

                    perm = meta.globj.OPT.permissiveFileSizeConjunction
                    if (perm and t.options.maxFileSize > options.maxFileSize) or (not perm and t.options.maxFileSize < options.maxFileSize):
                        options.maxFileSize = t.options.maxFileSize

                    if t.options.minPicSize > options.minPicSize:
                        options.minPicSize = t.options.minPicSize
                    if t.options.thumbSize < options.thumbSize:
                        options.thumbSize = t.options.thumbSize

                tagRulesList = t.options.specialRules.split(';')
                for rule in tagRulesList:
                    if rule and not rule in rulesList:
                        rulesList.append(rule)

        options.rulesList = rulesList

        if optionsFlag:
            options.imagelessThread = meta.globj.OPT.defImagelessThread
            options.imagelessPost = meta.globj.OPT.defImagelessPost
            options.images = meta.globj.OPT.defImages
            options.enableSpoilers = meta.globj.OPT.defEnableSpoilers
            options.canDeleteOwnThreads = meta.globj.OPT.defCanDeleteOwnThreads
            options.maxFileSize = meta.globj.OPT.defMaxFileSize
            options.minPicSize = meta.globj.OPT.defMinPicSize
            options.thumbSize = meta.globj.OPT.defThumbSize
            options.selfModeration = meta.globj.OPT.defSelfModeration
            options.showInOverview = meta.globj.OPT.defShowInOverview
            options.bumplimit = meta.globj.OPT.defBumplimit
            options.specialRules = u''
        return options

    @staticmethod
    def getStats():
        boards = Tag.getAll()
        ret = empty()
        ret.boards = []
        ret.tags = []
        ret.stags = []
        ret.totalBoardsThreads = 0
        ret.totalBoardsPosts = 0
        ret.totalTagsThreads = 0
        ret.totalTagsPosts = 0
        ret.totalSTagsThreads = 0
        ret.totalSTagsPosts = 0
        for b in boards:
            if not b.id in meta.globj.forbiddenTags:
                bc = empty()
                bc.count = b.threadCount
                bc.postsCount = b.replyCount
                bc.board = b

                if b.options and b.options.persistent:
                    ret.boards.append(bc)
                    ret.totalBoardsThreads += bc.count
                    ret.totalBoardsPosts += bc.postsCount
                elif not (b.options and b.options.service):
                    ret.tags.append(bc)
                    ret.totalTagsThreads += bc.count
                    ret.totalTagsPosts += bc.postsCount
                else:
                    ret.stags.append(bc)
                    ret.totalSTagsThreads += bc.count
                    ret.totalSTagsPosts += bc.postsCount
        return ret

    @staticmethod
    def checkForConfilcts(tags):
        disabledTags = meta.globj.disabledTags
        maxTagLen = int(meta.globj.OPT.maxTagLen)
        tagsPermOk = True
        problemTags = []
        for tag in tags:
            lengthNeedsToBeChecked = ((not tag.options) or (tag.options and not tag.options.persistent))
            tagLengthProblem = lengthNeedsToBeChecked and len(tag.tag) > maxTagLen
            tagDisabled = tag.tag.lower() in disabledTags
            if (tagLengthProblem or tagDisabled):
                tagsPermOk = False
                errorMsg = N_("Too long. Maximal length: %s" % maxTagLen)
                if tagDisabled:
                    errorMsg = N_("Disabled")
                problemTags.append(tag.tag + " [%s]" % errorMsg)
        return (tagsPermOk, problemTags)

    @staticmethod
    def tagsInConflict(options, postid):
        return not options.images and ((not options.imagelessThread and not postid) or (postid and not options.imagelessPost))
