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
from beaker.cache import CacheManager

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.model import *
from Orphereus.lib.interfaces.AbstractHomeExtension import AbstractHomeExtension

import logging
log = logging.getLogger(__name__)

class HomeStatisticsPlugin(BasePlugin, AbstractHomeExtension):
    def __init__(self):
        config = {'name' : N_('Statistics for main page'),
                  'deps' : ('base_view',)
                 }

        BasePlugin.__init__(self, 'statistics', config)
        AbstractHomeExtension.__init__(self, 'statistics')

    def prepareData(self, controller, container):
        container.totalPostsCount = 0
        mstat = False
        vts = False
        userStats = (0, 0)
        chTime = g.OPT.statsCacheTime

        if chTime > 0:
            cm = CacheManager(type = 'memory')
            cch = cm.get_cache('home_stats')
            container.totalPostsCount = cch.get_value(key = "totalPosts", createfunc = Post.getPostsCount, expiretime = chTime)
            mstat = cch.get_value(key = "mainStats", createfunc = Tag.getStats, expiretime = chTime)
            userStats = cch.get_value(key = "userStats", createfunc = User.getStats, expiretime = chTime)
            vts = cch.get_value(key = "vitalSigns", createfunc = Post.vitalSigns, expiretime = chTime)
        else:
            container.totalPostsCount = Post.getPostsCount()
            userStats = User.getStats()
            mstat = Tag.getStats()
            vts = Post.vitalSigns()

        def taglistcmp(a, b):
            return cmp(b.count, a.count) or cmp(a.board.tag, b.board.tag)

        container.totalUsersCount = userStats[0]
        container.bannedUsersCount = userStats[1]

        container.boards = sorted(mstat.boards, taglistcmp)
        container.tags = sorted(mstat.tags, taglistcmp)
        container.stags = sorted(mstat.stags, taglistcmp)
        container.totalBoardsThreads = mstat.totalBoardsThreads
        container.totalBoardsPosts = mstat.totalBoardsPosts
        container.totalTagsThreads = mstat.totalTagsThreads
        container.totalTagsPosts = mstat.totalTagsPosts
        container.totalSTagsThreads = mstat.totalSTagsThreads
        container.totalSTagsPosts = mstat.totalSTagsPosts

        container.last1KUsersCount = vts.last1KUsersCount
        container.prev1KUsersCount = vts.prev1KUsersCount
        container.lastWeekMessages = vts.lastWeekMessages
        container.prevWeekMessages = vts.prevWeekMessages

    def updateGlobals(self, globj):
        intValues = [('statistics',
                               ('statsCacheTime',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(intValues, CFG_INT)

