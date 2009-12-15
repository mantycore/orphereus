# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Hedger                                                   #
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
import datetime

from Orphereus.lib.BasePlugin import *
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.miscUtils import getUserIp
#from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class DebugLogPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Debug request logger'),
                 }
        BasePlugin.__init__(self, 'dbglog', config)

    def beforeRequestCallback(self, baseController):
        uidn = baseController.userInst.uidNumber
        if g.OPT.dumpRequests and uidn >= g.OPT.minimalUidNumberToLog:
            params = (uidn,
                      str(request),
                      str(request.GET),
                      str(request.POST),
                      )
            requestData = 'user: %d\nreq: %s\nget: %s\npost: %s' % params
            if g.OPT.dumpHeaders:
                requestData = '%s\nheaders: %s' % (requestData, request.headers)
            if g.OPT.dumpEnv:
                requestData = '%s\nenv: %s' % (requestData, request.environ)
            log.error("{%s}" % requestData)

    def updateGlobals(self, globj):
        intValues = [('dbglog',
                               ('minimalUidNumberToLog',
                               )
                              ),
                            ]
        boolValues = [('dbglog',
                               ('dumpRequests', 'dumpEnv', 'dumpHeaders'
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(boolValues, CFG_BOOL)
