from pylons.i18n import get_lang

class AbstractMenuProvider(object):
    def menuItemsFor(self, menuId):
        ret = None
        id = menuId + get_lang()[0]
        if not getattr(self, "__pmenuItems", None): # we don't want to write constructor only for this variable
            self.__pmenuItems = {}
        ret = self.__pmenuItems.get(id, False)
        if not ret:
            ret = self.menuItems(menuId)
            self.__pmenuItems[id] = ret
        return ret

    def MenuItemIsVisible(self, id, baseController):
        return True

    def menuItems(self, menuId):
        return ()
