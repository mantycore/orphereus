from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.base import *
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

def menuItems(menuId):
    menu = None
    if menuId == "managementMenu":
        menu = (MenuItem('id_ExtSettings', _("Extended settings"), h.url_for('hsCfgManage'), 601, 'id_adminBoard'),)

    return menu

def routingInit(map):
    map.connect('hsCfgManage', '/holySynod/configuration/', controller = 'setsmgr', action = 'show')
    map.connect('hsCfgReset', '/holySynod/configuration/reset/', controller = 'setsmgr', action = 'reset')

def pluginInit(g = None):
    config = {'name' : N_('Engine runtime settings editing tool'),
              'routeinit' : routingInit,
              'menuitems' : menuItems
             }

    return PluginInfo('setsmgr', config)

from OrphieBaseController import *

class SetsmgrController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu")
            
    def getSettingsDict(self,settings):
        return dict([(setting.name, setting.value) for setting in settings])
    
    def cutSectionNames(self, sectDict):
        return dict([(key.split('.')[1], val) for key, val in sectDict.iteritems()])
        
    def getSectionNames(self):
        keys = sorted(self.getSettingsDict(Setting.getAll()).keys())
        keys = map(lambda str: str.split('.')[0], keys)
        return list(set(keys))

    def initChecks(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canChangeRights()) or self.userInst.isBanned():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')

        c.boardName = _('Engine configuration')
        c.currentItemId = 'id_ExtSettings'
        
    def reset(self):
        self.initChecks()
        Setting.clearAll()
        init_globals(g, False)
        c.message = N_('Engine settings were set to default values.')
        return self.render('managementMessage')
    
    def show(self):
        self.initChecks()
        if request.POST.get('update', False):
            if not self.userInst.canChangeSettings():
                return self.error(_("No way! You aren't holy enough!"))
            
            currSettings = self.getSettingsDict(Setting.getAll())
            for s in request.POST:
                if s in currSettings.keys():
                    shortName = s.split('.')[1]
                    val = filterText(request.POST[s])
                    if g.OPT.getValueType(shortName) == CFG_INT:
                        if not isNumber(val):
                            return self.error(_("'%s' isn't correct number, but '%s' must be an integer number.") % (val, s))
                    if g.OPT.getValueType(shortName)  == CFG_LIST:
                        valarr = filter(lambda l: l, re.split('\r+|\n+|\r+\n+', val))
                        val = ','.join(valarr)
                    if currSettings[s] != val:
                        toLog(LOG_EVENT_SETTINGS_EDIT, _("Changed %s from '%s' to '%s'") % (s, currSettings[s], val))
                        Setting.getSetting(s).setValue(val)
                        g.OPT.autoSetValue(shortName, val)
            upd_globals()
            c.message = _('Settings were updated')
        
        c.cfg = {}
        for sect in self.getSectionNames():
            c.cfg[sect] = self.cutSectionNames(self.getSettingsDict(Setting.getSection(sect)))

        return self.render('manageExtSettings')