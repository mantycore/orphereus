from pylons.i18n import N_
from string import *

from fc.lib.pluginInfo import *
from fc.lib.base import *
from fc.model import *

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

def pluginInit(globj = None):
    if globj:
        h.exampleHelper = exampleHelper

    config = {'filters' : textFilter, # filter helper
             'basehook' : requestHook, # hook for base controller constructor
             'routeinit' : routingInit, # routing initializer
             'orminit' : ormInit, # ORM initializer
             'deps' : False, # plugin dependencies, for example ('users', 'statistics')
             'name' : N_('Example'),
             'deployHook' : deployHook,
             }

    return PluginInfo('example', config)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import *

class ExampleController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__init__(self)
        self.pluginInfo = pluginInit()
        #c.pageTitle = _('Test controller 2')

    def index(self):
        c.pageText = TextValue.get('indexContent').value
        return "<h1>Hello world!</h1><br/><br/>%s" % c.pageText

