import logging

from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
import sqlalchemy
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
from wakabaparse import WakabaParser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class FcajaxController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.userInst = self.userInst
        if not self.currentUserIsAuthorized or self.userInst.isBanned():
            abort(403)

    def getPost(self, post):
        postInst = Post.query.get(post)
        if postInst:
            if postInst.parentid == -1:
                parent = postInst
            else:
                parent = Post.query.get(postInst.parentid)

            for t in parent.tags:
                if t.id in g.forbiddenTags and not self.userInst.isAdmin():
                    abort(403)
            return postInst.message
        else:
            abort(404)

    def getRenderedPost(self, post):
        postInst = Post.query.get(post)
        if postInst:
            if postInst.parentid == -1:
                parent = postInst
            else:
                parent = Post.query.get(postInst.parentid)

            for t in parent.tags:
                if t.id in g.forbiddenTags and not self.userInst.isAdmin():
                    abort(403)

            #uncomment to disable folding for big posts
            #parent.enableShortMessages=False
            return self.render('postReply', thread=parent, post = postInst)
        else:
            abort(404)

    def getRepliesCountForThread(self, post):
        postInst = Post.query.get(post)
        if postInst and postInst.parentid == -1:
            return str(Post.query.filter(Post.parentid == postInst.id).count())
        else:
            abort(404)

    def getThreadIds(self, post):
        postInst = Post.query.get(post)
        if postInst and postInst.parentid == -1:
            replies = Post.query.filter(Post.parentid == postInst.id).all()
            ret = [str(post)]
            if replies:
                for reply in replies:
                    ret.append(str(reply.id))
            return ','.join(ret)
        else:
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

    def hideThread(self,post,url):
        if self.userInst.Anonymous:
            abort(403)
        postInst = Post.query.get(post)
        if postInst:
            if postInst.parentid == -1:
                hideThreads = self.userInst.hideThreads()
                if not post in hideThreads:
                    hideThreads.append(post)
                    self.userInst.hideThreads(hideThreads)
                    meta.Session.commit()
        if url:
            return redirect_to(str('/%s' % url.encode('utf-8')))
        else:
            return ''

    def showThread(self,post,redirect):
        if self.userInst.Anonymous:
            abort(403)
        postInst = Post.query.get(post)
        if postInst:
            if postInst.parentid == -1:
                hideThreads = self.userInst.hideThreads()
                if post in hideThreads:
                    hideThreads.remove(post)
                    self.userInst.hideThreads(hideThreads)
                    meta.Session.commit()
        if redirect:
            return redirect_to(str('/%s' %redirect.encode('utf-8')))
        else:
            return ''
