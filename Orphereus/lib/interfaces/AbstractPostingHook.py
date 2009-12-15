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

class ExtraPostingField(object):
    def __init__(self, name, text, **kwargs):
        self.name = name
        self.text = text

class AbstractPostingHook(object):
    def tagCheckHandler(self, tagName, userInst):
        pass

    def tagCreationHandler(self, tagstring, userInst, textFilter):
        return (tagstring, None)

    def afterPostCallback(self, post, userInst, params):
        pass

    def beforePostCallback(self, controller, request, **kwargs):
        return None

    def tagHandler(self, tag, userInst):
        return None, None

    def extraPostingFields(self, context, atTop):
        return None
