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
import string
import re
from fc.lib.miscUtils import *
from fc.lib.FakeUser import FakeUser
from fc.lib.constantValues import *

log = logging.getLogger(__name__)

class OrphieBaseController(BaseController):
    def __before__(self):
        if g.OPT.devMode:
            c.log = []
            c.sum = 0

        self.userInst = False
        uid = self.sessUid()
        if uid > 0 and g.OPT.allowLogin:
            self.userInst = User.getUser(uid)
        if not self.userInst:
            self.userInst = FakeUser()

        c.userInst = self.userInst
        c.uidNumber = self.userInst.uidNumber
        #log.debug(session.get('uidNumber', -1))
        if g.OPT.checkUAs and self.userInst.isValid() and not self.userInst.Anonymous:
            for ua in g.OPT.badUAs:
                if filterText(request.headers.get('User-Agent', '?')).startswith(ua):
                    self.userInst.ban(2, _("[AUTOMATIC BAN] Security alert type 1: %s") %  hashlib.md5(ua).hexdigest(), -1)
                    break
    def sessUid(self):
        if g.OPT.allowLogin:
            return session.get('uidNumber', -1)
        return -1

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

        #log.debug(request.cookies.get('fc',''))
        #log.debug(request.cookies)
        sessCookie = request.cookies.get('fc', '')
        if sessCookie:
            response.set_cookie('fc', str(sessCookie), domain='.'+g.OPT.baseDomain)

        c.menuLinks = g.additionalLinks
        c.sectionNames = g.sectionNames

        if self.userInst.Anonymous:
            anonCaptId = session.get('anonCaptId', False)
            if not anonCaptId or not Captcha.exists(anonCaptId):
                #log.debug('recreate')
                captcha = Captcha.create()
                session['anonCaptId'] = captcha.id
                session.save()
                c.captcha = captcha
            else:
                c.captcha = Captcha.getCaptcha(anonCaptId)

            remPassCookie = request.cookies.get('orhpieRemPass', randomStr())
            c.remPass = remPassCookie
            response.set_cookie('orhpieRemPass', str(remPassCookie), max_age=3600)

    def render(self, page, **options):
        tname = 'std'
        tpath = "%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        c.actuator = "actuators/%s/" % (g.OPT.actuator)
        c.actuatorTest = c.actuator

        try:
            if self.userInst and not self.userInst.isBanned():
                tname = self.userInst.template()
                tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
                c.actuatorTest = "%s/actuators/%s/" % (tname, g.OPT.actuator)
        except: #userInst not defined or user banned
            pass

        fpath = os.path.join(g.OPT.templPath, tpath)
        #TODO: it may be excessive
        if page and os.path.isfile(fpath) and os.path.abspath(fpath).replace('\\', '/')== fpath.replace('\\', '/'):
            return render('/'+tpath, **options)
        else:
            abort(404) #return _("Template problem: " + page)

    def showStatic(self, page):
        c.boardName = _(page)
        return self.render('static.%s' % page) #render('/%s.static.mako' % self.userInst.template())

    def paginate(self, count, page, tpp):
        if count > 1:
            p = divmod(count, tpp)
            c.pages = p[0]
            if p[1]:
                c.pages += 1
            if (page + 1) > c.pages:
                page = c.pages - 1
            c.page = page

            if c.pages>15:
                c.showPagesPartial = True
                if c.page-5>1:
                    c.leftPage = c.page-5
                else:
                    c.leftPage=2

                if c.page+5<c.pages-2:
                    c.rightPage = c.page+5
                else:
                    c.rightPage=c.pages-2
        elif count == 1:
            c.page  = False
            c.pages = False
        elif count == 0:
            c.page  = False
            c.pages = False
        c.count = count

    def currentUserCanPost(self):
        return g.OPT.allowPosting and self.userInst and ((self.userInst.Anonymous and g.OPT.allowAnonymousPosting) or not self.userInst.Anonymous)

    def currentUserIsAuthorized(self):
        return self.userInst.isValid() and (self.sessUid() == self.userInst.uidNumber)

    # Parser callbacks

    def formatPostReference(self, postid, prependGt = True):
        post = Post.getPost(postid)
        if post:
            parentid = post.parentid
            linkText = '%s%s' % (prependGt and '&gt;&gt;' or '', postid)
            linkUrl = h.postUrl(parentid, postid)
            return '<a href="%s" onclick="highlight(%s)">%s</a>' % (linkUrl, postid, linkText)
        else:
            return "%s%s" % (prependGt and '&gt;&gt;' or '', postid)

