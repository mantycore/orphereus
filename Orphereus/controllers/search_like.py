from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import filterText

import logging
log = logging.getLogger(__name__)

def searchRoutine(filteringClause, text, page, postsPerPage):
    ns = g.pluginsDict['search_like'].pnamespace
    minLen = 3
    failInfo = None
    postIds = []
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
        filter = base.filter(ns.Post.message.like('%%%s%%' % text))
        count = filter.count()
        posts = filter.order_by(ns.Post.date.desc())[(page * postsPerPage):(page + 1) * postsPerPage]
        for post in posts:
            highlights[post.id] = (highlight(post.title, text), highlight(post.message, text))
    return (posts, count, failInfo, highlights, warnings)

def pluginInit(globj = None):
    if globj:
        pass

    config = {'searchRoutine' : searchRoutine,
             'deps' : False,
             'name' : N_('Search based on LIKE operator'),
             }

    return PluginInfo('search_like', config)
