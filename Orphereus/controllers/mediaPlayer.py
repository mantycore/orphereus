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
from string import *

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.lib.interfaces.AbstractPostOutputHook import AbstractPostOutputHook
from Orphereus.lib.constantValues import CFG_STRING
from Orphereus.model import *

from logging import getLogger
log = getLogger(__name__)

class MediaPlayerPlugin(BasePlugin, AbstractPostOutputHook):
    def __init__(self):
        config = {'name' : N_('Flash player for music files'),
                 }

        BasePlugin.__init__(self, 'mediaplayer', config)

    def overrideThumbnail(self, post, context, attachment):
        if attachment.extension.type == g.OPT.extensionTypeToPlay:
            return True
        return None

    def thumbnailForPost(self, post, context, attachment):
        return 'mediaplayer'

    def updateGlobals(self, globj):
        stringValues = [('mediaplayer',
                               ('extensionTypeToPlay',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(stringValues, CFG_STRING)
