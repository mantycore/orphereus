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
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import filterText
from Orphereus.lib.interfaces.AbstractHomeExtension import AbstractHomeExtension
from Orphereus.lib.interfaces.AbstractPostingHook import AbstractPostingHook

import logging
log = logging.getLogger(__name__)

class HomeNewsFeedPlugin(BasePlugin, AbstractHomeExtension, AbstractPostingHook):
    def __init__(self):
        config = {'name' : N_('News feed for main page'),
                  'deps' : ('base_view',)
                 }

        BasePlugin.__init__(self, 'newsgenerator', config)
        AbstractHomeExtension.__init__(self, 'newsfeed')

    def prepareData(self, controller, container):
        container.newsFeed = []
        newsTag = unicode(g.OPT.newsTag)
        if Tag.getTag(newsTag):
            posts = Post.buildMetaboardFilter(newsTag, controller.userInst)[0].order_by(Post.date.desc())
            count = posts.count()
            if count > 0:
                posts = posts[0:g.OPT.newsToShow]
                container.newsFeed = posts

    def beforePostCallback(self, controller, request, **kwargs):
        tags = kwargs.get('tags', None)
        thread = kwargs.get('thread', None)
        if g.OPT.newsTag in (tag.tag for tag in tags):
            if thread and not(g.OPT.usersCanCommentNews) and (not controller.userInst.isAdmin()):
                return _("News commenting is not allowed.")
            if tags and g.OPT.onlyAdminsCanPostNews and (not controller.userInst.isAdmin()) and not(thread and g.OPT.usersCanCommentNews):
                return _("Posting into board /%s/ is prohibited." % g.OPT.newsTag)
        return None

    def deployCallback(self):
        tagname = config['newsgenerator.newsTag']
        newsTag = None
        try:
            newsTag = Tag.getTag(tagname)
        except:
            newsTag = None
            log.info(("News tag %s doesn't exists") % tagname)

        if not newsTag:
            log.info("Creating news tag...")
            newTag = Tag(tagname)
            meta.Session.add(newTag)
            meta.Session.commit()

    def updateGlobals(self, globj):
        booleanValues = [('newsgenerator',
                               ('onlyAdminsCanPostNews', 'usersCanCommentNews',
                               )
                              ),
                            ]
        intValues = [('newsgenerator',
                               ('newsToShow',
                               )
                              ),
                            ]
        stringValues = [('newsgenerator',
                               ('newsTag',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(booleanValues, CFG_BOOL)
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(stringValues, CFG_STRING)
