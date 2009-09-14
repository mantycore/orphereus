from pylons.i18n import N_
from string import *

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.lib.interfaces.AbstractPostOutputHook import AbstractPostOutputHook
from Orphereus.lib.constantValues import CFG_STRING
from Orphereus.model import *

from logging import getLogger
log = getLogger(__name__)

class MediaPlayerPlugin(BasePlugin, AbstractPostOutputHook):
    def __init__(self):
        config = {'name' : N_('Flash player for music files'),
                 }

        BasePlugin.__init__(self, 'mediaplayer', config)

    def overrideThumbnail(self, post, context):
        if post.file.extension.type == g.OPT.extensionTypeToPlay:
            return True
        return None

    def thumbnailForPost(self, post, context):
        return 'mediaplayer'

    def updateGlobals(self, globj):
        stringValues = [('mediaplayer',
                               ('extensionTypeToPlay',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.registerCfgValues(stringValues, CFG_STRING)
