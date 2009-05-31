

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

    def deps(self):
        return self.__pdeps

    def pluginName(self):
        return self.__pName

