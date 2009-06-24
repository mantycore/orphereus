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
    posts = []
    count = 0
    if not text or len(text) < minLen:
        failInfo = _("Query too short (minimal length: %d)") % minLen
    if not failInfo:
        base = meta.Session.query(ns.Post.id).filter(filteringClause)
        filter = base.filter(ns.Post.message.like('%%%s%%' % text))
        count = filter.count()
        posts = filter.order_by(ns.Post.date.desc())[(page * postsPerPage):(page + 1) * postsPerPage]
        posts = map(lambda seq: seq[0], posts)
    return (posts, count, failInfo)

def pluginInit(globj = None):
    if globj:
        pass

    config = {'searchRoutine' : searchRoutine,
             'deps' : False,
             'name' : N_('Search based on LIKE operator'),
             }

    return PluginInfo('search_like', config)
