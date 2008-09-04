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
import Image, ImageDraw, ImageFilter, ImageFont
import StringIO
import urllib
import os
import hashlib
import re
import random
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from fc.lib.settings import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class FcpController(OrphieBaseController):
    def __before__(self):
        settingsMap = getSettingsMap()
        c.title = settingsMap['title'].value
        c.devmode = devMode 
        ref = request.headers.get('REFERER', False)
        
        if ref:
            rickroll = True
            for rc in refControlList:
                if rc in ref:
                    rickroll = False
                
            if (rickroll):
                redir = fakeLinks[random.randint(0, len(fakeLinks) - 1)]
                addLogEntry(LOG_EVENT_RICKROLLD, "Request rickrolld. Referer: %s, Redir: %s, IP: %s, User-Agent: %s" % (ref, redir, request.environ["REMOTE_ADDR"], request.headers.get('User-Agent', '?')))                
                redirect_to(redir)
        
    def login(self, user):
        session['uidNumber'] = user.uidNumber
        session.save()
        
    def logout(self):
        session.delete()        
        redirect_to('/')
        
    def createCaptcha(self):
        meta.Session.commit() 
        captcha = Captcha()
        captcha.text = self.randomStr()
        meta.Session.save(captcha)
        meta.Session.commit()                

        return captcha
        
    def randomStr(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        min = 5
        max = 6
        str=''
        
        for x in random.sample(alphabet,random.randint(min,max)):
            str+=x
            
        return str
        
    def captchaPic(self, cid):
        captcha = meta.Session.query(Captcha).filter(Captcha.id==cid).first()  
        if not captcha:
            return 'Id problem'
        else:
            text = captcha.text
            pw = 300
            ph = 80
            im = Image.new('RGB', (pw, ph), 'orange')
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype(captchaFont, 64)
            w = font.getsize(text)[0]
            h = font.getsize(text)[1]
            draw.text(((pw - w)/2 + random.randrange(-20, 20), (ph - h)/2 + random.randrange(-10, 10)), captcha.text, font=font)
            im = im.filter(ImageFilter.BLUR)
            #im = im.filter(ImageFilter.MinFilter)
            
            f = StringIO.StringIO()
            im.save(f, "PNG")
            pic = f.getvalue()
            response.headers['Content-Length'] = len(pic)
            response.headers['Content-Type'] = 'image/png'

            return pic
        
    def authorize(self, url):
        if url:
            c.currentURL = '/' + str(url.encode('utf-8')) + '/'
        else:
            c.currentURL = '/'
        
        ip = request.environ["REMOTE_ADDR"]
        tracker = meta.Session.query(LoginTracker).filter(LoginTracker.ip==ip).first()
        if not tracker:
            tracker = LoginTracker()
            tracker.ip = ip
            tracker.attempts = 0
            tracker.lastAttempt = datetime.datetime.now()              
            meta.Session.save(tracker)  
            meta.Session.commit()
            #log.debug('new tracker')
                    
        captchaOk = True
        captcha = False

        if tracker.attempts>=2:
            c.showCaptcha = True
            captchaOk = False
            
            if tracker.cid:
                captcha = meta.Session.query(Captcha).filter(Captcha.id==tracker.cid).first()            

            if not captcha:
                captcha = self.createCaptcha()
                tracker.cid = captcha.id
                meta.Session.commit()
                #log.debug('new captcha')
                
            c.captid = tracker.cid
            #log.debug('captcha')
                
        if request.POST.get('code', False):
            code = self.genUid(request.POST['code'].encode('utf-8')) #hashlib.sha512(request.POST['code'].encode('utf-8') + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
            user = meta.Session.query(User).options(eagerload('options')).filter(User.uid==code).first()
                        
            #log.debug(code)            

            captid = request.POST.get('captid', False)
            captval = request.POST.get('captcha', False)      
            #log.debug("%s:%s" %(captid, captval))
             
            if (not captchaOk) and captid and captval and isNumber(captid): 
                if captcha:
                    captchaOk = (captcha.text == captval)
                    meta.Session.delete(captcha)
                    if not captchaOk:
                        #log.debug('recreated captcha')                    
                        captcha = self.createCaptcha()
                        tracker.cid = captcha.id                    
                    #log.debug('captdel')
                
            if user and captchaOk:
                meta.Session.delete(tracker)
                self.login(user)
            else:
                tracker.attempts += 1    
                tracker.lastAttempt = datetime.datetime.now()  

            meta.Session.commit()
            #log.debug(c.currentURL)
            redirect_to(c.currentURL)                
        
        c.boardName = _('Login')
        return self.render('login')
        
    def register(self, invite):
        if 'invite' not in session:
            invite_q = meta.Session.query(Invite).filter(Invite.invite==invite).first()
            if invite_q:
                meta.Session.delete(invite_q)
                meta.Session.commit()
                session['invite'] = invite
                session['iid'] = invite_q.id
                session.save()
            else:
                c.currentURL = '/'
                return self.render('login')
                
        key = request.POST.get('key','').encode('utf-8')
        key2 = request.POST.get('key2','').encode('utf-8')
            
        if key:
            if len(key)>=minPassLength and key == key2:      
                uid = self.genUid(key) #hashlib.sha512(key + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
                user = meta.Session.query(User).options(eagerload('options')).filter(User.uid==uid).first()
                if user:
                    self.banUser(user, 7777, "Your Security Code was used during registration by another user. Contact administrator immediately please.")
                    del session['invite']
                    del session['iid']
                    c.boardName = _('Error')
                    c.errorText = _("You entered already existing password. Previous account was banned. Contact administrator please.")
                    return self.render('error')
            
                user = User()
                user.uid = uid
                meta.Session.save(user)
                addLogEntry(LOG_EVENT_INVITE_USED, "Used invite #%d" % (session['iid']))                
                meta.Session.commit()
                del session['invite']
                del session['iid']
                session.save()
                self.login(user)
                redirect_to('/')
        c.boardName = _('Register')
        return self.render('register')
        
    def oekakiSave(self, environ, start_response, url, tempid):
        start_response('200 OK', [('Content-Type','text/plain'),('Content-Length','2')])
        oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
        cl = int(request.environ['CONTENT_LENGTH'])
        if oekaki and cl:
            id = request.environ['wsgi.input'].read(1)
            if id == 'S':
                headerLength = int(request.environ['wsgi.input'].read(8))
                header = request.environ['wsgi.input'].read(headerLength)
                bodyLength = int(request.environ['wsgi.input'].read(8))
                request.environ['wsgi.input'].read(2)
                body = request.environ['wsgi.input'].read(bodyLength)
                headers = header.split('&')
                type = filterText(headers[0].split('=')[1])
                time = headers[1].split('=')[1]
                localFilePath = os.path.join(uploadPath, tempid + '.' + type)
                localFile = open(localFilePath,'wb')
                localFile.write(body)
                localFile.close()
                oekaki.time = time
                oekaki.path = tempid + '.' + type
                meta.Session.commit()
        return ['ok']
        
    def banned(self):
        self.userInst = FUser(session.get('uidNumber',-1))
        c.userInst = self.userInst
        if self.userInst.isBanned():
            c.boardName = _('Banned')
            return self.render('banned')
        else:
            c.boardName = _('Error')
            c.errorText = _("ORLY?")
            return self.render('error')
            
    def UnknownAction(self):      
        c.boardName = _('Error')
        c.errorText = _("Excuse me, WTF are you?")
        return self.render('error')
    
