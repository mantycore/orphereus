import logging

from fc.lib.base import *

log = logging.getLogger(__name__)

class FcajaxController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'
