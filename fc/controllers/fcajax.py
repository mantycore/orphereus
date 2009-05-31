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

from fc.lib.base import *
from fc.model import *
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class FcajaxController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.userInst = self.userInst
        if not self.currentUserIsAuthorized() or self.userInst.isBanned():
            abort(403)

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
            return self.render('postReply', None, thread = parent, post = postInst)
        abort(404)

    def getRenderedReplies(self, thread):
        postInst = Post.getPost(thread)
        c.currentUserCanPost = self.currentUserCanPost()
        if postInst and not postInst.parentPost:
            if not self.userInst.isAdmin():
                for t in postInst.tags:
                    if t.id in g.forbiddenTags:
                        abort(403)
            postInst.Replies = postInst.filterReplies().all()
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

    def hideThread(self, post, redirect):
        if self.userInst.Anonymous and not g.OPT.allowAnonProfile:
            abort(403)
        postInst = Post.getPost(post)
        if postInst and not postInst.parentPost:
            hideThreads = self.userInst.hideThreads()
            if not post in hideThreads:
                hideThreads.append(post)
                self.userInst.hideThreads(hideThreads)
                meta.Session.commit()
        if redirect:
            return redirect_to(str('/%s' % redirect.encode('utf-8')))
        return ''

    def showThread(self, post, redirect):
        if self.userInst.Anonymous and not g.OPT.allowAnonProfile:
            abort(403)
        postInst = Post.getPost(post)
        if postInst and not postInst.parentPost:
            hideThreads = self.userInst.hideThreads()
            if post in hideThreads:
                hideThreads.remove(post)
                self.userInst.hideThreads(hideThreads)
                meta.Session.commit()
        if redirect:
            return redirect_to(str('/%s' % redirect.encode('utf-8')))
        return ''

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