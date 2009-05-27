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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #                                                                         #
################################################################################

import logging
from fc.lib.base import *
from fc.model import *
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
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class FcaController(OrphieBaseController):
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

    def index(self):
        c.boardName = _('Index')
        c.admins = User.getAdmins()
        return self.render('managementIndex')

    def manageSettings(self):
        c.boardName = _('Settings management')
        c.settingsDescription = settingsDescription

        if request.POST.get('update', False):
            if not self.userInst.canChangeSettings():
                c.errorText = _("No way! You aren't holy enough!")
                return self.render('error')

            for s in request.POST:
                if s in settingsDef:
                    val = filterText(request.POST[s])
                    if settingsDescription[s][1] == int and not isNumber(val):
                        c.errorText = _("'%s' isn't correct number, but '%s' must be an integer number.") % (val, s)
                        return self.render('error')
                    if settingsDescription[s][1] == list:
                        valarr = filter(lambda l: l, re.split('\r+|\n+|\r+\n+', val))
                        val = '|'.join(valarr)
                    if g.settingsMap[s].value != val:
                        toLog(LOG_EVENT_SETTINGS_EDIT, _("Changed %s from '%s' to '%s'") % (s, g.settingsMap[s].value, val))
                        Setting.getSetting(s).setValue(val)
                        g.settingsMap[s].value = val
                    init_globals(config['pylons.app_globals'], False)
            c.message = _('Settings updated')
        return self.render('manageSettings')

    def viewLog(self, page):
        c.boardName = _('Logs')
        page = int(page)
        count = LogEntry.count()
        tpp = 50
        self.paginate(count, page, tpp)
        c.logs = LogEntry.getRange(page * tpp, (page + 1) * tpp)
        return self.render('managementLogs')

    def invitePage(self):
        if not self.userInst.canMakeInvite():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Invites')

        return self.render('invitePage')

    def makeInvite(self):
        if not self.userInst.canMakeInvite():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Invite creation')
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
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Bans management')

        c.bans = Ban.getBans()
        #c.showCount = request.POST.get('showCount', False)
        #log.debug('rendering list, msg=%s' %c.message)
        return self.render('manageBans')

    def editBan(self, id):
        #log.debug('ban')
        if not self.userInst.canManageUsers():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Editing ban %s') % id
        id = request.POST.get('id', id)

        c.exists = True
        ban = Ban.getBanById(id)

        if not ban:
            c.exists = False
            c.boardName = _('New IP ban')
            ip = c.ipToBan or 0
            c.ban = Ban.create(ip, h.dottedToInt('255.255.255.255'), 0, '', datetime.datetime.now(), 30, True)
            #log.debug('Made obj: %s, id: %s' %(c.ban,c.ban.id))
            toLog(LOG_EVENT_BAN_ADD, _('Added ban no. %s') % c.ban.id)
        else:
            c.ban = ban

        postedId = request.POST.get('id', -1)
        if (postedId > -1):
            if not request.POST.get('delete', False):
                try:
                    ip = h.dottedToInt(filterText(request.POST.get('ip', 0)))
                    mask = h.dottedToInt(filterText(request.POST.get('mask', 0)))
                except:
                    c.errorText = _("Please check the format of IP addresses and masks.")
                    return self.render('error')

                type = request.POST.get('type', False) == 'on'
                enabled = request.POST.get('enabled', False) == 'on'
                reason = filterText(request.POST.get('reason', ''))
                date = request.POST.get('date', 0)
                period = request.POST.get('period', 0)

                ban = Ban.getBanById(id)
                if ban:
                    ban.setData(ip, mask, type, reason, date, period, enabled)
                toLog(LOG_EVENT_BAN_EDIT, _('Updated ban no. %s, reason: %s') % (ban.id, ban.reason))
                c.exists = True
                c.message = _('Ban properties were updated')
                return self.manageBans()
            elif ban:
                banId = ban.id
                if ban.delete():
                    toLog(LOG_EVENT_BAN_REMOVE, _('Deleted ban %s') % banId)
                    c.message = _('Ban record no. %s deleted' % banId)
                    return self.manageBans()
        return self.render('manageBan')

    def manageExtensions(self):
        if not self.userInst.canManageExtensions():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Extensions management')
        c.extensions = Extension.getList(False)
        c.showCount = request.POST.get('showCount', False)
        return self.render('manageExtensions')

    def editExtension(self, name):
        if not self.userInst.canManageExtensions():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Editing extension %s') % name
        if not name:
            name = ''

        name = filterText(request.POST.get('ext', name))
        if len(name) > 10:
            c.errorText = _('Too long extension')
            return self.render('error')

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
            if not request.POST.get('delete', False):
                path = filterText(request.POST.get('path', ''))
                enabled = request.POST.get('enabled', False)
                newWindow = request.POST.get('newWindow', False)
                type = filterText(request.POST.get('type', 'image'))
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
        return self.render('manageExtension')

    def manageMappings(self, act, id, tagid):
        if not self.userInst.canManageMappings():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

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
            c.errorText = _("Incorrect input values")
            return self.render('error')

        if act == 'show':
            if id and id > 0:
                post = Post.getPost(id)
                if post and not post.parentid:
                    c.post = post
                else:
                    c.errorText = _("This is not op-post")
                    return self.render('error')

            return self.render('manageMappings')
        elif act in ['del', 'add']:
            post = Post.getPost(id)
            if post and not post.parentid:
                if act == 'del' and tagid > 0:
                    if len(post.tags) > 1:
                        tag = Tag.getById(tagid)
                        tag.threadCount -= 1
                        tag.replyCount -= post.replyCount
                        toLog(LOG_EVENT_EDITEDPOST, _('Removed tag %s from post %d') % (tag.tag, post.id))
                        post.tags.remove(tag)
                    else:
                        c.errorText = _("Can't delete last tag!")
                        return self.render('error')
                elif act == 'add':
                    tag = Tag.getById(tagid)
                    if tag:
                        toLog(LOG_EVENT_EDITEDPOST, _('Added tag %s to post %d') % (tag.tag, post.id))
                        post.tags.append(tag)
                        tag.threadCount += 1
                        tag.replyCount += post.replyCount
                    else:
                        c.errorText = _("Non-existent tag")
                        return self.render('error')

                meta.Session.commit()

            redirect_to('hsMappings', act = 'show', id = id)
           # return self.render('manageMappings')
        else:
            redirect_to('hsMappings')

    def manageBoards(self):
        if not self.userInst.canManageBoards():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('Boards management')
        boards = Tag.getAll()
        c.boards = {-1:[]}
        c.sectionList = []
        for b in boards:
            if b.options and b.options.persistent and b.options.sectionId >= 0:
                sid = b.options.sectionId
                if not sid in c.boards:
                    c.boards[sid] = []
                    c.sectionList.append(sid)
                c.boards[sid].append(b)
            else:
                c.boards[-1].append(b)

        for sid in c.boards.keys():
            def tagcmp(a, b):
                return cmp(a.tag, b.tag)
            c.boards[sid] = sorted(c.boards[sid], tagcmp)
        c.sectionList = sorted(c.sectionList)
        c.sectionList.append(-1)
        return self.render('manageBoards')

    def editBoard(self, tag):
        if not self.userInst.canManageBoards():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')
        c.boardName = _('Edit board')
        c.message = u''
        c.tag = Tag.getTag(tag)
        if not c.tag:
            c.tag = Tag(tag)

        #TODO: legacy code
        if not c.tag.options:
            c.tag.options = TagOptions()

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
                    c.tag.options.comment = filterText(request.POST.get('comment', u''))
                    c.tag.options.specialRules = filterText(request.POST.get('specialRules', u''))
                    sid = request.POST.get('sectionId', 0)
                    if isNumber(sid) and int(sid) >= 0:
                        sid = int(sid)
                    else:
                        sid = 0
                    c.tag.options.sectionId = sid
                    c.tag.options.persistent = request.POST.get('persistent', False)
                    c.tag.options.service = request.POST.get('service', False)
                    c.tag.options.imagelessThread = request.POST.get('imagelessThread', False)
                    c.tag.options.imagelessPost = request.POST.get('imagelessPost', False)
                    c.tag.options.images = request.POST.get('images', False)
                    c.tag.options.enableSpoilers = request.POST.get('spoilers', False)
                    c.tag.options.canDeleteOwnThreads = request.POST.get('canDeleteOwnThreads', False)
                    c.tag.options.selfModeration = request.POST.get('selfModeration', False)
                    c.tag.options.maxFileSize = request.POST.get('maxFileSize', g.OPT.defMaxFileSize)
                    c.tag.options.minPicSize = request.POST.get('minPicSize', g.OPT.defMinPicSize)
                    c.tag.options.thumbSize = request.POST.get('thumbSize', g.OPT.defThumbSize)
                    c.tag.save()
                    if request.POST.get('deleteBoard', False) and c.tag.id:
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
        return self.render('manageBoard')

    def manageUsers(self):
        if not self.userInst.canManageUsers():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

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
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('User edit attemption')
        c.pid = pid
        c.showAttemptForm = True
        return self.render('manageUser')

    def ipBanAttempt(self, pid):
        if not self.userInst.canManageUsers():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        # TODO: perform reason request
        post = Post.getPost(pid)
        c.ipToBan = post.ip
        return self.editBan(-1)

    def editUserByPost(self, pid):
        if not self.userInst.canManageUsers():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = _('User management')

        post = Post.getPost(pid)
        if post:
            reason = request.POST.get("UIDViewReason", _('No reason given!'))
            #toLog(LOG_EVENT_USER_GETUID, "Viewed UID for user '%s' from post '<a href='/%s#i%s'>%s</a>'. Reason: %s" % (post.uidNumber, post.parentid > 0 and post.parentid or post.id, pid, pid, reason))
            toLog(LOG_EVENT_USER_GETUID, _("Viewed UID for user '%s' from post '%s'. Reason: %s") % (post.uidNumber, post.id, reason))
            return redirect_to('hsUserEdit', uid = post.uidNumber)
        else:
            c.errorText = _("Post not found")
            return self.render('error')

    def editUser(self, uid):
        if not self.userInst.canManageUsers():
            c.errorText = _("No way! You aren't holy enough!")
            return self.render('error')

        c.boardName = 'Edit user %s' % uid
        user = User.getUser(uid) #meta.Session.query(User).options(eagerload('options')).get(uid)
        if user:
            c.user = user
            c.userInst = self.userInst
            if request.POST.get('access', False) and self.userInst.canChangeRights():
                #Basic admin right
                isAdmin = request.POST.get('isAdmin', False) and True or False
                if user.options.isAdmin != isAdmin:
                    user.options.isAdmin = isAdmin
                    toLog(LOG_EVENT_USER_ACCESS, _('Changed user %s isAdmin to %s') % (user.uidNumber, isAdmin))

                def setRight(name):
                    right = request.POST.get(name, False) and True or False
                    if getattr(user.options, name) != right:
                        setattr(user.options, name, right)
                        toLog(LOG_EVENT_USER_ACCESS, _('Changed right "%s" for user #%s to %s') % (name, user.uidNumber, right))

                setRight("canDeleteAllPosts")
                setRight("canMakeInvite")
                setRight("canChangeRights")
                setRight("canChangeSettings")
                setRight("canManageBoards")
                setRight("canManageUsers")
                setRight("canManageExtensions")
                setRight("canManageMappings")
                setRight("canRunMaintenance")
                c.message = _('User access was changed')
            elif request.POST.get('ban', False):
                if user.options.bantime > 0:
                    c.message = _('This user is already banned')
                else:
                    banreason = filterText(request.POST.get('banreason', '???'))
                    bantime = request.POST.get('bantime', '0')
                    c.message = user.ban(bantime, banreason, self.userInst.uidNumber)
            elif request.POST.get('unban', False):
                if user.options.bantime > 0:
                    banreason = user.options.banreason
                    bantime = user.options.bantime
                    user.options.bantime = 0
                    user.options.banreason = u''
                    toLog(LOG_EVENT_USER_UNBAN, _('Unbanned user %s (%s days for reason "%s")') % (user.uidNumber, bantime, banreason))
                    c.message = _('User was unbanned')
                else:
                    c.message = _('This user is not banned')
            elif request.POST.get('lookup', False):
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
            elif request.POST.get('passwd', False):
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
                    c.boardName = _('Error')
                    c.errorText = passwdRet
                    return self.render('error')
            elif request.POST.get('delete', False):
                reason = filterText(request.POST.get('deletereason', u''))
                deleteLegacy = request.POST.get('deleteLegacy', False)
                if self.userInst.canChangeRights():
                    if len(reason) > 1:
                        if deleteLegacy:
                            posts = Post.filterByUid(user.uidNumber).all()
                            removed = []
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
            return self.render('manageUser')
        else:
            c.errorText = _('No such user exists.')
            return self.render('error')

