# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Hedger                                                   #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

"""The application's Globals object"""
from pylons import config
from pylons.i18n import get_lang
import sys
import os
import re
import inspect

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.cache import *
from Orphereus.lib.constantValues import engineVersion
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider

import logging
_log = logging.getLogger("CORE")
_log.setLevel(logging.DEBUG)

class OptHolder(object):
    def __init__(self, appName, eggSetupMode = False):
        #in most cases you don't need to change these paths
        self.eggSetupMode = eggSetupMode
        applicationDirectory = os.path.dirname(__file__)
        applicationDirectory = applicationDirectory.replace('%(sep)s%(appname)s%(sep)slib' % {'appname' : appName, 'sep' : os.path.sep}, '')
        self.appRoot = os.path.realpath(applicationDirectory)

        self.appPath = os.path.realpath(os.path.join(self.appRoot, appName))
        self.templPath = os.path.realpath(os.path.join(self.appPath, 'templates'))

        self.captchaFont = os.path.join(self.appRoot, 'Orphereus/cfont.ttf')
        self.revisionId = ''
        f = None
        try:
            f = open(os.path.join(self.appRoot, 'revision'))
            self.revisionId = re.sub("[^\d]", "", f.read())
        except:
            pass
        finally:
            if f:
                f.close()
        self.disabledModules = []

        self.booleanValues = [('core',
                               ('secondaryIndex', 'allowPosting',
                                'allowRegistration', 'setReadonlyToRegistered',
                                'allowAnonymous',
                                'allowLogin', 'allowAnonymousPosting', 'allowAnonProfile',
                               )
                              ),

                              ('debug',
                               ('devMode', 'requestProfiling',
                               )
                              ),

                              ('memcache',
                               ('memcachedPosts', 'memcachedBans', 'memcachedUsers',
                               )
                              ),

                              ('frontend',
                                ('invisibleBump', 'usersCanViewLogs', 'vitalSigns',
                                 'allowCrossposting', 'allowCrosspostingSvc',
                                 'allowPureSvcTagline', 'allowTagCreation',
                                 'allowAnswersWithoutCaptcha', 'forbidCaptcha',
                                 'useFrameLogo', 'permissiveFileSizeConjunction',
                                 'boardWideProoflabels', 'allowOverview', 'framedMain',
                                 'showShortStatistics', 'mixOldThreads',
                                 'newsSiteMode', 'useTopPaginator', 'useZMenu', 'dvachStyleMenu',
                                 'permissiveAdditionalFilesCountConjunction',
                                 'easyCaptcha',
                                )
                              ),

                              ('defaults',
                               ('defImagelessThread', 'defImagelessPost', 'defImages',
                                'defEnableSpoilers', 'defCanDeleteOwnThreads', 'defSelfModeration',
                                'defShowInOverview',
                               )
                              ),

                              ('security',
                               ('useXRealIP', 'saveAnyIP',
                                'refControlEnabled', 'refControlForAnyRequest',
                                'refControlWhenAnonEnabled',
                                'checkUAs', 'spiderTrap',
                                'useAnalBarriering',
                               ),
                              ),
                             ]

        self.stringValues = [('core',
                               ('urlPrefix', 'hashSecret', 'baseDomain',
                                'staticPathWeb', 'filesPathWeb', 'actuator',
                                'staticPath', 'uploadPath',
                                'searchPluginId',
                                'typeToExtractID3Tags'
                               )
                              ),

                              ('debug',
                               ('profileDumpFile',
                               )
                              ),

                              ('memcache',
                               ('cachePrefix',
                               )
                              ),

                              ('security',
                               ('alertServer', 'alertSender', 'alertPassword',
                                'obfuscator',
                               )
                              ),

                              ('frontend',
                                ('title', 'frameLogo', 'defaultBoard', 'favicon',
                                )
                              ),

]

        self.intValues = [('core',
                               ('minPassLength',
                               )
                              ),

                              ('memcache',
                               ('banCacheSeconds',
                               )
                              ),

                              ('defaults',
                               ('defThumbSize', 'defMinPicSize', 'defMaxFileSize', 'defBumplimit',
                                'allowedAdditionalFiles',
                               )
                              ),

                              ('security',
                               ('alertPort',
                               )
                              ),

                              ('frontend',
                                ('maxTagsCount', 'maxTagLen', 'maxLinesInPost',
                                 'cutSymbols',
                                )
                              ),


                            ]

        self.strListValues = [('core',
                               ('languages', 'templates',
                                'javascripts', 'styles',
                                # 'disabledModules',
                               )
                              ),

                              ('memcache',
                               ('memcachedServers',
                               )
                              ),

                              ('security',
                               ('alertEmail', 'refControlList', 'fakeLinks',
                                'badUAs', 'trustedIPRanges'
                               )
                              ),

                              ('frontend',
                                ('disabledTags', 'additionalLinks',
                                 'sectionNames', 'homeModules',
                                )
                              ),

                            ]

        if not eggSetupMode:
            # a couple of workarounds for early init stages
            self.disabledModules = self.strListGetter(config['core.disabledModules'])
            self.framedMain = True

            # recovery option
            self.recoveryMode = self.booleanGetter(config['core.recovery'])
        else:
            self.recoveryMode = True

    def registerCfgValues(self, values, type):
        dest = {CFG_BOOL: self.booleanValues,
                CFG_INT: self.intValues,
                CFG_STRING: self.stringValues,
                CFG_LIST: self.strListValues,
                }
        dest[type].extend(values)

    def getValueType(self, valName):
        types = {self.booleanGetter: CFG_BOOL,
                 self.intGetter: CFG_INT,
                 self.stringGetter: CFG_STRING,
                 self.strListGetter: CFG_LIST,
                 }
        try:
            return types[self.valueGetters[valName]]
        except:
            return None

    def initValues(self, settingObj):
        _log.info('LOADING SETTINGS...')
        if self.recoveryMode:
            _log.warning('RUNNING IN RECOVERY MODE')
        self.setter = settingObj
        self.valueGetters = {}
        self.setValues(self.booleanValues, self.booleanGetter)
        self.setValues(self.stringValues, self.stringGetter)
        self.setValues(self.intValues, self.intGetter)
        self.setValues(self.strListValues, self.strListGetter)

        # Basic IB settings
        if not os.path.exists(self.uploadPath):
            self.uploadPath = os.path.join(self.appRoot, 'Orphereus/uploads/')
            log.error("Upload path doesn't exists, using '%s' instead" % self.uploadPath)

        if not os.path.exists(self.staticPath):
            self.staticPath = os.path.join(self.appRoot, 'Orphereus/public/')
            log.error("Static path doesn't exists, using '%s' instead" % self.staticPath)

        self.uploadPath = os.path.realpath(self.uploadPath)
        self.staticPath = os.path.realpath(self.staticPath)

        if not os.access(self.uploadPath, os.F_OK | os.R_OK | os.W_OK | os.X_OK):
            msg = "Upload path '%s' is not writeable, aborting..." % self.uploadPath
            log.critical(msg)
            raise Exception(msg)

        #self.languages.insert(0, 'Default')
        self.obfuscator = self.obfuscator.replace('$(', '%(')
        self.allowAnonymousPosting = self.allowAnonymous and self.allowAnonymousPosting
        self.allowAnonProfile = self.allowAnonymous and self.allowAnonProfile

        self.cssFiles = {}
        self.jsFiles = {}
        rex = re.compile(r"^(.+)=(.+)$")
        for elem in self.styles:
            matcher = rex.match(elem)
            if not matcher:
                raise Exception("Incorrect styles list")
            else:
                self.cssFiles[matcher.group(1)] = matcher.group(2).split('|')
        for elem in self.javascripts:
            matcher = rex.match(elem)
            if not matcher:
                raise Exception("Incorrect js list")
            else:
                self.jsFiles[matcher.group(1)] = matcher.group(2).split('|')
        fullCssList = []
        for cssList in self.cssFiles.values():
            fullCssList += cssList
        self.styles = fullCssList
        self.defaultLang = config['lang']

    @staticmethod
    def booleanGetter(value):
        return value.lower() == 'true'
    @staticmethod
    def stringGetter(value):
        return value
    @staticmethod
    def intGetter(value):
        return int(value)
    @staticmethod
    def strListGetter(value):
        return value.split(',')

    def autoSetValue(self, name, rawValue):
        getter = self.valueGetters[name]
        value = getter(rawValue)
        setattr(self, name, value)

    def setValues(self, source, getter):
        for section in source:
            sectionName = section[0]
            for valueName in section[1]:
                paramName = '%s.%s' % (sectionName, valueName)
                rawValue = config.get(paramName, None)
                if rawValue is None:
                    msg = "Required option '%s' (assotiated with '%s') isn't defined in config!" % (paramName, getter.__name__)
                    log.critical(msg)
                    raise Exception(msg)
                value = getter(rawValue)
                if self.setter and not(self.recoveryMode):
                    sqlValue = None
                    sqlValueObj = self.setter.getSetting(paramName)
                    if sqlValueObj:
                        sqlValue = sqlValueObj.value
                        value = getter(sqlValue)
                    else:
                        self.setter.create(paramName, unicode(rawValue))
                setattr(self, valueName, value)
                self.valueGetters[valueName] = getter

