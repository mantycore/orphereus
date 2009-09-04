class AbstractPageHook(object):
    def threadPanelCallback(self, thread, userInst):
        return None

    def postPanelCallback(self, thread, post, userInst):
        return None

    def threadInfoCallback(self, thread, userInst):
        return None

    def headCallback(self, context):
        return None
