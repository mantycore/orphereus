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
    #          id        link       name                weight   parent
    menu = None
    if menuId == "managementMenu":
        menu = (MenuItem('id_ExtSettings', _("Extended settings"), h.url_for('hsCfgManage'), 601, 'id_adminBoard'),)

    return menu

def routingInit(map):
    map.connect('hsCfgManage', '/holySynod/configuration/', controller = 'setsmgr', action = 'show')

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
        vals = {}
        for setting in settings:
            vals[setting.name] = setting.value
        return vals 
    
    def cutSectionNames(self, sectDict):
        newDict = {}
        for key, val in sectDict.iteritems():
            newDict[key.split('.')[1]] = val
        return newDict
        #return filter(lambda str: str.split('.')[1], sectDict.iterkeys())
        
    def getSectionNames(self):
        keys = sorted(self.getSettingsDict(Setting.getAll()).keys())
        keys = filter(lambda str: str.find('.')>-1, keys)  # aww, lambdas. fap-fap-fap 
        keys = map(lambda str: str.split('.')[0], keys)
        return list(set(keys))
    
    def show(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canChangeRights()) or self.userInst.isBanned():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')

        c.boardName = _('Engine settings')
        c.currentItemId = 'id_ExtSettings'
        
        log.debug(g.OPT)
        if request.POST.get('update', False):
            if not self.userInst.canChangeSettings():
                return self.error(_("No way! You aren't holy enough!"))
            
            currSettings = self.getSettingsDict(Setting.getAll())
            for s in request.POST:
                if s in currSettings.keys():
                    val = filterText(request.POST[s])
                    if guessType(currSettings[s]) == CFG_INT:
                        if not isNumber(val):
                            return self.error(_("'%s' isn't correct number, but '%s' must be an integer number.") % (val, s))
                    if guessType(currSettings[s]) == CFG_LIST:
                        valarr = filter(lambda l: l, re.split('\r+|\n+|\r+\n+', val))
                        val = ','.join(valarr)
                    if currSettings[s] != val:
                        toLog(LOG_EVENT_SETTINGS_EDIT, _("Changed %s from '%s' to '%s'") % (s, currSettings[s], val))
                        Setting.getSetting(s).setValue(val)
                        g.OPT.autoSetValue(s.split('.')[1], val)
                        #setattr(g.OPT, s.split('.')[1], val) 
                    #init_globals(config['pylons.app_globals'], False)
            c.message = _('Settings updated')
        
        
        c.guesser = guessType
        c.cfg = {}
        for sect in self.getSectionNames():
            c.cfg[sect] = self.cutSectionNames(self.getSettingsDict(Setting.getSection(sect)))

        return self.render('manageExtSettings')
