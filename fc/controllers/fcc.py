import logging

from fc.lib.base import *
from fc.model import *

import datetime

log = logging.getLogger(__name__)

class FccController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'

    def GetOverview(self):
        c.board = '*'
        c.PostAction = ''
        post_q = meta.Session.query(Post).filter(Post.parentid==-1)
        c.threads = post_q.all()
        for i in c.threads:
            i.Replies = meta.Session.query(Post).filter(Post.parentid==i.id).all()
        #return render('/board.mako')
        return render('/wakaba.posts.mako')


    def GetThread(self, post):
        ThePost = meta.Session.query(Post).filter(Post.id==post).one()
        if ThePost.parentid != -1:
           Thread = meta.Session.query(Post).filter(Post.id==ThePost.parentid).one()
        else:
           Thread = ThePost
        Thread.Replies = meta.Session.query(Post).filter(Post.parentid==Thread.id).all()
        c.PostAction = Thread.id
        c.threads = [Thread]
        return render('/wakaba.posts.mako')

    def GetBoard(self, board):
        c.board = board
        c.PostAction = board
        post_q = meta.Session.query(Post).filter(Post.tags.any(tag=board))
        c.threads = post_q.all()
        for i in c.threads:
            i.Replies = meta.Session.query(Post).filter(Post.parentid==i.id).all()
        #return render('/board.mako')
        return render('/wakaba.posts.mako')

    def PostReply(self, post):
        ThePost = meta.Session.query(Post).filter(Post.id==post).one()
        if ThePost.parentid != -1:
           Thread = meta.Session.query(Post).filter(Post.id==ThePost.parentid).one()
        else:
           Thread = ThePost
        postq = Post()
        postq.message = request.POST.get('message', '')
        postq.parentid = Thread.id
        postq.date = datetime.datetime.now()
        meta.Session.save(postq)
        meta.Session.commit()
        Thread.last_date = datetime.datetime.now()
        meta.Session.commit()
        redirect_to(action='GetThread')

    def PostThread(self, board):
        post = Post()
        post.message = request.POST.get('message', '')
        post.parentid = -1
        post.date = datetime.datetime.now()
        post.last_date = datetime.datetime.now()
        post.tags.append(Tag(board))
        meta.Session.save(post)
        meta.Session.commit()
        redirect_to(action='GetBoard')

    #def DeletePost(self, post):
    #def UnknownAction(self):      
