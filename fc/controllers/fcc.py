import logging

from fc.lib.base import *
from fc.model import *
import os
import cgi
import shutil
import datetime
import time
import Image
import posix
import hashlib

import wakabaparse

class FieldStorageLike(object):
    def __init__(self,filename,filepath):
       self.filename = filename
       self.file = open(filepath,'rb')

def isNumber(n):
   import re
   if re.match("^[-+]?[0-9]+$", n):
      return True
   else:
      return False

log = logging.getLogger(__name__)
uploadPath = 'fc/public/uploads/'
uploadPathWeb = '/uploads/'
hashSecret = 'paranoia' # We will hash it by sha512, so no need to have it huge

class FccController(BaseController):
    def isAuthorized(self):
        return 'uid_number' in session

    def getParentID(self, id):
        post = meta.Session.query(Post).filter(Post.id==id).first()
        if post:
           return post.parentid
        else:
           return False
    
    def isPostOwner(self, id):
        post = meta.Session.query(Post).filter(Post.id==id).first()
        if post and post.uid_number == session['uid_number']:
           return post.parentid
        else:
           return False

    def makeThumbnail(self, source, dest, maxSize):
        sourceImage = Image.open(source)
        size = sourceImage.size
        if sourceImage:
           sourceImage.thumbnail(maxSize,Image.ANTIALIAS)
           sourceImage.save(dest)
           return size + sourceImage.size
        else:
           return []

    def processFile(self, file):
        if isinstance(file,cgi.FieldStorage) or isinstance(file,FieldStorageLike):
           #if isinstance(file,cgi.FieldStorage):
           #   filef  = file.file
           #   finenm = file.filename
           #else:
           #   filef  = file['file']
           #   filenm = file['filename']
           # We should check whether we got this file already or not
           # If we dont have it, we add it
           name = str(long(time.time() * 10**7))
           ext  = file.filename.rsplit('.',1)[:0:-1]
           if ext:
              ext = ext[0].lstrip(os.sep)
           else:
              # Panic, no extention found
              ext = ''
              return ''
           # Make sure its something we want to have
           extParams = meta.Session.query(Extension).filter(Extension.ext==ext).first()
           if not extParams:
              return ''
           
           localFilePath = os.path.join(uploadPath,name + '.' + ext)
           localFile = open(localFilePath,'w')
           shutil.copyfileobj(file.file, localFile)
           file.file.close()
           localFile.close()
           
           if extParams.type == 'image':
              thumbFilePath = name + 's.' + ext
              size = self.makeThumbnail(localFilePath, os.path.join(uploadPath,thumbFilePath), (250,250))
           else:
               if extParams.type == 'image-jpg':
                  thumbFilePath = name + 's.jpg'
                  size = self.makeThumbnail(localFilePath, os.path.join(uploadPath,thumbFilePath), (250,250))
               else:
                  thumbFilePath = extParams.path
                  size = [0,0,extParams.thwidth,extParams.thheight]
           pic = Picture()
           pic.path = name + '.' + ext
           pic.thumpath = thumbFilePath
           pic.width = size[0]
           pic.height = size[1]
           pic.thwidth = size[2]
           pic.thheight = size[3]
           pic.extid = extParams.id
           pic.size = posix.stat(localFilePath)[6]
           meta.Session.save(pic)
           meta.Session.commit()
           return pic.id
        else:
           return ''  

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'

    def GetOverview(self):
	c.currentURL = '/'
	if not self.isAuthorized():
	   return render('/wakaba.login.mako')
        c.board = '*'
        c.PostAction = ''
        c.uploadPathWeb = uploadPathWeb
        post_q = meta.Session.query(Post).filter(Post.parentid==-1).order_by(Post.last_date.desc())
        c.threads = post_q.all()
        for i in c.threads:
            i.Replies = meta.Session.query(Post).filter(Post.parentid==i.id).all()
            # Really fugly code, shouldnt be like this, should auto-LEFT JOIN
            for j in i.Replies:
               if j.picid:
                  j.file = meta.Session.query(Picture).filter(Picture.id==j.picid).one()
               else:
                  j.file = False
            if i.picid:
               i.file = meta.Session.query(Picture).filter(Picture.id==i.picid).one()
            else:
               i.file = False
        c.oekaki = False
        return render('/wakaba.posts.mako')


    def GetThread(self, post, tempid):
        c.currentURL = request.path_info + '/'
        if not self.isAuthorized():
           return render('/wakaba.login.mako')
        ThePost = meta.Session.query(Post).filter(Post.id==post).one()
        if ThePost.parentid != -1:
           Thread = meta.Session.query(Post).filter(Post.id==ThePost.parentid).one()
        else:
           Thread = ThePost
        if Thread.picid:
           Thread.file = meta.Session.query(Picture).filter(Picture.id==Thread.picid).one()
        else:
           Thread.file = False
        Thread.Replies = meta.Session.query(Post).filter(Post.parentid==Thread.id).all()
        for i in Thread.Replies:
           if i.picid:
              i.file = meta.Session.query(Picture).filter(Picture.id==i.picid).one()
           else:
              i.file = False
        c.PostAction = Thread.id
        c.threads = [Thread]
        c.uploadPathWeb = uploadPathWeb
        
        if tempid:
           oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
           c.oekaki = oekaki
        else:
           c.oekaki = False
        return render('/wakaba.posts.mako')

    def GetBoard(self, board, tempid):
        c.currentURL = request.path_info + '/'
        if not self.isAuthorized():
           return render('/wakaba.login.mako')
        c.board = board
        c.PostAction = board
        c.uploadPathWeb = uploadPathWeb
        post_q = meta.Session.query(Post).filter(Post.tags.any(tag=board)).order_by(Post.last_date.desc())
        c.threads = post_q.all()
        for i in c.threads:
            i.Replies = meta.Session.query(Post).filter(Post.parentid==i.id).all()
            # Really fugly code, shouldnt be like this, should auto-LEFT JOIN
            for j in i.Replies:
               if j.picid:
                  j.file = meta.Session.query(Picture).filter(Picture.id==j.picid).one()
               else:
                  j.file = False
            if i.picid:
               i.file = meta.Session.query(Picture).filter(Picture.id==i.picid).one()
            else:
               i.file = False

        if tempid:
           oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
           c.oekaki = oekaki
        else:
           c.oekaki = False

        return render('/wakaba.posts.mako')

    def PostReply(self, post):
        c.currentURL = request.path_info + '/'
        if not self.isAuthorized():
           return render('/wakaba.login.mako')
        ThePost = meta.Session.query(Post).filter(Post.id==post).one()
        if ThePost.parentid != -1:
           Thread = meta.Session.query(Post).filter(Post.id==ThePost.parentid).one()
        else:
           Thread = ThePost
        tempid = request.POST.get('tempid',False)
        postq = Post()
        postq.message = request.POST.get('message', '')
        if tempid:
           oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
           file = FieldStorageLike(oekaki.path,os.path.join(uploadPath,oekaki.path))
           postq.message += "\r\nDrawn with **%s** in %s seconds" % (oekaki.type,str(int(oekaki.time/1000)))
           if oekaki.source:
              postq.message += ", source >>%s" % oekaki.source
        else:
           file = request.POST.get('file',False)
        if postq.message:
           postq.message = wakabaparse.parseWakaba(postq.message,self)
        postq.title = request.POST['title']
        postq.parentid = Thread.id
        postq.date = datetime.datetime.now()
        postq.picid = self.processFile(file)
        postq.uid_number = session['uid_number']
        postq.sage = request.POST.get('sage', False)
        meta.Session.save(postq)
        meta.Session.commit()
        if not postq.sage:
           Thread.last_date = datetime.datetime.now()
           meta.Session.commit()
        redirect_to(action='GetThread')

    def PostThread(self, board):
        c.currentURL = request.path_info + '/'
        if not self.isAuthorized():
           return render('/wakaba.login.mako')
        post = Post()
        post.message = request.POST.get('message', '')
        tempid = request.POST.get('tempid',False)
        if tempid:
           oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
           file = FieldStorageLike(oekaki.path,os.path.join(uploadPath,oekaki.path))
           post.message += "\r\nDrawn with **%s** in %s seconds" % (oekaki.type,str(int(oekaki.time/1000)))
           if oekaki.source:
              post.message += ", source >>%s" % oekaki.source
        else:
           file = request.POST.get('file',False)
        if post.message:
           post.message = wakabaparse.parseWakaba(post.message,self)                
        post.parentid = -1
        post.title = request.POST['title']
        post.date = datetime.datetime.now()
        post.last_date = datetime.datetime.now()
        post.picid = self.processFile(file)
        post.uid_number = session['uid_number']
        post.tags.append(Tag(board))
        meta.Session.save(post)
        meta.Session.commit()
        redirect_to(action='GetBoard')
    def authorize(self, url):
        if url:
          c.currentURL = '/' + str(url) + '/'
        else:
          c.currentURL = '/'
        if request.POST['code']:
           code = hashlib.sha512(request.POST['code'] + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
           user = meta.Session.query(User).filter(User.uid==code).first()
           if user:
              session['uid_number'] = user.uid_number
              session.save()
              redirect_to(c.currentURL)
        return render('/wakaba.login.mako')
    def makeInvite(self):
        #c.currentURL = request.path_info + '/'
        #if not self.isAuthorized():
        #   return render('/wakaba.login.mako')
        invite = Invite()
        invite.date = datetime.datetime.now()
        invite.invite = hashlib.sha512(str(long(time.time() * 10**7)) + hashlib.sha512(hashSecret).hexdigest()).hexdigest()
        meta.Session.save(invite)
        meta.Session.commit()
        return "<a href='/register/%s'>INVITE</a>" % invite.invite
    
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
               session['uid_number']=user.uid_number
               del session['invite']
               session.save()
               redirect_to('/')
        return render('/wakaba.register.mako')
    def oekakiDraw(self,url):
        c.currentURL = request.path_info + '/'
        if not self.isAuthorized():
           return render('/wakaba.login.mako')
        c.url = url
        c.uploadPathWeb = uploadPathWeb
        c.canvas = False
        c.width  = 300
        c.height = 300
        c.tempid = str(long(time.time() * 10**7))
        oekaki = Oekaki()
        oekaki.tempid = c.tempid
        oekaki.picid = -1
        oekaki.time = -1
        oekaki.type = 'Shi normal'
        oekaki.uid_number = session['uid_number']
        oekaki.path = ''        
        oekaki.source = 0
        if isNumber(url):
           post = meta.Session.query(Post).filter(Post.id==url).one()
           if post.picid:
              pic = meta.Session.query(Picture).filter(Picture.id==post.picid).first()
              if pic and pic.width:
                 oekaki.source = post.id
                 c.canvas = pic.path
                 c.width  = pic.width
                 c.height = pic.height
        meta.Session.save(oekaki)
        meta.Session.commit()
        return render('/spainter.mako')
    def oekakiSave(self, environ, start_response, url,tempid):
        start_response('200 OK', [('Content-Type','text/plain'),('Content-Length','2')])
        oekaki = meta.Session.query(Oekaki).filter(Oekaki.tempid==tempid).first()
        print oekaki
        cl = int(request.environ['CONTENT_LENGTH'])
        if oekaki and cl:
           id = request.environ['wsgi.input'].read(1)
           if id == 'S':
              headerLength = int(request.environ['wsgi.input'].read(8))
              print headerLength
              header = request.environ['wsgi.input'].read(headerLength)
              print header
              bodyLength = int(request.environ['wsgi.input'].read(8))
              #print bodyLength
              request.environ['wsgi.input'].read(2)
              body = request.environ['wsgi.input'].read(bodyLength)
              #print type(body)
              headers = header.split('&')
              type = headers[0].split('=')[1]
              time = headers[1].split('=')[1]
              localFilePath = os.path.join(uploadPath,tempid + '.' + type)
              localFile = open(localFilePath,'wb')
              localFile.write(body)
              localFile.close()
              oekaki.time = time
              oekaki.type = 'Shi normal'
              oekaki.path = tempid + '.' + type
              meta.Session.commit()
        return ['ok']
    def oekakiFinish(self,url,tempid):
        print type(c)
        return 'ok'
    #def DeletePost(self, post):
    #def UnknownAction(self):      
