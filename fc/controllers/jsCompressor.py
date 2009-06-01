from pylons.i18n import N_
from string import *

from fc.lib.pluginInfo import *
from fc.lib.base import *
from fc.lib.helpers import makeLangValid
from fc.lib.jsMinify import jsmin
from fc.model import *

import logging
log = logging.getLogger(__name__)

def requestHook(baseController):
    if g.firstRequest:
        for lang in g.OPT.languages:
            lid = makeLangValid(lang)
            if lid:
                set_lang(lid)
            #else:
            #    set_lang(g.OPT.defaultLang)
            newJS = ""
            for js in g.OPT.jsFiles:
                newJS += render('/' + js) + "\n"
            newJS = jsmin(newJS)
            basePath = os.path.join(g.OPT.staticPath, "js")
            path = os.path.join(basePath, "full_%s.js" % lang)
            f = open(path, 'w')
            f.write(newJS)
            f.close()
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

