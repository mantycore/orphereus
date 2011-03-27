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
from Orphereus.lib.base import redirect_to, request, g
from Orphereus.lib.interfaces.AbstractMultifileHook import AbstractMultifileHook
from Orphereus.model import Post, meta

import logging
log = logging.getLogger(__name__)

class PostdeletePlugin(BasePlugin, AbstractMultifileHook):
    template = "multifile.spoiler"
    action = "spoiler"
    def __init__(self):
        config = {'name' : 'Post censoring',
                  'deps' : ('base_public',)
                 }
        BasePlugin.__init__(self, 'postspoiler', config)
        
    def allowDisplay(self, context, user):
        return user.canDeleteAllPosts()
    
    def operationCallback(self, controller, postIds, noRedirect):
        if not controller.userInst.canDeleteAllPosts():
            return controller.error(_("Operation prohibited"))

        redirectAddr = request.POST.get('tagLine', g.OPT.allowOverview and '~' or '!')
        
        for post in postIds:
            res = Post.getPost(post)
            for attach in res.attachments:
                attach.spoiler = True
        meta.Session.commit()
        
        # FIXME: redirect!
        return (not(noRedirect) and redirect_to('boardBase', board = redirectAddr)) or None
        