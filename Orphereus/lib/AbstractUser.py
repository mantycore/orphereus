import pickle

from Orphereus.lib.constantValues import *
import Orphereus.lib.helpers as h
from pylons import g

class AbstractUser(object):
    booleanValues = ('hideLongComments',
                          'useFrame',
                          'useAjax',
                          'mixOldThreads',
                          'expandImages',
                          'oekUseSelfy',
                          'oekUseAnim',
                          'oekUsePro',
                          'useTitleCollapse',
                          'hlOwnPosts',
                          'invertSortingMode',
                         )
    intValues = ('threadsPerPage',
                 'repliesPerThread',
                 'maxExpandWidth',
                 'maxExpandHeight',
                 'defaultGoto',
                 )
    stringValues = ('style',
                    'template',
                    'lang',
                    'cLang',
                    )
    pickleValues = ('homeExclude',
                    'hideThreads',
                    )
    restrictions = {'threadsPerPage' : lambda val: 0 < val < 30,
                    'repliesPerThread' : lambda val: 0 < val < 100,
                    'maxExpandWidth' : lambda val: 0 < val < 4096,
                    'maxExpandHeight' : lambda val: 0 < val < 4096,
                    'defaultGoto' : lambda val: val in destinations.keys(),

                    'style' : lambda val: val in g.OPT.styles,
                    'template' : lambda val: val in g.OPT.templates,
                    'lang' : lambda val: val in g.OPT.languages,
                    'cLang' : lambda val: val in g.OPT.languages,
                   }

    proxies = {'lang' : lambda val: h.makeLangValid(val),
               'cLang' : lambda val: h.makeLangValid(val),
               'homeExclude' : lambda val: pickle.dumps(val),
               'hideThreads' : lambda val: pickle.dumps(val),
              }

    preparators = {'homeExclude' : lambda val: pickle.loads(val),
                   'hideThreads' : lambda val: pickle.loads(val),
                  }
    simpleValues = booleanValues + intValues + stringValues + pickleValues

    def __getattr__(self, name):
        if name in self.simpleValues:
            val = self.simpleGetter(name)
            preparator = self.preparators.get(name, None)
            if preparator:
                val = preparator(val)
            return val
        #else:
        #    return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if name in self.simpleValues:
            proxy = self.proxies.get(name, None)
            if proxy:
                value = proxy(value)
            self.simpleSetter(name, value)
        else:
            object.__setattr__(self, name, value)
