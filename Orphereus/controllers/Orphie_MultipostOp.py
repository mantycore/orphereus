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

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.interfaces.AbstractMultifileHook import AbstractMultifileHook
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)


class OrphieMultipostOpPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Multi-post operations (Obligatory)'),
                  'deps' : False
                 }
        BasePlugin.__init__(self, 'base_multipost', config)

    # Implementing BasePlugin
    def postInitRoutes(self, map):
        map.connect('process', '/{board}/process',
                    controller = 'Orphie_MultipostOp',
                    action = 'process',
                    conditions = dict(method = ['POST']))


class OrphieMultipostopController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def process(self):
        posts = []
        task = ''
        retest = re.compile("^\d+$")
        for i in request.POST:
            if retest.match(request.POST[i]):
                posts.append(int(request.POST[i]))
            if i.startswith('task_'):
                task = i[5:]

        gvars = config['pylons.app_globals']
        callbacks = gvars.implementationsOf(AbstractMultifileHook)
        for cb in callbacks:
            callback, action = getattr(cb, 'operationCallback'), getattr(cb, 'action')
            if (action == task):
                return callback(self, posts, False) 
        return "Callback for action %s not found!" % task

        #return "Using task: %s \nposts: %s ^_^\n" % (task, posts)

