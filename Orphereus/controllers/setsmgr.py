from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.base import *
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST, engineVersion
from Orphereus.model import *

import datetime
import logging
log = logging.getLogger(__name__)

def menuItems(menuId):
    menu = None
    if menuId == "managementMenu":
        menu = (MenuItem('id_ExtSettings', _("Extended settings"), h.url_for('hsCfgManage'), 601, 'id_adminBoard'),)
    return menu

def menuTest(id, baseController):
    user = baseController.userInst
    if id == 'id_ExtSettings':
        return user.canChangeSettings()

class SettingsManagerPlugin(PluginInfo):
    def __init__(self):
        config = {'name' : N_('Engine runtime settings editing tool'),
                  'menuitems' : menuItems,
                  'menutest' : menuTest
                 }
        PluginInfo.__init__(self, 'setsmgr', config)

    # Implementing PluginInfo
    def initRoutes(self, map):
        map.connect('hsCfgManage', '/holySynod/configuration/', controller = 'setsmgr', action = 'show')
        map.connect('hsCfgReset', '/holySynod/configuration/reset/', controller = 'setsmgr', action = 'reset')
        map.connect('hsCfgClearOrphaned', '/holySynod/configuration/cleanOrphaned/', controller = 'setsmgr', action = 'deleteOrphaned')

def pluginInit(g = None):
    return SettingsManagerPlugin()

from OrphieBaseController import *

class SetsmgrController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu")

    def __init__(self):
        self.settings = self.getSettingsDict(Setting.getAll())

    def getSettingsDict(self, settings):
        return dict([(setting.name, setting.value) for setting in settings])

    def cutSectionNames(self, sectDict):
        return dict([(key.split('.')[1], val) for key, val in sectDict.iteritems()])

    def getSectionNames(self):
        keys = sorted(self.settings.keys())
        keys = map(lambda str: str.split('.')[0], keys)
        return list(set(keys))

    def initChecks(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canChangeSettings()) or self.userInst.isBanned():
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
        toLog(LOG_EVENT_SETTINGS_EDIT, _("Performed global settings reset."))
        c.message = N_('Engine settings were set to default values.')
        c.returnUrl = h.url_for('hsCfgManage')
        return self.render('managementMessage')

    def deleteOrphaned(self):
        self.initChecks()
        settingsNamesDict = dict((s.split('.')[1], s) for s in self.settings.keys())
        orphanedSettings = filter(lambda key: g.OPT.getValueType(key) == None, settingsNamesDict.keys())
        map(lambda s: Setting.getSetting(settingsNamesDict[s]).delete(), orphanedSettings)
        c.message = N_('Deleted %s orphaned settings.' % len(orphanedSettings))
        c.returnUrl = h.url_for('hsCfgManage')
        return self.render('managementMessage')

    def show(self):
        self.initChecks()
        if request.POST.get('update', False):
            if not self.userInst.canChangeSettings():
                return self.error(_("No way! You aren't holy enough!"))

            for s in request.POST:
                if s in self.settings.keys():
                    shortName = s.split('.')[1]
                    val = filterText(request.POST[s])
                    valType = g.OPT.getValueType(shortName)
                    if not(valType):
                        continue
                    if valType == CFG_INT:
                        if not isNumber(val):
                            return self.error(_("'%s' isn't correct number, but '%s' must be an integer number.") % (val, s))
                    elif valType == CFG_LIST:
                        valarr = filter(lambda l: l, re.split('\r+|\n+|\r+\n+', val))
                        val = ','.join(valarr)
                    if self.settings[s] != val:
                        toLog(LOG_EVENT_SETTINGS_EDIT, _("Changed %s from '%s' to '%s'") % (s, self.settings[s], val))
                        Setting.getSetting(s).setValue(val)
                        g.OPT.autoSetValue(shortName, val)
            upd_globals()
            c.message = _('Settings were updated')

        c.cfg = {}
        c.ver = engineVersion
        c.now = datetime.datetime.now()
        c.allSettings = self.settings
        for sect in self.getSectionNames():
            c.cfg[sect] = self.cutSectionNames(self.getSettingsDict(Setting.getSection(sect)))

        return self.render('manageExtSettings')