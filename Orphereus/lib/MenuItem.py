class MenuItem(object):
    def __init__(self, id,
                       text,
                       route,
                       weight,
                       parentId = False,
                       hint = '',
                       collapse = False,
                       onclick = None,
                       target = None):
        self.id = id
        self.text = text
        self.route = route
        self.weight = weight
        self.parentId = parentId
        self.plugin = ''
        self.hint = hint
        self.collapse = collapse
        self.onclick = onclick
        self.target = target

    def __repr__(self):
        return self.id
        #return "<%s/%d (%s)::'%s' (%s)>" % (self.id, self.weight, self.route, self.text, str(self.plugin and self.plugin.pluginId()))

#
