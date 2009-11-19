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

import logging
from Orphereus.lib.base import *
from Orphereus.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from Orphereus.controllers.OrphieBaseController import OrphieBaseController
from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.userBan import UserBan
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook

log = logging.getLogger(__name__)

class AdminPanelPlugin(BasePlugin, AbstractMenuProvider, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('Administration panel'),
                 }
        BasePlugin.__init__(self, 'adminpanel', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('holySynod', '/holySynod', controller = 'administration/Orphie_Admin', action = 'index')
        map.connect('hsViewLogBase', '/holySynod/viewLog', controller = 'administration/Orphie_Admin', action = 'viewLog', page = 0)
        map.connect('hsViewLog', '/holySynod/viewLog/page/:page', controller = 'administration/Orphie_Admin', action = 'viewLog', requirements = dict(page = '\d+'))
        map.connect('hsInvite', '/holySynod/makeInvite', controller = 'administration/Orphie_Admin', action = 'makeInvite')
        map.connect('hsMappings', '/holySynod/manageMappings/:act/:id/:tagid', controller = 'administration/Orphie_Admin', action = 'manageMappings', act = 'show', id = 0, tagid = 0, requirements = dict(id = '\d+', tagid = '\d+'))
        map.connect('hsMergeTags', '/holySynod/mergeTags/:act', controller = 'administration/Orphie_Admin', action = 'mergeTags', act = None)
        map.connect('hsBans', '/holySynod/manageBans', controller = 'administration/Orphie_Admin', action = 'manageBans')
        map.connect('hsBanEdit', '/holySynod/manageBans/edit/:id', controller = 'administration/Orphie_Admin', id = 0, action = 'editBan')
        map.connect('hsExtensions', '/holySynod/manageExtensions', controller = 'administration/Orphie_Admin', action = 'manageExtensions')
        map.connect('hsExtensionEdit', '/holySynod/manageExtensions/edit/:name', controller = 'administration/Orphie_Admin', name = '', action = 'editExtension')
        map.connect('hsBoards', '/holySynod/manageBoards', controller = 'administration/Orphie_Admin', action = 'manageBoards')
        map.connect('hsBoardEdit', '/holySynod/manageBoards/edit/:tag', controller = 'administration/Orphie_Admin', tag = '', action = 'editBoard')
        map.connect('hsUsers', '/holySynod/manageUsers', controller = 'administration/Orphie_Admin', action = 'manageUsers')
        map.connect('hsUserEditAttempt', '/holySynod/manageUsers/editAttempt/:pid', controller = 'administration/Orphie_Admin', action = 'editUserAttempt', requirements = dict(pid = '\d+'))
        map.connect('hsIpBanAttempt', '/holySynod/manageUsers/banAttempt/:pid', controller = 'administration/Orphie_Admin', action = 'ipBanAttempt', requirements = dict(pid = '\d+'))
        map.connect('hsUserEditByPost', '/holySynod/manageUsers/editUserByPost/:pid', controller = 'administration/Orphie_Admin', action = 'editUserByPost', requirements = dict(pid = '\d+'))
        map.connect('hsUserEdit', '/holySynod/manageUsers/edit/:uid', controller = 'administration/Orphie_Admin', action = 'editUser', requirements = dict(uid = '\d+'))
        map.connect('hsPin', '/holySynod/pinThread/:act/:id', controller = 'administration/Orphie_Admin', action = 'pinThread', requirements = dict(id = '\d+'))
        map.connect('hsManageByIp', '/holySynod/manageByIp/:ip/:act', controller = 'administration/Orphie_Admin', action = 'manageByIp', act = 'show', requirements = dict(ip = '\d+'))

    def MenuItemIsVisible(self, id, baseController):
        user = baseController.userInst
        if id == 'id_hsSettings':
            return user.canChangeSettings()
        if id == 'id_hsBoards':
            return user.canManageBoards()
        if id == 'id_hsUsers':
            return user.canManageUsers()
        if id == 'id_hsBans':
            return user.canManageUsers()
        if id == 'id_hsExtensions':
            return user.canManageExtensions()
        if id == 'id_hsMappings':
            return user.canManageMappings()
        if id == 'id_hsMergeTags':
            return user.canManageMappings()
        if id == 'id_hsInvite':
            return user.canMakeInvite()
        if id == 'id_hsViewLogBase':
            return True
        return True

    def menuItems(self, menuId):
        #          id        link       name                weight   parent
        menu = None
        if menuId == "managementMenu":
            menu = (MenuItem('id_adminDashboard', _("Dashboard"), h.url_for('holySynod'), 200, False),
                    MenuItem('id_adminBoard', _("Common settings"), None, 200, False),
                    MenuItem('id_adminUsers', _("Users"), None, 210, False),
                    MenuItem('id_adminPosts', _("Threads and posts"), None, 220, False),
                    MenuItem('id_hsExtensions', _("Manage extensions"), h.url_for('hsExtensions'), 240, 'id_adminBoard'),
                    MenuItem('id_hsUsers', _("Manage users"), h.url_for('hsUsers'), 220, 'id_adminUsers'),
                    MenuItem('id_hsBans', _("Manage bans"), h.url_for('hsBans'), 230, 'id_adminUsers'),
                    MenuItem('id_hsInvite', _("Generate invite"), h.url_for('hsInvite'), 270, 'id_adminUsers'),
                    MenuItem('id_hsBoards', _("Manage boards"), h.url_for('hsBoards'), 210, 'id_adminPosts'),
                    MenuItem('id_hsMappings', _("Manage mappings"), h.url_for('hsMappings'), 250, 'id_adminPosts'),
                    MenuItem('id_hsMergeTags', _("Merge tags"), h.url_for('hsMergeTags'), 270, 'id_adminPosts'),
                    MenuItem('id_hsViewLogBase', _("View logs"), h.url_for('hsViewLogBase'), 260, False),
                    )
        return menu

    def postPanelCallback(self, thread, post, userInst):
        from webhelpers.html.tags import link_to
        result = ''
        if userInst.isAdmin() and userInst.canManageUsers():
            if post.uidNumber:
                result += link_to(_("[User]"), h.url_for('hsUserEditAttempt', pid = post.id))
            if post.ip:
                result += link_to(_("[IP Ban]"), h.url_for('hsIpBanAttempt', pid = post.id))
        return result

    def threadPanelCallback(self, thread, userInst):
        from webhelpers.html.tags import link_to
        result = self.postPanelCallback(thread, thread, userInst)
        """
            if userInst.isAdmin() and userInst.canManageUsers():
                if post.uidNumber:
                    result += link_to(_("[User]"), h.url_for('hsUserEditAttempt', pid = thread.id))
                if post.ip:
                    result += link_to(_("[IP Ban]"), h.url_for('hsIpBanAttempt', pid = thread.id))
        """
        if c.userInst.isAdmin() and c.userInst.canManageMappings():
            result += link_to(_("[Tags]"), h.url_for('hsMappings', act = 'show', id = thread.id))

        if c.userInst.isAdmin() and c.userInst.canManageMappings():
            if thread.pinned:
                result += link_to(_("[Unpin]"), h.url_for('hsPin', act = 'unpin', id = thread.id))
            else:
                result += link_to(_("[Pin]"), h.url_for('hsPin', act = 'pin', id = thread.id))
        return result

class OrphieAdminController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not self.userInst.isAdmin() or self.userInst.isBanned():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')
        self.requestForMenu("managementMenu")

    def index(self):
        c.boardName = _('Index')
        c.admins = User.getAdmins()
        c.currentItemId = 'id_adminDashboard'
        return self.render('managementIndex')

    def viewLog(self, page):
        c.boardName = _('Logs')
        c.currentItemId = 'id_hsViewLogBase'
        page = int(page)
        count = LogEntry.count()
        tpp = 50
        self.paginate(count, page, tpp)
        c.logs = LogEntry.getRange(page * tpp, (page + 1) * tpp)
        return self.render('managementLogs')

    def invitePage(self):
        if not self.userInst.canMakeInvite():
            return self.error(_("No way! You aren't holy enough!"))

        c.boardName = _('Invites')
        c.currentItemId = 'id_hsInvite'

        return self.render('invitePage')

    def makeInvite(self):
        if not self.userInst.canMakeInvite():
            return self.error(_("No way! You aren't holy enough!"))

        c.boardName = _('Invite creation')
        c.currentItemId = 'id_hsInvite'
        c.inviteCode = False
        reason = request.POST.get('inviteReason', False)
        if reason and len(reason) > 1:
            reason = filterText(reason)
            invite = Invite.create(g.OPT.hashSecret)

            toLog(LOG_EVENT_INVITE, _("Generated invite id %s. Reason: %s") % (invite.id, reason))
            c.inviteCode = invite.invite
        return self.render('manageInvites')

    def manageBans(self):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.boardName = _('Bans management')
        c.currentItemId = 'id_hsBans'

        c.bans = Ban.getBans()
        #c.userBans = map(lambda u: UserBan(u.uidNumber), User.getBanned())
        c.userBans = list([UserBan(u.uidNumber) for u in User.getBanned()])
        return self.render('manageBans')

    def editBan(self, id):

        def getPostData():
            try:
                ip = h.ipToInt(filterText(request.POST.get('ip', 0)))
                mask = h.ipToInt(filterText(request.POST.get('mask', 0)))
            except:
                return self.error(_("Please check the format of IP addresses and masks."))
            type = bool(request.POST.get('type', False))
            enabled = bool(request.POST.get('enabled', False))
            reason = filterText(unicode(request.POST.get('reason', '')))
            date = request.POST.get('date', 0)
            period = request.POST.get('period', 0)
            return ip, mask, type, reason, date, period, enabled


        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.boardName = _('Editing ban %s') % id
        c.currentItemId = 'id_hsBans'

        if c.ShowAttemptForm:
            c.boardName = _('New IP ban')
            return self.render('manageBan')

        id = request.POST.get('id', id)

        c.exists = True
        ban = Ban.getBanById(id)

        if not ban:
            c.exists = False
            c.boardName = _('New IP ban')
            ip = c.ipToBan or 0
            # TODO: FIXME: VERY BAD CODE.
            # You should NOT create temporary object.
            # For example, if autocommit == True, this will break database integrity
            # Empty() is temporary solution
            c.ban = empty()
            c.ban.id = 0
            c.ban.ip = ip
            c.ban.mask = h.ipToInt('255.255.255.255')
            c.ban.type = 0   # 0 for read-only access, 1 for full ban
            c.ban.reason = ''
            c.ban.date = datetime.datetime.now()
            c.ban.period = 30
            c.ban.enabled = True
        else:
            c.ban = ban

        postedId = request.POST.get('id', None)
        if (postedId):
            if (int(postedId) > 0):
                if not bool(request.POST.get('delete', False)):
                    ban = Ban.getBanById(id)
                    if ban:
                        ban.setData(*getPostData())
                    else:
                        self.error(_("This ban doesn't exist."))
                    toLog(LOG_EVENT_BAN_EDIT, _("Updated ban no. %s") % ban.id)
                    c.exists = True
                    c.message = _('Ban properties were updated')
                    return self.manageBans()
                elif ban:
                    banId = ban.id
                    if ban.delete():
                        toLog(LOG_EVENT_BAN_REMOVE, _('Deleted ban %s') % banId)
                        c.message = _('Ban record no. %s deleted' % banId)
                        return self.manageBans()
            elif (int(postedId) == 0):
                c.ban = Ban(ip, h.ipToInt('255.255.255.255'), 0, '', datetime.datetime.now(), 30, True)
                c.ban.setData(*getPostData())
                meta.Session.add(c.ban)
                meta.Session.commit()
                toLog(LOG_EVENT_BAN_ADD, _('Added ban no. %s. Reason: %s') % (c.ban.id, c.ban.reason))
                c.message = _('Added ban no. %s') % c.ban.id
                return redirect_to('hsBans')
        return self.render('manageBan')

    def manageExtensions(self):
        if not self.userInst.canManageExtensions():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsExtensions'
        c.boardName = _('Extensions management')
        c.extensions = Extension.getList(False)
        c.showCount = bool(request.POST.get('showCount', False))
        return self.render('manageExtensions')

    def editExtension(self, name):
        if not self.userInst.canManageExtensions():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsExtensions'
        c.boardName = _('Editing extension %s') % name
        if not name:
            name = ''

        name = filterText(request.POST.get('ext', name))
        if len(name) > 10:
            return self.error(_('Too long extension'))

        c.exists = True
        ext = Extension.getExtension(name)

        if not ext:
            c.exists = False
            c.ext = empty()
            c.ext.ext = name
            c.ext.path = ''
            c.ext.thwidth = 0
            c.ext.thheight = 0
            c.ext.type = 'image'
            c.ext.enabled = True
            c.ext.newWindow = True
        else:
            c.ext = ext

        name = request.POST.get('ext', False)
        if name:
            if not bool(request.POST.get('delete', False)):
                path = filterText(request.POST.get('path', ''))
                enabled = bool(request.POST.get('enabled', False))
                newWindow = bool(request.POST.get('newWindow', False))
                type = filterText(request.POST.get('type', 'image')).strip().lower()
                thwidth = request.POST.get('thwidth', 0)
                thheight = request.POST.get('thheight', 0)
                if not ext:
                    ext = Extension.create(name, enabled, newWindow, type, path, thwidth, thheight)
                    toLog(LOG_EVENT_EXTENSION_EDIT, _('Created extension %s') % ext.ext)
                    c.exists = True
                    c.message = _('Extension created')
                else:
                    ext.setData(enabled, newWindow, type, path, thwidth, thheight)
                    toLog(LOG_EVENT_EXTENSION_EDIT, _('Edited extension %s') % ext.ext)
                    c.message = _('Extension edited')
            elif ext:
                extName = ext.ext
                if ext.delete():
                    toLog(LOG_EVENT_EXTENSION_EDIT, _('Deleted extension %s') % extName)
                    c.message = _('Extension deleted')
                    c.exists = False
                else:
                    c.message = _("Can't delete extension. Uploaded files with this extension exists.")
        del g.caches['extensions']
        return self.render('manageExtension')

    def pinThread(self, act, id):
        if not self.userInst.canManageMappings():
            return self.error(_("No way! You aren't holy enough!"))

        c.boardName = _('Pin thread')
        if isNumber(id):
            id = int(id)
            post = Post.getPost(id)
            if post:
                if act == 'pin':
                    post.pinned = True
                else:
                    post.pinned = None
                meta.Session.commit()
                c.message = _('Post %d is %s now') % (id, post.pinned and "pinned" or "not pinned")
                return self.render('managementMessage')

        return self.error(_("Incorrect thread number"))

    def mergeTags(self, act):
        if not self.userInst.canManageMappings():
            return self.error(_("No way! You aren't holy enough!"))

        badTags = Tag.getAllByThreadCount(1)
        badTagList = []
        for tag in badTags:
            badTagList.append(tag.tag)
        c.proposedTags = ','.join(badTagList)
        if act == 'merge':
            source = filterText(request.POST.get('sourceTags', '')).strip()
            target = filterText(request.POST.get('targetTag', '')).strip()
            if source:
                targetTag = Tag.getTag(target)
                source = source.split(',')
                sourceTags = Tag.getAllByNames(source)
                if targetTag and sourceTags:
                    if not targetTag in sourceTags:
                        def tagsToStr(tags):
                            taglist = []
                            for tag in post.tags:
                                taglist.append(unicode(tag))
                            return '; '.join(taglist)
                        c.result = []
                        for tag in sourceTags:
                            posts = Post.filter(and_(Post.parentid == None, Post.tags.any(Tag.id == tag.id))).all()
                            for post in posts:
                                tmp = [post.id, tagsToStr(post.tags)]
                                post.removeTag(tag)
                                """
                                    tags = post.tags
                                    tags.remove(tag)
                                    tag.threadCount -= 1
                                    tag.replyCount -= (post.replyCount + 1)
                                    if not targetTag in tags:
                                        tags.append(targetTag)
                                        targetTag.threadCount += 1
                                        targetTag.replyCount += (post.replyCount + 1)
                                """
                                post.appendTag(targetTag)
                                tmp.append(tagsToStr(post.tags))
                                options = Tag.conjunctedOptionsDescript(post.tags)
                                if not Tag.tagsInConflict(options, None):
                                    tmp.append(_('Accepted'))
                                else:
                                    tmp.append(_("Declined: unacceptable combination of tags"))
                                c.result.append(tmp)
                        meta.Session.commit()
                    else:
                        return self.error(_("Source tags contains target tag"))
                else:
                    return self.error(_("Incorrect source or target"))
        c.currentItemId = 'id_hsMergeTags'
        c.boardName = _('Merge tags')
        return self.render('mergeTags')

    def manageMappings(self, act, id, tagid):
        if not self.userInst.canManageMappings():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsMappings'
        c.boardName = _('Manage mappings')

        #log.debug("%s\n\n%s\nact:%s" %(c,request.POST,act))

        if isNumber(id) and isNumber(tagid):
            id = int(id)
            tagid = int(tagid)

            if id == 0:
                id = filterText(request.POST.get('postId', ''))
                if id and isNumber(id):
                    id = int(id)

            if tagid == 0:
                tagName = filterText(request.POST.get('tagName', u''))
                if tagName:
                    tag = Tag.getTag(tagName)
                    if tag:
                        tagid = tag.id
        else:
            return self.error(_("Incorrect input values"))

        if act == 'show':
            if id and id > 0:
                post = Post.getPost(id)
                if post and not post.parentid:
                    c.post = post
                else:
                    return self.error(_("This is not op-post"))

            return self.render('manageMappings')
        elif act in ['del', 'add']:
            post = Post.getPost(id)
            if post and not post.parentid:
                if act == 'del' and tagid > 0:
                    if len(post.tags) > 1:
                        tag = Tag.getById(tagid)
                        #tag.threadCount -= 1
                        #tag.replyCount -= (post.replyCount + 1)
                        #post.tags.remove(tag)
                        post.removeTag(tag)
                        toLog(LOG_EVENT_EDITEDPOST, _('Removed tag %s from post %d') % (tag.tag, post.id))
                    else:
                        return self.error(_("Can't delete last tag!"))
                elif act == 'add':
                    tag = Tag.getById(tagid)
                    if tag:
                        toLog(LOG_EVENT_EDITEDPOST, _('Added tag %s to post %d') % (tag.tag, post.id))
                        post.appendTag(tag)
                        #post.tags.append(tag)
                        #tag.threadCount += 1
                        #tag.replyCount += (post.replyCount + 1)
                    else:
                        return self.error(_("Non-existent tag"))

                meta.Session.commit()

            redirect_to('hsMappings', act = 'show', id = id)
            # return self.render('manageMappings')
        else:
            redirect_to('hsMappings')

    def manageBoards(self):
        if not self.userInst.canManageBoards():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsBoards'
        c.boardName = _('Boards management')
        boards = Tag.getAll()
        c.boards = {-1:[]}
        c.sectionList = []
        for b in boards:
            if b.persistent and b.sectionId >= 0:
                sid = b.sectionId
                if not sid in c.boards:
                    c.boards[sid] = []
                    c.sectionList.append(sid)
                c.boards[sid].append(b)
            else:
                c.boards[-1].append(b)

        for sid in c.boards.keys():
            c.boards[sid] = sorted(c.boards[sid], lambda a, b: cmp(a.tag, b.tag))
        c.sectionList = sorted(c.sectionList)
        c.sectionList.append(-1)
        return self.render('manageBoards')

    def editBoard(self, tag):
        if not self.userInst.canManageBoards():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsBoards'
        c.boardName = _('Edit board')
        c.message = u''
        c.tag = Tag.getTag(tag)
        if not c.tag:
            c.tag = Tag(tag)

        #TODO: legacy code
        #if not c.tag.options:
        #    c.tag.options = TagOptions()

        if request.POST.get('tag', False):
            newtag = request.POST.get('tag', False)
            newtagre = re.compile(r"""([^,@~\#\+\-\&\s\/\\\(\)<>'"%\d][^,@~\#\+\-\&\s\/\\\(\)<>'"%]*)""").match(newtag)
            if newtagre:
                newtag = newtagre.groups()[0]
                newtagRecord = Tag.getTag(newtag)
                if not newtagRecord or newtagRecord.id == c.tag.id:
                    if c.tag.tag != newtag:
                        oldtag = c.tag.tag
                        c.tag.tag = newtag
                    else:
                        oldtag = u''
                    c.tag.comment = filterText(request.POST.get('comment', u''))
                    c.tag.specialRules = filterText(request.POST.get('specialRules', u''))
                    sid = request.POST.get('sectionId', 0)
                    if isNumber(sid) and int(sid) >= 0:
                        sid = int(sid)
                    else:
                        sid = 0
                    c.tag.sectionId = sid
                    c.tag.persistent = bool(request.POST.get('persistent', False))
                    c.tag.service = bool(request.POST.get('service', False))
                    c.tag.imagelessThread = bool(request.POST.get('imagelessThread', False))
                    c.tag.imagelessPost = bool(request.POST.get('imagelessPost', False))
                    c.tag.images = bool(request.POST.get('images', False))
                    c.tag.enableSpoilers = bool(request.POST.get('spoilers', False))
                    c.tag.canDeleteOwnThreads = bool(request.POST.get('canDeleteOwnThreads', False))
                    c.tag.selfModeration = bool(request.POST.get('selfModeration', False))
                    c.tag.showInOverview = bool(request.POST.get('showInOverview', False))
                    c.tag.adminOnly = bool(request.POST.get('adminOnly', False))
                    c.tag.maxFileSize = request.POST.get('maxFileSize', g.OPT.defMaxFileSize)
                    c.tag.minPicSize = request.POST.get('minPicSize', g.OPT.defMinPicSize)
                    c.tag.thumbSize = request.POST.get('thumbSize', g.OPT.defThumbSize)
                    allowedFilesCount = request.POST.get('allowedAdditionalFiles', g.OPT.allowedAdditionalFiles)
                    c.tag.allowedAdditionalFiles = isNumber(allowedFilesCount) and int(allowedFilesCount) or None
                    bumplimit = request.POST.get('bumplimit', g.OPT.defBumplimit)
                    if not isNumber(bumplimit) or int(bumplimit) == 0:
                        bumplimit = None
                    c.tag.bumplimit = bumplimit
                    c.tag.save()
                    if bool(request.POST.get('deleteBoard', False)) and c.tag.id:
                        count = c.tag.getExactThreadCount()
                        if count > 0:
                            c.message = _("Board must be empty for deletion")
                        else:
                            meta.Session.delete(c.tag)
                            toLog(LOG_EVENT_BOARD_EDIT, _("Deleted board %s %s") % (newtag, oldtag and ("(that was renamed from %s)" % oldtag) or ""))
                            meta.Session.commit()
                            return redirect_to('hsBoards')
                    elif not c.tag.id:
                        meta.Session.add(c.tag)

                    c.message = _("Updated board")
                    toLog(LOG_EVENT_BOARD_EDIT, _("Edited board %s %s") % (newtag, oldtag and ("(renamed from %s)" % oldtag) or ""))
                    meta.Session.commit()

                else:
                    c.message = _("Board %s already exists!") % newtag
            else:
                c.message = _("Board name should be non-empty and should contain only valid symbols")
        del g.caches['boardlist']
        return self.render('manageBoard')

    def manageUsers(self):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsUsers'
        c.boardName = _('Users management')
        uid = request.POST.get("uid", False)
        if uid:
            user = False
            if isNumber(uid):
                user = User.getUser(uid)
            else:
                user = User.getByUid(uid)
            if user:
                return redirect_to('hsUserEdit', uid = user.uidNumber)
            else:
                c.message = _('No such user exists.')
        return self.render('manageUsers')

    def editUserAttempt(self, pid):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsUsers'
        c.boardName = _('User edit attemption')
        c.pid = pid
        c.showAttemptForm = True
        return self.render('manageUser')

    def ipBanAttempt(self, pid):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        # TODO: perform reason request
        post = Post.getPost(pid)
        c.pid = pid
        c.ipToBan = post.ip

        IpViewReason = request.POST.get('IpViewReason', None)
        c.showAttemptForm = not(bool(IpViewReason))
        if bool(IpViewReason):
            toLog(LOG_EVENT_USER_GETUID, _("Viewed IP for post '%s'. Reason: %s") % (post.id, IpViewReason))

        return self.editBan(-1)

    def manageByIp(self, ip, act):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsManageByIp'
        c.boardName = _('IP-based moderation')

        c.act = act
        c.ip = ip
        allFilter = Post.filter(Post.ip == ip)
        unregFilter = Post.filter(and_(Post.ip == ip, not_(Post.uidNumber > 0)))
        c.postsCount = allFilter.count()
        if not c.postsCount:
            return self.error(_("No posts are associated with this IP"))

        c.firstPost = allFilter.first() # TODO: it's hack for bad IP ban logic
        c.unregPostsCount = unregFilter.count()
        if act == 'showAll':
            c.postsList = allFilter.all()
        elif act == 'showUnreg':
            c.postsList = unregFilter.all()
        if 'removeAll' in request.POST:
            reason = filterText(request.POST.get('deletereason', u'No reason given'))
            threads = []
            replies = []
            for post in c.postsList:
                if post.parentid:
                    replies.append(post)
                else:
                    threads.append(post)
            for post in replies + threads:
                post.deletePost(self.userInst, False, True, reason)
            return redirect_to('hsManageByIp', ip = post.ip, act = act)
        return self.render('manageByIp')

    def editUserByPost(self, pid):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsUsers'
        c.boardName = _('User management')

        post = Post.getPost(pid)
        if post:
            reason = request.POST.get("UIDViewReason", _('No reason given!'))
            #toLog(LOG_EVENT_USER_GETUID, "Viewed UID for user '%s' from post '<a href='/%s#i%s'>%s</a>'. Reason: %s" % (post.uidNumber, post.parentid > 0 and post.parentid or post.id, pid, pid, reason))
            toLog(LOG_EVENT_USER_GETUID, _("Viewed UID for user '%s' from post '%s'. Reason: %s") % (post.uidNumber, post.id, reason))
            if post.uidNumber == -1:
                if not post.ip:
                    return self.error(_("This post is created by a non-registered user whose IP wasn't saved"))
                else:
                    return redirect_to('hsManageByIp', ip = post.ip)
            elif not post.uidNumber:
                return self.error(_("This post is anonymized"))
            return redirect_to('hsUserEdit', uid = post.uidNumber)
        else:
            return self.error(_("Post not found"))

    def editUser(self, uid):
        if not self.userInst.canManageUsers():
            return self.error(_("No way! You aren't holy enough!"))

        c.currentItemId = 'id_hsUsers'
        c.boardName = 'Editing user %s' % uid
        user = User.getUser(uid, False)
        if user:
            if user.uidNumber <= 0:
                return self.error("Can't edit internal users!")

            c.user = user
            c.userInst = self.userInst
            if bool(request.POST.get('access', False)) and self.userInst.canChangeRights():
                #Basic admin right
                isAdmin = bool(request.POST.get('isAdmin', False))
                if user.options.isAdmin != isAdmin:
                    user.options.isAdmin = isAdmin
                    toLog(LOG_EVENT_USER_ACCESS, _('Changed user %s isAdmin to %s') % (user.uidNumber, isAdmin))

                def setRight(name):
                    right = bool(request.POST.get(name, False))
                    if getattr(user.options, name) != right:
                        setattr(user.options, name, right)
                        toLog(LOG_EVENT_USER_ACCESS, _('Changed right "%s" for user #%s to %s') % (name, user.uidNumber, right))

                map(setRight, ["canDeleteAllPosts", "canMakeInvite", "canChangeRights", "canChangeSettings",
                                 "canManageBoards", "canManageUsers", "canManageExtensions", "canManageMappings",
                                 "canRunMaintenance"])
                c.message = _('User access was changed')
            elif bool(request.POST.get('ban', False)):
                if user.options.bantime > 0:
                    c.message = _('This user is already banned')
                else:
                    banreason = filterText(request.POST.get('banreason', '???'))
                    bantime = request.POST.get('bantime', '0')
                    c.message = user.ban(bantime, banreason, self.userInst.uidNumber)
            elif bool(request.POST.get('unban', False)):
                if user.options.bantime > 0:
                    banreason = user.options.banreason
                    bantime = user.options.bantime
                    user.options.bantime = 0
                    user.options.banreason = u''
                    toLog(LOG_EVENT_USER_UNBAN, _('Unbanned user %s (%s days for reason "%s")') % (user.uidNumber, bantime, banreason))
                    c.message = _('User was unbanned')
                else:
                    c.message = _('This user is not banned')
            elif bool(request.POST.get('lookup', False)):
                reason = filterText(request.POST.get('lookupreason', u''))
                quantity = int(request.POST.get('quantity', '0'))
                if isNumber(quantity) and int(quantity) > 0:
                    if len(reason) > 1:
                        c.posts = Post.filterByUid(user.uidNumber).order_by(Post.date.desc())[:quantity]
                        toLog(LOG_EVENT_USER_DELETE, _('Performed posts lookup for user %s for "%s", quantity: %s') % (user.uidNumber, reason, quantity))
                        if c.posts:
                            return self.render('postsLookup')
                        else:
                            c.message = _('No posts found')
                    else:
                        c.message = _('You should specify lookup reason')
                else:
                    c.message = _('Incorrect quantity value')
            elif bool(request.POST.get('passwd', False)):
                key = request.POST.get('key', '').encode('utf-8')
                key2 = request.POST.get('key2', '').encode('utf-8')
                passwdRet = user.passwd(key, key2, True, False)
                if passwdRet == True:
                    c.message = _('Password was successfully changed.')
                    toLog(LOG_EVENT_USER_PASSWD, _('Changed password for user "%s"') % (user.uidNumber))
                    c.message = _('Security code changed')
                elif passwdRet == False:
                    c.message = _('Incorrect security codes')
                else:
                    return self.error(passwdRet)
            elif bool(request.POST.get('delete', False)):
                reason = filterText(request.POST.get('deletereason', u'No reason given'))
                deleteLegacy = bool(request.POST.get('deleteLegacy', False))
                if self.userInst.canChangeRights():
                    if len(reason) > 1:
                        if deleteLegacy:
                            posts = Post.filterByUid(user.uidNumber).all()
                            removed = []

                            threads = []
                            replies = []
                            for post in posts:
                                if post.parentid:
                                    replies.append(post)
                                else:
                                    threads.append(post)
                            posts = replies + threads

                            for post in posts:
                                if not post.parentid:
                                    removed.append(str(post.id))
                                else:
                                    removed.append("%d/%d" % (post.id, post.parentid))
                                post.deletePost(self.userInst, False, False, reason)
                            toLog(LOG_EVENT_USER_DELETE, _('Removed legacy of %s for "%s" [%s]') % (user.uidNumber, reason, ', '.join(removed)))
                        meta.Session.delete(user)
                        toLog(LOG_EVENT_USER_DELETE, _('Deleted user %s for "%s"') % (user.uidNumber, reason))
                        c.message = _("User deleted")
                        return self.render('manageUsers')
                    else:
                        c.message = _('You should specify deletion reason')
                else:
                    c.message = _("You haven't rights to delete user")
            if g.OPT.memcachedUsers and request.POST:
                g.mc.delete('u%s' % user.uidNumber)
            return self.render('manageUser')
        else:
            return self.error(_('No such user exists.'))

