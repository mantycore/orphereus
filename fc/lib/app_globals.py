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

import logging
log = logging.getLogger(__name__)

class OptHolder(object):
    def __init__(self):
        #in most cases you don't need to change these paths
        self.appPath = os.path.dirname(__file__).replace('/fc/lib', '').replace('\\fc\\lib', '')  #sys.path[0] #os.path.dirname(__file__)
        self.templPath = os.path.join(self.appPath, 'fc/templates/')
        self.captchaFont = os.path.join(self.appPath, 'fc/cfont.ttf')
        self.markupFile = os.path.join(self.appPath, 'wakabaparse/mark.def')

        self.booleanValues = [('core',
                               ('devMode', 'secondaryIndex', 'vitalSigns', 'allowPosting',
                                'allowRegistration', 'allowAnonymous',
                                'allowLogin', 'allowCrossposting', 'allowCrosspostingSvc',
                                'allowPureSvcTagline', 'allowTagCreation', 'boardWideProoflabels',
                                'allowFeeds', 'allowOverview', 'framedMain',
                                'useFrameLogo', 'permissiveFileSizeConjunction',
                                'allowAnonymousPosting', 'allowAnonProfile'
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
                               ('version', 'hashSecret', 'baseDomain',
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
                               ('templates', 'styles', 'languages',
                               )
                              ),

                              ('security',
                               ('alertEmail', 'refControlList', 'fakeLinks',
                                'badUAs',
                               )
                              ),

                            ]

        def booleanGetter(value):
            return value == 'true'
        def stringGetter(value):
            return value
        def intGetter(value):
            return int(value)
        def strListGetter(value):
            return value.split(',')
        def setValues(source, getter):
            for section in source:
                sectionName = section[0]
                for valueName in section[1]:
                    value = getter(config['%s.%s' % (sectionName, valueName)])
                    setattr(self, valueName, value)
                    log.debug('%s.%s = %s' % (sectionName, valueName, str(getattr(self, valueName))))

        setValues(self.booleanValues, booleanGetter)
        setValues(self.stringValues, stringGetter)
        setValues(self.intValues, intGetter)
        setValues(self.strListValues, strListGetter)

        # Basic IB settings
        if not os.path.exists(self.uploadPath):
            self.uploadPath = os.path.join(self.appPath, 'fc/uploads/')

        if not os.path.exists(self.staticPath):
            self.staticPath = os.path.join(self.appPath, 'fc/public/')

        self.languages.insert(0, 'Default')
        self.obfuscator = self.obfuscator.replace('$(', '%(')
        self.allowAnonymousPosting = self.allowAnonymous and self.allowAnonymousPosting
        self.allowAnonProfile = self.allowAnonymous and self.allowAnonProfile

class Globals(object):
    def __init__(self):
        self.OPT = OptHolder()
        self.caches = {}

        self.uniqueVals = ()

