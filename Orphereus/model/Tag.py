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

from Orphereus.model import meta
#from Orphereus.model.TagOptions import TagOptions
from Orphereus.lib.miscUtils import empty
import datetime
import re

from pylons.i18n import _, ungettext, N_

import logging
log = logging.getLogger(__name__)

from Orphereus.model import meta

def t_tags_init(dialectProps):
    t_tags = sa.Table("tag", meta.metadata,
        sa.Column("id"       , sa.types.Integer, sa.Sequence('tag_id_seq'), primary_key = True),
        sa.Column("tag"      , sa.types.Unicode(meta.dialectProps['tagLengthHardLimit']), nullable = False, unique = True, index = True),
        sa.Column("replyCount" , sa.types.Integer, nullable = False, server_default = '0'),
        sa.Column("threadCount" , sa.types.Integer, nullable = False, server_default = '0'),
        sa.Column("comment"  , sa.types.UnicodeText, nullable = True),
        sa.Column("sectionId", sa.types.Integer, nullable = False),
        sa.Column("persistent", sa.types.Boolean, nullable = False,),
        sa.Column("service", sa.types.Boolean, nullable = False,),
        sa.Column("imagelessThread", sa.types.Boolean, nullable = False),
        sa.Column("imagelessPost", sa.types.Boolean, nullable = False),
        sa.Column("images"   , sa.types.Boolean, nullable = False),
        sa.Column("maxFileSize" , sa.types.Integer, nullable = False),
        sa.Column("minPicSize", sa.types.Integer, nullable = False),
        sa.Column("thumbSize", sa.types.Integer, nullable = False),
        sa.Column("enableSpoilers", sa.types.Boolean, nullable = False),
        sa.Column("canDeleteOwnThreads", sa.types.Boolean, nullable = False),
        sa.Column("specialRules"  , sa.types.UnicodeText, nullable = True),
        sa.Column("selfModeration", sa.types.Boolean, nullable = False),
        sa.Column("showInOverview", sa.types.Boolean, nullable = False, index = True),
        sa.Column("bumplimit", sa.types.Integer, nullable = True),
        sa.Column("allowedAdditionalFiles", sa.types.Integer, nullable = True),
        sa.Column("adminOnly", sa.types.Boolean, nullable = False, index = True),
        sa.Column("sectionWeight", sa.types.Integer, nullable = False),
        )

    t_tagsToPostsMap = sa.Table("tagsToPostsMap", meta.metadata,
    #    sa.Column("id"          , sa.types.Integer, primary_key=True),
        sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id'), primary_key = True),
        sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('tag.id'), primary_key = True),
        )
    if not meta.dialectProps['disableComplexIndexes']:
        sa.Index('ix_tagmap_postid_tagid',
                 t_tagsToPostsMap.c.postId,
                 t_tagsToPostsMap.c.tagId,
                 unique = True)

    return t_tags, t_tagsToPostsMap

