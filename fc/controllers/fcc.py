import logging

from fc.lib.base import *

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
        return render('/form.mako')

    #def PostReply(self, post):
    def PostThread(self, board):
        log.debug('@PostThread')
        redirect_to(action='GetOverview')

    #def DeletePost(self, post):
    #def UnknownAction(self):      