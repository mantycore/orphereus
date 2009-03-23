import logging

from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
import os
import datetime

from fc.lib.miscUtils import *
from fc.lib.constantValues import *
from OrphieBaseController import OrphieBaseController

from webhelpers.feedgenerator import Atom1Feed, Rss201rev2Feed

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
        if g.OPT.allowLogin:
            session['uidNumber'] = user.uidNumber
            session.save()
        else:
            self.logout()

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
            c.currentURL = u'/%s' % url #.encode('utf-8')
        else:
            c.currentURL = u''

        if not g.OPT.allowLogin:
            c.boardName = _('Error')
            c.errorText = _("Authorization disabled")
            return self.render('error')

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

            c.captcha = Captcha.getCaptcha(tracker.cid)

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
            return redirect_to(h.url_for('boardBase', board=c.currentURL))

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
                regId = user.secid() * user.secid() - user.secid()
                toLog(LOG_EVENT_INVITE_USED, _("Utilized invite #%d [RID:%d]") % (session['iid'], regId ))
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

    def rss(self, watch, authid, uid, feedType):
        if not g.OPT.allowFeeds:
            abort(403)

        if not self.currentUserIsAuthorized():
            user = User.getByUid(uid)
            if not user or not int(authid) == user.authid():
                return redirect_to('/')
            # enable static files downloading
            session['feedAuth'] = True
            session.save()
            self.setCookie()
        else:
            user = self.userInst
        self.userInst = user

        title = u''
        descr = u'%s News Feed' % g.OPT.baseDomain
        posts = []
        if re.compile("^\d+$").match(watch):
            watch = int(watch)
            thePost = Post.getPost(watch)
            if not thePost:
                abort(404)
            title = _(u"%s: thread #%d") % (g.settingsMap['title'].value, watch)
            thread = Post.buildThreadFilter(user, thePost.id).first()
            if not thread:
                abort(404)
            replies = thread.filterReplies().all()
            posts = [thread]
            if replies:
                posts += replies
        else:
            title = _(u"%s: %s") % (g.settingsMap['title'].value, watch)
            filter = Post.buildMetaboardFilter(watch, user)[0]
            tpp = user.threadsPerPage()
            posts = filter.order_by(Post.bumpDate.desc())[0 : tpp]

        feed = None
        args = dict(title=title,
                link=h.url_for(),
                description=descr,
                language=u"en",
                )

        if feedType == 'rss':
            feed = Rss201rev2Feed(**args)
            response.content_type = 'application/rss+xml'
        else:
            feed = Atom1Feed(**args)
            response.content_type = 'application/atom+xml'

        for post in posts:
            parent = post.parentPost
            if not parent:
                parent = post
            parent.enableShortMessages=False

            title=None
            if not post.parentPost:
                post.replies = post.replyCount
                title = _(u"Thread #%d") % post.id
            else:
                post.replies = None
                title = _(u"#%d") % post.id
            descr = self.render('rssPost', 'std', thread=parent, post = post).decode('utf-8')

            feed.add_item(title=title,
                          link=h.url_for('thread', post = post.id),
                          description=descr)

        out = feed.writeString('utf-8')
        #css = str(h.staticFile(g.OPT.styles[0] + ".css"))
        #out = out.replace('<?xml version="1.0" encoding="utf-8"?>',
        #                  '<?xml version="1.0" encoding="utf-8"?>\n<?xml-stylesheet type="text/css" href="%s"?>' % css)
        return out
