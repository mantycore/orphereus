# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Hedger                                                   #
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

from pylons.i18n import N_
from string import *

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.miscUtils import *
from Orphereus.lib.base import *
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.lib.interfaces.AbstractProfileExtension import AbstractProfileExtension
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

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
        ns = g.pluginsDict['usertags'].pnamespace
        return ns.UserTag.query.filter(and_(ns.UserTag.userId == userId, ns.UserTag.posts.any(Post.id == postid))).all()

    def addToThread(self, thread):
        if not thread in self.posts:
            self.posts.append(thread)
            meta.Session.commit()
            return True
        return False
    """
        @staticmethod
        def getMappingTable():
            if not UserTag.userTagsToPostsMappingTable:
                UserTag.userTagsToPostsMappingTable = sa.Table("usertagsToPostsMap", meta.metadata,
                sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id')),
                sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('usertag.id')),
                )
            return UserTag.userTagsToPostsMappingTable
    """

class UserTagsPlugin(BasePlugin, AbstractPostingHook, AbstractProfileExtension, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('Personal tags module'),
                 }
        BasePlugin.__init__(self, 'usertags', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('userTagsMapper', '/postTags/:post/:act/:tagid', controller = 'usertags', action = 'postTags', act = 'show', tagid = 0, requirements = dict(post = '\d+', tagid = '\d+'))
        map.connect('userTagsManager', '/userProfile/manageUserTags/:act/:tagid', controller = 'usertags', action = 'postTagsManage', act = 'show', tagid = 0, requirements = dict(tagid = '\d+'))

    def initORM(self, orm, engine, dialectProps, propDict):
        namespace = self.namespace()
        t_usertags = sa.Table("usertag", meta.metadata,
            sa.Column("id"       , sa.types.Integer, primary_key = True),
            sa.Column('userId'  , sa.types.Integer, sa.ForeignKey('user.uidNumber')),
            sa.Column("tag"      , sa.types.Unicode(meta.dialectProps['tagLengthHardLimit']), nullable = False),
            sa.Column("comment"  , sa.types.UnicodeText, nullable = True),
            )

        t_userTagsToPostsMappingTable = sa.Table("usertagsToPostsMap", meta.metadata,
            sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id'), primary_key = True),
            sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('usertag.id'), primary_key = True),
            )

        sa.Index('ix_usertagmap_postid_tagid',
                 t_userTagsToPostsMappingTable.c.postId,
                 t_userTagsToPostsMappingTable.c.tagId,
                 unique = True)

        if not dialectProps.get('disableTextIndexing', None):
            sa.Index('ix_usertags_uidnum_tag',
                     t_usertags.c.userId,
                     t_usertags.c.tag,
                     unique = True)
        else:
            log.warning("Current SQL dialect doesn't support text indexing!")

        #orm.mapper
        meta.mapper(namespace.UserTag, t_usertags, properties = {
            'user' : orm.relation(User),
            'posts' : orm.relation(Post, secondary = t_userTagsToPostsMappingTable),
            })
    """
        def extendORMProperties(self, orm, engine, dialectProps, propDict):
            namespace = self.namespace()
            propDict['Post']['userTags'] = orm.relation(namespace.UserTag, secondary = namespace.UserTag.getMappingTable())
    """
    # Implementing AbstractPostingHook
    def tagCheckHandler(self, tagName, userInst):
        ns = self.namespace()
        name = tagName
        if name.startswith('$'):
            name = Tag.cutTag(tagName[1:], True)
        if not userInst.Anonymous:
            return ns.UserTag.get(name, userInst)
        else:
            return name != tagName

    def tagCreationHandler(self, tagstring, userInst, textFilter):
        afterPostCallbackParams = []
        #newTagString = tagstring
        from Orphereus.controllers.Orphie_Main import OrphieMainController
        ns = self.namespace()
        tags, dummy, nonexistent = Tag.stringToTagLists(tagstring, False)
        for usertag in nonexistent:
            if usertag.startswith('$'):
                nonexistent.remove(usertag)
                if not userInst.Anonymous:
                    tagName = Tag.cutTag(usertag[1:], True)
                    tag = ns.UserTag.get(tagName, userInst)
                    if not tag:
                        descr = OrphieMainController.getTagDescription(usertag, textFilter)
                        tag = ns.UserTag(tagName, descr, userInst.uidNumber)
                        meta.Session.add(tag)
                        meta.Session.commit()
                    afterPostCallbackParams.append(tag)
        newTagString = ''
        for tag in tags:
            newTagString += '%s ' % tag.tag
        newTagString += ' '.join(nonexistent)
        return (newTagString, afterPostCallbackParams)

    def afterPostCallback(self, post, userInst, params):
        if params:
            for tag in params:
                tag.addToThread(post)

    def tagHandler(self, tag, userInst):
        if tag.startswith('$'):
            ns = self.namespace()
            if not userInst.Anonymous:
                newName = tag[1:]
                tag = ns.UserTag.get(newName, userInst)
                if tag:
                    ids = []
                    for post in tag.posts:
                        ids.append(post.id)
                    #log.critical(ids)
                    if ids:
                        return Post.id.in_(ids), newName
                return None, newName
        return None, None

    # Implementing AbstractProfileExtension
    def additionalProfileLinks(self, userInst):
        links = []
        if not userInst.Anonymous:
            links = (('userTagsManager', {}, _('User tags')),)
            return links

    # AbstractPageHook
    def threadPanelCallback(self, thread, userInst):
        from webhelpers.html.tags import link_to
        if not userInst.Anonymous:
            return link_to(_("[My tags]"), h.url_for('userTagsMapper', post = thread.id), target = "_blank")
        return ''

    def threadInfoCallback(self, thread, userInst):
        ns = self.namespace()
        from webhelpers.html.tags import link_to
        result = ''
        if not userInst.Anonymous:
            tags = ns.UserTag.getPostTags(thread.id, userInst.uidNumber)
            result = " "
            for t in tags:
                result += ("%s ") % link_to("/$%s/" % t.tag, h.url_for('boardBase', board = '$' + t.tag), title = t.comment)
        return result

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import OrphieBaseController

