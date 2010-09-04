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
import time

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.miscUtils import filterText
from Orphereus.lib.thirdParty.sphinxapi import *
from Orphereus.lib.interfaces.AbstractSearchModule import AbstractSearchModule

import logging
log = logging.getLogger(__name__)

class SphinxSearchPlugin(BasePlugin, AbstractSearchModule):
    def __init__(self):
        config = {'name' : N_('Search with Sphinx full-text search engine'),
                  'deps' : ('base_search',)
                 }
        BasePlugin.__init__(self, 'search_sphinx', config)

    # Implementing AbstractSearchModule
    def helpTemplateName(self):
        return "man.search.sphinx"

    def search(self, filteringClause, text, page, postsPerPage):
        count = 0
        failInfo = None
        highlights = {}
        posts = []
        warnings = []

        maxCount = 1000
        maxCountForRestrictions = 500

        if text.strip():
            result = []

            postIds = []
            if g.OPT.enableFiltersForSearch and not (filteringClause is None):
                timestart = time.time()
                base = meta.Session.query(Post.id).filter(filteringClause)
                negBase = meta.Session.query(Post.id).filter(not_(filteringClause))
                positiveCount = base.count()
                negativeCount = negBase.count()
                if positiveCount < maxCountForRestrictions or negativeCount < maxCountForRestrictions:
                    # We should select minimal array of post ids to search trough
                    positive = positiveCount <= negativeCount
                    #log.critical("%d : %d" % (positiveCount, negativeCount))
                    if positive:
                        postIds = base.all()
                    else:
                        postIds = negBase.all()
                    postIds = map(lambda seq: int(seq[0]), postIds)
                else:
                    warnings.append(_("Search restrictions were ignored due to large allowed range"))
                c.log.append("Search: restriction computing time: %s" % (time.time() - timestart))
            else:
                warnings.append(_("Search restrictions were ignored due to config settings"))

            timestart = time.time()

            mode = SPH_MATCH_EXTENDED2
            host = str(g.OPT.sphinxHost)
            port = g.OPT.sphinxPort
            index = str(g.OPT.sphinxIndexName)
            sortby = str(g.OPT.sphinxPostDatePseudo)
            postIdPseudo = str(g.OPT.sphinxPostIdPseudo)
            cl = SphinxClient()
            cl.SetServer(host, port)
            if postIds:
                cl.SetFilter(postIdPseudo, postIds, not positive)
            cl.SetSortMode(SPH_SORT_ATTR_DESC, sortby)
            cl.SetLimits((page * postsPerPage), postsPerPage, (page * postsPerPage) + postsPerPage)
            #cl.SetWeights ([100, 1])
            cl.SetMatchMode(mode)
            res = cl.Query(text, index)

            c.log.append("Search: index searching time: %s" % (time.time() - timestart))
            timestart = time.time()

            if not res:
                failInfo = _("Search failed. Sphinx engine returned '%s'") % cl.GetLastError()
            elif res.has_key('matches'):
                count = res['total_found']
                if count > maxCount:
                    warnings.append(_("%d posts were found during search, %d was ignored due to engine restrictions") % (count, count - maxCount))
                    count = maxCount
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
            c.log.append("Search: posts resolving time: %s" % (time.time() - timestart))
        return (posts, count, failInfo, highlights, warnings)

    def updateGlobals(self, globj):
        booleanValues = [('sphinx',
                               ('enableFiltersForSearch',
                               )
                              ),
                            ]
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
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(stringValues, CFG_STRING)
            globj.OPT.registerCfgValues(booleanValues, CFG_BOOL)
