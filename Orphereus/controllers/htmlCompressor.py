from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.constantValues import CFG_LIST
from Orphereus.lib.base import *

import tidy

import logging
log = logging.getLogger(__name__)

def htmlCompress(inp):
    if c.template in g.OPT.disableCompressionList:
        return inp
    options = dict(output_xhtml = 1,
                add_xml_decl = 0,
                indent = 0,
                tidy_mark = 0,
                input_encoding = 'utf8',
                output_encoding = 'utf8',
                )
    result = str(tidy.parseString(str(inp), **options))
    if result:
        return result
    return inp

def pluginInit(g = None):
    if g:
        listValues = [('htmlCompressor', ('disableCompressionList',)),]

        if not g.OPT.eggSetupMode:
            g.OPT.registerCfgValues(listValues, CFG_LIST)
            
    config = {'name' : N_('Output revalidation and compression tool'),
              'globfilters' : (htmlCompress,),
             }

    return PluginInfo('htmlCompressor', config)


