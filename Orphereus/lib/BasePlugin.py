

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

            self.__pEntryPoints = pluginConfig.get('entryPoints', False)

            self.__pfilters = pluginConfig.get('filters', False)
            self.__pGlobalFilters = pluginConfig.get('globfilters', False)

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

    def entryPoints(self):
        return self.__pEntryPoints

    def filters(self):
        return self.__pfilters

    def globalFilters(self):
        return self.__pGlobalFilters

    # new methods
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

