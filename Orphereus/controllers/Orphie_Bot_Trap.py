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

from Orphereus.lib.base import *
from Orphereus.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.orm import class_mapper
import sqlalchemy
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
import base64
from Orphereus.lib.OrphieMark.OrphieParser import OrphieParser
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from Orphereus.lib.fileHolder import AngryFileHolder
from Orphereus.lib.processFile import processFile
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook
from Orphereus.lib.interfaces.AbstractProfileExtension import AbstractProfileExtension
from Orphereus.lib.interfaces.AbstractSearchModule import AbstractSearchModule
from Orphereus.lib.interfaces.AbstractHomeExtension import AbstractHomeExtension
from OrphieBaseController import OrphieBaseController
from mutagen.easyid3 import EasyID3
from urllib import quote_plus, unquote

import logging
log = logging.getLogger(__name__)

#TODO: new debug system. Don't forget about c.log and c.sum

class OrphieBotTrapController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def selfBan(self, confirm):
        if g.OPT.spiderTrap and not self.userInst.Anonymous:
            if confirm:
                self.userInst.ban(2, _("[AUTOMATIC BAN] Security alert type 2"), -1)
                redirect_to('boardBase')
            else:
                return self.render('selfBan')
        else:
            return redirect_to('boardBase')
