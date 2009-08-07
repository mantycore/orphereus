from pylons.i18n import N_

from Orphereus.lib.pluginInfo import *
from Orphereus.lib.constantValues import CFG_LIST
from Orphereus.lib.base import *
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.processFile import processFile

from Orphereus.lib.ibparser.chans.Post import *
from Orphereus.lib.ibparser.chans.Thread import *
from Orphereus.lib.ibparser.reader import ThreadReader
from Orphereus.model.Post import Post as OrphiePost
from Orphereus.model.Tag import Tag

def menuItems(menuId):
    menu = None
    if menuId == "managementMenu":
        menu = (MenuItem('id_ImportThread', _("Import thread"), h.url_for('hsImportThread'), 601, 'id_adminPosts'),)

    return menu

def routingInit(map):
    map.connect('hsImportThread', '/holySynod/import', controller = 'threadImport', action = 'importThread')

def pluginInit(g = None):
    if g:
        pass
        
    config = {'name' : N_('Thread import tool'),
              'routeinit' : routingInit,
              'menuitems' : menuItems
             }

    return PluginInfo('threadimport', config)

from OrphieBaseController import *

class ThreadimportController(OrphieBaseController):
    postMappings = {}
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu")
            
    def initChecks(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canManageBoards() or self.userInst.isBanned()):
            c.errorText = _("No way! You aren't holy enough!")
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')
        
    def fixReferences(self, text):
        def replacer(match):
            postId = match.groups()[0]
            if self.postMappings.has_key(postId):
                localPostId = self.postMappings[postId]
                localPost = OrphiePost.getPost(localPostId)
                localPostLink = h.url_for('thread', **h.postKwargs(localPost.parentid, localPost.id))
                log.debug(localPostLink)
                if self.saveIds:
                    urlArgs = (localPostLink,localPostId,postId)
                else:
                    urlArgs = (localPostLink,localPostId,localPostId)
                return '<a href="%s" onclick="highlight(%s)">&gt;&gt;%s</a>' %urlArgs
        
        refRe = re.compile('<a href=[^>]+>&gt\;&gt\;(\d+)</a>')
        return refRe.sub(replacer, text)
    
    def postToPInfo(self, post, tagstr, parent = None):
        pInfo = empty()
        pInfo.message = self.fixReferences(unicode(post.text))
        pInfo.title = unicode(post.topic)
        pInfo.savedId = post.id
        if self.saveDates:
            pInfo.date = post.date
        if self.saveIds:
            pInfo.secondaryIndex = post.id
        pInfo.postSage = (post.link=='mailto:sage')
        pInfo.messageShort = pInfo.messageRaw = pInfo.messageInfo = pInfo.removemd5 = u''
        pInfo.ip = pInfo.uidNumber = 0
        pInfo.spoiler = False
        pInfo.thread = parent
        pInfo.tags = Tag.stringToTagLists(tagstr, True)[0]
        pInfo.bumplimit = 0
        fileDescriptors = processFile(self.reader.fieldStorage(post.localName), 200, False)
        picInfo = existentPic = fileHolder = False
        if fileDescriptors:
            fileHolder = fileDescriptors[0] # Object for file auto-removing
            if fileHolder:
                fileHolder.disableDeletion()
            picInfo = fileDescriptors[1]
            existentPic = fileDescriptors[2]
            errorMessage = fileDescriptors[3]
            if errorMessage:
                log.error(errorMessage)
                return None
        pInfo.picInfo = picInfo
        pInfo.existentPic = existentPic  
        return pInfo
    
    def savePost(self, pInfo):
        newPost = OrphiePost.create(pInfo)
        self.postMappings[pInfo.savedId] = newPost.id
        return newPost
    
    def importProcess(self, file):
        tags = filterText(request.POST.get('tagline', None))
        self.saveDates = bool(request.POST.get('useDate', False))
        self.saveIds = bool(request.POST.get('useIds', False))
        self.target = int(request.POST.get('target', 0))
        if ((not tags) and (not self.target)):
            c.message = N_('Specify thread or tagline.')
            return
        try:
            self.reader = ThreadReader.createFromPostData(file)
        except:
            c.message = N_('This file is not a thread archive.')
            return
        self.reader.fsClass = FieldStorageLike
        startIndex = 1
        if self.target:
            startIndex = 0
            opPost = OrphiePost.getPost(self.target)
        else:
            opPostInfo = self.postToPInfo(self.reader.thread.posts[0], tags)
            opPost = self.savePost(opPostInfo)
        for post in self.reader.thread.posts[startIndex:]:
            self.savePost(self.postToPInfo(post, None, opPost))
        return opPost
        
    def importThread(self):
        self.initChecks()
        c.boardName = _('Thread import')
        c.currentItemId = 'id_ImportThread'
        file = request.POST.get('file', None)
        if isinstance(file, cgi.FieldStorage) or isinstance(file, FieldStorageLike):
            resPost = self.importProcess(file)
            if resPost:
                c.message = N_('Posts were imported successfully into <a href="%s" target="_blank">this thread<a>.' 
                               %(h.url_for('thread', post=resPost.id)))
        else:
            c.message = N_('Please, select a file.')

        return self.render('importThread')