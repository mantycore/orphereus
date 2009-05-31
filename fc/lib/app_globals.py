################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #                                                                         #
################################################################################

"""The application's Globals object"""
from pylons import config
import sys
import os

from fc.lib.pluginInfo import PluginInfo

import logging
log = logging.getLogger("CORE")

class OptHolder(object):
    def __init__(self, appName):
        #in most cases you don't need to change these paths
        self.appRoot = os.path.dirname(__file__).replace('/%s/lib' % appName, '').replace('\\%s\\lib' % appName, '')
        self.appPath = os.path.join(self.appRoot, appName)
        self.templPath = os.path.join(self.appPath, 'templates')

        self.captchaFont = os.path.join(self.appRoot, 'fc/cfont.ttf')
        self.markupFile = os.path.join(self.appRoot, 'wakabaparse/mark.def')

        self.booleanValues = [('core',
                               ('devMode', 'secondaryIndex', 'vitalSigns', 'allowPosting',
                                'allowRegistration', 'allowAnonymous',
                                'allowLogin', 'allowCrossposting', 'allowCrosspostingSvc',
                                'allowPureSvcTagline', 'allowTagCreation', 'boardWideProoflabels',
                                'allowFeeds', 'allowOverview', 'framedMain',
                                'useFrameLogo', 'permissiveFileSizeConjunction',
                                'allowAnonymousPosting', 'allowAnonProfile',
                                'obligatoryFrameCreation',
                               )
                              ),

                              ('defaults',
                               ('defImagelessThread', 'defImagelessPost', 'defImages',
                                'defEnableSpoilers', 'defCanDeleteOwnThreads', 'defSelfModeration',
                               )
                              ),

                              ('security',
                               ('useXRealIP', 'saveAnyIP', 'refControlEnabled',
                                'checkUAs', 'spiderTrap', 'interestingNumbers',
                                'useAnalBarriering', 'enableFinalAnonymity', 'hlAnonymizedPosts',
                               ),

                              )
                             ]

        self.stringValues = [('core',
                               ('urlPrefix', 'version', 'hashSecret', 'baseDomain',
                                'staticPathWeb', 'filesPathWeb', 'actuator',
                                'defaultFrame', 'staticPath', 'uploadPath',
                               )
                              ),

                              ('security',
                               ('alertServer', 'alertSender', 'alertPassword',
                                'obfuscator',
                               )
                              ),
                            ]

        self.intValues = [('core',
                               ('minPassLength', 'statsCacheTime',
                               )
                              ),

                              ('defaults',
                               ('defThumbSize', 'defMinPicSize', 'defMaxFileSize',
                               )
                              ),

                              ('security',
                               ('alertPort', 'finalAHoursDelay',
                               )
                              ),

                            ]

        self.strListValues = [('core',
                               ('disabledModules', 'templates', 'styles', 'languages',
                               )
                              ),

                              ('security',
                               ('alertEmail', 'refControlList', 'fakeLinks',
                                'badUAs',
                               )
                              ),

                            ]

        self.setValues(self.booleanValues, self.booleanGetter)
        self.setValues(self.stringValues, self.stringGetter)
        self.setValues(self.intValues, self.intGetter)
        self.setValues(self.strListValues, self.strListGetter)

        # Basic IB settings
        if not os.path.exists(self.uploadPath):
            self.uploadPath = os.path.join(self.appRoot, 'fc/uploads/')

        if not os.path.exists(self.staticPath):
            self.staticPath = os.path.join(self.appRoot, 'fc/public/')

        self.languages.insert(0, 'Default')
        self.obfuscator = self.obfuscator.replace('$(', '%(')
        self.allowAnonymousPosting = self.allowAnonymous and self.allowAnonymousPosting
        self.allowAnonProfile = self.allowAnonymous and self.allowAnonProfile

    @staticmethod
    def booleanGetter(value):
        return value == 'true'
    @staticmethod
    def stringGetter(value):
        return value
    @staticmethod
    def intGetter(value):
        return int(value)
    @staticmethod
    def strListGetter(value):
        return value.split(',')
    def setValues(self, source, getter):
        for section in source:
            sectionName = section[0]
            for valueName in section[1]:
                value = getter(config['%s.%s' % (sectionName, valueName)])
                setattr(self, valueName, value)
                log.debug('%s.%s = %s' % (sectionName, valueName, str(getattr(self, valueName))))



