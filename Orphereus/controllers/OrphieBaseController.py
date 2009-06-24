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
import string
import re
from Orphereus.lib.miscUtils import *
from Orphereus.lib.FakeUser import FakeUser
from Orphereus.lib.constantValues import *

log = logging.getLogger(__name__)

class OrphieBaseController(BaseController):
    def __before__(self):
        if g.OPT.devMode:
            c.log = []
            c.sum = 0
            self.startTime = time.time()

        self.userInst = False
        uid = self.sessUid()
        if uid > 0 and g.OPT.allowLogin:
            self.userInst = User.getUser(uid)
        if not self.userInst:
            self.userInst = FakeUser()

        c.userInst = self.userInst
        if self.userInst.isValid():
            c.jsFiles = g.OPT.jsFiles[self.userInst.template]
        c.uidNumber = self.userInst.uidNumber
        self.requestedMenus = []
        self.builtMenus = {}

        ################# TODO: rewrite. Dont't like this.
        ipStr = getUserIp()
        ip = h.dottedToInt(ipStr)
        banInfo = Ban.getBanByIp(ip)
        currentURL = request.path_info.decode('utf-8', 'ignore')

        if currentURL.endswith('/'):
            currentURL = c.currentURL[:-1]

        #log.debug('ipstr: %s, ip: %s, ban: %s, url: %s' %(ipStr,ip,banInfo,currentURL))

        if banInfo and banInfo.enabled:
            c.ban = banInfo
            if (currentURL != '/ipBanned') and banInfo.type:
                redirect_to('ipBanned')

        ###############

        if g.OPT.checkUAs and self.userInst.isValid() and not self.userInst.Anonymous:
            for ua in g.OPT.badUAs:
                if filterText(request.headers.get('User-Agent', '?')).startswith(ua):
                    self.userInst.ban(2, _("[AUTOMATIC BAN] Security alert type 1: %s") % hashlib.md5(ua).hexdigest(), -1)
                    break

        #log.debug(request.cookies)
        #log.debug(session)
        self.setLang()

        for plugin in g.plugins:
            hook = plugin.requestHook()
            if hook:
                hook(self)

        if g.firstRequest:
            g.firstRequest = False

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
        c.title = g.settingsMap['title'].value
        boards = Tag.getBoards()
        c.boardlist = []
        sectionId = -1
        section = []

        def sectionName(id):
            sName = ''
            if sectionId < len(g.sectionNames):
                sName = g.sectionNames[id]
            return sName
        for b in boards:
            if sectionId == -1:
                sectionId = b.options.sectionId
                section = []
            if sectionId != b.options.sectionId:
                c.boardlist.append((section, sectionName(sectionId)))
                sectionId = b.options.sectionId
                section = []
            bc = empty()
            bc.tag = b.tag
            bc.comment = b.options.comment
            section.append(bc) #b.tag)
        if section:
            c.boardlist.append((section, sectionName(sectionId)))

        c.sectionNames = []
        for i in range(0, len(c.boardlist)):
            if i < len(g.sectionNames):
                c.sectionNames.append(g.sectionNames[i])
            else:
                c.sectionNames.append(None)

        #log.debug(request.cookies.get('Orphereus',''))
        #log.debug(request.cookies)

        self.setCookie()

        c.menuLinks = g.additionalLinks
        c.sectionNames = g.sectionNames

        if self.userInst.Anonymous:
            anonCaptId = session.get('anonCaptId', False)
            if not anonCaptId or not Captcha.exists(anonCaptId):
                #log.debug('recreate')
                oldLang = h.setLang(self.userInst.cLang)
                captcha = Captcha.create()
                h.setLang(oldLang)
                session['anonCaptId'] = captcha.id
                session.save()
                c.captcha = captcha
            else:
                c.captcha = Captcha.getCaptcha(anonCaptId)

            remPassCookie = request.cookies.get('orhpieRemPass', randomStr())
            c.remPass = remPassCookie
            response.set_cookie('orhpieRemPass', unicode(remPassCookie), max_age = 3600)
        self.setRightsInfo()

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

    def requestForMenu(self, menuId):
        if not menuId in self.requestedMenus:
            self.requestedMenus.append(menuId)

    def buildMenu(self, id, level, source, target):
        if source and id in source:
            for item in source[id]:
                test = item.plugin.menuTest()
                if (not test or (test and test(item.id, self))):
                    target.append((item, level))
                    self.buildMenu(item.id, level + 1, source, target)

    def render(self, page, tmplName = None, **options):
        tname = 'std'
        tpath = "%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        c.actuator = "actuators/%s/" % (g.OPT.actuator)
        c.actuatorTest = c.actuator

        try:
            if not tmplName == 'std' and self.userInst and not self.userInst.isBanned():
                tname = tmplName
                if not tname:
                    tname = self.userInst.template
                tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
                c.actuatorTest = "%s/actuators/%s/" % (tname, g.OPT.actuator)
        except: #userInst not defined or user banned
            pass

        fpath = os.path.join(g.OPT.templPath, tpath)
        #log.debug ("Tpath:  %s ; Fpath: %s" %(tpath,fpath))

        for menuName in self.requestedMenus:
            menu = []
            self.buildMenu(False, 0, g.getMenuItems(menuName), menu)
            if menu:
                self.builtMenus[menuName] = menu
        c.builtMenus = self.builtMenus
        #log.debug(self.builtMenus)

        #TODO: it may be excessive
        if page and os.path.isfile(fpath) and os.path.abspath(fpath).replace('\\', '/') == fpath.replace('\\', '/'):
            if g.OPT.devMode:
                c.renderStartTime = time.time()
                c.log.append("processing: %s" % str(c.renderStartTime - self.startTime))
            output = render('/' + tpath, extra_vars = options)
            if g.globalFilterStack and not options.get('disableFiltering', None):
                return h.applyFilters(output, True)
            else:
                return output
        else:
            log.debug ("Template problem:  %s" % page)
            abort(404)

    def error(self, text, header = None):
        c.errorText = text
        if not header:
            header = _('Error')
        c.boardName = header
        return self.render('error')

    def showStatic(self, page):
        c.boardName = _(page)
        return self.render('static.%s' % page)

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
        return g.OPT.allowPosting and self.userInst and ((self.userInst.Anonymous and g.OPT.allowAnonymousPosting) or not self.userInst.Anonymous)

    def currentUserIsAuthorized(self):
        return self.userInst.isValid() and (self.sessUid() == self.userInst.uidNumber)

    def setRightsInfo(self):
        c.currentUserCanPost = self.currentUserCanPost()
        c.uidNumber = self.userInst.uidNumber
        c.enableAllPostDeletion = self.userInst.canDeleteAllPosts()
        c.isAdmin = self.userInst.isAdmin()

    # Parser callbacks
    @staticmethod
    def formatPostReference(postid, prependGt = True):
        post = Post.getPost(postid)
        if post:
            parentid = post.parentid
            linkText = '%s%s' % (prependGt and '&gt;&gt;' or '', postid)
            linkUrl = h.postUrl(parentid, postid)
            return '<a href="%s" onclick="highlight(%s)">%s</a>' % (linkUrl, postid, linkText)
        else:
            return "%s%s" % (prependGt and '&gt;&gt;' or '', postid)

