from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.base import *
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def newsGenerator(controller, container):
    posts = Post.buildMetaboardFilter(g.OPT.newsTag, controller.userInst)[0].order_by(Post.date.desc())
    count = posts.count()
    c.newsFeed = []
    if count > 0:
        posts = posts[0:g.OPT.newsToShow]
        c.newsFeed = posts

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

        globj.OPT.setValues(intValues, globj.OPT.intGetter)
        globj.OPT.setValues(stringValues, globj.OPT.stringGetter)

    config = {'homeTemplate' : "newsfeed",
              'homeGenerator' : newsGenerator,
             'deps' : False,
             'name' : N_('News feed for main page'),
             }

    return PluginInfo('newsgenerator', config)
