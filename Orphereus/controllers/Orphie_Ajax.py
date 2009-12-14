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
#                                                                              #
################################################################################

import logging
from paste.deploy.converters import asbool

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)

class AjaxServicesPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Ajax helpers'),
                  'deps' : ('base_view', 'base_profile')
                 }
        BasePlugin.__init__(self, 'ajaxhelpers', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('ajHideThread', '/ajax/hideThread/{post}/{redirect}/{realm}/{page}',
                    controller = 'Orphie_Ajax', action = 'hideThread',
                    redirect = '', realm = '',
                    page = 0,
                    requirements = dict(post = r'\d+', page = r'\d+'))
        map.connect('ajShowThread', '/ajax/showThread/{post}/{redirect}/{realm}/{page}',
                    controller = 'Orphie_Ajax', action = 'showThread',
                    redirect = '',
                    realm = '',
                    page = 0,
                    requirements = dict(post = r'\d+', page = r'\d+'))
        map.connect('ajGetPost', '/ajax/getPost/{post}',
                    controller = 'Orphie_Ajax', action = 'getPost',
                    requirements = dict(post = r'\d+'))
        map.connect('ajGetRenderedPost', '/ajax/getRenderedPost/{post}',
                    controller = 'Orphie_Ajax', action = 'getRenderedPost',
                    requirements = dict(post = r'\d+'))
        map.connect('ajGetRenderedReplies', '/ajax/getRenderedReplies/{thread}',
                    controller = 'Orphie_Ajax', action = 'getRenderedReplies',
                    requirements = dict(thread = r'\d+'))
        map.connect('ajAddUserFilter', '/ajax/addUserFilter/{filter}',
                    controller = 'Orphie_Ajax', action = 'addUserFilter')
        map.connect('ajEditUserFilter', '/ajax/editUserFilter/{fid}/{filter}',
                    controller = 'Orphie_Ajax', action = 'editUserFilter',
                    requirements = dict(fid = r'\d+'))
        map.connect('ajDeleteUserFilter', '/ajax/deleteUserFilter/{fid}',
                    controller = 'Orphie_Ajax', action = 'deleteUserFilter',
                    requirements = dict(fid = r'\d+'))
        map.connect('ajCheckCaptcha', '/ajax/checkCaptcha/{id}/{text}',
                    controller = 'Orphie_Ajax', action = 'checkCaptcha',
                    text = '', requirements = dict(id = r'\d+'))
        map.connect('ajPostThread', '/ajax/postThread/{board}',
                    controller = 'Orphie_Profile', action = 'ajaxPostThread',
                    conditions = dict(method = ['POST']))
        map.connect('ajPostReply', '/ajax/postReply/{post}',
                    controller = 'Orphie_Profile', action = 'ajaxPostReply',
                    conditions = dict(method = ['POST']),
                    requirements = dict(post = r'\d+'))
        map.connect('ajTagsCheck', '/ajax/checkTags',
                    controller = 'Orphie_Ajax', action = 'checkTags')
        map.connect('ajGetMyPostIds', '/ajax/getMyPostIds/{thread}',
                    controller = 'Orphie_Ajax', action = 'getMyPostIds',
                    requirements = dict(thread = r'\d+'))
        map.connect('ajChangeOption', '/ajax/option/{name}/{value}/set',
                    controller = 'Orphie_Ajax', action = 'changeOption')

        # routines below isn't actually used
        map.connect('ajGetText', '/ajax/getText/{text}',
                    controller = 'Orphie_Ajax', action = 'getText',
                    text = '')
        map.connect('/ajax/getRepliesCountForThread/{post}',
                    controller = 'Orphie_Ajax', action = 'getRepliesCountForThread',
                    requirements = dict(post = r'\d+'))
        map.connect('/ajax/getRepliesIds/{post}',
                    controller = 'Orphie_Ajax', action = 'getRepliesIds',
                    requirements = dict(post = r'\d+'))
        map.connect('/ajax/getUserSettings',
                    controller = 'Orphie_Ajax', action = 'getUserSettings')
        map.connect('/ajax/getUploadsPath',
                    controller = 'Orphie_Ajax', action = 'getUploadsPath')

    def menuItems(self, menuId):
        menu = None
        if menuId == "topMenu":
            menu = [MenuItem('id_profile_ProfileQS', _("Quick switch"), None, 200, 'id_profile_Profile'),
                    MenuItem('id_profile_frame', "", "", 300, 'id_profile_Profile'),
                    MenuItem('id_profile_style', _("Style"), None, 400, 'id_profile_Profile'),
                    ]

            #for style in c.styles:
        return menu

    def menuItemIsVisible(self, id, baseController):
        #user = baseController.userInst
        return id.startswith('id_profile_')

    def modifyMenuItem(self, menuItem, baseController):
        user = baseController.userInst
        if menuItem.id == 'id_profile_frame':
            menuItem.route = h.url_for('ajChangeOption',
                                       name = 'useFrame',
                                       value = not user.useFrame,
                                       returnTo = c.currentURL)
            menuItem.text = user.useFrame and _("Turn frame off") or _("Turn frame on")
        return menuItem

    def insertAfterMenuItem(self, menuItem, baseController):
        user = baseController.userInst
        ret = []
        if menuItem.id == 'id_profile_style':
            onclicktemplate = "changeCSS(event, '%s', '%s')"
            for style in c.styles:
                ret.append(MenuItem('id_profile_style_%s' % style,
                                    style,
                                    h.url_for('ajChangeOption', name = 'style', value = style, returnTo = c.currentURL),
                                    401,
                                    'id_profile_Profile',
                                    onclick = onclicktemplate % (style, h.staticFile("%s.css" % style))))
        return ret

    def beforeRequestCallback(self, baseController):
        if baseController.userInst.isValid():
            c.styles = g.OPT.cssFiles[baseController.userInst.template]

class OrphieAjaxController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.userInst = self.userInst
        if not self.currentUserIsAuthorized() or self.userInst.isBanned():
            abort(403)
        self.disableMenu("topMenu")

    def checkTags(self):
        tags = request.POST.get('tags', '')
        freeNames = Tag.stringToTagLists(tags, False)[2]
        if freeNames:
            postingHooks = g.implementationsOf(AbstractPostingHook)
            existentNames = []
            for tagname in freeNames:
                for hook in postingHooks:
                    tag = hook.tagCheckHandler(tagname, self.userInst)
                    if tag:
                        existentNames.append(tagname)
            freeNames = list(set(freeNames).difference(existentNames))
            c.tags = freeNames
        if freeNames:
            return self.render('tagNames', disableFiltering = True)
        return ''

    def realmRedirect(self, redirect, realm, page):
        args = {}
        page = toNumber(page, 0, 0)
        if realm:
            if 'board' == redirect:
                args['board'] = realm
                args['page'] = page
            elif 'thread' == redirect:
                args['post'] = realm
        return redirect_to(redirect, **args)

    def hideThread(self, post, redirect, realm, page):
        if self.userInst.Anonymous and not g.OPT.allowAnonProfile:
            abort(403)
        self.forceNoncachedUser()
        post = int(post)
        postInst = Post.getPost(post)
        Post.normalizeHiddenThreadsList(self.userInst)
        if postInst and not postInst.parentPost:
            hideThreads = self.userInst.hideThreads
            if not post in hideThreads:
                hideThreads.append(post)
                self.userInst.hideThreads = hideThreads
                meta.Session.commit()
        if redirect:
            return self.realmRedirect(redirect, realm, page)
            #return redirect_to(str('/%s' % redirect.encode('utf-8')))
        return ''

    def showThread(self, post, redirect, realm, page):
        if self.userInst.Anonymous and not g.OPT.allowAnonProfile:
            abort(403)
        self.forceNoncachedUser()
        post = int(post)
        postInst = Post.getPost(post)
        Post.normalizeHiddenThreadsList(self.userInst)
        if postInst and not postInst.parentPost:
            hideThreads = self.userInst.hideThreads
            if post in hideThreads:
                hideThreads.remove(post)
                self.userInst.hideThreads = hideThreads
                meta.Session.commit()
        if redirect:
            return self.realmRedirect(redirect, realm, page)
            #return redirect_to(str('/%s' % redirect.encode('utf-8')))
        return ''

    def getPost(self, post):
        postInst = Post.getPost(post)
        if postInst:
            if not self.userInst.isAdmin() and postInst.parentPost:
                for t in postInst.parentPost.tags:
                    if t.adminOnly:
                        abort(403)
            return postInst.message
        abort(404)

    @jsonify
    def getMyPostIds(self, thread):
        if self.userInst.Anonymous:
            abort(403)
        postInst = Post.getPost(int(thread))
        if postInst and not postInst.parentPost:
            ids = meta.Session.query(Post.id).filter(and_(Post.parentid == thread, Post.uidNumber == self.userInst.uidNumber)).all()
            ids = map(lambda x: x[0], ids)
            return ids
        abort(404)

    def getRenderedPost(self, post):
        postInst = Post.getPost(post)
        if postInst:
            if not self.userInst.isAdmin() and postInst.parentPost:
                for t in postInst.parentPost.tags:
                    if t.adminOnly:
                        abort(403)
            parent = postInst.parentPost
            if not parent:
                parent = postInst
            #uncomment to disable folding for big posts
            #parent.enableShortMessages=False
            self.setRightsInfo()
            return self.render('postReply', None, disableFiltering = True, thread = parent, post = postInst)
        abort(404)

    def getRenderedReplies(self, thread):
        c.board = 'Fake'
        postInst = Post.getPost(thread)
        if postInst and not postInst.parentPost:
            if not self.userInst.isAdmin():
                for t in postInst.tags:
                    if t.adminOnly:
                        abort(403)
            postInst.Replies = postInst.filterReplies().all()
            self.setRightsInfo()
            return self.render('replies', None, disableFiltering = True, thread = postInst)
        abort(404)

    def getRepliesCountForThread(self, post):
        postInst = Post.getPost(post)
        ret = False
        if postInst:
            ret = postInst.getExactReplyCount()
        if ret:
            return str(ret)
        abort(404)

    def getRepliesIds(self, post):
        postInst = Post.getPost(post)
        if postInst:
            replies = postInst.filterReplies().all()
            ret = []
            if replies:
                for reply in replies:
                    ret.append(str(reply.id))
                return str(','.join(ret))
        abort(404)


    @jsonify
    def getUserSettings(self):
        return self.userInst.optionsDump()

    def getUploadsPath(self):
        return g.OPT.filesPathWeb

    def editUserFilter(self, fid, filter):
        if self.userInst.Anonymous:
            abort(403)
        if self.userInst.changeFilter(fid, filter):
            return filter
        abort(404)

    def deleteUserFilter(self, fid):
        if self.userInst.Anonymous:
            abort(403)
        if self.userInst.deleteFilter(fid):
            return ''
        abort(404)

    def addUserFilter(self, filter):
        if self.userInst.Anonymous:
            abort(403)
        userFilter = self.userInst.addFilter(filter)
        return self.render('ajax.userFilter', None, disableFiltering = True, userFilter = userFilter)

    def checkCaptcha(self, id, text):
        ct = Captcha.getCaptcha(id)
        if ct:
            #log.debug("testing: " + str(id))
            ok = ct.test(text, True)
            if ok:
                #log.debug('chck - ok')
                return 'ok'
            else:
                ct = Captcha.create()
                session['anonCaptId'] = ct.id
                #log.debug('chk - fail ' + str(ct.id))
                session.save()
                return str(ct.id)
        else:
            abort(404)

    def changeOption(self, name, value):
        val = None
        ok = True
        if name in self.userInst.booleanValues:
            val = asbool(value)
        elif name in self.userInst.intValues and isNumber(value):
            val = int(val)
        elif name in self.userInst.stringValues:
            val = filterText(value)
        else:
            ok = None
        if ok:
            self.forceNoncachedUser()
            setattr(self.userInst, str(name), val)
            if not c.userInst.Anonymous:
                meta.Session.commit()
            returnTo = request.params.get('returnTo', None)
            if not returnTo is None:
                if c.userInst.useFrame:
                    c.frameTargetToRedir = returnTo
                    c.currentURL = None
                else:
                    c.currentURL = returnTo
                c.proceedRedirect = True
                c.suppressLoginMessage = True
                return self.render('loginRedirect')
            else:
                return 'ok. "%s" changed to "%s"' % (str(name), str(val))
        return abort(404)
