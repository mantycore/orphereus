from pylons.i18n import N_
from string import *

from Orphereus.lib.BasePlugin import *
from Orphereus.lib.constantValues import CFG_LIST
from Orphereus.lib.base import *

import tidy

import logging
log = logging.getLogger(__name__)

class HTMLCompressorPlugin(BasePlugin):
    def __init__(self):
        config = {'name' : N_('Output revalidation and compression tool'),
                 }
        BasePlugin.__init__(self, 'htmlCompressor', config)

    # Implementing BasePlugin
    def globalFiltersList(self):
        return (self.htmlCompress,)

    # own
    def htmlCompress(self, inp):
        if c.template in g.OPT.disableCompressionList:
            return inp
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
        #return inp

    def updateGlobals(self, globj):
        listValues = [('htmlCompressor', ('disableCompressionList',)), ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(listValues, CFG_LIST)
