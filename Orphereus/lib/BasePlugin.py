

class BasePlugin(object):
    def __init__(self, pluginId, pluginConfig = False):
        self.__pId = pluginId

        # plugin config
        if pluginConfig:
            self.config = pluginConfig

            self.__pName = pluginConfig.get('name', False)
            self.__pdeps = pluginConfig.get('deps', False)

        # internal variables, init in app_globals.py
        self.setDetails(None, '', '')

    def setDetails(self, namespace, namespaceName, fileName):
        self.pnamespace = namespace
        self.pnamespaceName = namespaceName
        self.pfileName = fileName

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
    def updateGlobals(self, globj):
        pass

    def entryPointsList(self):
        return []

    def initRoutes(self, map):
        pass

    def postInitRoutes(self, map):
        pass

    def initORM(self, orm, engine, dialectProps, propDict):
        pass

    def extendORMProperties(self, orm, engine, dialectProps, propDict):
        pass

    def deployCallback(self):
        pass

    def beforeRequestCallback(self, baseController):
        pass

    def globalFiltersList(self):
        return []

    def filtersList(self):
        return []
