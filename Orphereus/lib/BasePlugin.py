

class BasePlugin():
    def __init__(self, pluginId, pluginConfig = False):
        # internal variables, init in app_globals.py
        self.pfileName = ''
        self.pnamespaceName = ''
        self.pnamespace = False

        self.__pId = pluginId

        # plugin config
        if pluginConfig:
            self.config = pluginConfig

            self.__pName = pluginConfig.get('name', False)
            self.__pdeps = pluginConfig.get('deps', False)

    def pluginId(self):
        return self.__pId

    def fileName(self):
        return self.pfileName

    def namespaceName(self):
        return self.pnamespaceName

    def namespace(self):
        return self.pnamespace

    #TODO: temporary ?
    def pluginName(self):
        return self.__pName

    def deps(self):
        return self.__pdeps

    # new methods
    def entryPointsList(self):
        return []

    def initRoutes(self, map):
        pass

    def initORM(self, orm, propDict):
        pass

    def extendORMProperties(self, orm, propDict):
        pass

    def deployCallback(self):
        pass

    def beforeRequestCallback(self, baseController):
        pass

    # global text filter
    def globalFiltersList(self):
        return []

    # text filtering helper
    def filtersList(self):
        return []
