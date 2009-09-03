
class AbstractPostingHook(object):
    def tagCheckHandler(self, tagName, userInst):
        pass

    def tagCreationHandler(self, tagstring, userInst, textFilter):
        pass

    def afterPostCallback(self, post, userInst, params):
        pass

    def beforePostCallback(self, controller, request, **kwargs):
        return None
