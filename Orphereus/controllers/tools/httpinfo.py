# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################
from pylons.i18n import N_
from string import *

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class HTTPInfoPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('HTTP headers dumper'),
                 }

        BasePlugin.__init__(self, 'httpinfo', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('/uaInfo', controller = 'tools/httpinfo', action = 'uaInfo')

# this import MUST be placed after public definitions to avoid loop importing
from Orphereus.controllers.OrphieBaseController import OrphieBaseController

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

