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

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.pluginInfo import PluginInfo

log = logging.getLogger(__name__)

def routingInit(map):
    map.connect('ajHideThread', '/ajax/hideThread/:post/:redirect/:realm/:page', controller = 'Orphie_Ajax', action = 'hideThread', redirect = '', realm = '', page = 0, requirements = dict(post = '\d+', page = '\d+'))
    map.connect('ajShowThread', '/ajax/showThread/:post/:redirect/:realm/:page', controller = 'Orphie_Ajax', action = 'showThread', redirect = '', realm = '', page = 0, requirements = dict(post = '\d+', page = '\d+'))
    map.connect('ajGetPost', '/ajax/getPost/:post', controller = 'Orphie_Ajax', action = 'getPost', requirements = dict(post = '\d+'))
    map.connect('ajGetRenderedPost', '/ajax/getRenderedPost/:post', controller = 'Orphie_Ajax', action = 'getRenderedPost', requirements = dict(post = '\d+'))
    map.connect('ajGetRenderedReplies', '/ajax/getRenderedReplies/:thread', controller = 'Orphie_Ajax', action = 'getRenderedReplies', requirements = dict(thread = '\d+'))
    map.connect('ajAddUserFilter', '/ajax/addUserFilter/:filter', controller = 'Orphie_Ajax', action = 'addUserFilter')
    map.connect('ajEditUserFilter', '/ajax/editUserFilter/:fid/:filter', controller = 'Orphie_Ajax', action = 'editUserFilter', requirements = dict(fid = '\d+'))
    map.connect('ajDeleteUserFilter', '/ajax/deleteUserFilter/:fid', controller = 'Orphie_Ajax', action = 'deleteUserFilter', requirements = dict(fid = '\d+'))
    map.connect('ajCheckCaptcha', '/ajax/checkCaptcha/:id/:text', controller = 'Orphie_Ajax', action = 'checkCaptcha', text = '', requirements = dict(id = '\d+'))
    map.connect('ajPostThread', '/ajax/postThread/:board', controller = 'Orphie_Main', action = 'ajaxPostThread', conditions = dict(method = ['POST']))
    map.connect('ajPostReply', '/ajax/postReply/:post', controller = 'Orphie_Main', action = 'ajaxPostReply', conditions = dict(method = ['POST']), requirements = dict(post = '\d+'))
    # routines below isn't actually used
    map.connect('ajGetText', '/ajax/getText/:text', controller = 'Orphie_Ajax', action = 'getText', text = '')
    map.connect('/ajax/getRepliesCountForThread/:post', controller = 'Orphie_Ajax', action = 'getRepliesCountForThread', requirements = dict(post = '\d+'))
    map.connect('/ajax/getRepliesIds/:post', controller = 'Orphie_Ajax', action = 'getRepliesIds', requirements = dict(post = '\d+'))
    map.connect('/ajax/getUserSettings', controller = 'Orphie_Ajax', action = 'getUserSettings')
    map.connect('/ajax/getUploadsPath', controller = 'Orphie_Ajax', action = 'getUploadsPath')

def pluginInit(globj = None):
    if globj:
        pass

    config = {'name' : N_('Ajax helpers'),
             'routeinit' : routingInit,
             }

    return PluginInfo('ajaxhelpers', config)

class OrphieAjaxController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.userInst = self.userInst
        if not self.currentUserIsAuthorized() or self.userInst.isBanned():
            abort(403)

    def realmRedirect(self, redirect, realm, page):
        args = {}
        if page and isNumber(page):
            page = int(page)
        else:
            page = 0
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
        postInst = Post.getPost(post)
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
        postInst = Post.getPost(post)
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
                    if t.id in g.forbiddenTags:
                        abort(403)
            return postInst.message
        abort(404)

    def getRenderedPost(self, post):
        postInst = Post.getPost(post)
        if postInst:
            if not self.userInst.isAdmin() and postInst.parentPost:
                for t in postInst.parentPost.tags:
                    if t.id in g.forbiddenTags:
                        abort(403)
            parent = postInst.parentPost
            if not parent:
                parent = postInst
            #uncomment to disable folding for big posts
            #parent.enableShortMessages=False
            self.setRightsInfo()
            return self.render('postReply', None, thread = parent, post = postInst)
        abort(404)

    def getRenderedReplies(self, thread):
        postInst = Post.getPost(thread)
        if postInst and not postInst.parentPost:
            if not self.userInst.isAdmin():
                for t in postInst.tags:
                    if t.id in g.forbiddenTags:
                        abort(403)
            postInst.Replies = postInst.filterReplies().all()
            self.setRightsInfo()
            return self.render('replies', None, thread = postInst)
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

    def getUserSettings(self):
        return str(self.userInst.optionsDump())

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
        c.userFilter = userFilter
        return self.render('ajax.addUserFilter')

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