class Globals(object):
    def __init__(self):
        appName = 'fc'
        self.OPT = OptHolder(appName)
        self.caches = {}
        self.uniqueVals = ()
        log.info("---------- Core settings:")
        log.info("appRoot   == %s" % self.OPT.appRoot)
        log.info("appPath   == %s" % self.OPT.appPath)
        log.info("templPath == %s" % self.OPT.templPath)
        log.info("----------")
        self.plugins = []
        self.pluginsDict = {}
        self.filterStack = []
        self.enumeratePlugins('%s.controllers.' % appName)
        self.firstRequest = True

    def registerPlugin(self, plugin):
        self.plugins.append(plugin)
        self.pluginsDict[plugin.pluginId()] = plugin

    def enumeratePlugins(self, basicNamespace):
        import sys
        def pluginscmp(a, b):
            return cmp(len(a.deps()), len(b.deps()))

        pluginDir = os.path.join(self.OPT.appPath, 'controllers')
        sys.path.append(pluginDir)
        #files = [f for f in os.listdir(pluginDir) if f[:3] == "atl" and  f[-3:]=='.py']
        files = [f for f in os.listdir(pluginDir) if f[-3:] == '.py']
        plugins = {}
        log.info('Started plugins enumerator...')
        for file in files:
            if not file in self.OPT.disabledModules:
                [fn, ext] = os.path.splitext(file)
                log.info('trying %s...' % file)
                mod = None
                try:
                    mod = __import__(fn)
                except Exception, e:
                    log.warning('Exception while importing %s: %s' % (file, str(e)))
                    mod = None
                if mod and ("pluginInit" in dir(mod)):
                    plinf = mod.pluginInit(self)
                    tmpInfo = PluginInfo('', {})
                    if plinf and type(plinf) == type(tmpInfo):
                        plid = plinf.pluginId()
                        log.info("Importing plugin: %s; file= %s" % (plid, file))

                        if not plugins.has_key(plid):
                            plinf.pfileName = file
                            # TODO: eliminate hardcoded name
                            plinf.pnamespaceName = basicNamespace + mod.__name__
                            plinf.pnamespace = __import__(plinf.pnamespaceName, globals(), locals(), '*', -1)
                            plugins[plid] = plinf
                        else:
                            log.critical("POSSIBLE CONFLICT: Plugin with id '%s' already imported!" % plid)
                    else:
                        log.warning('Plugin returned incorrect descriptor')
                else:
                    log.info('Not a plugin: %s' % file)
            else:
                log.warning('Ignored due config settings: %s' % file)
        log.info("IMPORT STAGE COMPLETED. Imported %d plugins: %s" % (len(plugins), str(plugins.keys())))
        log.info('RESOLVING DEPENDENCIES...')
        needCheck = True
        while needCheck:
            needCheck = False
            for id in plugins.keys():
                deps = plugins[id].deps()
                if deps:
                    for dep in deps:
                        if not dep in plugins:
                            log.warning('[WARNING] Disconnected: "%s"; non-existent dependence: "%s"' % (id, dep))
                            del plugins[id]
                            needCheck = True
                            break

        log.info('Arranging plugins...')
        resolved = []
        needIteration = True
        while needIteration:
            needIteration = False
            for id in plugins.keys():
                #log.info('testing: ' + id)
                deps = plugins[id].deps()

                ok = True
                if deps:
                    for dep in deps:
                        ok = ok and dep in resolved

                if ok:
                    #if not deps:
                    #    log.info('No dependencies for "%s"; adding as %d' % (id, len(self.plugins)))
                    #else:
                    #    log.info('Already resolved dependencies for "%s"; adding as %d' % (id, len(self.plugins)))
                    self.registerPlugin(plugins[id])
                    resolved.append(id)
                    del plugins[id]
                    needIteration = True
                    break
            #log.info('new iteration, already resolved: %s' % resolved)

        cyclicDeps = sorted(plugins.values(), pluginscmp)
        for plugin in cyclicDeps:
            log.warning('[WARNING] Adding loop-dependant plugin "%s" (deps: %s)' % (plugin.pluginId(), str(plugin.deps())))
            self.registerPlugin(plugin)

        #log.info("Connected %d plugins" % len(self.plugins))
        log.info("RESOLVING STAGE COMPLETED. Connected %d plugins: %s" % (len(self.plugins), str(self.pluginsDict.keys())))

        # creating filters stack
        log.info("Populating filter's stack...")
        for plugin in self.plugins:
            filter = plugin.outHook()
            if filter:
                self.filterStack.append(filter)
                log.info('Added text filter %s from %s' % (str(filter), plugin.pluginId()))

        log.info('COMPLETED PLUGINS CONNECTION STAGE')
