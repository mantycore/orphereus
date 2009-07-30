from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.miscUtils import filterText
from Orphereus.lib.sphinxapi import *

import logging
log = logging.getLogger(__name__)

def searchRoutine(filteringClause, text, page, postsPerPage):
    count = 0
    failInfo = None
    highlights = {}
    posts = []
    if text.strip():
        result = []
        base = meta.Session.query(Post.id).filter(filteringClause)
        negBase = meta.Session.query(Post.id).filter(not_(filteringClause))
        positiveCount = base.count()
        negativeCount = negBase.count()

        # We should select minimal array of post ids to search trough
        positive = positiveCount <= negativeCount
        #log.critical("%d : %d" % (positiveCount, negativeCount))
        postIds = []
        if positive:
            postIds = base.all()
        else:
            postIds = negBase.all()
        postIds = map(lambda seq: int(seq[0]), postIds)

        mode = SPH_MATCH_EXTENDED2
        host = g.OPT.sphinxHost
        port = g.OPT.sphinxPort
        index = g.OPT.sphinxIndexName
        sortby = g.OPT.sphinxPostDatePseudo
        postIdPseudo = g.OPT.sphinxPostIdPseudo
        cl = SphinxClient()
        cl.SetServer(host, port)
        if postIds:
            cl.SetFilter(postIdPseudo, postIds, not positive)
        cl.SetSortMode(SPH_SORT_ATTR_DESC, sortby)
        cl.SetLimits((page * postsPerPage), postsPerPage, (page * postsPerPage) + postsPerPage)
        #cl.SetWeights ([100, 1])
        cl.SetMatchMode(mode)
        res = cl.Query(text, index)

        if not res:
            failInfo = _("Search failed. Sphinx engine returned '%s'") % cl.GetLastError()
        elif res.has_key('matches'):
            count = res['total_found']
            for match in res['matches']:
                result.append(match['id'])
        if result:
            posts = Post.filter(Post.id.in_(result)).order_by(Post.date.desc()).all()

            # Highlight found entries
            ids = []
            titles = []
            messages = []
            for post in posts:
                titles.append(post.title)
                messages.append(post.message)
                ids.append(post.id)
            options = {'before_match' : '<span style="background-color:yellow">', 'after_match' : '</span>'}
            hlarr = cl.BuildExcerpts(titles + messages, index, text, options)
            if hlarr:
                shift = len(titles)
                for num, id in enumerate(ids):
                    highlights[id] = (hlarr[num].decode('utf-8'), hlarr[num + shift].decode('utf-8'))
    return (posts, count, failInfo, highlights)

def pluginInit(globj = None):
    if globj:
        intValues = [('sphinx',
                               ('sphinxPort',
                               )
                              ),
                            ]
        stringValues = [('sphinx',
                               ('sphinxHost', 'sphinxIndexName',
                                'sphinxPostDatePseudo', 'sphinxPostIdPseudo'
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerExtendedValues(intValues, CFG_INT)
            globj.OPT.registerExtendedValues(stringValues, CFG_STRING)
            #globj.OPT.setValues(intValues, globj.OPT.intGetter)
            #globj.OPT.setValues(stringValues, globj.OPT.stringGetter)

    config = {'searchRoutine' : searchRoutine,
             'deps' : False,
             'name' : N_('Search with Sphinx full-text search engine'),
             }

    return PluginInfo('search_sphinx', config)
