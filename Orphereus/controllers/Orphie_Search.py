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

import logging
import re

from sqlalchemy.sql import and_, or_, not_

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.interfaces.AbstractSearchModule import AbstractSearchModule
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)

class OrphieSearchPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Search support (Obligatory)'),
                  'deps' : ('base_view',)
                 }
        BasePlugin.__init__(self, 'base_search', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('searchBase', '/search/{text}',
                    controller = 'Orphie_Search',
                    action = 'search',
                    text = '',
                    page = 0,
                    requirements = dict(page = r'\d+'))
        map.connect('search', '/search/{text}/page/{page}',
                    controller = 'Orphie_Search',
                    action = 'search',
                    requirements = dict(page = r'\d+'))

class OrphieSearchController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def search(self, text, page = 0):
        rawtext = text
        if not text:
            rawtext = request.POST.get('query', u'')
        text = filterText(rawtext)

        if isNumber(page):
            page = int(page)
        else:
            page = 0

        pp = self.userInst.threadsPerPage
        c.boardName = _("Search")
        c.query = text

        tagfilter = None
        filteredQueryRe = re.compile("^(([^:]+):){1}(.+)$").match(text)
        if filteredQueryRe:
            groups = filteredQueryRe.groups()
            filterName = groups[1]
            text = groups[2]
            tagfilter = Post.buildMetaboardFilter(filterName, self.userInst)[2]

        if tagfilter is None:
            tagfilter = Post.buildMetaboardFilter(None, self.userInst)[2]

        filteringClause = None
        if not tagfilter is None:
            filteringClause = or_(tagfilter, Post.parentPost.has(tagfilter))

        searchModules = g.implementationsOf(AbstractSearchModule)
        searchPlugin = None
        for sm in searchModules:
            if sm.pluginId() == g.OPT.searchPluginId:
                searchPlugin = sm

        if not searchPlugin:
            return self.error(_("Search plugin isn't configured"))

        #searchRoutine = searchPlugin.config.get('searchRoutine', None)
        #if not searchRoutine:
        #    return self.error(_("The plugin selected to search doesn't provide search features"))

        posts, count, failInfo, highlights, warnings = searchPlugin.search(filteringClause, text, page, pp)
        if failInfo:
            return self.error(failInfo)
        self.paginate(count, page, pp)

        c.warnings = warnings
        c.highlights = highlights
        c.posts = posts
        return self.render('search')
