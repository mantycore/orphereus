import logging

from fc.lib.base import *
from fc.model import *

import os
import shutil
import datetime
import time
import Image
import posix

log = logging.getLogger(__name__)
uploadPath = 'fc/public/uploads/'
uploadPathWeb = '/uploads/'

class FccController(BaseController):
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
        if file.filename:
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
        c.board = '*'
        c.PostAction = ''
        c.uploadPathWeb = uploadPathWeb
        post_q = meta.Session.query(Post).filter(Post.parentid==-1)
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
        #return render('/board.mako')
        return render('/wakaba.posts.mako')


    def GetThread(self, post):
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
        return render('/wakaba.posts.mako')

    def GetBoard(self, board):
        c.board = board
        c.PostAction = board
        c.uploadPathWeb = uploadPathWeb
        post_q = meta.Session.query(Post).filter(Post.tags.any(tag=board))
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
        #return render('/board.mako')
        return render('/wakaba.posts.mako')

    def PostReply(self, post):
        ThePost = meta.Session.query(Post).filter(Post.id==post).one()
        if ThePost.parentid != -1:
           Thread = meta.Session.query(Post).filter(Post.id==ThePost.parentid).one()
        else:
           Thread = ThePost
        file = request.POST['file'];
        postq = Post()
        postq.message = request.POST.get('message', '')
        postq.parentid = Thread.id
        postq.date = datetime.datetime.now()
        postq.picid = self.processFile(file)
        meta.Session.save(postq)
        meta.Session.commit()
        Thread.last_date = datetime.datetime.now()
        meta.Session.commit()
        redirect_to(action='GetThread')

    def PostThread(self, board):
        post = Post()
        post.message = request.POST.get('message', '')
        file = request.POST['file'];
        post.parentid = -1
        post.date = datetime.datetime.now()
        post.last_date = datetime.datetime.now()
        post.picid = self.processFile(file)
        post.tags.append(Tag(board))
        meta.Session.save(post)
        meta.Session.commit()
        redirect_to(action='GetBoard')

    #def DeletePost(self, post):
    #def UnknownAction(self):      
