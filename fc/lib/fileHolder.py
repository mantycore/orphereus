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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #                                                                         #
################################################################################

import os

import logging
log = logging.getLogger(__name__)

class AngryFileHolder:
    def __init__(self, filenames):
        self.__files = filenames
        self.__deleteOnDestroy = True

    def disableDeletion(self):
        self.__deleteOnDestroy = False

    def paths(self):
        return self.__files

    def __del__(self):
        if self.__deleteOnDestroy:
            for file in self.__files:
                if file:
                    os.unlink(file)
                    #log.debug("File %s deleted" % file)