class UsertagsController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def postTags(self, post, act, tagid):
        if self.userInst.Anonymous:
            return self.error(_("User tags allowed only for registered users"))
        c.boardName = _('User tags of thread')
        thread = Post.query.get(int(post))
        if thread:
            doRedir = False
            if act == 'delete':
                tag = UserTag.query.filter(and_(UserTag.id == int(tagid), UserTag.userId == self.userInst.uidNumber)).first()
                if tag:
                    if thread in tag.posts:
                        tag.posts.remove(thread)
                        meta.Session.commit()
                        doRedir = True
                    else:
                        return self.error(_("This tag isn't mapped to this post"))
                else:
                    return self.error(_("Incorrect tag id"))

            if act == 'add':
                tagName = filterText(request.params.get('tagName', ''))
                tag = UserTag.get(tagName, self.userInst)
                if not tag:
                    tag = UserTag.getById(tagid, self.userInst)
                if not tag:
                    return self.error(_("Tag doesn't exists"))
                if tag.addToThread(thread):
                    doRedir = True
                else:
                    return self.error(_("This tag already mapped to this post"))
            if doRedir:
                return redirect_to('userTagsMapper', post = thread.id)
            c.thread = thread
            c.userTags = UserTag.getPostTags(thread.id, self.userInst.uidNumber)
            c.allTags = UserTag.query.filter(UserTag.userId == self.userInst.uidNumber).all()
            return self.render('userTagsForPost')
        else:
            return self.error(_("Incorrect thread id"))

    def postTagsManage(self, act, tagid):
        if self.userInst.Anonymous:
            return self.error(_("User tags allowed only for registered users"))

        c.boardName = _('User tags management')
        doRedir = False
        tagDescr = filterText(request.params.get('tagDescr', ''))
        if act == 'add':
            tagName = filterText(request.params.get('tagName', ''))
            tag = UserTag.get(tagName, self.userInst)
            if tagName:
                if not tag:
                    tag = UserTag(tagName, tagDescr, self.userInst.uidNumber)
                    meta.Session.add(tag)
                    meta.Session.commit()
                    doRedir = True
                else:
                    return self.error(_("Tag already exists"))
        elif act in ['delete', 'removefromall', 'rename']:
            tag = UserTag.getById(tagid, self.userInst)
            if tag:
                if act == 'delete':
                    if not tag.posts:
                        meta.Session.delete(tag)
                        meta.Session.commit()
                        doRedir = True
                    else:
                        return self.error(_("Can't delete mapped tag"))
                elif act == 'removefromall':
                    tag.posts = []
                    meta.Session.commit()
                    doRedir = True
                elif act == 'rename':
                    tag.comment = tagDescr
                    meta.Session.commit()
                    doRedir = True
            else:
                return self.error(_("Incorrect tag id"))
        if doRedir:
            return redirect_to('userTagsManager')
        c.userTags = UserTag.query.filter(UserTag.userId == self.userInst.uidNumber).all()
        return self.render('userTags')
