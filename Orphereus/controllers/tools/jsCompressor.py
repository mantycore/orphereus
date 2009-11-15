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

from Orphereus.lib.BasePlugin import *
from Orphereus.lib.base import *
from Orphereus.lib.helpers import makeLangValid
from Orphereus.lib.thirdParty.jsMinify import jsmin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.lib.miscUtils import checkAdminIP
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class JSCompressorPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Javascript compression tool'),
                 }
        BasePlugin.__init__(self, 'jsCompressor', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('hsRebuildJs', '/holySynod/rebuildJs', controller = 'tools/jsCompressor', action = 'rebuild')

    def beforeRequestCallback(self, baseController):
        if g.firstRequest and not g.OPT.disableJSRegeneration:
            oldLang = get_lang()
            log.info('Generating js files...')
            self.generateFiles()
            set_lang(oldLang)

        if baseController.userInst.isValid():
            lang = baseController.userInst.lang
            template = baseController.userInst.template
            if not lang:
                lang = g.OPT.languages[0]
            if not template:
                template = g.OPT.templates[0]
            c.jsFiles = ["%s_%s.js" % (template, lang)]

    @staticmethod
    def generateFiles():
        for template in g.OPT.templates:
            for lang in g.OPT.languages:
                lid = makeLangValid(lang)
                if not lid:
                    lid = g.OPT.defaultLang
                set_lang(lid)
                path = "%s_%s.js" % (template, lang)
                log.info("Generating '%s' as '%s'..." % (path, lid))
                newJS = ""
                for js in g.OPT.jsFiles.get(template, []):
                    log.info("Adding '%s'..." % js)
                    newJS += render('/%s/%s' % (template, js)) + "\n"
                uncompressedLen = len(newJS)
                newJS = jsmin(newJS)
                basePath = os.path.join(g.OPT.staticPath, "js")
                path = os.path.join(basePath, path)
                f = open(path, 'w')
                f.write(newJS.encode('utf-8'))
                f.close()
                newLen = len(newJS)
                log.info("Done. Length: %d (saved: %d)" % (newLen, uncompressedLen - newLen))

    def menuItems(self, menuId):
        #          id        link       name                weight   parent
        menu = None
        if menuId == "managementMenu":
            menu = (MenuItem('id_RebuildJs', N_("Rebuild JavaScript"), h.url_for('hsRebuildJs'), 310, 'id_hsMaintenance'),
                    )
        return menu

    def MenuItemIsVisible(self, id, baseController):
        user = baseController.userInst
        if id == 'id_RebuildJs':
            return user.canRunMaintenance()

    def updateGlobals(self, globj):
        booleanValues = [('jsCompressor',
                               ('disableJSRegeneration',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(booleanValues, CFG_BOOL)

from Orphereus.controllers.OrphieBaseController import OrphieBaseController

class JscompressorController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu")

    def rebuild(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canRunMaintenance()) or self.userInst.isBanned():
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')

        JSCompressorPlugin.generateFiles()

        c.boardName = _('Rebuild JavaScrtipt')
        c.message = _("Rebuild completed")
        c.returnUrl = h.url_for('holySynod')
        c.currentItemId = 'id_RebuildJs'
        return self.render('managementMessage')