class Globals(object):
    def __init__(self, eggSetupMode = False):
        appName = self.__module__.split('.')[0]
        _log.info('Starting application "%s"...' % appName)
        if eggSetupMode:
            _log.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter("[SETUP] %(asctime)s %(name)s:%(levelname)s: %(message)s")
            ch.setFormatter(formatter)
            _log.addHandler(ch)
            _log.info("Setup mode")

        self.OPT = OptHolder(appName, eggSetupMode)
        self.caches = CacheDict()
        self.uniqueVals = ()
        _log.info("---------- Core settings:")
        _log.info("appRoot   == %s" % self.OPT.appRoot)
        _log.info("appPath   == %s" % self.OPT.appPath)
        _log.info("templPath == %s" % self.OPT.templPath)
        _log.info("----------")
        self.plugins = []
        self.pluginsDict = {}
        self.filterStack = []
        self.globalFilterStack = []
        self.enumeratePlugins('%s.controllers.' % appName)
        self.firstRequest = True
        self.version = engineVersion
        if self.OPT.revisionId:
            self.version += ".%s" % self.OPT.revisionId
        self.menuCache = {}
        self.mc = None

    def registerPlugin(self, plugin):
        self.plugins.append(plugin)
        self.pluginsDict[plugin.pluginId()] = plugin

    def enumeratePlugins(self, basicNamespace, eggSetupMode = False):
        pluginsDir = os.path.realpath(os.path.join(self.OPT.appPath, 'controllers'))
        sys.path.append(pluginsDir)
        _log.info("Collecting names of possible plugins...")
        _log.info("Plugins root directory: %s" % pluginsDir)

        namespacesToImport = []
        for root, dirs, files in os.walk(pluginsDir):
            def useFilePred(file):
                if file in self.OPT.disabledModules:
                    _log.warning('File ignored due config settings: %s' % file)
                    return False
                return True
            fileList = filter(lambda x: x.endswith('.py') and not x.startswith('__'), files)
            fileList = filter(useFilePred, fileList)
            fileList = map(lambda x: os.path.join(root, x), fileList)
            fileList = map(lambda x: os.path.splitext(x)[0], fileList)
            fileList = map(lambda x: x.replace(pluginsDir + os.path.sep, ''), fileList)
            fileList = map(lambda x: x.replace(os.path.sep, '.'), fileList)
            namespacesToImport.extend(fileList)

        plugins = {}
        _log.info('Started plugins enumerator...')
        for nsToImport in namespacesToImport:
            if not nsToImport in self.OPT.disabledModules:
                #_log.info('trying %s...' % nsToImport)
                mod = None
                try:
                    mod = __import__(nsToImport, fromlist = '*')
                except Exception, e:
                    _log.warning('Exception while importing %s: %s' % (nsToImport, str(e)))
                    mod = None

                possiblePlugins = []
                plPredicate = lambda x: type(x) == type and issubclass(x, BasePlugin) and x != BasePlugin
                possiblePlugins = inspect.getmembers(mod, plPredicate)
                if possiblePlugins:
                    possiblePlugins = map(lambda x: x[1], possiblePlugins)

                if possiblePlugins:
                    for possiblePlugin in possiblePlugins:
                        instance = possiblePlugin()
                        plid = instance.pluginId()
                        #_log.info("Importing plugin: %s; base=%s" % (plid, nsToImport))

                        if not plugins.has_key(plid):
                            nsName = basicNamespace + mod.__name__
                            ns = __import__(nsName, {}, {}, '*', -1)
                            instance.setDetails(
                                namespace = ns,
                                namespaceName = nsName,
                                fileName = ns.__file__.replace(pluginsDir + os.path.sep, '')
                            )
                            plugins[plid] = instance
                            #_log.info("Successfully imported: %s; %s; %s" % (ns, nsName, nsToImport))
                        else:
                            _log.critical("POSSIBLE CONFLICT: Plugin with id '%s' already imported!" % plid)
                else:
                    _log.info('Not a plugin: %s' % nsToImport)
            else:
                _log.warning('Namespace ignored due config settings: %s' % nsToImport)

        _log.info("IMPORT STAGE COMPLETED. Imported %d plugins:" % len(plugins))
        for plugin in plugins.values():
            _log.info("* %s, %s, %s" % (plugin.pluginId(), plugin.namespaceName(), plugin.fileName()))
        _log.info('RESOLVING DEPENDENCIES...')
        needCheck = True
        while needCheck:
            needCheck = False
            for id in plugins.keys():
                deps = plugins[id].deps()
                if deps:
                    for dep in deps:
                        if not dep in plugins:
                            _log.warning('[WARNING] Disconnected: "%s"; non-existent dependence: "%s"' % (id, dep))
                            del plugins[id]
                            needCheck = True
                            break

        _log.info('Arranging plugins...')
        resolved = []
        needIteration = True
        while needIteration:
            needIteration = False
            for id in plugins.keys():
                #_log.info('testing: ' + id)
                deps = plugins[id].deps()

                ok = True
                if deps:
                    for dep in deps:
                        ok = ok and dep in resolved

                if ok:
                    #if not deps:
                    #    _log.info('No dependencies for "%s"; adding as %d' % (id, len(self.plugins)))
                    #else:
                    #    _log.info('Already resolved dependencies for "%s"; adding as %d' % (id, len(self.plugins)))
                    self.registerPlugin(plugins[id])
                    resolved.append(id)
                    del plugins[id]
                    needIteration = True
                    break
            #_log.info('new iteration, already resolved: %s' % resolved)

        cyclicDeps = sorted(plugins.values(), lambda a, b: cmp(len(a.deps()), len(b.deps())))
        for plugin in cyclicDeps:
            _log.warning('[WARNING] Adding loop-dependant plugin "%s" (deps: %s)' % (plugin.pluginId(), str(plugin.deps())))
            self.registerPlugin(plugin)

        pluginsNames = map(lambda p: p.pluginId(), self.plugins)
        _log.info("RESOLVING STAGE COMPLETED. Connected %d plugins: %s" % (len(self.plugins), str(pluginsNames)))

        _log.info("Updating globals...")
        for plugin in self.plugins:
            plugin.updateGlobals(self) #not eggSetupMode and self or None)

        # creating filters stack
        _log.info("Populating filter's stack...")
        for plugin in self.plugins:
            filters = plugin.filtersList()
            if filters:
                for tfilter in filters:
                    self.filterStack.append(tfilter)
                    _log.info('Added text filter %s from %s' % (str(tfilter), plugin.pluginId()))
            filters = plugin.globalFiltersList()
            if filters:
                for tfilter in filters:
                    self.globalFilterStack.append(tfilter)
                    _log.info('Added global text filter %s from %s' % (str(tfilter), plugin.pluginId()))

        _log.info('COMPLETED PLUGINS CONNECTION STAGE')

    def invalidateMenuCache(self, menuId):
        if menuId in self.menuCache:
            self.menuCache[menuId] = None
        else:
            _log.warning("Nothing to invalidate: %s" % str(menuId))

    def getMenuItems(self, menuId):
        def itemsscmp(a, b):
            return cmp(a.weight, b.weight)
        langMenuId = menuId + get_lang()[0]
        mitems = self.menuCache.get(langMenuId, None)
        if not mitems:
            parentedItems = {}
            uniqueIds = []
            menuProviders = self.implementationsOf(AbstractMenuProvider)
            for plugin in menuProviders:
                items = plugin.menuItemsFor(menuId)
                if items:
                    for item in items:
                        id = item.id
                        if id in uniqueIds:
                            _log.error('Duplicated menu item Ids: %s' % id)
                        else:
                            uniqueIds.append(id)
                        parentid = item.parentId
                        item.plugin = plugin

                        if not parentid in parentedItems:
                            parentedItems[parentid] = []
                        parentedItems[parentid].append(item)

            for key in parentedItems.keys():
                parentedItems[key] = sorted(parentedItems[key], itemsscmp)
            self.menuCache[langMenuId] = parentedItems
            mitems = parentedItems
        return mitems

    def extractFromConfigs(self, elementName):
        #TODO: cache results?
        _log.error('extractFromConfigs() is deprecated, use interfaces and implementationsOf() instead')
        result = []
        plugins = []
        for plugin in self.plugins:
            config = plugin.config
            element = config.get(elementName, None)
            if element:
                result.append(element)
                plugins.append(plugin)
        return (result, plugins)

    def _implementationsOf(self, InterfaceClass):
        #TODO: cache results?
        plugins = []
        for plugin in self.plugins:
            if (issubclass(type(plugin), InterfaceClass)):
                plugins.append(plugin)
        return plugins

    def implementationsOf(self, InterfaceClass):
        return self.caches.setdefaultEx(InterfaceClass, self._implementationsOf, InterfaceClass)
