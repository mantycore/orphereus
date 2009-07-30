from pylons.i18n import N_
from string import *
from beaker.cache import CacheManager

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def statGenerator(controller, container):
    c.totalPostsCount = 0
    mstat = False
    vts = False
    userStats = (0, 0)
    chTime = g.OPT.statsCacheTime

    if chTime > 0:
        cm = CacheManager(type = 'memory')
        cch = cm.get_cache('home_stats')
        c.totalPostsCount = cch.get_value(key = "totalPosts", createfunc = Post.getPostsCount, expiretime = chTime)
        mstat = cch.get_value(key = "mainStats", createfunc = Tag.getStats, expiretime = chTime)
        userStats = cch.get_value(key = "userStats", createfunc = User.getStats, expiretime = chTime)
        vts = cch.get_value(key = "vitalSigns", createfunc = Post.vitalSigns, expiretime = chTime)
    else:
        c.totalPostsCount = Post.getPostsCount()
        userStats = User.getStats()
        mstat = Tag.getStats()
        vts = Post.vitalSigns()

    def taglistcmp(a, b):
        return cmp(b.count, a.count) or cmp(a.board.tag, b.board.tag)

    c.totalUsersCount = userStats[0]
    c.bannedUsersCount = userStats[1]

    c.boards = sorted(mstat.boards, taglistcmp)
    c.tags = sorted(mstat.tags, taglistcmp)
    c.stags = sorted(mstat.stags, taglistcmp)
    c.totalBoardsThreads = mstat.totalBoardsThreads
    c.totalBoardsPosts = mstat.totalBoardsPosts
    c.totalTagsThreads = mstat.totalTagsThreads
    c.totalTagsPosts = mstat.totalTagsPosts
    c.totalSTagsThreads = mstat.totalSTagsThreads
    c.totalSTagsPosts = mstat.totalSTagsPosts

    c.last1KUsersCount = vts.last1KUsersCount
    c.prev1KUsersCount = vts.prev1KUsersCount
    c.lastWeekMessages = vts.lastWeekMessages
    c.prevWeekMessages = vts.prevWeekMessages

def pluginInit(g = None):
    if g:
        intValues = [('statistics',
                               ('statsCacheTime',
                               )
                              ),
                            ]

        if not g.OPT.eggSetupMode:
            g.OPT.registerExtendedValues(intValues, CFG_INT)
            #g.OPT.setValues(booleanValues, g.OPT.booleanGetter)

    config = {'homeTemplate' : "statistics", # hook for base controller constructor
              'homeGenerator' : statGenerator,
              'name' : N_('Statistics for main page'),
             }

    return PluginInfo('statistics', config)
