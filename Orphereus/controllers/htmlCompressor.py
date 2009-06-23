from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import *

import tidy

import logging
log = logging.getLogger(__name__)

def htmlCompress(inp):
    options = dict(output_xhtml = 1,
                add_xml_decl = 0,
                indent = 0,
                tidy_mark = 0,
                input_encoding = 'utf8',
                output_encoding = 'utf8',
                )
    return str(tidy.parseString(str(inp), **options))

def pluginInit(g = None):
    if g:
        pass
    config = {'name' : N_('Output revalidation and compression tool'),
              'globfilters' : (htmlCompress,),
             }

    return PluginInfo('htmlCompressor', config)


