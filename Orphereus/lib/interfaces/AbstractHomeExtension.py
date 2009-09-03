class AbstractHomeExtension(object):
    def __init__(self, templateName):
        self.templateName = templateName

    def prepareData(self, controller, container):
        pass
