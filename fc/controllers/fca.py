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
from fc.lib.settings import *

log = logging.getLogger(__name__)

class FcaController(BaseController):
    def __before__(self):
        self.userInst = FUser(session.get('uidNumber',-1))
        if not self.userInst.isAuthorized():
            c.currentURL = '/holySynod/'
            return redirect_to('/')
        initEnvironment()
        if not self.userInst.isAdmin():
            c.errorText = "No way! You aren't holy enough!"
            return redirect_to('/')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('/')
            
    def index(self):
        c.boardName = 'Index'
        c.admins = meta.Session.query(User).join('options').filter(or_(UserOptions.isAdmin==True,UserOptions.canDeleteAllPosts==True)).all()
        return render('/wakaba.adminIndex.mako')
    def manageSettings(self):
        c.boardName = 'Settings management'
        settingsMap = getSettingsMap()
        
        if request.POST.get('update',False):
            for s in request.POST:
                if s in settingsDef:
                    if settingsMap[s].value != request.POST[s]:
                        addLogEntry(LOG_EVENT_SETTINGS_EDIT,"Changed %s from '%s' to '%s'" % (s,settingsMap[s].value,request.POST[s]))
                        settingsMap[s].value = filterText(request.POST[s])
            meta.Session.commit()
            c.message = _('Updated settings')
        c.settings = settingsMap
        return render('/wakaba.manageSettings.mako')
        
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
        return render('/wakaba.manageBoards.mako')
    def editBoard(self,tag):
        c.boardName = 'Edit board'
        c.message = ''
        c.tag = meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag==tag).first()
        if not c.tag:
            c.tag = Tag(tag)
        if not c.tag.options:
            c.tag.options = TagOptions()
            c.tag.options.comment = ''
            c.tag.options.sectionId = 0
            c.tag.options.persistent = False
            c.tag.options.imagelessThread = True
            c.tag.options.imagelessPost = True
            c.tag.options.images = True
            c.tag.options.enableSpoilers = False
            c.tag.options.maxFileSize = 3145728
            c.tag.options.minPicSize = 50
            c.tag.options.thumbSize = 180
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
                        oldtag = ''
                    c.tag.options.comment = filterText(request.POST.get('comment',''))
                    c.tag.options.sectionId = request.POST.get('sectionId',0)
                    c.tag.options.persistent = request.POST.get('persistent',False)
                    c.tag.options.imagelessThread = request.POST.get('imagelessThread',False)
                    c.tag.options.imagelessPost = request.POST.get('imagelessPost',False)
                    c.tag.options.images = request.POST.get('images',False)
                    c.tag.options.enableSpoilers = request.POST.get('spoilers',False)
                    c.tag.options.maxFileSize = request.POST.get('maxFileSize',3145728)
                    c.tag.options.minPicSize = request.POST.get('minPicSize',0)
                    c.tag.options.thumbSize = request.POST.get('thumbSize',250)
                    
                    if request.POST.get('deleteBoard', False) and c.tag.id:
                        count = meta.Session.query(Post).filter(Post.tags.any(tag=tag)).count()
                        if count>0:
                            c.message = _("Board must be empty for deletion")                        
                        else:
                            log.debug('delete')
                            meta.Session.delete(c.tag)                    
                            meta.Session.commit()
                            addLogEntry(LOG_EVENT_BOARD_EDIT,"Deleted board %s %s" % (newtag, oldtag and ("(that was renamed from %s)"%oldtag) or ""))
                            return redirect_to('/holySynod/manageBoards/')                       
                    elif not c.tag.id:
                        meta.Session.save(c.tag)
                        meta.Session.commit()
                        addLogEntry(LOG_EVENT_BOARD_EDIT,"Edited board %s %s" % (newtag,oldtag and ("(renamed from %s)"%oldtag) or ""))
                        c.message = _("Updated board")                       
                else:
                    c.message = _("Board %s already exists!") % newtag
            else:
                c.message = _("Board name should be non-empty and should contain only valid symbols")
        return render('/wakaba.editBoard.mako')
        
    def manageUsers(self):
        c.boardName = 'Users management'
        if request.POST.get("uid",False):
            uid = request.POST.get("uid",False)
            user = meta.Session.query(User).filter(or_(User.uid==uid,User.uidNumber==uid)).first()
            if user:
                return redirect_to('/holySynod/manageUsers/edit/%s' % user.uidNumber)
            else:
                c.message = _('No such user exists.')
        return render('/wakaba.manageUsers.mako')
        
    def editUserAttempt(self, pid):
        c.boardName = 'User edit attemption'
        c.pid = pid
        return render('/wakaba.editUserAttempt.mako')
        
    def editUserByPost(self, pid):
        post = meta.Session.query(Post).options(eagerload('file')).filter(Post.id==pid).order_by(Post.id.asc()).first()
        reason = request.POST.get("UIDViewReason", 'No reason given!')
        addLogEntry(LOG_EVENT_USER_GETUID, "Viewed UID for user '%s' from post '%s'. Reason: %s" % (post.uidNumber, pid, reason))
        return redirect_to('/holySynod/manageUsers/edit/%s' % post.uidNumber)        
        
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
            elif request.POST.get('ban',False):
                if user.options.bantime > 0:
                    c.message = _('This user is already banned')
                else:
                    banreason = filterText(request.POST.get('banreason',''))
                    bantime = request.POST.get('bantime','0')
                    if len(banreason)>1:
                        if isNumber(bantime) and int(bantime) > 0:
                            bantime = int(bantime)
                            user.options.bantime = bantime
                            user.options.banreason = banreason
                            addLogEntry(LOG_EVENT_USER_BAN,_('Banned user %s for %s days for reason "%s"') % (user.uidNumber,bantime,banreason))
                            c.message = _('User was banned')
                        else:
                            c.message = _('You should specify ban time in days')
                    else:
                        c.message = _('You should specify ban reason')
            elif request.POST.get('unban',False):
                if user.options.bantime > 0:
                    banreason = user.options.banreason
                    bantime = user.options.bantime
                    user.options.bantime = 0
                    user.options.banreason = ''
                    addLogEntry(LOG_EVENT_USER_UNBAN,_('Unbanned user %s (%s days for reason "%s")') % (user.uidNumber,bantime,banreason))
                    c.message = _('User was unbanned')
                else:
                    c.message = _('This user is not banned')
            elif request.POST.get('lookup',False):
		        c.message = _('NOT IMPLEMENTED YET')
            elif request.POST.get('delete',False):
                reason = filterText(request.POST.get('deletereason',''))
                if len(reason)>1:
                    meta.Session.delete(user)
                    addLogEntry(LOG_EVENT_USER_DELETE,_('Deleted user %s for "%s"') % (user.uidNumber,reason))
                    c.message = "User deleted"
                    return render('/wakaba.manageUsers.mako')
                else:
                    c.message = _('You should specify deletion reason')
            return render('/wakaba.editUser.mako')
        else:
            c.errorText = _('No such user exists.')
            return render('/wakaba.error.mako')
    def manageExtensions(self):
        c.extensions = meta.Session.query(Extension).order_by(Extension.type).all()
        return render('/wakaba.manageExtensions.mako')
    def editExtension(self,ext):
        if not ext:
            ext = ''
        ext = filterText(request.POST.get('ext',ext))
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
        if request.POST.get('ext',False):
            c.ext.path = filterText(request.POST.get('path',''))
            c.ext.thwidth = request.POST.get('thwidth',0)
            c.ext.thheight = request.POST.get('thheight',0)
            c.ext.type = filterText(request.POST.get('type','image'))
            if not c.ext.id:
                meta.Session.save(c.ext)
            meta.Session.commit()
            addLogEntry(LOG_EVENT_EXTENSION_EDIT,_('Edited extension %s') % c.ext.ext)
            c.message = _('Extension edited')
        return render('/wakaba.editExtension.mako')
    def manageQuestions(self):
        c.boardName = 'Questions management'
        return render('/wakaba.manageQuestions.mako')        
    def manageApplications(self):
        c.boardName = 'Applications management'
        return render('/wakaba.manageApplications.mako')     
    def invitePage(self):
        return render('/wakaba.invitePage.mako') 
    def makeInvite(self):         
        if not self.userInst.canMakeInvite():
            c.errorText = "No way! You aren't holy enough!"
            return render('/wakaba.error.mako') 
        c.boardName = 'Invites'
        invite = Invite()
        invite.date = datetime.datetime.now()
        invite.invite = hashlib.sha512(str(long(time.time() * 10**7)) + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
        meta.Session.save(invite)
        meta.Session.commit()
        addLogEntry(LOG_EVENT_INVITE,"Generated invite id %s. Reason: %s" % (invite.id, filterText(request.POST.get('inviteReason','???'))))
        c.inviteLink = "<a href='/register/%s'>INVITE</a>" % invite.invite
        return render('/wakaba.newInvite.mako')
    def viewLog(self,page):
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
        return render('/wakaba.adminLogs.mako')
