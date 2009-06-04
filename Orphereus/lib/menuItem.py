class MenuItem(object):
    def __init__(self, id, text, route, weight, parentId = False ):
        self.id = id
        self.text = text
        self.route = route
        self.weight = weight
        self.parentId = parentId
        self.plugin = ''
        
    def __repr__(self):
        return "<%s/%d (%s)::'%s' (%s)>" % (self.id, self.weight, self.route, self.text, str(self.plugin and self.plugin.pluginId()))
    