class Tag(object):
    TAGREGEX = r"""([^,@~\#\+\-\&\s\/\\\(\)<>'"%\d][^,@~\#\+\-\&\s\/\\\(\)<>'"%]*)"""

    def __repr__(self):
        return u"%s (#%d)" % (self.tag, self.id)

    def __init__(self, tag):
        self.tag = tag
        self.replyCount = 0
        self.threadCount = 0
        self.sectionWeight = 0
        #self.options = TagOptions()
        self.sectionId = 0
        self.persistent = False
        self.service = False
        self.adminOnly = False
        self.comment = u''
        self.specialRules = u''
        self.imagelessThread = meta.globj.OPT.defImagelessThread
        self.imagelessPost = meta.globj.OPT.defImagelessPost
        self.images = meta.globj.OPT.defImages
        self.enableSpoilers = meta.globj.OPT.defEnableSpoilers
        self.canDeleteOwnThreads = meta.globj.OPT.defCanDeleteOwnThreads
        self.maxFileSize = meta.globj.OPT.defMaxFileSize
        self.minPicSize = meta.globj.OPT.defMinPicSize
        self.thumbSize = meta.globj.OPT.defThumbSize
        self.selfModeration = meta.globj.OPT.defSelfModeration
        self.showInOverview = meta.globj.OPT.defShowInOverview
        self.bumplimit = meta.globj.OPT.defBumplimit
        self.allowedAdditionalFiles = meta.globj.OPT.allowedAdditionalFiles

    def save(self):
        meta.Session.commit()

    def getExactThreadCount(self):
        from Orphereus.model.Post import Post
        return Post.query.filter(Post.tags.any(Tag.id == self.id)).count()
    """
    def __le__(self, other):
        return cmp(self.tag, other.tag)

    def __ge__(self, other):
        return ncmp(other.tag, self.tag)
    """
    @staticmethod
    def getBoards():
        return Tag.query.filter(Tag.persistent == True).order_by(Tag.sectionId).all()

    @staticmethod
    def getTag(tagName):
        return Tag.query.filter(Tag.tag == tagName).first()

    @staticmethod
    def getById(tagId):
        return Tag.query.filter(Tag.id == tagId).first()

    @staticmethod
    def getAll():
        return Tag.query.all()

    @staticmethod
    def getAllByIds(idList):
        return Tag.query.filter(Tag.id.in_(idList)).all()

    @staticmethod
    def getAllByNames(names):
        return Tag.query.filter(Tag.tag.in_(names)).all()

    @staticmethod
    def getAllByThreadCount(tc):
        return Tag.query.filter(Tag.threadCount == tc).all()

    @staticmethod
    def splitTagString(tagstr):
        if tagstr:
            tagstr = tagstr.replace('&amp;', '&')
            regex = re.compile(Tag.TAGREGEX)
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
    """
    @staticmethod
    def csStringToExTagIdList(string):
        result = []
        tags = string #.split('|')
        for tag in tags:
            aTag = Tag.query.filter(Tag.tag == tag).first()
            if aTag:
                result.append(aTag.id)
        return result
    """
    @staticmethod
    def conjunctedOptionsDescript(tags):
        options = empty()
        optionsFlag = True
        rulesList = []
        for t in tags:
            if optionsFlag:
                options.imagelessThread = t.imagelessThread
                options.imagelessPost = t.imagelessPost
                options.images = t.images
                options.enableSpoilers = t.enableSpoilers
                options.maxFileSize = t.maxFileSize
                options.minPicSize = t.minPicSize
                options.thumbSize = t.thumbSize
                options.canDeleteOwnThreads = t.canDeleteOwnThreads
                options.selfModeration = t.selfModeration
                options.showInOverview = t.showInOverview
                options.bumplimit = t.bumplimit
                options.allowedAdditionalFiles = t.allowedAdditionalFiles is None and meta.globj.OPT.allowedAdditionalFiles or t.allowedAdditionalFiles
                optionsFlag = False
            else:
                options.imagelessThread = options.imagelessThread & t.imagelessThread
                options.imagelessPost = options.imagelessPost & t.imagelessPost
                options.enableSpoilers = options.enableSpoilers & t.enableSpoilers
                options.canDeleteOwnThreads = options.canDeleteOwnThreads & t.canDeleteOwnThreads
                options.images = options.images & t.images
                options.selfModeration = options.selfModeration | t.selfModeration
                options.showInOverview = options.showInOverview & t.showInOverview

                if t.bumplimit and (not options.bumplimit or (t.bumplimit < options.bumplimit)):
                    options.bumplimit = t.bumplimit

                perm = meta.globj.OPT.permissiveFileSizeConjunction
                if (perm and t.maxFileSize > options.maxFileSize) or (not perm and t.maxFileSize < options.maxFileSize):
                    options.maxFileSize = t.maxFileSize

                if t.minPicSize > options.minPicSize:
                    options.minPicSize = t.minPicSize
                if t.thumbSize < options.thumbSize:
                    options.thumbSize = t.thumbSize

                currentAllowed = t.allowedAdditionalFiles
                if currentAllowed is None:
                    currentAllowed = meta.globj.OPT.allowedAdditionalFiles
                assert type(currentAllowed) == int or type(currentAllowed) == long
                perm = meta.globj.OPT.permissiveAdditionalFilesCountConjunction
                if (perm and currentAllowed > options.allowedAdditionalFiles) or (not perm and currentAllowed < options.allowedAdditionalFiles):
                    options.allowedAdditionalFiles = currentAllowed
            tagRulesList = t.specialRules.split(';')
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
            options.allowedAdditionalFiles = meta.globj.OPT.allowedAdditionalFiles
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
            if not b.adminOnly:
                bc = empty()
                bc.count = b.threadCount
                bc.postsCount = b.replyCount
                bc.board = b

                if b.persistent:
                    ret.boards.append(bc)
                    ret.totalBoardsThreads += bc.count
                    ret.totalBoardsPosts += bc.postsCount
                elif not b.service:
                    ret.tags.append(bc)
                    ret.totalTagsThreads += bc.count
                    ret.totalTagsPosts += bc.postsCount
                else:
                    ret.stags.append(bc)
                    ret.totalSTagsThreads += bc.count
                    ret.totalSTagsPosts += bc.postsCount
        return ret

    @staticmethod
    def maxLen(onlyHardLimit = False):
        if onlyHardLimit:
            return meta.dialectProps['tagLengthHardLimit']
        return min(int(meta.globj.OPT.maxTagLen), meta.dialectProps['tagLengthHardLimit'])

    @staticmethod
    def cutTag(tagName, onlyHardLimit = False):
        return tagName[:Tag.maxLen(onlyHardLimit)]

    @staticmethod
    def checkForConfilcts(tags):
        disabledTags = meta.globj.disabledTags
        maxTagLen = Tag.maxLen()
        tagsPermOk = True
        problemTags = []
        for tag in tags:
            lengthNeedsToBeChecked = not tag.persistent
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
