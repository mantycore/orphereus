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
import datetime

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.miscUtils import getUserIp
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def banUser(user):
    if user.Anonymous:
        Ban.create(h.ipToInt(getUserIp()),h.ipToInt('255.255.255.255'),int(g.OPT.autoBanAnonTotally),  
                       _("[AUTOMATIC BAN] Exceeded posting speed limits"),
                       datetime.datetime.now(), g.OPT.banTimeDays, True)
    else:
        user.ban(g.OPT.banTimeDays, _("[AUTOMATIC BAN] Exceeded posting speed limits"))
    
def restrictor(controller, request, **kwargs):
    user = controller.userInst
    timeBnd = datetime.datetime.now() - datetime.timedelta(seconds = g.OPT.checkIntervalSeconds)
    if user.Anonymous:
        filterCond = and_(Post.date > timeBnd, Post.ip == h.ipToInt(getUserIp()))
    else:
        filterCond = and_(Post.date > timeBnd, Post.uidNumber == user.options.uidNumber)
    lastPosts = Post.filter(filterCond).all()
    lastThreads = filter(lambda post: (post.parentid == None), lastPosts)
   # log.info('Last posts: %s; threads: %s. Limits: %s/%s' %(len(lastPosts), len(lastThreads), g.OPT.postLimit, g.OPT.threadLimit))
    
    if (len(lastPosts) == g.OPT.postLimit or len(lastThreads) == g.OPT.threadLimit):
        if g.OPT.enableAutoBan:
            banUser(user)
            return _("[AUTOMATIC BAN] Exceeded posting speed limits")
        else:
            return _("You are posting too fast.")
    
    return None

def pluginInit(globj = None):
    if globj:
        intValues = [('antispam',
                               ('checkIntervalSeconds','postLimit','threadLimit','banTimeDays',
                               )
                              ),
                            ]
        boolValues = [('antispam',
                               ('enableAutoBan','autoBanAnonTotally',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(boolValues, CFG_BOOL)
    
    config = {'name' : N_('Wipe filter with auto-ban features'),
              'postingRestrictor' : restrictor,
             }

    return PluginInfo('antispam', config)    