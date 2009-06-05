from pylons.i18n import get_lang

class PluginInfo():
    def __init__(self, pluginId, pluginConfig = False):
        # internal variables, init in app_globals.py
        self.pfileName = ''
        self.pnamespaceName = ''
        self.pnamespace = False

        self.__pId = pluginId # plugin id

        # plugin config
        if pluginConfig:
            self.config = pluginConfig
            self.__proutingInit = pluginConfig.get('routeinit', False)
            self.__poutHook = pluginConfig.get('filters', False)
            self.__prequestHook = pluginConfig.get('basehook', False)
            self.__pormInit = pluginConfig.get('orminit', False)
            self.__pdeps = pluginConfig.get('deps', False)
            self.__pName = pluginConfig.get('name', False)
            self.__pDeployHook = pluginConfig.get('deployHook', False)
            self.__pEntryPoints = pluginConfig.get('entryPoints', False)

            self.__pmenuInit = pluginConfig.get('menuitems', False)
            self.__pmenuTest = pluginConfig.get('menutest', False)
            self.__pmenuItems = {} #pluginConfig.get('menu', False)

    def pluginId(self):
        return self.__pId

    def fileName(self):
        return self.pfileName

    def namespaceName(self):
        return self.pnamespaceName

    def namespace(self):
        return self.pnamespace

    # HOOKS BEGIN
    def outHook(self):
        return self.__poutHook

    def routingInit(self):
        return self.__proutingInit

    def ormInit(self):
        return self.__pormInit

    def requestHook(self):
        return self.__prequestHook

    def deployHook(self):
        return self.__pDeployHook
    # HOOKS END

    def menuItems(self, menuId):
        ret = None
        if self.__pmenuInit:
            id = menuId + get_lang()[0]
            ret = self.__pmenuItems.get(id, False)
            if not ret:
                ret = self.__pmenuInit(menuId)
                self.__pmenuItems[id] = ret
        return ret

    def menuTest(self):
        return self.__pmenuTest

    def deps(self):
        return self.__pdeps

    def pluginName(self):
        return self.__pName

    def entryPoints(self):
        return self.__pEntryPoints
