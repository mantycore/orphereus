class AbstractMultifileHook(object):
    template = None
    action = ''
    
    def allowDisplay(self, context, user):
        return False
    
    def operationCallback(self, controller, postIds):
        return 