from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.base import *
from Orphereus.model import *
from Orphereus.lib.miscUtils import filterText

import logging
log = logging.getLogger(__name__)

def newsGenerator(controller, container):
    posts = Post.buildMetaboardFilter(g.OPT.newsTag, controller.userInst)[0].order_by(Post.date.desc())
    count = posts.count()
    c.newsFeed = []
    if count > 0:
        posts = posts[0:g.OPT.newsToShow]
        c.newsFeed = posts

def restrictor(controller, request):
    if not controller.userInst.isAdmin():
        log.critical('here')
        tagstr = filterText(request.POST.get('tags', ''))
        taglist = Tag.stringToTagList(tagstr, False)
        for tag in taglist:
            if tag.tag == g.OPT.newsTag:
                return _("Posting into board /%s/ is prohibited" % g.OPT.newsTag)
    return None

def pluginInit(globj = None):
    if globj:
        intValues = [('newsgenerator',
                               ('newsToShow',
                               )
                              ),
                            ]
        stringValues = [('newsgenerator',
                               ('newsTag',
                               )
                              ),
                            ]

        if not globj.OPT.eggSetupMode:
            globj.OPT.setValues(intValues, globj.OPT.intGetter)
            globj.OPT.setValues(stringValues, globj.OPT.stringGetter)

    config = {'homeTemplate' : "newsfeed",
              'homeGenerator' : newsGenerator,
              'postingRestrictor' : restrictor,
             'deps' : False,
             'name' : N_('News feed for main page'),
             }

    return PluginInfo('newsgenerator', config)
