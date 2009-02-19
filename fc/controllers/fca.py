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
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class FcaController(OrphieBaseController):
    def __before__(self):  
        OrphieBaseController.__before__(self)  
        #self.userInst = FUser(session.get('uidNumber',-1))
        if not self.userInst.isAuthorized():
            c.currentURL = '/holySynod/'
            return redirect_to('/')
        self.initEnvironment()
        if not self.userInst.isAdmin():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('/')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('/')            
            
    def index(self):
        c.boardName = 'Index'
        c.admins = meta.Session.query(User).join('options').filter(or_(UserOptions.isAdmin==True,UserOptions.canDeleteAllPosts==True)).all()
        return self.render('adminIndex') 
        
    def manageSettings(self):
        c.boardName = 'Settings management'
        #settingsMap = getSettingsMap()
        
        if request.POST.get('update', False):
            for s in request.POST:
                if s in settingsDef:
                    if g.settingsMap[s].value != request.POST[s]:
                        addLogEntry(LOG_EVENT_SETTINGS_EDIT,"Changed %s from '%s' to '%s'" % (s, g.settingsMap[s].value,request.POST[s]))
                        val = filterText(request.POST[s])
                        setting = meta.Session.query(Setting).filter(Setting.name==s).first()
                        setting.value = val                        
                        g.settingsMap[s].value = val
            meta.Session.commit()
            c.message = _('Updated settings')
        #c.settings = settingsMap
        return self.render('manageSettings') 
        
    def manageBoards(self):
        c.boardName = 'Boards management'
        boards = meta.Session.query(Tag).options(eagerload('options')).all()
        c.boards = {999:[]}
        for b in boards:
            if b.options and b.options.persistent and b.options.sectionId:
                if not b.options.sectionId in c.boards:
                    c.boards[b.options.sectionId]=[]
                c.boards[b.options.sectionId].append(b)
            else:
                c.boards[999].append(b)
        bs = {}
        for key in sorted(c.boards.iterkeys()):
            bs[key] = c.boards[key]
        c.boards = bs
        return self.render('manageBoards')
        
    def editBoard(self,tag):
        c.boardName = 'Edit board'
        c.message = u''
        c.tag = meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag==tag).first()
        if not c.tag:
            c.tag = Tag(tag)
        if not c.tag.options:
            c.tag.options = TagOptions()
            c.tag.options.comment = u''
            c.tag.options.sectionId = 0
            c.tag.options.persistent = False
            c.tag.options.imagelessThread = g.OPT.defImagelessThread
            c.tag.options.imagelessPost = g.OPT.defImagelessPost
            c.tag.options.images = g.OPT.defImages
            c.tag.options.enableSpoilers = g.OPT.defEnableSpoilers
            c.tag.options.canDeleteOwnThreads = g.OPT.defCanDeleteOwnThreads
            c.tag.options.maxFileSize = g.OPT.defMaxFileSize
            c.tag.options.minPicSize = g.OPT.defMinPicSize
            c.tag.options.thumbSize = g.OPT.defThumbSize
            c.tag.options.specialRules = u''
        if request.POST.get('tag',False):
            newtag = request.POST.get('tag',False)
            newtagre = re.compile(r"""([^,@~\#\+\-\&\s\/\\\(\)<>'"%\d][^,@~\#\+\-\&\s\/\\\(\)<>'"%]*)""").match(newtag)
            if newtagre:
                newtag = newtagre.groups()[0]
                newtagRecord = meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag==newtag).first()
                if not newtagRecord or newtagRecord.id == c.tag.id:
                    if c.tag.tag != newtag:
                        oldtag = c.tag.tag
                        c.tag.tag = newtag
                    else:
                        oldtag = u''
                    c.tag.options.comment = filterText(request.POST.get('comment', u''))
                    c.tag.options.specialRules = filterText(request.POST.get('specialRules', u''))                    
                    c.tag.options.sectionId = request.POST.get('sectionId',0)
                    c.tag.options.persistent = request.POST.get('persistent',False)
                    c.tag.options.imagelessThread = request.POST.get('imagelessThread',False)
                    c.tag.options.imagelessPost = request.POST.get('imagelessPost',False)
                    c.tag.options.images = request.POST.get('images',False)
                    c.tag.options.enableSpoilers = request.POST.get('spoilers',False)
                    c.tag.options.canDeleteOwnThreads = request.POST.get('canDeleteOwnThreads',False)
                    c.tag.options.maxFileSize = request.POST.get('maxFileSize',3145728)
                    c.tag.options.minPicSize = request.POST.get('minPicSize',0)
                    c.tag.options.thumbSize = request.POST.get('thumbSize',250)
                    
                    if request.POST.get('deleteBoard', False) and c.tag.id:
                        count = Post.query.filter(Post.tags.any(tag=tag)).count()
                        if count>0:
                            c.message = _("Board must be empty for deletion")                        
                        else:
                            meta.Session.delete(c.tag)        
                            addLogEntry(LOG_EVENT_BOARD_EDIT, "Deleted board %s %s" % (newtag, oldtag and ("(that was renamed from %s)"%oldtag) or ""))
                            meta.Session.commit()                              
                            return redirect_to('/holySynod/manageBoards/')                       
                    elif not c.tag.id:                    
                        meta.Session.add(c.tag)                        
                        
                    c.message = _("Updated board")    
                    addLogEntry(LOG_EVENT_BOARD_EDIT, "Edited board %s %s" % (newtag,oldtag and ("(renamed from %s)"%oldtag) or ""))                        
                    meta.Session.commit()                       
                                        
                else:
                    c.message = _("Board %s already exists!") % newtag
            else:
                c.message = _("Board name should be non-empty and should contain only valid symbols")
        return self.render('editBoard')
        
    def manageUsers(self):
        c.boardName = 'Users management'
        uid = request.POST.get("uid", False)
        if uid:            
            user = False
            if isNumber(uid):
                user = meta.Session.query(User).filter(User.uidNumber==uid).first()               
            else:
                user = meta.Session.query(User).filter(User.uid==uid).first()
            if user:
                return redirect_to('/holySynod/manageUsers/edit/%s' % user.uidNumber)
            else:
                c.message = _('No such user exists.')
        return self.render('manageUsers')
        
    def editUserAttempt(self, pid):
        c.boardName = 'User edit attemption'
        c.pid = pid
        return self.render('editUserAttempt')
        
    def editUserByPost(self, pid):
        post = Post.query.options(eagerload('file')).filter(Post.id==pid).order_by(Post.id.asc()).first()
        if post:
            reason = request.POST.get("UIDViewReason", 'No reason given!')
            addLogEntry(LOG_EVENT_USER_GETUID, "Viewed UID for user '%s' from post '<a href='/%s#i%s'>%s</a>'. Reason: %s" % (post.uidNumber, post.parentid > 0 and post.parentid or post.id, pid, pid, reason))
            return redirect_to('/holySynod/manageUsers/edit/%s' % post.uidNumber)
        else:
            c.errorText = _("Post not found")
            return self.render('error')
        
    def editUser(self,uid):
        c.boardName = 'Edit user %s' % uid
        user = meta.Session.query(User).options(eagerload('options')).get(uid)
        if user:
            c.user = user
            c.userInst = self.userInst
            if request.POST.get('access', False) and self.userInst.canChangeRights():
                canDeleteAllPosts = request.POST.get('canDeleteAllPosts',False) and True or False
                if user.options.canDeleteAllPosts != canDeleteAllPosts:
                    user.options.canDeleteAllPosts = canDeleteAllPosts
                    addLogEntry(LOG_EVENT_USER_ACCESS,_('Changed user %s canDeleteAllPosts to %s') % (user.uidNumber,canDeleteAllPosts))
                isAdmin = request.POST.get('isAdmin',False) and True or False
                if user.options.isAdmin != isAdmin:
                    user.options.isAdmin = isAdmin
                    addLogEntry(LOG_EVENT_USER_ACCESS,_('Changed user %s isAdmin to %s') % (user.uidNumber,isAdmin))                
                canMakeInvite = request.POST.get('canMakeInvite',False) and True or False
                if user.options.canMakeInvite != canMakeInvite:
                    user.options.canMakeInvite = canMakeInvite
                    addLogEntry(LOG_EVENT_USER_ACCESS,_('Changed user %s canMakeInvite to %s') % (user.uidNumber,canMakeInvite))                
                canChangeRights = request.POST.get('canChangeRights',False) and True or False
                if user.options.canChangeRights != canChangeRights:
                    user.options.canChangeRights = canChangeRights
                    addLogEntry(LOG_EVENT_USER_ACCESS,_('Changed user %s canChangeRights to %s') % (user.uidNumber,canChangeRights))                                    
                c.message = _('User access was changed')
            elif request.POST.get('ban', False):
                if user.options.bantime > 0:
                    c.message = _('This user is already banned')
                else:
                    banreason = filterText(request.POST.get('banreason','???'))
                    bantime = request.POST.get('bantime','0')
                    c.message = self.banUser(user, bantime, banreason)
            elif request.POST.get('unban',False):
                if user.options.bantime > 0:
                    banreason = user.options.banreason
                    bantime = user.options.bantime
                    user.options.bantime = 0
                    user.options.banreason = u''
                    addLogEntry(LOG_EVENT_USER_UNBAN,_('Unbanned user %s (%s days for reason "%s")') % (user.uidNumber,bantime,banreason))
                    c.message = _('User was unbanned')
                else:
                    c.message = _('This user is not banned')
            elif request.POST.get('lookup', False):
                reason = filterText(request.POST.get('lookupreason', u''))
                quantity = int(request.POST.get('quantity', '0'))
                if isNumber(quantity) and int(quantity) > 0:
                    if len(reason) > 1:
                        c.posts = Post.query.filter(Post.uidNumber==user.uidNumber).order_by(Post.date.desc())[:quantity]
                        addLogEntry(LOG_EVENT_USER_DELETE,_('Performed posts lookup for user %s for "%s", quantity: %s') % (user.uidNumber, reason, quantity))
                        if c.posts:
                            return self.render('postsLookup')
                        else:
                            c.message = _('No posts found')
                    else:
                        c.message = _('You should specify lookup reason')
                else:
                    c.message = _('Incorrect quantity value')
            elif request.POST.get('passwd', False):
                key = request.POST.get('key','').encode('utf-8')
                key2 = request.POST.get('key2','').encode('utf-8')
                # XXX: temporary code. Methods from OrphieBaseController must be moved into model
                passwdRet = self.passwd(key, key2, True, False, user)
                meta.Session.commit()
                if passwdRet == False:
                    c.message = _('Incorrect security codes')
                elif passwdRet != True:
                    return passwdRet
                else:
                    addLogEntry(LOG_EVENT_USER_PASSWD,_('Changed password for user "%s"') % (user.uidNumber))
                    c.message = _('Security code changed')
            elif request.POST.get('delete', False):
                reason = filterText(request.POST.get('deletereason', u''))
                deleteLegacy = request.POST.get('deleteLegacy', False)
                if self.userInst.canChangeRights():
                    if len(reason)>1:
                        if deleteLegacy:
                            posts = self.sqlAll(Post.query.filter(Post.uidNumber==user.uidNumber))
                            removed = []
                            for post in posts:
                                if post.parentid == -1:
                                    removed.append(str(post.id))
                                else:
                                    removed.append("%d/%d" % (post.id, post.parentid))
                                    
                                self.processDelete(post.id, False, False, reason)
                            addLogEntry(LOG_EVENT_USER_DELETE,_('Removed legacy of %s for "%s" [%s]') % (user.uidNumber, reason, ', '.join(removed)))
                        meta.Session.delete(user)
                        addLogEntry(LOG_EVENT_USER_DELETE,_('Deleted user %s for "%s"') % (user.uidNumber,reason))
                        c.message = "User deleted"
                        return self.render('manageUsers')
                    else:
                        c.message = _('You should specify deletion reason')
                else:
                    c.message = "You haven't rights to delete user"
            return self.render('editUser')
        else:
            c.errorText = _('No such user exists.')
            return self.render('error')
            
    def manageExtensions(self):
        c.extensions = meta.Session.query(Extension).order_by(Extension.type).all()
        return self.render('manageExtensions')
        
    def editExtension(self, ext):
        if not ext:
            ext = ''
        ext = filterText(request.POST.get('ext', ext))
        if len(ext) > 10:
            ext = ''
            
        c.ext = meta.Session.query(Extension).filter(Extension.ext==ext).first()
        if not c.ext:
            c.ext = Extension()
            c.ext.ext = ext
            c.ext.path = ''
            c.ext.thwidth = 0
            c.ext.thheight= 0
            c.ext.type = 'image'
            
        if request.POST.get('ext', False):
            c.ext.path = filterText(request.POST.get('path', ''))
            c.ext.thwidth = request.POST.get('thwidth', 0)
            c.ext.thheight = request.POST.get('thheight', 0)
            c.ext.type = filterText(request.POST.get('type', 'image'))
            if not c.ext.id:
                meta.Session.add(c.ext)
            meta.Session.commit()
            addLogEntry(LOG_EVENT_EXTENSION_EDIT, _('Edited extension %s') % c.ext.ext)
            c.message = _('Extension edited')
        return self.render('editExtension')
        
    def manageQuestions(self):
        c.boardName = 'Questions management'
        return self.render('manageQuestions')   
        
    def manageApplications(self):
        c.boardName = 'Applications management'
        return self.render('manageApplications')  
        
    def viewLog(self, page):
        c.boardName = 'Logs'
        page = int(page)
        count = meta.Session.query(LogEntry).count()
        p = divmod(count, 100)
        c.pages = p[0]
        if p[1]:
            c.pages += 1
        if (page + 1) > c.pages:
            page = c.pages - 1
        c.page = page        
        c.logs = meta.Session.query(LogEntry).options(eagerload('user')).order_by(LogEntry.date.desc())[page*100:(page+1)*100]
        return self.render('adminLogs')

    def manageMappings(self, act, id, tagid):
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
                    tag = meta.Session.query(Tag).filter(Tag.tag==tagName).first()
                    if tag:
                        tagid = tag.id                
        else:
            c.errorText = _("Incorrect input values")            
            return self.render('error')        
    
        if act == 'show':      
            if id and id > 0:
                post = Post.query.filter(Post.id==id).first()  
                if post and post.parentid == -1:
                    c.post = post      
                else:
                    c.errorText = _("This is not op-post")
                    return self.render('error')   
            
            return self.render('adminMappings')                                              
        elif act in ['del', 'add']:                 
            post = Post.query.filter(Post.id==id).first()  
            if post and post.parentid == -1:        
                if act == 'del' and tagid > 0:
                    if len(post.tags) > 1:
                        tag = meta.Session.query(Tag).filter(Tag.id==tagid).first()
                        tag.threadCount -= 1
                        tag.replyCount -= post.replyCount
                        addLogEntry(LOG_EVENT_EDITEDPOST,_('Removed tag %s from post %d') % (tag.tag, post.id))                        
                        post.tags.remove(tag)  
                    else:
                        c.errorText = "Can't delete last tag!"
                        return self.render('error')
                elif act == 'add':
                    tag = meta.Session.query(Tag).filter(Tag.id==tagid).first()
                    if tag:
                        addLogEntry(LOG_EVENT_EDITEDPOST,_('Added tag %s to post %d') % (tag.tag, post.id))                        
                        post.tags.append(tag)
                        tag.threadCount += 1
                        tag.replyCount += post.replyCount
                    else:
                        c.errorText = _("Non-existent tag")
                        return self.render('error')   
                
                meta.Session.commit()
                
            redirect_to('/holySynod/manageMappings/show/%d' % id)
        else:
            redirect_to('/holySynod/manageMappings')
            
    def invitePage(self):
        return self.render('invitePage') 
        
    def makeInvite(self):
        if not self.userInst.canMakeInvite():
            c.errorText = "No way! You aren't holy enough!"
            return self.render('error')
        
        c.boardName = _('Invite creation')
        c.inviteCode = False
        reason = request.POST.get('inviteReason', False)
        if reason and len(reason) > 1:
            reason = filterText(reason)
            invite = Invite()
            invite.date = datetime.datetime.now()
            invite.invite = self.genInviteId()
            meta.Session.add(invite)
            meta.Session.commit()
            addLogEntry(LOG_EVENT_INVITE,"Generated invite id %s. Reason: %s" % (invite.id, reason))
            c.inviteCode = invite.invite
        return self.render('newInvite')
