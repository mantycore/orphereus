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
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)

class OrphiePublicPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Public services (Obligatory)'),
                 }
        BasePlugin.__init__(self, 'base_public', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('authorize', '/authorize',
                    controller = 'Orphie_Public',
                    action = 'authorize',
                    url = '')
        map.connect('authorizeToUrl',
                    '/{url:.*?}/authorize',
                    controller = 'Orphie_Public',
                    action = 'authorize',
                    url = '')
        map.connect('logout', '/logout',
                    controller = 'Orphie_Public',
                    action = 'logout',
                    url = '')
        map.connect('captcha',
                    '/captcha/{cid}',
                    controller = 'Orphie_Public',
                    action = 'captchaPic',
                    cid = 0)
        map.connect('register', '/register/{invite}',
                    controller = 'Orphie_Public',
                    action = 'register')
        map.connect('banned', '/youAreBanned',
                    controller = 'Orphie_Public',
                    action = 'banned')
        map.connect('ipBanned', '/ipBanned',
                    controller = 'Orphie_Public',
                    action = 'ipBanned')
        map.connect('oekakiSave',
                    '/oekakiSave/:url/:tempid',
                    controller = 'Orphie_Public',
                    action = 'oekakiSave',
                    url = '',
                    requirements = dict(tempid = r'\d+'))

    def menuItems(self, menuId):
        menu = None
        if menuId == "topMenu":
            reloadJS = "parent.top.list.location.reload(true);"
            menu = [MenuItem('id_auth_tmPages', _("Auth pages"), None, 1000, False),
                    MenuItem('id_auth_Login', _("Login"), None, 1100, 'id_auth_tmPages'),
                    MenuItem('id_auth_Logout', _("Logout"), h.url_for('logout'), 1200, 'id_auth_tmPages', onclick = reloadJS, target = "_top"),
                    MenuItem('id_auth_Kill', _("Kill session"), h.url_for('logout'), 1300, 'id_auth_tmPages', onclick = reloadJS, target = "_top"),
                    MenuItem('id_auth_Reg', _("Register"), h.url_for('register', invite = 'register'), 1400, 'id_auth_tmPages'),
                    ]
        return menu

    def menuItemIsVisible(self, id, baseController):
        user = baseController.userInst
        if id == 'id_auth_Login':
            return user.Anonymous
        if id == 'id_auth_Logout':
            return not user.Anonymous
        if id == 'id_auth_Kill':
            return user.Anonymous
        if id == 'id_auth_Reg':
            return user.Anonymous and g.OPT.allowRegistration
        return id.startswith('id_auth_')

    def modifyMenuItem(self, menuItem, baseController):
        user = baseController.userInst
        if menuItem.id == 'id_auth_Login':
            if c.currentURL:
                menuItem.route = h.url_for('authorizeToUrl', url = c.currentURL)
            else:
                menuItem.route = h.url_for('authorize')
        return menuItem

class OrphiePublicController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.title = g.OPT.title
        if not g.OPT.refControlForAnyRequest:
            self.refererCheck()
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
        self.destroySession()
        redirect_to('boardBase')

    def captchaPic(self, cid):
        #log.debug('user cap lang: %s' %c.userInst.cLang)
        self.setLang(True)
        pic = Captcha.picture(cid, g.OPT.captchaFont, g.OPT.easyCaptcha)
        if not pic:
            newCaptcha = Captcha.create()
            session['anonCaptId'] = newCaptcha.id
            session.save()
            redirect_to('captcha', cid = newCaptcha.id)
        response.headers['Content-Length'] = len(pic)
        response.headers['Content-Type'] = 'image/png'
        return str(pic)

    def authorize(self, url):
        #log.warning("Access request for url: %s" % str(url))
        if url:
            c.currentURL = u'/%s' % url #.encode('utf-8')
        else:
            c.currentURL = u''

        if not g.OPT.allowLogin:
            return self.error(_("Authorization disabled"))

        if self.userInst.isValid() and not self.userInst.Anonymous:
            c.loginSuccessful = True
            return self.redirectAuthorized(self.userInst)

        ip = getUserIp()
        tracker = LoginTracker.getTracker(ip)

        captchaOk = True
        captcha = False

        if tracker.attempts >= 2:
            #log.warning('captcha')
            if session and session.has_key('anonCaptId'):
                anonCapt = Captcha.getCaptcha(session['anonCaptId'])
                # If captcha in session differs from one in tracker remove old captcha in tracker
                if tracker.cid and (not anonCapt or (str(tracker.cid) != str(anonCapt.id))):
                    trackerCapt = Captcha.getCaptcha(tracker.cid)
                    if trackerCapt:
                        trackerCapt.delete()
                if not anonCapt:
                    print "NOT"
                    anonCapt = self.initSessionCaptcha(True)
                tracker.cid = anonCapt.id
                meta.Session.commit()

            c.showCaptcha = True
            captchaOk = False

            if tracker.cid:
                captcha = Captcha.getCaptcha(tracker.cid)

            if not captcha:
                captcha = self.initSessionCaptcha(True)
                tracker.cid = captcha.id
                meta.Session.commit()
                """
                if c.userInst.isValid():
                    oldLang = h.setLang(self.userInst.cLang)
                captcha = Captcha.create()
                if c.userInst.isValid():
                    h.setLang(oldLang)
                tracker.cid = captcha.id
                meta.Session.commit()
                """
            #c.captcha = Captcha.getCaptcha(tracker.cid)
            c.captcha = captcha
        code = request.POST.get('password', False)
        if code:
            code = User.genUid(code.encode('utf-8'))
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
            return self.redirectAuthorized(user)
        c.boardName = _('Login')
        return self.render('login')

    def redirectAuthorized(self, user):
        if (not g.OPT.framedMain or (user and not(user.useFrame))): # (1) frame turned off
            if (g.OPT.allowAnonymous): # (1.1) remove navigation frame if exists
                c.proceedRedirect = True
                c.frameEnabled = False
                return self.render('loginRedirect')
            else: # (1.2) frame is impossible
                return redirect_to('boardBase', board = c.currentURL)
        else: # (2) frame turned on
            if g.OPT.allowAnonymous: # and not g.OPT.obligatoryFrameCreation):
                # (2.1) change navigation frame location if exists. DON'T create frame!
                c.proceedRedirect = True
                c.frameEnabled = True
                return self.render('loginRedirect')
            else: # (2.2) create new frame with correct target.
                if c.currentURL:
                    return redirect_to('boardBase', frameTarget = c.currentURL)
                else:
                    return redirect_to('boardBase')

    def register(self, invite):
        def sessionDel(name):
            if name in session:
                del session[name]
        def cleanup():
            sessionDel('invite')
            sessionDel('iid')
            sessionDel('roinvite')
            session.save()

        if 'invite' not in session:
            invitedata = Invite.utilize(invite)
            iid = invitedata['id']
            roinvite = invitedata['readonly']
            if iid:
                toLog(LOG_EVENT_INVITE_USED, _("Utilized invite #%d") % iid)
                session['invite'] = invite
                session['iid'] = iid
                session['roinvite'] = roinvite
                session['openReg'] = False
                session.save()
            elif g.OPT.allowRegistration:
                session['invite'] = invite
                session['iid'] = False
                session['roinvite'] = g.OPT.setReadonlyToRegistered
                session['openReg'] = True
                session.save()
            else:
                cleanup()
                c.currentURL = u''
                return self.render('login')

        c.openReg = session['openReg']
        c.roInvite = session['roinvite']
        c.captcha = None
        captchaOk = True
        if c.openReg:
            captchaOk = None
            captcha = request.POST.get('captcha', False)
            if captcha:
                captchaOk = self.checkSessionCaptcha(captcha)
            if not captchaOk:
                if captcha:
                    c.message = _("Captcha failed")
                c.captcha = self.initSessionCaptcha(True)
            """
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
            """
        key = request.POST.get('key', '').encode('utf-8')
        key2 = request.POST.get('key2', '').encode('utf-8')
        if key and captchaOk:
            if len(key) >= g.OPT.minPassLength and key == key2:
                uid = User.genUid(key)
                user = User.getByUid(uid)
                if user:
                    user.ban(7777, _("Your Security Code was used during registration by another user. Contact administrator immediately please."), -1)
                    cleanup()
                    return self.error(_("You entered already existing password. Previous account was banned. Contact administrator please."))

                user = User.create(uid, session['roinvite'])
                regId = user.secid() * user.secid() - user.secid()
                infoline = "[%d]" % regId

                if user.options.readonly:
                    infoline += "[readonly]"

                toLog(LOG_EVENT_INVITE_USED, _("Completed registration by invite #%d; %s") % (session['iid'], infoline))
                cleanup()
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
        oekaki = Oekaki.get(tempid)
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


