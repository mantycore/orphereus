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
