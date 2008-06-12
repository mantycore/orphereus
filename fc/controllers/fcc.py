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
        return 'Overview'

    def GetThread(self, post):
        return 'Thread: '+post

    def GetBoard(self, board):
        c.board = board
        post_q = meta.Session.query(Post)
        c.posts = post_q.all()
        return render('/board.mako')

    #def PostReply(self, post):
    def PostThread(self, board):
        post = Post()
        post.message = request.POST.get('message', '')
        post.parentid = -1
        post.date = datetime.datetime.now()
        meta.Session.save(post)
        meta.Session.commit()
        redirect_to(action='GetBoard')

    #def DeletePost(self, post):
    #def UnknownAction(self):      