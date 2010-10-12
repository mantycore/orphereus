from pylons.i18n import N_
from string import *

from Orphereus.lib.BasePlugin import *
from Orphereus.lib.base import redirect_to, request, g, _
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.lib.interfaces.AbstractMultifileHook import AbstractMultifileHook

from Orphereus.model import *
from Orphereus.lib.miscUtils import *

import datetime
import logging
log = logging.getLogger(__name__)

class PicListManagerPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : 'File-only moderation system',
                  'deps' : ('adminpanel',)
                 }
        BasePlugin.__init__(self, 'setsmgr', config)

    def menuItems(self, menuId):
        menu = None
        if menuId == "managementMenu":
            menu = (MenuItem('id_FilesMod', _("Files"), h.url_for('hsFileMod', page=0), 601, 'id_adminPosts'),)
        return menu

    '''def menuItemIsVisible(self, id, baseController)
        %user = baseController.userInst
        if id == 'id_FilesMod':
            return user.canChangeSettings()'''

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('hsFileMod', '/holySynod/pictures/page/{page}', 
                    controller = 'administration/piclist', 
                    action = 'list', 
                    requirements = dict(page = r'\d+'))
        map.connect('hsFileInfo', '/holySynod/pictures/id/{id}', 
                    controller = 'administration/piclist', 
                    action = 'picinfo', 
                    requirements = dict(id = r'\d+'))
        map.connect('hsFileProcess', '/holySynod/pictures/process', 
                    controller = 'administration/piclist', 
                    action = 'process')
                
        """map.connect('hsFilesAct', '/holySynod/pictures/page/{page}', 
                    controller = 'administration/piclist', 
                    action = 'list', 
                    requirements = dict(page = r'\d+'))"""

from Orphereus.controllers.OrphieBaseController import OrphieBaseController

class PiclistController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu", True)

        # multifile ops template init
        c.multifileTemplates = []
        gvars = config['pylons.app_globals']
        callbacks = gvars.implementationsOf(AbstractMultifileHook)
        for cb in callbacks:
            allowDisplay, template = getattr(cb, 'allowDisplay'), getattr(cb, 'template')
            if allowDisplay(c, self.userInst):
                c.multifileTemplates.append(template) 
        #log.info("APPROVED TEMPLATES: %s" % c.multifileTemplates)
            
            
    def __admin__init__(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not self.userInst.isAdmin() or self.userInst.isBanned():
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')
        self.requestForMenu("managementMenu")
        
    def _getPostsForPic(self, picId):
        assocList = PictureAssociation.query.filter(PictureAssociation.fileId == picId).all()
        posts = map(lambda assoc: Post.getPost(assoc.postId).id, assocList)
        return posts
    
    def _getPostsForPics(self, picIds):
        posts = []
        for pic in picIds:
            posts.extend(self._getPostsForPic(pic))
        return posts

    def process(self):
        page = request.POST.get('curpage', 0)
        pictures = []
        task = ''
        retest = re.compile("^\d+$")
        for i in request.POST:
            if retest.match(request.POST[i]):
                pictures.append(int(request.POST[i]))
            if i.startswith('task_'):
                task = i[5:]
        
        posts = self._getPostsForPics(pictures)
        gvars = config['pylons.app_globals']
        callbacks = gvars.implementationsOf(AbstractMultifileHook)
        for cb in callbacks:
            callback, action = getattr(cb, 'operationCallback'), getattr(cb, 'action')
            if (action == task):
                # return "Performed %s on posts %s" % (action, posts)
                callback(self, posts, True)
                return redirect_to("hsFileMod", page=page) 
        return "Callback for action %s not found!" % task
        
    def list(self, page):
        self.__admin__init__()
        c.boardName = 'Files'
        c.currentItemId = 'id_FilesMod'
        count = Picture.query.count()
        page = int(page)
        tpp = 40
        self.paginate(count, page, tpp)
        c.files = Picture.query.order_by(Picture.id.asc())[page * tpp : (page + 1) * tpp]
        return self.render('filelist')
    
    def picinfo(self, id):
        self.__admin__init__()
        c.boardName = 'File info'
        c.currentItemId = 'id_FilesMod'
        c.pic =  Picture.query.get(id)
        assocList = PictureAssociation.query.filter(PictureAssociation.fileId == id).all()
        c.posts = map(lambda assoc: Post.getPost(assoc.postId), assocList)
        return self.render('filelist.file')
        # return "Pic %s: %s<br/> Posts: %s" % (id, c.pic, postList)
