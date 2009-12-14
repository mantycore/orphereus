#experimental module

from pylons.i18n import N_
from pylons.decorators import jsonify
from string import *

from Orphereus.lib.BasePlugin import *
from Orphereus.lib.base import *
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.model import *
from Orphereus.lib.miscUtils import checkAdminIP

import logging
log = logging.getLogger(__name__)

class PluginsListPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Plugins list'),
                  'deps' : ('adminpanel',)
                 }
        BasePlugin.__init__(self, 'pluginsList', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('hsListPlugins', '/holySynod/listPlugins', controller = 'tools/pluginsList', action = 'show')
        map.connect('hsAjPluginsList', '/holySynod/listPlugins/ajax', controller = 'tools/pluginsList', action = 'ajax')


    def menuItems(self, menuId):
        #          id        link       name                weight   parent
        menu = None
        if menuId == "managementMenu":
            menu = (MenuItem('id_ListPlugins', N_("Show active plugins"), h.url_for('hsListPlugins'), 320, 'id_hsMaintenance'),
                    )
        return menu

    def menuItemIsVisible(self, id, baseController):
        user = baseController.userInst
        if id == 'id_ListPlugins':
            return user.canRunMaintenance()

from OrphieBaseController import OrphieBaseController

class PluginslistController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu", True)
        

    def show(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canRunMaintenance()) or self.userInst.isBanned():
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')

        c.boardName = _('Active plugins list')
        c.returnUrl = h.url_for('holySynod')
        c.currentItemId = 'id_ListPlugins'

        c.plugins = g.plugins
        return self.render('pluginsList')

    @jsonify
    def ajax(self):
        ret = {}
        result = []
        for plugin in g.plugins:
            info = {'id' : plugin.pluginId(),
                    'descr' : plugin.pluginName(),
                    'deps' : plugin.deps(),
                    'namespace' : plugin.namespaceName(),
                    'file' : plugin.fileName()
                    }
            result.append(info)
        ret['results'] = result
        ret['total'] = len(g.plugins)
        return ret

