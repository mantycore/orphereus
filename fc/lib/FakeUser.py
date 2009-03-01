import pickle
from fc.lib.base import *
from fc.lib.miscUtils import *
from fc.model import UserOptions

#it's not really needed to implement all User interface.

class FakeUser(object):
    def __init__(self):
        self.__valid = False
        self.Anonymous = False

        if g.OPT.allowAnonymous:
            self.__valid = True
            self.Anonymous = True
            self.uidNumber = -1
            self.uid = "Anonymous"
            self.filters = ()

            self.__user = empty()
            self.__user.uidNumber = -1
            self.__user.filters = ()

            self.__user.options = empty()
            UserOptions.initDefaultOptions(self.__user.options, g.OPT)

    def isValid(self):
        return self.__valid

    def setUid(self, value=None):
        return self.__user.uid

    def isBanned(self):
        return False

    def secid(self):
        return 0

    def sessValue(self, name, value, default):
        if value != None:
            session[name] = value
            session.save()
        return session.get(name, default)

    def sessPickleValue(self, name, value, default):
        if value != None:
            session[name] = pickle.dumps(value)
            session.save()
        return  pickle.loads(session.get(name, default))

    #customizable options
    def defaultGoto(self, value = None):
        return self.sessValue('defaultGoto', value, self.__user.options.defaultGoto)

    def hideLongComments(self, value=None):
        return self.sessValue('hideLongComments', value, self.__user.options.hideLongComments)

    def mixOldThreads(self, value=None):
        return self.sessValue('mixOldThreads', value, self.__user.options.mixOldThreads)

    def useAjax(self, value=None):
        return self.sessValue('useAjax', value, self.__user.options.useAjax)

    def threadsPerPage(self, value = None):
        return self.sessValue('threadsPerPage', value, self.__user.options.threadsPerPage)

    def repliesPerThread(self, value = None):
        return self.sessValue('repliesPerThread', value, self.__user.options.repliesPerThread)

    def style(self, value = None):
        return self.sessValue('style', value, self.__user.options.style)

    def template(self, value = None):
        return self.sessValue('template', value, self.__user.options.template)

    def expandImages(self, value = None):
        return self.sessValue('expandImages', value, self.__user.options.expandImages)

    def maxExpandWidth(self, value = None):
        return self.sessValue('maxExpandWidth', value, self.__user.options.maxExpandWidth)

    def maxExpandHeight(self, value = None):
        return self.sessValue('maxExpandHeight', value, self.__user.options.maxExpandHeight)

    def homeExclude(self, value = None):
        return self.sessPickleValue('homeExclude',  value, self.__user.options.homeExclude)

    def hideThreads(self, value = None):
        return self.sessPickleValue('hideThreads',  value, self.__user.options.hideThreads)

    # disable any dangerous action
    def isAdmin(self):
        return False

    def canDeleteAllPosts(self):
        return False

    def bantime(self):
        return 0

    def banreason(self):
        return u''

    def optionsDump(self):
        return UserOptions.optionsDump(self.options)

