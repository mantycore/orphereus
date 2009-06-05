from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.base import *
from Orphereus.lib.helpers import makeLangValid
from Orphereus.lib.jsMinify import jsmin
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def requestHook(baseController):
    if g.firstRequest:
        log.info('Generating js files...')
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
    if baseController.userInst.isValid():
        lang = baseController.userInst.lang()
        if not lang:
            lang = g.OPT.languages[0]
        c.jsFiles = ["full_%s.js" % lang]

def pluginInit(g = None):
    if g:
        pass

    config = {'name' : N_('Javascript compression tool'),
              'basehook' : requestHook,
             }

    return PluginInfo('jsCompressor', config)

