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
              }

    simpleValues = booleanValues + intValues + stringValues

    def __getattr__(self, name):
        if name in self.simpleValues:
            return self.simpleGetter(name)
        else:
            return object.__getattr__(self, name)

    def __setattr__(self, name, value):
        if name in self.simpleValues:
            self.simpleSetter(name, value)
        else:
            object.__setattr__(self, name, value)
