# -*- coding: utf-8 -*-
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
import os
import datetime

from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

log = logging.getLogger(__name__)

class OrphiePublicController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.title = g.OPT.title
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
        else:
            self.setCookie()

    def ipBanned(self):
        if c.ban:
            return self.error(_('You are banned on %s for %s days for the following reason:<br/>%s') % (c.ban.date, c.ban.period, c.ban.reason))
        else:
            return self.error(_("ORLY?"))

    def login(self, user):
        if g.OPT.allowLogin:
            session['uidNumber'] = user.uidNumber
            session.save()
        else:
            self.logout()

    def logout(self):
        session.clear()
        session.save()
        session.delete()
        redirect_to('boardBase')

    def captchaPic(self, cid):
        # TODO: fix shitty code
        #log.debug('user cap lang: %s' %c.userInst.cLang)
        self.setLang(True)

        """
            sessionCid = None
            if session.has_key('anonCaptId'):
                sessionCid = session['anonCaptId']
            if session.has_key('cid'):
                sessionCid = session['cid']
        """
        pic = Captcha.picture(cid, g.OPT.captchaFont)
        """
            if sessionCid:
                log.debug("%s:%s" % (str(cid), str(sessionCid)))
                if (str(cid) != str(sessionCid)):
                   redirect_to('captcha', cid = sessionCid)
        """
        if ("Wrong ID" == pic):
           newCaptcha = Captcha.create()
           session['anonCaptId'] = newCaptcha.id
           session.save()
           redirect_to('captcha', cid = newCaptcha.id)
        response.headers['Content-Length'] = len(pic)
        response.headers['Content-Type'] = 'image/png'
        return str(pic)

    def authorize(self, url):
        if url:
            c.currentURL = u'/%s' % url #.encode('utf-8')
        else:
            c.currentURL = u''

        if not g.OPT.allowLogin:
            return self.error(_("Authorization disabled"))

        ip = getUserIp()
        tracker = LoginTracker.getTracker(ip)

        captchaOk = True
        captcha = False

        if tracker.attempts >= 2:
            if session and session.has_key('anonCaptId'):
                anonCapt = Captcha.getCaptcha(session['anonCaptId'])
                if tracker.cid and (str(tracker.cid) != str(anonCapt.id)):
                     trackerCapt = Captcha.getCaptcha(tracker.cid)
                     if trackerCapt:
                         trackerCapt.delete()
                tracker.cid = anonCapt.id
                meta.Session.commit()

            c.showCaptcha = True
            captchaOk = False

            if tracker.cid:
                captcha = Captcha.getCaptcha(tracker.cid)

            if not captcha:
                if c.userInst.isValid():
                    oldLang = h.setLang(self.userInst.cLang)
                captcha = Captcha.create()
                if c.userInst.isValid():
                    h.setLang(oldLang)
                tracker.cid = captcha.id
                meta.Session.commit()

            c.captcha = Captcha.getCaptcha(tracker.cid)

        if request.POST.get('code', False):
            code = User.genUid(request.POST['code'].encode('utf-8'))
            user = User.getByUid(code)
            #log.debug("code: %s user: %s",code,str(user))

            captid = request.POST.get('captid', False)
            captval = request.POST.get('captcha', False)
            #log.debug("got: %s:%s" %(captid, captval))

            if (not captchaOk) and captid and captval and isNumber(captid):
                if captcha and int(captid) == captcha.id:
                    captchaOk = captcha.test(captval)
                    captcha = False
                    if not captchaOk:
                        if c.userInst.isValid():
                            oldLang = h.setLang(self.userInst.cLang)
                        captcha = Captcha.create()
                        if c.userInst.isValid():
                            h.setLang(oldLang)
                        tracker.cid = captcha.id

            if user and captchaOk:
                if tracker:
                    tracker.delete()
                if captcha:
                    captcha.delete()
                self.login(user)
                c.loginSuccessful = True
            else:
                tracker.attempts += 1
                tracker.lastAttempt = datetime.datetime.now()

            meta.Session.commit()
            #log.debug("redir: %s" % c.currentURL)
            if (not g.OPT.framedMain or (user and not(user.useFrame))): # (1) frame turned off
                if (g.OPT.allowAnonymous): # (1.1) remove navigation frame if exists
                    c.proceedRedirect = True
                    c.frameEnabled = False
                    return self.render('loginRedirect')
                else: # (1.2) frame is impossible
                    return redirect_to('boardBase', board = c.currentURL)
            else: # (2) frame turned on
                if (g.OPT.allowAnonymous and not g.OPT.obligatoryFrameCreation):
                    # (2.1) change navigation frame location if exists. DON'T create frame!
                    c.proceedRedirect = True
                    c.frameEnabled = True
                    return self.render('loginRedirect')
                else: # (2.2) create new frame with correct target.
                    if c.currentURL:
                        return redirect_to('boardBase', frameTarget = c.currentURL)
                    else:
                        return redirect_to('boardBase')

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
                c.currentURL = u''
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
            if len(key) >= g.OPT.minPassLength and key == key2:
                uid = User.genUid(key)
                user = User.getByUid(uid)
                if user:
                    user.ban(7777, _("Your Security Code was used during registration by another user. Contact administrator immediately please."), -1)
                    del session['invite']
                    del session['iid']
                    return self.error(_("You entered already existing password. Previous account was banned. Contact administrator please."))

                user = User.create(uid)
                regId = user.secid() * user.secid() - user.secid()
                toLog(LOG_EVENT_INVITE_USED, _("Utilized invite #%d [RID:%d]") % (session['iid'], regId))
                del session['invite']
                del session['iid']
                session.save()
                self.login(user)
                redirect_to('boardBase', board = '!')
        c.boardName = _('Register')
        return self.render('register')

    def banned(self):
        c.userInst = self.userInst
        if self.userInst.isValid() and self.userInst.isBanned():
            c.boardName = _('Banned')
            return self.render('banned')
        else:
            return self.error(_("ORLY?"))

    def UnknownAction(self):
        c.userInst = self.userInst
        return self.error(_("Excuse me, WTF are you?"))

    def saveUploaded(self, expandedName, content):
        localFilePath = os.path.join(g.OPT.uploadPath, expandedName)
        targetDir = os.path.dirname(localFilePath)
        if not os.path.exists(targetDir):
           os.makedirs(targetDir)
        localFile = open(localFilePath, 'wb')
        localFile.write(content)
        localFile.close()

    def oekakiSave(self, environ, start_response, url, tempid):
        start_response('200 OK', [('Content-Type', 'text/plain'), ('Content-Length', '2')])
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


