from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.base import *
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def routingInit(map):
    map.connect('/uaInfo', controller = 'httpinfo', action = 'uaInfo')

def pluginInit(globj = None):
    if globj:
        pass

    config = {'routeinit' : routingInit, # routing initializer
             'deps' : False, # plugin dependencies, for example ('users', 'statistics')
             'name' : N_('HTTP headers dumper'),
             }

    return PluginInfo('httpinfo', config)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import *

class HttpinfoController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)

    def uaInfo(self):
        out = ''
        response.headers['Content-type'] = "text/plain"
        for key in request.environ.keys():
            if 'HTTP' in key or 'SERVER' in key or 'REMOTE' in key:
                out += key + ':' + request.environ[key] + '\n'
        out += 'test:' + str(request.POST.get('test', ''))
        return filterText(out)

