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
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *

log = logging.getLogger(__name__)

class OrphieBaseController(BaseController):
    def __before__(self):
        if g.OPT.devMode:
            c.log = []
            c.sum = 0

        self.userInst = FUser(session.get('uidNumber', -1))
        c.userInst = self.userInst
        #log.debug(session.get('uidNumber', -1))
        if g.OPT.checkUAs and self.userInst.isValid():
            for ua in g.OPT.badUAs:
                if filterText(request.headers.get('User-Agent', '?')).startswith(ua):
                    self.banUser(meta.Session.query(User).filter(User.uidNumber == self.userInst.uidNumber()).first(), 2, _("[AUTOMATIC BAN] Security alert type 1: %s") %  hashlib.md5(ua).hexdigest())
                    break

    def initEnvironment(self):
        c.title = g.settingsMap['title'].value
        boards = meta.Session.query(Tag).join('options').filter(TagOptions.persistent==True).order_by(TagOptions.sectionId).all()
        c.boardlist = []
        sectionId = 0
        section = []
        for b in boards:
            if not sectionId:
                sectionId = b.options.sectionId
                section = []
            if sectionId != b.options.sectionId:
                c.boardlist.append(section)
                sectionId = b.options.sectionId
                section = []
            bc = empty()
            bc.tag = b.tag
            bc.comment = b.options.comment
            section.append(bc) #b.tag)
        if section:
            c.boardlist.append(section)

        #log.debug(request.cookies.get('fc',''))
        #log.debug(request.cookies)
        sessCookie = request.cookies.get('fc','')
        response.set_cookie('fc', str(sessCookie), domain='.'+g.OPT.baseDomain)

        c.menuLinks = []
        linksstr = g.settingsMap['additionalLinks'].value
        links = linksstr.split(',')
        if links:
            for link in links:
                c.menuLinks.append(link.split('|'))

        if self.userInst.Anonymous:
            anonCaptId = session.get('anonCaptId', False)
            if not anonCaptId or not Captcha.exists(anonCaptId):
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


    def banUser(self, user, bantime, banreason):
        if len(banreason)>1:
            if isNumber(bantime) and int(bantime) > 0:
                bantime = int(bantime)
                if bantime > 10000:
                    bantime = 10000
                user.options.bantime = bantime
                user.options.banreason = banreason
                user.options.banDate = datetime.datetime.now()
                toLog(LOG_EVENT_USER_BAN, _('Banned user %s for %s days for reason "%s"') % (user.uidNumber, bantime, banreason))
                meta.Session.commit()
                return _('User was banned')
            else:
                return _('You should specify ban time in days')
        else:
            return _('You should specify ban reason')

    def conjunctTagOptions(self, tags):
        options = empty()
        optionsFlag = True
        rulesList = []
        for t in tags:
            if t.options:
                if optionsFlag:
                    options.imagelessThread = t.options.imagelessThread
                    options.imagelessPost   = t.options.imagelessPost
                    options.images   = t.options.images
                    options.enableSpoilers = t.options.enableSpoilers
                    options.maxFileSize = t.options.maxFileSize
                    options.minPicSize = t.options.minPicSize
                    options.thumbSize = t.options.thumbSize
                    options.canDeleteOwnThreads = t.options.canDeleteOwnThreads
                    optionsFlag = False
                else:
                    options.imagelessThread = options.imagelessThread & t.options.imagelessThread
                    options.imagelessPost = options.imagelessPost & t.options.imagelessPost
                    options.enableSpoilers = options.enableSpoilers & t.options.enableSpoilers
                    options.canDeleteOwnThreads = options.canDeleteOwnThreads & t.options.canDeleteOwnThreads
                    options.images = options.images & t.options.images

                    perm = g.OPT.permissiveFileSizeConjunction
                    if (perm and t.options.maxFileSize > options.maxFileSize) or (not perm and t.options.maxFileSize < options.maxFileSize):
                        options.maxFileSize = t.options.maxFileSize

                    if t.options.minPicSize > options.minPicSize:
                        options.minPicSize = t.options.minPicSize
                    if t.options.thumbSize < options.thumbSize:
                        options.thumbSize = t.options.thumbSize

                tagRulesList = t.options.specialRules.split(';')
                for rule in tagRulesList:
                    if rule and not rule in rulesList:
                        rulesList.append(rule)

        options.rulesList = rulesList

        if optionsFlag:
            options.imagelessThread = g.OPT.defImagelessThread
            options.imagelessPost   = g.OPT.defImagelessPost
            options.images = g.OPT.defImages
            options.enableSpoilers = g.OPT.defEnableSpoilers
            options.canDeleteOwnThreads = g.OPT.defCanDeleteOwnThreads
            options.maxFileSize = g.OPT.defMaxFileSize
            options.minPicSize = g.OPT.defMinPicSize
            options.thumbSize = g.OPT.defThumbSize
            options.specialRules = u''
        return options

    def deletePicture(self, post, commit = True):
        pic = self.sqlFirst(meta.Session.query(Picture).filter(Picture.id==post.picid))
        refcount = self.sqlCount(Post.query.filter(Post.picid==post.picid))
        if pic and refcount == 1:
            filePath = os.path.join(g.OPT.uploadPath, pic.path)
            thumPath = os.path.join(g.OPT.uploadPath, pic.thumpath)

            if os.path.isfile(filePath):
                os.unlink(filePath)

            ext = pic.extension
            if not ext.path:
                if os.path.isfile(thumPath):
                    os.unlink(thumPath)
            meta.Session.delete(pic)
            if commit:
                meta.Session.commit()
        return pic

    def processDelete(self, postid, fileonly=False, checkOwnage=True, reason = "???", rempPass = False):
        p = self.sqlGet(Post.query, postid)

        opPostDeleted = False
        if p:
            if self.userInst.Anonymous and p.removemd5 != rempPass:
                return False

            if checkOwnage and not (p.uidNumber == self.userInst.uidNumber() or self.userInst.canDeleteAllPosts()):
                # print some error stuff here
                return False

            threadRemove = True
            tags = p.tags
            if p.parentid>0:
                parentp = p.parentPost #self.sqlGet(Post.query, p.parentid)
                tags = parentp.tags
                threadRemove = False

            tagline = u''
            taglist = []
            for tag in tags:
                taglist.append(tag.tag)

                tag.replyCount -= 1
                if threadRemove:
                    tag.threadCount -= 1
            tagline = ', '.join(taglist)

            postOptions = self.conjunctTagOptions(p.parentid>0 and parentp.tags or p.tags)
            if checkOwnage and not p.uidNumber == self.userInst.uidNumber():
                logEntry = u''
                if p.parentid>0:
                    logEntry = _("Deleted post %s (owner %s); from thread: %s; tagline: %s; reason: %s") % (p.id, p.uidNumber, p.parentid, tagline, reason)
                else:
                    logEntry = _("Deleted thread %s (owner %s); tagline: %s; reason: %s") % (p.id, p.uidNumber, tagline, reason)
                if fileonly:
                    logEntry += " %s" % _("(file only)")
                toLog(LOG_EVENT_POSTS_DELETE, logEntry)

            if p.parentid == -1 and not fileonly:
                if not (postOptions.canDeleteOwnThreads or self.userInst.canDeleteAllPosts()):
                    return False
                opPostDeleted = True
                for post in self.sqlAll(Post.query.filter(Post.parentid==p.id)):
                    self.processDelete(postid=post.id, checkOwnage=False)

            pic = self.deletePicture(p, False)

            if fileonly and postOptions.imagelessPost:
                if pic:
                    p.picid = -1
            else:
                invisBumpDisabled = (g.settingsMap['invisibleBump'].value == 'false')
                parent = self.sqlFirst(Post.query.filter(Post.id==p.parentid))
                if parent:
                    parent.replyCount -= 1

                if invisBumpDisabled and p.parentid != -1:
                    thread = self.sqlAll(Post.query.filter(Post.parentid==p.parentid))
                    if thread and thread[-1].id == p.id: #wut?
                        if len(thread) > 1 and not thread[-2].sage:
                            parent.bumpDate = thread[-2].date
                        else:
                            parent.bumpDate = parent.date

                meta.Session.delete(p)
        meta.Session.commit()
        return opPostDeleted

    def passwd(self, key, key2, adminRights = False, currentKey = False, user = False):
        newuid = User.genUid(key)
        olduid = self.userInst.uid()
        if user:
            olduid = user.uid

        if key == key2 and newuid != olduid and len(key) >= g.OPT.minPassLength:
            if not (adminRights or User.genUid(currentKey) == olduid):
                c.boardName = _('Error')
                c.errorText = _("You have entered incorrect current security code!")
                return self.render('error')

            anotherUser = self.sqlFirst(meta.Session.query(User).options(eagerload('options')).filter(User.uid==newuid))
            if not anotherUser:
                if not user:
                    self.userInst.uid(newuid)
                else:
                    user.uid = newuid
                c.profileMsg = _('Password was successfully changed.')
                return True
            else:
                if not adminRights:
                    currentUser = self.sqlFirst(meta.Session.query(User).options(eagerload('options')).filter(User.uid==olduid))
                    self.banUser(currentUser, 7777, "Your are entered already existing Security Code. Contact administrator immediately please.")
                    self.banUser(anotherUser, 7777, "Your Security Code was used during profile update by another user. Contact administrator immediately please.")
                    c.boardName = _('Error')
                    c.errorText = _("You entered already existing Security Code. Both accounts was banned. Contact administrator please.")
                    return self.render('error')
                else:
                    c.boardName = _('Error')
                    c.errorText = _("You entered already existing Security Code.")
                    return self.render('error')
        return False

    def getParentID(self, id):
        post = self.sqlFirst(Post.query.filter(Post.id==id))
        if post:
           return post.parentid
        else:
           return False

    def isPostOwner(self, id):
        post = self.sqlFirst(Post.query.filter(Post.id==id))
        if post and post.uidNumber == self.userInst.uidNumber():
           return post.parentid
        else:
           return False

    def postOwner(self, id):
        post = self.sqlFirst(Post.query.filter(Post.id==id))
        if post:
           return post.parentid
        else:
           return False

    def formatPostReference(self, postid, parentid = False): # TODO FIXME: move to parser
        if not parentid:
            parentid = self.getParentID(postid)

        #if parentid == -1:
        #    return '<a href="/%s">&gt;&gt;%s</a>' % (postid, postid)
        #else:
        # We will format all posts same way. Why not?
        #Also, changed to /postid#ipostid instead of /parentid#ipostid.
        #Forget it, changed back.
        return '<a href="/%s#i%s" onclick="highlight(%s)">&gt;&gt;%s</a>' % (parentid>0 and parentid or postid, postid, postid, postid)
