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
        response.set_cookie('fc', request.cookies.get('fc',''), domain='.'+g.OPT.baseDomain)
         
    def render(self, page, **options):
        #log.debug(options)
        #return
        tname = 'std'
        tpath = "%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        
        try:
            if self.userInst and not self.userInst.isBanned():
                tname = self.userInst.template()
                tpath = "%(template)s/%(template)s.%(page)s.mako" % {'template' : tname, 'page' : page}
        except: #userInst not defined or user banned
            pass
        
        if page and os.path.isfile(os.path.join(g.OPT.templPath, tpath)):               
            return render('/'+tpath, **options)
        else:
            return _("Template problem: " + page)
            
    def showStatic(self, page):
        c.boardName = _(page)
        return self.render('static.%s' % page) #render('/%s.static.mako' % self.userInst.template())
        
    def genUid(self, key):
        return hashlib.sha512(key + hashlib.sha512(g.OPT.hashSecret).hexdigest()).hexdigest()    

    def genInviteId(self):
        return hashlib.sha512(str(long(time.time() * 10**7)) + hashlib.sha512(g.OPT.hashSecret).hexdigest()).hexdigest()  
        
    def banUser(self, user, bantime, banreason):
        if len(banreason)>1:
            if isNumber(bantime) and int(bantime) > 0:
                bantime = int(bantime)
                if bantime > 10000:
                    bantime = 10000
                user.options.bantime = bantime
                user.options.banreason = banreason
                user.options.banDate = datetime.datetime.now() 
                addLogEntry(LOG_EVENT_USER_BAN, _('Banned user %s for %s days for reason "%s"') % (user.uidNumber, bantime, banreason))
                meta.Session.commit()
                return _('User was banned')
            else:
                return _('You should specify ban time in days')
        else:
            return _('You should specify ban reason')
        
    def deletePicture(self, post, commit = True):
        pic = self.sqlFirst(meta.Session.query(Picture).filter(Picture.id==post.picid))
        if pic and self.sqlCount(meta.Session.query(Post).filter(Post.picid==post.picid)) == 1:
            filePath = os.path.join(g.OPT.uploadPath, pic.path)
            thumPath = os.path.join(g.OPT.uploadPath, pic.thumpath)
            
            if os.path.isfile(filePath):
                os.unlink(filePath)
                
            ext = self.sqlFirst(meta.Session.query(Extension).filter(Extension.id==pic.extid))
            if not ext.path:
                if os.path.isfile(thumPath): os.unlink(thumPath)
            meta.Session.delete(pic)
            if commit:
                meta.Session.commit()
        return pic
            
    def conjunctTagOptions(self, tags):
        options = TagOptions()
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
                    if t.options.maxFileSize < options.maxFileSize:
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
            options.imagelessThread = True
            options.imagelessPost   = True
            options.images   = True
            options.enableSpoilers = True
            options.canDeleteOwnThreads = True
            options.maxFileSize = 2621440
            options.minPicSize = 50
            options.thumbSize = 180
            options.specialRules = ''
        return options
    
    def processDelete(self, postid, fileonly=False, checkOwnage=True, reason = "???"):
        p = self.sqlGet(meta.Session.query(Post), postid)
                 
        opPostDeleted = False
        if p:
            if checkOwnage and not (p.uidNumber == self.userInst.uidNumber() or self.userInst.canDeleteAllPosts()):
                # print some error stuff here
                return False
            
            if p.parentid>0:  
                parentp = self.sqlGet(meta.Session.query(Post), p.parentid)
                
            postOptions = self.conjunctTagOptions(p.parentid>0 and parentp.tags or p.tags)
            if checkOwnage and not p.uidNumber == self.userInst.uidNumber():
                tagline = ''
                taglist = []
                if p.parentid>0:
                    for tag in parentp.tags:
                        taglist.append(tag.tag)
                    tagline = ', '.join(taglist)
                    log = _("Deleted post %s (owner %s); from thread: %s; tagline: %s; reason: %s") % (p.id, p.uidNumber, p.parentid, tagline, reason)
                else:
                    for tag in p.tags:
                        taglist.append(tag.tag)
                    tagline = ', '.join(taglist)                   
                    log = _("Deleted thread %s (owner %s); tagline: %s; reason: %s") % (p.id, p.uidNumber, tagline, reason)
                addLogEntry(LOG_EVENT_POSTS_DELETE, log)
            
            if p.parentid == -1 and not fileonly:
                if not (postOptions.canDeleteOwnThreads or self.userInst.canDeleteAllPosts()):
                    return False
                opPostDeleted = True
                for post in self.sqlAll(meta.Session.query(Post).filter(Post.parentid==p.id)):
                    self.processDelete(postid=post.id, checkOwnage=False)
                    
            pic = self.deletePicture(p, False)
            
            if fileonly and postOptions.imagelessPost: 
                if pic:
                    p.picid = -1
            else:
                invisBump = (g.settingsMap['invisibleBump'].value == 'false')
                parent = self.sqlFirst(meta.Session.query(Post).filter(Post.id==p.parentid))
                if parent:
                    parent.replyCount -= 1
                        
                if invisBump and p.parentid != -1:
                    thread = self.sqlAll(meta.Session.query(Post).filter(Post.parentid==p.parentid))
                    if thread and thread[-1].id == p.id:
                        if len(thread) > 1:
                            parent.bumpDate = thread[-2].date
                        else:
                            parent.bumpDate = parent.date
                            
                meta.Session.delete(p)
        meta.Session.commit()
        return opPostDeleted
