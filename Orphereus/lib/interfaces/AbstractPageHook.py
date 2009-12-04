class AbstractPageHook(object):
    def headCallback(self, context):
        return None

    def boardInfoCallback(self, context):
        return None

    #[X] {panel callback} 01.01.1979 12:34:56 {header callback} [Reply] {info callback}
    def threadPanelCallback(self, thread, userInst):
        return None

    def postPanelCallback(self, thread, post, userInst):
        return None

    def threadInfoCallback(self, thread, userInst):
        return None

    def postHeaderCallback(self, thread, post, userInst):
        return None

    def threadHeaderCallback(self, thread, userInst):
        return None
