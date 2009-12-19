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
import hashlib
import string
import re
from Orphereus.lib.miscUtils import *
from Orphereus.lib.cachedutils import *
from Orphereus.lib.FakeUser import FakeUser
from Orphereus.lib.constantValues import *
from Orphereus.lib.cache import CacheDict

log = logging.getLogger(__name__)

class OrphieBaseController(BaseController):
    def __before__(self):
        if g.OPT.refControlForAnyRequest:
            self.refererCheck()

        c.log = []
        if g.OPT.devMode:
            c.sum = 0
            self.startTime = time.time()

        self.userInst = False
        uid = self.sessUid()
        if uid > 0 and g.OPT.allowLogin:
            self.userInst = User.getUser(uid)
        if not self.userInst:
            self.userInst = FakeUser()
        c.userInst = self.userInst
        c.cache = CacheDict()
        c.uidNumber = self.userInst.uidNumber
        if self.userInst.isValid():
            c.jsFiles = g.OPT.jsFiles[self.userInst.template]
        self.requestedMenus = {}
        self.disabledMenus = []
        self.builtMenus = {}

        # IP ban checks
        self.userIp = h.ipToInt(getUserIp())
        c.userIp = self.userIp
        c.ban = Ban.getBanByIp(self.userIp)

        if c.ban and c.ban.enabled:
            currentURL = request.path_info.decode('utf-8', 'ignore')
            if currentURL.endswith('/'):
                currentURL = c.currentURL[:-1]
            #FIXME: mind the prefix
            if (currentURL != '/ipBanned') and c.ban.type:
                redirect_to('ipBanned')
        else:
            c.ban = None

        if g.OPT.checkUAs and self.userInst.isValid() and not self.userInst.Anonymous:
            for ua in g.OPT.badUAs:
                if filterText(request.headers.get('User-Agent', '?')).startswith(ua):
                    self.userInst.ban(2, _("[AUTOMATIC BAN] Security alert type 1: %s") % hashlib.md5(ua).hexdigest(), -1)
                    break

        c.userPostsToHighlight = []
        #log.debug(request.cookies)
        #log.debug(session)
        self.setLang()

        for plugin in g.plugins:
            plugin.beforeRequestCallback(self)

        if g.firstRequest:
            g.firstRequest = False

    def forceNoncachedUser(self):
        if g.OPT.memcachedUsers and not(self.userInst.Anonymous):
            g.mc.delete('u%s' % self.userInst.uidNumber)
            self.userInst = c.userInst = User.getUser(self.userInst.uidNumber, False)

    def setLang(self, captcha = False):
        lang = ""
        if self.userInst.isValid():
            if captcha:
                lang = self.userInst.cLang
            else:
                lang = self.userInst.lang
        h.setLang(lang)

    def sessUid(self):
        if g.OPT.allowLogin:
            return session.get('uidNumber', -1)
        return - 1

    def setCookie(self):
        response.set_cookie('Orphie-test', '^_^')# for cookie tester
        sessCookie = request.cookies.get('Orphereus', '')
        if sessCookie:
            response.set_cookie('Orphereus', str(sessCookie), domain = '.' + g.OPT.baseDomain)

    def initEnvironment(self):
        self.requestForMenu("topMenu", False)
        c.title = g.OPT.title
        c.boardlist = g.caches.setdefaultEx('boardlist', chBoardList)
        #c.sectionNames = g.caches.setdefaultEx('sectionNames', chSectionNames, c.boardlist)
        c.menuLinks = g.additionalLinks
        #c.renderedTopMenu = self.fastRender('menu', bottomMenu = False)
        #c.renderedBottomMenu = self.fastRender('menu', bottomMenu = True)
        c.sectionNames = g.sectionNames

        self.setCookie()
        c.captcha = self.initSessionCaptcha()

        if self.userInst.Anonymous:
            remPassCookie = request.cookies.get('orhpieRemPass', randomStr())
            c.remPass = remPassCookie
            response.set_cookie('orhpieRemPass', unicode(remPassCookie), max_age = 3600)
        self.setRightsInfo()

    def initSessionCaptcha(self, force = False):
        if self.userInst.Anonymous or force:
            anonCaptId = session.get('anonCaptId', None)
            if not anonCaptId or not Captcha.exists(anonCaptId):
                #log.debug('recreate')
                captcha = None
                if self.userInst.isValid() and self.userInst.cLang:
                    oldLang = h.setLang(self.userInst.cLang)
                    captcha = Captcha.create()
                    h.setLang(oldLang)
                else:
                    captcha = Captcha.create()
                session['anonCaptId'] = captcha.id
                session.save()
                return captcha
            else:
                return Captcha.getCaptcha(anonCaptId)
        return None

    def checkSessionCaptcha(self, value, id = None):
        anonCaptId = session.get('anonCaptId', id)
        if anonCaptId:
            captcha = Captcha.getCaptcha(anonCaptId)
            #log.debug("captcha: id == %s, object == %s " %(str(anonCaptId), str(captcha)))
            if captcha:
                return captcha.test(value)
        return None

    def initiate(self):
        c.destinations = destinations

        c.currentURL = request.path_info.decode('utf-8', 'ignore')

        if c.currentURL.endswith('/'):
            c.currentURL = c.currentURL[:-1]

        if not self.currentUserIsAuthorized():
            return redirect_to('authorizeToUrl', url = c.currentURL)
        if self.userInst.isBanned():
            #abort(500, 'Internal Server Error')     # calm hidden ban
            return redirect_to('banned')
        #c.currentUserCanPost = self.currentUserCanPost()
        if self.userInst.isAdmin() and not checkAdminIP():
            return redirect_to('boardBase')
        self.initEnvironment()

    def refererCheck(self):
        if g.OPT.refControlEnabled and (not g.OPT.allowAnonymous or g.OPT.refControlWhenAnonEnabled):
            ref = request.headers.get('REFERER', False)
            if ref:
                ref = filterText(ref)

            if ref:
                rickroll = True
                for rc in g.OPT.refControlList:
                    if rc in ref:
                        rickroll = False

                if (rickroll):
                    redir = g.OPT.fakeLinks[random.randint(0, len(g.OPT.fakeLinks) - 1)]
                    toLog(LOG_EVENT_RICKROLLD, "Request rickrolld. Referer: %s, Redir: %s, IP: %s, User-Agent: %s" % (ref, redir, getUserIp(), filterText(request.headers.get('User-Agent', '?'))))
                    redirect_to(str(redir))

    def requestForMenu(self, menuId, linearize):
        if (not menuId in self.requestedMenus) and (not menuId in self.disabledMenus):
            self.requestedMenus[menuId] = {'linearize' : linearize}

    def disableMenu(self, menuId):
        if not menuId in self.disabledMenus:
            self.disabledMenus.append(menuId)
        if menuId in self.requestedMenus:
            self.requestedMenus.pop(menuId)

    def buildLinearMenu(self, id, level, source, target):
        if source and id in source:
            for item in source[id]:
                if item.plugin.menuItemIsVisible(item.id, self):
                    target.append((item.plugin.modifyMenuItem(item, self), level))
                    dynItems = item.plugin.insertAfterMenuItem(item, self)
                    for ditem in dynItems:
                        target.append((ditem, level))
                    self.buildLinearMenu(item.id, level + 1, source, target)

    def buildMenu(self, id, source, target):
        for sourceBranch in source:
            branch = []
            for item in source[sourceBranch]:
                if item.plugin.menuItemIsVisible(item.id, self):
                    branch.append(item.plugin.modifyMenuItem(item, self))
                    branch.extend(item.plugin.insertAfterMenuItem(item, self))
            target[sourceBranch] = branch

    def fastRender(self, tname, **options):
        return self._fastRender(self.fastTemplatePath(tname), **options)

    def _fastRender(self, tpath, **options):
        return render('/' + tpath, extra_vars = options)

    def fastTemplatePath(self, page):
        tpath = "std.banned.mako"
        if not self.userInst.isBanned():
            tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : self.userInst.template, 'page' : page}
        return tpath

    # returns template filename and actuator test path
    def getTemplatePaths(self, page, tmplName = None):
        if page:
            templRelativePath = "std.%s.mako" % page
            actuator = actuatorTest = "actuators/%s/" % (g.OPT.actuator)

            try:
                if not tmplName == 'std' and self.userInst and not self.userInst.isBanned():
                    templName = tmplName or self.userInst.template
                    templRelativePath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : templName, 'page' : page}
                    actuatorTest = "%s/actuators/%s/" % (templName, g.OPT.actuator)
            except: #userInst not defined or user banned
                pass
            return templRelativePath, actuator, actuatorTest

    def render(self, page, tmplName = None, **options):
        pathResolution = self.getTemplatePaths(page, tmplName)
        c.template = tpath = pathResolution[0]
        c.actuator, c.actuatorTest = pathResolution[1], pathResolution[2]

        #fpath = os.path.join(g.OPT.templPath, tpath)
        #log.debug ("Tpath:  %s ; Fpath: %s" %(tpath,fpath))
        for menuName in self.requestedMenus:
            menuItems = g.getMenuItems(menuName)
            menu = None
            if self.requestedMenus[menuName]['linearize']:
                menu = []
                self.buildLinearMenu(False, 0, menuItems, menu)
            else:
                menu = {}
                self.buildMenu(False, menuItems, menu)
            if menu:
                self.builtMenus[menuName] = menu
        c.builtMenus = self.builtMenus
        #log.debug(self.builtMenus)

        if g.OPT.devMode:
            c.renderStartTime = time.time()
            c.processStartTime = 0
            if self.__dict__.has_key('startTime'):
                c.processStartTime = self.startTime
                c.log.append("processing: %s" % str(c.renderStartTime - self.startTime))
        options['controller'] = self
        output = render('/' + tpath, extra_vars = options)
        if g.globalFilterStack and not options.get('disableFiltering', None):
            return h.applyFilters(output, True)
        else:
            return output

    def error(self, text, header = None):
        c.errorText = text
        if not header:
            header = _('Error')
        c.boardName = header
        return self.render('error')

    def paginate(self, count, page, tpp):
        if count > 1:
            p = divmod(count, tpp)
            c.pages = p[0]
            if p[1]:
                c.pages += 1
            if (page + 1) > c.pages:
                page = c.pages - 1
            c.page = page

            if c.pages > 15:
                c.showPagesPartial = True
                if c.page - 5 > 1:
                    c.leftPage = c.page - 5
                else:
                    c.leftPage = 2

                if c.page + 5 < c.pages - 2:
                    c.rightPage = c.page + 5
                else:
                    c.rightPage = c.pages - 2
        elif count == 1:
            c.page = False
            c.pages = False
        elif count == 0:
            c.page = False
            c.pages = False
        c.count = count

    def currentUserCanPost(self):
        return g.OPT.allowPosting and self.userInst \
              and not self.userInst.readonly()
              #and ((self.userInst.Anonymous and g.OPT.allowAnonymousPosting) or not self.userInst.Anonymous)

    def destroySession(self):
        session.clear()
        session.save()
        session.delete()

    def currentUserIsAuthorized(self):
        return self.userInst.isValid() and (self.sessUid() == self.userInst.uidNumber)

    def setRightsInfo(self):
        c.currentUserCanPost = self.currentUserCanPost()
        c.uidNumber = self.userInst.uidNumber
        c.enableAllPostDeletion = self.userInst.canDeleteAllPosts()
        c.isAdmin = self.userInst.isAdmin()

    # Parser callbacks
    @staticmethod
    def formatPostReference(postid, prependGt = True, **kwargs):
        post = Post.getPost(postid)
        if post:
            parentid = post.parentid
            linkUrl = h.postUrl(parentid, postid)
            postid = g.OPT.secondaryIndex and post.secondaryIndex or post.id
            linkText = '%s%s' % (prependGt and '&gt;&gt;' or '', postid)
            linkText = kwargs.get('linkText', linkText)
            return '<a href="%s" onclick="highlight(%s)">%s</a>' % (linkUrl, postid, linkText)
        else:
            return "%s%s" % (prependGt and '&gt;&gt;' or '', postid)

