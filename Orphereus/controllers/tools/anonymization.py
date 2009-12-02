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
from sqlalchemy.sql import and_, or_, not_
from webhelpers.html.tags import link_to

from Orphereus.lib.base import *
from Orphereus.model import Post
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
from Orphereus.controllers.OrphieBaseController import OrphieBaseController
from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.lib.constantValues import CFG_INT, CFG_BOOL

log = logging.getLogger(__name__)

class FinalAnonymizationPlugin(BasePlugin, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('Final anonymization'),
                 }
        BasePlugin.__init__(self, 'anonymiztaion', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('anonymize', '/:post/anonymize', controller = 'tools/anonymization', action = 'Anonimyze', requirements = dict(post = '\d+'))

    def updateGlobals(self, globj):
        boolValues = [('finalanonymity', ('enableFinalAnonymity', 'hlAnonymizedPosts',)), ]
        intValues = [('finalanonymity', ('finalAHoursDelay',)), ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(boolValues, CFG_BOOL)

    def postPanelCallback(self, thread, post, userInst):
        result = ''
        if g.OPT.enableFinalAnonymity and (g.OPT.memcachedPosts or (not userInst.Anonymous and post.uidNumber == c.uidNumber)):
            result += link_to(_("[FA]"), h.url_for('anonymize', post = post.id))
        return result

    def threadPanelCallback(self, thread, userInst):
        result = self.postPanelCallback(thread, thread, userInst)
        return result

    def postHeaderCallback(self, thread, post, userInst):
        result = ''
        if g.OPT.hlAnonymizedPosts and post.uidNumber == 0:
            result = '<b class="signature">%s</b>' % link_to(_("FA"), h.url_for('static', page = 'finalAnonymity'), target = "_blank")
        return result

    def threadHeaderCallback(self, thread, userInst):
        result = self.postHeaderCallback(thread, thread, userInst)
        return result

    def boardInfoCallback(self, context):
        faState = _('Final Anonymity: %s %s') % (not g.OPT.enableFinalAnonymity and _('off') or _('on'),
                                                   g.OPT.enableFinalAnonymity and
                                                   (g.OPT.hlAnonymizedPosts and _('(with marks)') or _('(without marks)')) or '')
        return "<li>%s</li>" % faState

class AnonymizationController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def Anonimyze(self, post):
        postid = request.POST.get('postId', False)
        batch = request.POST.get('batchFA', False)
        if postid and isNumber(postid):
            c.FAResult = self.processAnomymize(int(postid), batch)
        else:
            c.boardName = _('Final Anonymization')
            c.FAResult = False
            c.postId = post
        return self.render('finalAnonymization')

    def processAnomymize(self, postid, batch):
        if not g.OPT.enableFinalAnonymity:
            return [_("Final Anonymity is disabled")]

        if self.userInst.Anonymous:
            return [_("Final Anonymity available only for registered users")]

        result = []
        post = Post.getPost(postid)
        if post:
            posts = []
            if not batch:
                posts = [post]
            else:
                posts = Post.filter(and_(Post.uidNumber == self.userInst.uidNumber, Post.date <= post.date)).all()
            for post in posts:
                if post.uidNumber != self.userInst.uidNumber:
                    result.append(_("You are not author of post #%s") % post.id)
                else:
                    delay = g.OPT.finalAHoursDelay
                    timeDelta = datetime.timedelta(hours = delay)
                    if post.date < datetime.datetime.now() - timeDelta:
                        post.uidNumber = 0
                        post.ip = None
                        result.append(_("Post #%d successfully anonymized") % post.id)
                    else:
                        params = (post.id, str(post.date + timeDelta), str(datetime.datetime.now()))
                        result.append(_("Can't anomymize post #%d now, it will be allowed after %s (now: %s)" % params))
            meta.Session.commit()
        else:
            result = [_("Nothing to anonymize")]

        return result

