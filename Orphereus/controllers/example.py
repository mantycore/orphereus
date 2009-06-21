from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.base import *
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class TextValue(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @staticmethod
    def get(name):
        return meta.Session.query(TextValue).filter(TextValue.name == name).first()

def ormInit(orm, namespace):
    t_textValues = sa.Table('textValue', meta.metadata,
                       sa.Column("id"    , sa.types.Integer, primary_key = True),
                       sa.Column("name"      , sa.types.String(128), nullable = False),
                       sa.Column("value"      , sa.types.UnicodeText, nullable = False),
                       )
    orm.mapper(namespace.TextValue, t_textValues)

def routingInit(map):
    map.connect('home', '/examplepage', controller = 'example', action = 'index')

def deployHook(ns):
    try:
        uc = meta.Session.query(TextValue).filter(TextValue.name == 'indexContent').count()
    except:
        uc = 0
        log.info('Page content not created')

    if uc == 0:
        log.info("Creating main page content")
        newPage = ns.TextValue('indexContent', u'Some information')
        meta.Session.add(newPage)
        meta.Session.commit()

def textFilter(inp):
    replaces = (('LOL', 'OLOLO'),
                )

    for rep in replaces:
        inp = inp.replace(rep[0], rep[1])
    return inp

def exampleHelper():
    return "hello world"

def requestHook(baseController):
    baseController.additionalData = 'Hello world!'

from paste.script import command
class CommandClass(command.Command):

    max_args = 1
    min_args = 1

    usage = "NAME"
    summary = "Say hello!"
    group_name = "My Package Name"

    parser = command.Command.standard_parser(verbose = True)
    parser.add_option('--goodbye',
                      action = 'store_true',
                      dest = 'goodbye',
                      help = "Say 'Goodbye' instead")

    def command(self):
        name = self.args[0]
        if self.verbose:
            print "Got name: %r" % name
        if self.options.goodbye:
            print "Goodbye", name
        else:
            print "Hello", name

from paste.script import command
class CommandClass2(command.Command):

    max_args = 1
    min_args = 1

    usage = "NAME 2"
    summary = "Say hello 2!"
    group_name = "My Package Name 2"

    parser = command.Command.standard_parser(verbose = True)
    parser.add_option('--goodbye',
                      action = 'store_true',
                      dest = 'goodbye',
                      help = "Say 'Goodbye' instead 2")

    def command(self):
        name = self.args[0]
        if self.verbose:
            print "2 Got name: %r" % name
        if self.options.goodbye:
            print "2 Goodbye", name
        else:
            print "2 Hello", name


def menuItems(menuId):
    #          id        link       name                weight   parent
    menu = None
    if menuId == "managementMenu":
        menu = (MenuItem('idItemOne', N_("Example top"), '', 400, False),
                MenuItem('idItemTwo', N_("Sub"), h.url_for('home'), 20, 'idItemOne'),
                )

    return menu

def threadInfoCallback(thread, userInst):
    return '<b>Text</b> from example callback'

def pluginInit(globj = None):
    if globj:
        h.exampleHelper = exampleHelper
        h.threadInfoCallbacks.append(threadInfoCallback)

    config = {'filters' : (textFilter,), # filter helper
              'globfilters' : (textFilter,), # filter helper
             'basehook' : requestHook, # hook for base controller constructor
             'routeinit' : routingInit, # routing initializer
             'orminit' : ormInit, # ORM initializer
             'deps' : False, # plugin dependencies, for example ('users', 'statistics')
             'name' : N_('Example'),
             'deployHook' : deployHook,
             'entryPoints' : [('mycommand', "CommandClass"),
                              ('mycommand2', "CommandClass2"), ],
             'menutest' : False, # returns True if menu item should be visible. If False, all items will be visible
             'menuitems' : menuItems, # menu items
             }

    return PluginInfo('example', config)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import *

class ExampleController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__init__(self)

    def index(self):
        c.pageText = TextValue.get('indexContent').value
        return "<h1>Hello world!</h1><br/><br/>%s" % c.pageText

