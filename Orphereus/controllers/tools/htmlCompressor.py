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
from Orphereus.lib.constantValues import CFG_LIST
from Orphereus.lib.base import *

#import tidy
from tidylib import tidy_document

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

        #options = dict(output_xhtml = 1,
        #            add_xml_decl = 0,
        #            indent = 0,
        #            tidy_mark = 0,
        #            input_encoding = 'utf8',
        #            output_encoding = 'utf8',
        #            )
        #result = str(tidy.parseString(str(inp), **options))
        result, errors = tidy_document(str(inp),
                                         options = {'output-xhtml' : 1,
                                                  'add-xml-decl' : 0,
                                                  'indent' : 0,
                                                  'tidy-mark' : 0,
                                                  'input-encoding' : 'utf8',
                                                  'output-encoding' : 'utf8',
                                                  })
        if errors:
            log.error("tidy errors for %s: %s" % (str(c.template), str(errors)))
        if result:
            return result
        #return inp

    def updateGlobals(self, globj):
        listValues = [('htmlCompressor', ('disableCompressionList',)), ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(listValues, CFG_LIST)
