from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.base import *
from Orphereus.lib.helpers import makeLangValid
from Orphereus.lib.jsMinify import jsmin
from Orphereus.lib.menuItem import MenuItem
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def generateFiles():
        for lang in g.OPT.languages:
            lid = makeLangValid(lang)
            if not lid:
                lid = g.OPT.defaultLang
            set_lang(lid)
            path = "full_%s.js" % lang
            log.info("Generating '%s' as '%s'..." % (path, lid))
            newJS = ""
            for js in g.OPT.jsFiles:
                newJS += render('/' + js) + "\n"
            uncompressedLen = len(newJS)
            newJS = jsmin(newJS)
            basePath = os.path.join(g.OPT.staticPath, "js")
            path = os.path.join(basePath, path)
            f = open(path, 'w')
            f.write(newJS)
            f.close()
            newLen = len(newJS)
            log.info("Done. Length: %d (saved: %d)" % (newLen, uncompressedLen - newLen))
    

def requestHook(baseController):
    if g.firstRequest and not g.OPT.disableJSRegeneration:
        oldLang = get_lang()
        log.info('Generating js files...')
        generateFiles()
        set_lang(oldLang)

    if baseController.userInst.isValid():
        lang = baseController.userInst.lang
        if not lang:
            lang = g.OPT.languages[0]
        c.jsFiles = ["full_%s.js" % lang]
        
def menuItems(menuId):
    #          id        link       name                weight   parent
    menu = None
    if menuId == "managementMenu":
        menu = (MenuItem('id_PluginItems', N_("Plug-in actions"), '', 500, False),
                MenuItem('id_RebuildJs', N_("Rebuild JavaScript"), h.url_for('hsRebuildJs'), 30, 'id_PluginItems'),
                )

    return menu

def routingInit(map):
    map.connect('hsRebuildJs', '/holySynod/service/rebuildJs', controller = 'jsCompressor', action = 'rebuild')

def pluginInit(g = None):
    if g:
        booleanValues = [('jsCompressor',
                               ('disableJSRegeneration',
                               )
                              ),
                            ]

        g.OPT.setValues(booleanValues, g.OPT.booleanGetter)

    config = {'name' : N_('Javascript compression tool'),
              'routeinit' : routingInit,
              'basehook' : requestHook,
              'menuitems' : menuItems
             }

    return PluginInfo('jsCompressor', config)

from OrphieBaseController import *

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
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')

        generateFiles()
        
        c.boardName = _('Rebuild JavaScrtipt')
        c.message = _("Rebuild completed")
        c.currentItemId = 'id_RebuildJs'
        return self.render('managementMessage')   