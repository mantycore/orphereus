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
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.model import *

from webhelpers.feedgenerator import Atom1Feed, Rss201rev2Feed
from webhelpers.html.tags import auto_discovery_link

import logging
log = logging.getLogger(__name__)

class RssFeedPlugin(BasePlugin, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('RSS/Atom feeds'),
                 }

        BasePlugin.__init__(self, 'rssfeed', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('feed', '/:watch/feed/auth/:authid/:uid.:feedType', controller = 'rssfeed', action = 'rss', requirements = dict(authid = '\d+'))

    # AbstractPageHook
    def headCallback(self, context):
        result = ''
        if g.OPT.allowFeeds and context.userInst.isValid() and context.threads:
            rssLink = h.url_for('feed', uid = context.userInst.uid,
                                authid = context.userInst.authid(),
                                watch = context.currentRealm, feedType = 'rss')
            atomLink = h.url_for('feed', uid = context.userInst.uid,
                                authid = context.userInst.authid(),
                                watch = context.currentRealm, feedType = 'atom')
            result += auto_discovery_link(rssLink, feed_type = 'rss') + '\n'
            result += auto_discovery_link(atomLink, feed_type = 'atom') + '\n'
        return result

    def updateGlobals(self, globj):
        booleanValues = [('rssfeed',
                               ('allowFeeds',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(booleanValues, CFG_BOOL)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import OrphieBaseController

class RssfeedController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)

    def rss(self, watch, authid, uid, feedType):
        if not g.OPT.allowFeeds:
            abort(403)

        if not self.currentUserIsAuthorized():
            user = User.getByUid(uid)
            if not user or not int(authid) == user.authid():
                return redirect_to('boardBase')
            if user.isAdmin() and not checkAdminIP():
                return redirect_to('boardBase')
            # enable static files downloading
            session['feedAuth'] = True
            session.save()
            self.setCookie()
        else:
            user = self.userInst
        self.userInst = user

        title = u''
        descr = u'%s News Feed' % g.OPT.baseDomain
        posts = []
        if re.compile("^\d+$").match(watch):
            watch = int(watch)
            thePost = Post.getPost(watch)
            if not thePost:
                abort(404)
            title = _(u"%s: thread #%d") % (g.OPT.title, watch)
            thread = Post.buildThreadFilter(user, thePost.id).first()
            if not thread:
                abort(404)
            replies = thread.filterReplies().all()
            posts = [thread]
            if replies:
                posts += replies
        else:
            title = _(u"%s: %s") % (g.OPT.title, watch)
            filter = Post.buildMetaboardFilter(watch, user)[0]
            tpp = user.threadsPerPage
            posts = filter.order_by(Post.bumpDate.desc())[0 : tpp]

        feed = None
        args = dict(title = title,
                link = h.url_for(),
                description = descr,
                language = u"en",
                )

        if feedType == 'rss':
            feed = Rss201rev2Feed(**args)
            response.content_type = 'application/rss+xml'
        else:
            feed = Atom1Feed(**args)
            response.content_type = 'application/atom+xml'

        for post in posts:
            parent = post.parentPost
            if not parent:
                parent = post
            parent.enableShortMessages = False

            title = None
            if not post.parentPost:
                post.replies = post.replyCount
                title = _(u"Thread #%d") % post.id
            else:
                post.replies = None
                title = _(u"#%d") % post.id
            descr = self.render('rssPost', 'std', thread = parent, post = post, disableFiltering = True) #.decode('utf-8')

            feed.add_item(title = title,
                          link = h.url_for('thread', post = post.id),
                          description = descr)

        out = feed.writeString('utf-8')
        #css = str(h.staticFile(g.OPT.styles[0] + ".css"))
        #out = out.replace('<?xml version="1.0" encoding="utf-8"?>',
        #                  '<?xml version="1.0" encoding="utf-8"?>\n<?xml-stylesheet type="text/css" href="%s"?>' % css)
        return out

