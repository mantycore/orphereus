from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.base import *
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class UserTag(object):
    userTagsToPostsMappingTable = None
    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    @staticmethod
    def get(name):
        return UserTag.query().filter(UserTag.name == name).first()

    @staticmethod
    def getMappingTable():
        if not UserTag.userTagsToPostsMappingTable:
            UserTag.userTagsToPostsMappingTable = sa.Table("usertagsToPostsMap", meta.metadata,
            sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id')),
            sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('usertag.id')),
            )
        return UserTag.userTagsToPostsMappingTable

def ormPropChanger(orm, propDict, namespace):
    propDict['Post']['userTags'] = orm.relation(namespace.UserTag, secondary = namespace.UserTag.getMappingTable())

def ormInit(orm, namespace):
    t_usertags = sa.Table("usertag", meta.metadata,
        sa.Column("id"       , sa.types.Integer, primary_key = True),
        sa.Column("tag"      , sa.types.UnicodeText, nullable = False),
        sa.Column("comment"  , sa.types.UnicodeText, nullable = True),
        )
    log.critical('here')
    orm.mapper(namespace.UserTag, t_usertags)

def routingInit(map):
    map.connect('usertags', '/examplepage', controller = 'example', action = 'index')

def requestHook(baseController):
    pass

def threadPanelCallback(thread, userInst):
    from webhelpers.html.tags import link_to
    return '1'

def postPanelCallback(thread, post, userInst):
    from webhelpers.html.tags import link_to
    return '2'

def threadInfoCallback(thread, userInst):
    return '<b>Text</b> from example callback'

def pluginInit(globj = None):
    if globj:
        h.threadPanelCallbacks.append(threadPanelCallback)
        h.postPanelCallbacks.append(postPanelCallback)
        h.threadInfoCallbacks.append(threadInfoCallback)

    config = {'basehook' : requestHook, # hook for base controller constructor
             'routeinit' : routingInit, # routing initializer
             'orminit' : ormInit, # ORM initializer
             'name' : N_('Personal tags module'),
             'ormPropChanger' : ormPropChanger
             }

    return PluginInfo('usertags', config)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import *

class UsertagsController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__init__(self)

    def index(self):
        c.pageText = TextValue.get('indexContent').value
        return "<h1>Hello world!</h1><br/><br/>%s" % c.pageText

