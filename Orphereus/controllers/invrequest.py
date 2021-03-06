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

import logging

from sqlalchemy.sql import and_, or_, not_

from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import *
from Orphereus.lib.OrphieMark.tools import filterText
from OrphieBaseController import OrphieBaseController
from Orphereus.lib.BasePlugin import BasePlugin

log = logging.getLogger(__name__)

class RequestPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Invite request'),
                  'deps' : ('base_public',)
                 }
        BasePlugin.__init__(self, 'invrequest', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('invRequest', '/requestInvite',
                    controller = 'invrequest',
                    action = 'invrequest',
                   )

    def updateGlobals(self, globj):
        intValues = [('invites',
                       ('threadToSaveApplications',)
                     ),
                    ]
        boolValues = [('invites',
                       ('enableInvitationRequest',)
                      ),
                     ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(intValues, CFG_INT)
            globj.OPT.registerCfgValues(boolValues, CFG_BOOL)

class InvrequestController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        c.boardName = _('Invitation request')
        c.captcha = self.initSessionCaptcha(True)

    def invrequest(self):
        if not(g.OPT.enableInvitationRequest):
            c.hideform = True
            c.message = "Invitation requests are not allowed."
        else:
            c.hideform = False
            mail, text = filterText(request.POST.get('mail', u'')), filterText(request.POST.get('text', u''))
            c.mail, c.text = filterText(mail), filterText(text)
            if mail and text:
                captchaOk = self.checkSessionCaptcha(request.POST.get('captcha', '')) #c.captcha.test(request.POST.get('captcha', ''))
                if not captchaOk:
                    c.message = _("Captcha failed")
                else:
                    targetPost = Post.getPost(g.OPT.threadToSaveApplications)
                    if (not targetPost or targetPost.parentid):
                        log.error("Thread for invitation requests configured improperly!")
                        return self.error(_("Incorrect plugin configuration"))

                    Post.createDef(title = 'Request',
                           message = c.text,
                           messageInfo = '<span class="postInfo">Contact: %s</span>' % c.mail,
                           parentid = g.OPT.threadToSaveApplications)
                    c.message = "Application saved."
                    c.hideform = True
            elif mail or text:
                c.message = "Please, fill in all fields."
        if self.userInst.isValid():
            return redirect_to(controller = 'Orphie_View', action = 'GetThread', post = g.OPT.threadToSaveApplications)
        return self.render('request')
