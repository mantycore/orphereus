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

import httplib, urllib, sys

class JSCompressorPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Javascript compression tool'),
                 }
        BasePlugin.__init__(self, 'jsCompressor', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('hsRebuildJs', '/holySynod/rebuildJs', controller = 'tools/jsCompressor', action = 'rebuild')

    def beforeRequestCallback(self, baseController):
        currentLang = get_lang()
        if g.firstRequest and not g.OPT.disableJSRegeneration:
            log.info('Generating js files...')
            self.generateFiles()
            set_lang(currentLang)

        if baseController.userInst.isValid():
            template = baseController.userInst.template
            if not currentLang:
                currentLang = h.langForCurrentRequest()
            else:
                currentLang = currentLang[0] # At this point correct language already set by OrphieBaseController
            if not template:
                template = g.OPT.templates[0]
            c.jsFiles = ["%s_%s.js" % (template, currentLang)]

    @staticmethod
    def generateFiles(useClosure = False, advancedOpt = False, joinOnly = False):
        logRecords = []
        def logMsg(s):
            log.info(s)
            logRecords.append(s)
        for template in g.OPT.templates:
            for lang in g.OPT.languages:
                lid = makeLangValid(lang)
                if not lid:
                    lid = g.OPT.defaultLang
                set_lang(lid)
                path = "%s_%s.js" % (template, lang)
                logMsg("Generating '%s' as '%s'..." % (path, lid))
                newJS = ""
                for js in g.OPT.jsFiles.get(template, []):
                    logMsg("Adding '%s'..." % js)
                    newJS += render('/%s/%s' % (template, js)) + "\n"
                uncompressedLen = len(newJS)
                if not joinOnly:
                    newJS = unicode(jsmin(newJS))
                else:
                    logMsg("Compression skipped")
                newLen = len(newJS)
                logMsg("Minified. Length: %d (saved: %d)" % (newLen, uncompressedLen - newLen))
                if useClosure:
                    logMsg("Sending data to closure compiler...")
                    optLevel = 'SIMPLE_OPTIMIZATIONS'
                    if advancedOpt:
                        optLevel = 'ADVANCED_OPTIMIZATIONS'
                    try:
                        params = urllib.urlencode([
                            ('js_code', newJS.encode('utf-8')),
                            ('compilation_level', optLevel),
                            ('output_format', 'text'),
                            ('output_info', 'compiled_code'),
                          ])
                        headers = { "Content-type": "application/x-www-form-urlencoded" }
                        conn = httplib.HTTPConnection('closure-compiler.appspot.com')
                        conn.request('POST', '/compile', params, headers)
                        response = conn.getresponse()
                        newJS = response.read()
                        conn.close
                    except Exception, e:
                        logMsg("Exception: %s" % str(e))
                basePath = os.path.join(g.OPT.staticPath, "js")
                path = os.path.join(basePath, path)
                f = open(path, 'w')
                f.write(newJS.encode('utf-8'))
                f.close()
                newLen = len(newJS)
                logMsg("Written. Length: %d (saved: %d)" % (newLen, uncompressedLen - newLen))
        return logRecords

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

        if 'rebuildjs' in request.POST:
            c.compressingResult = JSCompressorPlugin.generateFiles('useGClosure' in request.POST,
                                                                   'advancedOpt' in request.POST,
                                                                   'joinOnly' in request.POST
                                                                   )

        c.boardName = _('Rebuild JavaScript')
        c.currentItemId = 'id_RebuildJs'
        return self.render('management.jscompressor')
