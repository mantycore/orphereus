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
import string
from fc.lib.fuser import FUser
from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class FcpController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.title = g.settingsMap['title'].value
        if g.OPT.refControlEnabled:
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
                    addLogEntry(LOG_EVENT_RICKROLLD, "Request rickrolld. Referer: %s, Redir: %s, IP: %s, User-Agent: %s" % (ref, redir, request.environ["REMOTE_ADDR"], filterText(request.headers.get('User-Agent', '?'))))                
                    redirect_to(redir)
        if (self.userInst and self.userInst.isValid()) or g.OPT.allowAnonymous:
            self.initEnvironment()
        
    def login(self, user):
        session['uidNumber'] = user.uidNumber
        session.save()
        
    def logout(self):
        session.clear()
        session.save()
        session.delete()        
        redirect_to('/')
        
    def createCaptcha(self):
        meta.Session.commit() 
        captcha = Captcha()
        captcha.text = self.randomStr()
        meta.Session.add(captcha)
        meta.Session.commit()                

        return captcha
        
    def randomStr(self):
        alphabet = string.ascii_lowercase + string.digits + '$%#@'
        min = 6
        max = 8
        str=''
        
        for x in random.sample(alphabet,random.randint(min,max)):
            str+=x
            
        return str
           
    def createHatchingTexture(self, density, width, height, fill): # cool procedure, found in google
    # create image and drawing surface
        hatchImage = Image.new("RGBA", (width, height), 0)
        hatchDraw = ImageDraw.Draw(hatchImage)
    # set density
        spacer = int(10 * density)
        doubleSpacer = spacer * 2
   # draw lines
        y1 = 0
        y2 = height
        for x in range(0, width, spacer):
            x1 = x + random.randint(-doubleSpacer, doubleSpacer)
            x2 = x + random.randint(-doubleSpacer, doubleSpacer)
            hatchDraw.line((x1, y1, x2, y2), fill=fill)
        x1 = 0
        x2 = width
        for y in range(0, height, spacer):
            y1 = y + random.randint(-doubleSpacer, doubleSpacer)
            y2 = y + random.randint(-doubleSpacer, doubleSpacer)
            hatchDraw.line((x1, y1, x2, y2), fill=fill)
        return hatchImage        
       
    def captchaPic(self, cid):
        captcha = meta.Session.query(Captcha).filter(Captcha.id==cid).first()  
        
        if not captcha:
            return 'Id problem'
        else:
            out = captcha.content
            if not out:
                text = captcha.text
                pw = 300
                ph = 80
            
                textPic = Image.new('RGBA', (pw, ph), 'orange')
                draw = ImageDraw.Draw(textPic)
                font = ImageFont.truetype(g.OPT.captchaFont, 64)
                w = font.getsize(text)[0]
                h = font.getsize(text)[1]      
                tcolor = (random.randrange(50, 150), random.randrange(50, 150), random.randrange(50, 150))
                draw.text(((pw - w)/2 + random.randrange(-20, 20), (ph - h)/2 + random.randrange(-10, 10)), text, font=font, fill=tcolor)
            
                noisePic = Image.new('RGBA', (pw, ph), 'yellow')            
                draw = ImageDraw.Draw(noisePic)
                pc = random.randrange(20)+10
                for c in range(pc):
                    x1 = random.randrange(0, pw)
                    y1 = random.randrange(0, ph)
                    x2 = random.randrange(x1, pw)
                    y2 = random.randrange(y1, ph)   
                    fcolor=(random.randrange(50,250), random.randrange(50,250), random.randrange(50,250))
                    ocolor=(random.randrange(50,250), random.randrange(50,250), random.randrange(50,250))
                    draw.ellipse((x1, y1, x2, y2), fill=tcolor, outline=ocolor)


                noisePic= noisePic.filter(ImageFilter.BLUR)                        
                #textPic = Image.blend(noisePic, textPic, 0.4)            
                textPic = Image.blend(textPic, noisePic, 0.6)   
                ht = self.createHatchingTexture(0.5, pw, ph, tcolor)
                textPic = Image.blend(textPic, ht, 0.3)   
            
                f = StringIO.StringIO()
                textPic.save(f, "PNG")
                pic = f.getvalue()
                captcha.content = pic
                meta.Session.commit()
                out = pic
                
            response.headers['Content-Length'] = len(out)
            response.headers['Content-Type'] = 'image/png'

            return str(out)
        
    def authorize(self, url):
        if url:
            c.currentURL = '/%s/' % url #.encode('utf-8')
        else:
            c.currentURL = '/'
        
        ip = request.environ["REMOTE_ADDR"]
        tracker = meta.Session.query(LoginTracker).filter(LoginTracker.ip==ip).first()
        if not tracker:
            tracker = LoginTracker()
            tracker.ip = ip
            tracker.attempts = 0
            tracker.lastAttempt = datetime.datetime.now()              
            meta.Session.add(tracker)  
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
                
        if request.POST.get('code', False):
            code = User.genUid(request.POST['code'].encode('utf-8')) 
            user = meta.Session.query(User).filter(User.uid==code).first()
            
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
                #log.debug('logged in')
            else:
                tracker.attempts += 1    
                tracker.lastAttempt = datetime.datetime.now()  

            meta.Session.commit()
            #log.debug(c.currentURL)
            redirect_to(c.currentURL.encode('utf-8'))
        
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
                session['openReg'] = False
                session.save()
            elif g.OPT.allowRegistration:
                 session['invite'] = invite
                 session['iid'] = False
                 session['openReg'] = True
                 session.save()
            else:
                c.currentURL = '/'
                return self.render('login')
        c.openReg = session['openReg']
        c.captcha = None
        captchaOk = True
        if session['openReg']:
            captchaOk = False
            if session.get('cid',False):
                captcha = meta.Session.query(Captcha).get(session['cid'])
                captchaOk = (captcha.text == request.POST.get('captcha', False))
                session['cid'] = None
                session.save()
                meta.Session.delete(captcha)
                meta.Session.commit()
            if not captchaOk:
                captcha = self.createCaptcha()
                session['cid'] = captcha.id
                session.save()
                c.captcha = captcha
         
        key = request.POST.get('key', '').encode('utf-8')
        key2 = request.POST.get('key2', '').encode('utf-8')
            
        if key and captchaOk:
            if len(key)>=g.OPT.minPassLength and key == key2:      
                uid = User.genUid(key) 
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
                meta.Session.add(user)
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
                localFilePath = os.path.join(g.OPT.uploadPath, tempid + '.' + type)
                localFile = open(localFilePath,'wb')
                localFile.write(body)
                localFile.close()
                oekaki.time = time
                oekaki.path = tempid + '.' + type
                meta.Session.commit()
        return ['ok']
        
    def banned(self):
        #self.userInst = FUser(session.get('uidNumber',-1))
        c.userInst = self.userInst
        if self.userInst.isValid() and self.userInst.isBanned():
            c.boardName = _('Banned')
            return self.render('banned')
        else:
            c.boardName = _('Error')
            c.errorText = _("ORLY?")
            return self.render('error')
            
    def UnknownAction(self):
        c.userInst = self.userInst      
        c.boardName = _('Error')
        c.errorText = _("Excuse me, WTF are you?")
        return self.render('error')
    
    def uaInfo(self):
        out = ''
        response.headers['Content-type'] = "text/plain" 
        for key in request.environ.keys():
            if 'HTTP' in key or 'SERVER' in key or 'REMOTE' in key:
                out += key + ':' +request.environ[key] + '\n'
        out += 'test:' + str(request.POST.get('test', '')) 
        return filterText(out)    
    
    
