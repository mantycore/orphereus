import logging

from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
import os
import datetime

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
                    toLog(LOG_EVENT_RICKROLLD, "Request rickrolld. Referer: %s, Redir: %s, IP: %s, User-Agent: %s" % (ref, redir, getUserIp(), filterText(request.headers.get('User-Agent', '?'))))
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

    def captchaPic(self, cid):
        pic = Captcha.picture(cid, g.OPT.captchaFont)
        response.headers['Content-Length'] = len(pic)
        response.headers['Content-Type'] = 'image/png'
        return str(pic)

    def authorize(self, url):
        if url:
            c.currentURL = u'/%s/' % url #.encode('utf-8')
        else:
            c.currentURL = u'/'

        ip = getUserIp()
        tracker = LoginTracker.getTracker(ip)

        captchaOk = True
        captcha = False

        if tracker.attempts >= 2:
            c.showCaptcha = True
            captchaOk = False

            if tracker.cid:
                captcha = Captcha.getCaptcha(tracker.cid)

            if not captcha:
                captcha = Captcha.create()
                tracker.cid = captcha.id
                meta.Session.commit()

            c.captid = tracker.cid

        if request.POST.get('code', False):
            code = User.genUid(request.POST['code'].encode('utf-8'))
            user = User.getByUid(code)
            #log.debug(code)

            captid = request.POST.get('captid', False)
            captval = request.POST.get('captcha', False)
            #log.debug("%s:%s" %(captid, captval))

            if (not captchaOk) and captid and captval and isNumber(captid):
                if captcha and int(captid) == captcha.id:
                    captchaOk = captcha.test(captval)
                    captcha = False
                    if not captchaOk:
                        captcha = Captcha.create()
                        tracker.cid = captcha.id

            if user and captchaOk:
                if tracker:
                    tracker.delete()
                if captcha:
                    captcha.delete()
                self.login(user)
            else:
                tracker.attempts += 1
                tracker.lastAttempt = datetime.datetime.now()

            meta.Session.commit()
            #log.debug("redir: %s" % c.currentURL)
            redirect_to(c.currentURL.encode('utf-8'))

        c.boardName = _('Login')
        return self.render('login')

    def register(self, invite):
        if 'invite' not in session:
            iid = Invite.getId(invite)
            if iid:
                session['invite'] = invite
                session['iid'] = iid
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
            if session.get('cid', False):
                captcha = Captcha.getCaptcha(session['cid'])
                if captcha:
                    captchaOk = captcha.test(request.POST.get('captcha', False))
                session['cid'] = None
                session.save()
            if not captchaOk:
                captcha = Captcha.create()
                session['cid'] = captcha.id
                session.save()
                c.captcha = captcha

        key = request.POST.get('key', '').encode('utf-8')
        key2 = request.POST.get('key2', '').encode('utf-8')

        if key and captchaOk:
            if len(key)>=g.OPT.minPassLength and key == key2:
                uid = User.genUid(key)
                user = User.getByUid(uid)
                if user:
                    user.ban(7777, _("Your Security Code was used during registration by another user. Contact administrator immediately please."), -1)
                    del session['invite']
                    del session['iid']
                    c.boardName = _('Error')
                    c.errorText = _("You entered already existing password. Previous account was banned. Contact administrator please.")
                    return self.render('error')

                user = User.create(uid)
                toLog(LOG_EVENT_INVITE_USED, _("Utilized invite #%d") % (session['iid']))
                del session['invite']
                del session['iid']
                session.save()
                self.login(user)
                redirect_to('/')
        c.boardName = _('Register')
        return self.render('register')

    def banned(self):
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

    def saveUploaded(self, expandedName, content):
        localFilePath = os.path.join(g.OPT.uploadPath, expandedName)
        targetDir = os.path.dirname(localFilePath)
        if not os.path.exists(targetDir):
           os.makedirs(targetDir)
        localFile = open(localFilePath, 'wb')
        localFile.write(content)
        localFile.close()

    def oekakiSave(self, environ, start_response, url, tempid):
        start_response('200 OK', [('Content-Type','text/plain'),('Content-Length','2')])
        oekaki = Oekaki.get(tempid) #meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
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
                savedOekakiPath = h.expandName('%s.%s' % (tempid, type))
                self.saveUploaded(savedOekakiPath, body)

                animPath = None
                animLength = request.environ['wsgi.input'].read(8)
                if animLength:
                    animLength = int(animLength)
                    anim = request.environ['wsgi.input'].read(animLength)
                    animPath = h.expandName('%s.%s' % (tempid, 'pch'))
                    self.saveUploaded(animPath, anim)


                oekaki.setPathsAndTime(savedOekakiPath, animPath, time)
        return ['ok']
