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

from pylons import config, request, c, g
from pylons.i18n import get_lang, set_lang
import miscUtils as utils

import logging
log = logging.getLogger(__name__)

from Orphereus.model import *

def chGetBoards():
    boards = Tag.getBoards()
    #map(lambda lol: lol.options, boards) # hack for lazy evaluation
    return boards

def chBoardList():
    boardlist = []
    sectionId = -1
    section = []
    boards = chGetBoards()

    def sectionName(id):
        sName = ''
        if sectionId < len(g.sectionNames):
            sName = g.sectionNames[id]
        return sName

    for b in boards:
        if sectionId == -1:
            sectionId = b.sectionId
            section = []
        if sectionId != b.sectionId:
            boardlist.append((section, sectionName(sectionId)))
            sectionId = b.sectionId
            section = []
        bc = empty()
        bc.tag = b.tag
        bc.comment = b.comment
        section.append(bc) #b.tag)
    if section:
        boardlist.append((section, sectionName(sectionId)))
    return boardlist

def chSectionNames(boardlist):
    sectionNames = []
    for i in range(0, len(boardlist)):
        if i < len(g.sectionNames):
            sectionNames.append(g.sectionNames[i])
        else:
            sectionNames.append(None)
    return sectionNames
