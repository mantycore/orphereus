# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009-2010 Johan Liebert, Mantycore, Hedger, Rusanon           #
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

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.miscUtils import *
from Orphereus.lib.base import *
from Orphereus.lib.interfaces.AbstractMultifileHook import AbstractMultifileHook
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class PostdeletePlugin(BasePlugin, AbstractMultifileHook):
    template = "multifile.delete"
    action = "delete"
    def __init__(self):
        config = {'name' : N_('Post deletion'),
                  'deps' : ('base_public',)
                 }
        BasePlugin.__init__(self, 'postdelete', config)
        
    def allowDisplay(self, context, user):
        return True
    
    def operationCallback(self, controller, postIds):
        if not controller.currentUserCanPost():
            return controller.error(_("Removing prohibited"))

        fileonly = 'fileonly' in request.POST
        redirectAddr = request.POST.get('tagLine', g.OPT.allowOverview and '~' or '!')

        opPostDeleted = False
        reason = filterText(request.POST.get('reason', '???'))

        remPass = ''
        if controller.userInst.Anonymous:
            remPass = hashlib.md5(request.POST.get('remPass', '').encode('utf-8')).hexdigest()

        for post in postIds:
            res = post.deletePost(controller.userInst, fileonly, True, reason, remPass)
            opPostDeleted = opPostDeleted or res

        """tagLine = request.POST.get('tagLine', g.OPT.allowOverview and '~' or '!')
        if opPostDeleted:
            redirectAddr = tagLine"""

        return redirect_to('boardBase', board = redirectAddr)
        