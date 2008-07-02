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
import Image
import os
import hashlib
import re
from fc.lib.fuser import FUser

log = logging.getLogger(__name__)

class FcpController(BaseController):
    def login(self, user):
        session['uid_number'] = user.uid_number
        session.save()
    def authorize(self, url):
        if url:
            c.currentURL = '/' + str(url.encode('utf-8')) + '/'
        else:
            c.currentURL = '/'
        if request.POST['code']:
            code = hashlib.sha512(request.POST['code'] + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
            user = meta.Session.query(User).options(eagerload('options')).filter(User.uid==code).first()
            if user:
                self.login(user)
                redirect_to(c.currentURL)
        return render('/wakaba.login.mako')
    def register(self,invite):
        if 'invite' not in session:
            invite_q = meta.Session.query(Invite).filter(Invite.invite==invite).first()
            if invite_q:
                meta.Session.delete(invite_q)
                meta.Session.commit()
                session['invite'] = invite
                session.save()
            else:
                c.currentURL = '/'
                return render('/wakaba.login.mako')
        key = request.POST.get('key','')
        key2 = request.POST.get('key2','')
        if key:
            if len(key)>=24 and key == key2:
                uid = hashlib.sha512(key + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
                user = User()
                user.uid = uid
                meta.Session.save(user)
                meta.Session.commit()
                del session['invite']
                self.login(user)
                redirect_to('/')
        return render('/wakaba.register.mako')
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
                type = headers[0].split('=')[1]
                time = headers[1].split('=')[1]
                localFilePath = os.path.join(uploadPath, tempid + '.' + type)
                localFile = open(localFilePath,'wb')
                localFile.write(body)
                localFile.close()
                oekaki.time = time
                oekaki.path = tempid + '.' + type
                meta.Session.commit()
        return ['ok']
    def UnknownAction(self):      
        c.errorText = "Excuse me, WTF are you?"
        return render('/wakaba.error.mako')