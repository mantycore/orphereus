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

from pylons.i18n import N_
from string import *

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import filterText
from Orphereus.lib.interfaces.AbstractSearchModule import AbstractSearchModule

import logging
log = logging.getLogger(__name__)

class LikeSearchPlugin(BasePlugin, AbstractSearchModule):
    def __init__(self):
        config = {'name' : N_('Search based on LIKE operator'),
                 }
        BasePlugin.__init__(self, 'search_like', config)

    # Implementing AbstractSearchModule
    def helpTemplateName(self):
        return "man.search.like"

    def search(self, filteringClause, text, page, postsPerPage):
        minLen = 3
        failInfo = None
        count = 0
        posts = []
        highlights = {}
        warnings = []
        def highlight(strtorepl, text):
            return strtorepl.replace(text, u'<span style="background-color:yellow">%s</span>' % text)
        if not text or len(text) < minLen:
            failInfo = _("Query too short (minimal length: %d)") % minLen
        if not failInfo:
            base = Post.query.filter(filteringClause)
            filter = base.filter(Post.message.like('%%%s%%' % text))
            count = filter.count()
            posts = filter.order_by(Post.date.desc())[(page * postsPerPage):(page + 1) * postsPerPage]
            for post in posts:
                highlights[post.id] = (highlight(post.title, text), highlight(post.message, text))
        return (posts, count, failInfo, highlights, warnings)
