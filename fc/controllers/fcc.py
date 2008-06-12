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
    def GetThread(self, thread):
        return 'Thread: '+thread
    def GetBoard(self, board):
        return 'Board: '+board