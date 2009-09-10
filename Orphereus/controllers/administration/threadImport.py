from pylons.i18n import N_

from Orphereus.lib.BasePlugin import *
from Orphereus.lib.constantValues import CFG_LIST
from Orphereus.lib.base import *
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.processFile import processFile

from Orphereus.lib.ibparser.chans.Post import *
from Orphereus.lib.ibparser.chans.Thread import *
from Orphereus.lib.ibparser.reader import ThreadReader
from Orphereus.lib.interfaces.AbstractMenuProvider import AbstractMenuProvider
from Orphereus.model.Post import Post as OrphiePost
from Orphereus.model.Tag import Tag

class ThreadImportPlugin(BasePlugin, AbstractMenuProvider):
    def __init__(self):
        config = {'name' : N_('Thread import tool'),
                 }
        BasePlugin.__init__(self, 'threadimport', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('hsImportThread', '/holySynod/import', controller = 'administration/threadImport', action = 'importThread')

    def entryPointsList(self):
        return [('import', "ConsoleImport"), ]

    # Implementing AbstractMenuProvider
    def menuItems(self, menuId):
        menu = None
        if menuId == "managementMenu":
            menu = (MenuItem('id_ImportThread', _("Import thread"), h.url_for('hsImportThread'), 601, 'id_adminPosts'),)
        return menu

    def menuTest(self, id, baseController):
        user = baseController.userInst
        if id == 'id_ImportThread':
            return user.canManageBoards()

from OrphieBaseController import *

class ImportWorker():
    postMappings = {}
    def fixReferences(self, text):
        def replacer(match):
            postId = match.groups()[0]
            if self.postMappings.has_key(postId):
                localPostId = self.postMappings[postId]
                localPost = OrphiePost.getPost(localPostId)
                localPostLink = h.url_for('thread', **h.postKwargs(localPost.parentid, localPost.id))
                log.debug(localPostLink)
                if self.saveIds:
                    urlArgs = (localPostLink, localPostId, postId)
                else:
                    urlArgs = (localPostLink, localPostId, localPostId)
                return '<a href="%s" onclick="highlight(%s)">&gt;&gt;%s</a>' % urlArgs
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
        pInfo.postSage = (post.link == 'mailto:sage')
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

    def importProcess(self):
        self.reader.fsClass = FieldStorageLike
        startIndex = 1
        if self.target:
            startIndex = 0
            opPost = OrphiePost.getPost(self.target)
        else:
            opPostInfo = self.postToPInfo(self.reader.thread.posts[0], self.tags)
            opPost = self.savePost(opPostInfo)
        for post in self.reader.thread.posts[startIndex:]:
            self.savePost(self.postToPInfo(post, None, opPost))
        return opPost

    def webImport(self, file):
        self.tags = filterText(request.POST.get('tagline', None))
        self.saveDates = bool(request.POST.get('useDate', False))
        self.saveIds = bool(request.POST.get('useIds', False))
        self.target = int(request.POST.get('target', 0))
        if ((not self.tags) and (not self.target)):
            c.message = N_('Specify thread or tagline.')
            return
        try:
            self.reader = ThreadReader.createFromPostData(file)
        except:
            c.message = N_('This file is not a thread archive.')
            return
        return self.importProcess()

    def fileImport(self, filename, saveDates, saveIds, tagline, target):
        self.tags = tagline
        self.saveDates = saveDates
        self.saveIds = saveIds
        self.target = target
        self.reader = ThreadReader(filename)
        return self.importProcess()

class ThreadimportController(OrphieBaseController):
    def __before__(self):
        OrphieBaseController.__before__(self)
        if ('adminpanel' in g.pluginsDict.keys()):
            self.requestForMenu("managementMenu")

    def initChecks(self):
        if not self.currentUserIsAuthorized():
            return redirect_to('boardBase')
        self.initEnvironment()
        if not (self.userInst.isAdmin() and self.userInst.canManageBoards() or self.userInst.isBanned()):
            return redirect_to('boardBase')
        c.userInst = self.userInst
        if not checkAdminIP():
            return redirect_to('boardBase')

    def importThread(self):
        self.initChecks()
        c.boardName = _('Thread import')
        c.currentItemId = 'id_ImportThread'
        file = request.POST.get('file', None)
        if isinstance(file, cgi.FieldStorage) or isinstance(file, FieldStorageLike):
            importer = ImportWorker()
            resPost = importer.webImport(file)
            if resPost:
                c.message = N_('Posts were imported successfully into <a href="%s" target="_blank">this thread<a>.'
                               % (h.url_for('thread', post = resPost.id)))
        else:
            c.message = N_('Please, select a file.')

        return self.render('importThread')

from paste.script import command
from Orphereus.config.environment import load_environment
from paste.deploy import appconfig

class ConsoleImport(command.Command):
    #max_args = 1
    min_args = 1

    usage = "thread.tar.gz"
    summary = "--config parameter is obligatory"
    group_name = "Thread Import"

    parser = command.Command.standard_parser(verbose = True)
    parser.add_option('--arc',
                      action = 'store',
                      dest = 'archFile',
                      help = "thread file")
    parser.add_option('--tags',
                      action = 'store',
                      dest = 'tags',
                      help = "target tagline, default='import'")
    parser.add_option('--thread',
                      action = 'store',
                      dest = 'thread',
                      help = "target thread")
    parser.add_option('--noids',
                      action = 'store_true',
                      dest = 'noIds',
                      help = 'don\'t restore original post IDs')
    parser.add_option('--nodates',
                      action = 'store_true',
                      dest = 'noDates',
                      help = 'don\'t restore original post timestamps')

    parser.add_option('--config',
                      action = 'store',
                      dest = 'config',
                      help = 'config name (e.g. "development.ini")')
    parser.add_option('--path',
                      action = 'store',
                      dest = 'path',
                      help = 'working dir (e.g. ".")')

    @staticmethod
    def setup_config(filename, relative_to):
        if not relative_to or not os.path.exists(relative_to):
            relative_to = "."
        print 'Loading config "%s" at path "%s"...' % (filename, relative_to)
        conf = appconfig('config:' + filename, relative_to = relative_to)
        load_environment(conf.global_conf, conf.local_conf, False)
        g._push_object(meta.globj) #zomg teh h4x

    def command(self):
        self.setup_config(self.options.config, self.options.path)

        name = self.args[0]
        tags = u'import'
        thread = 0
        if self.options.thread:
            thread = int(self.options.thread)
        if self.options.tags:
            tags = unicode(self.options.tags)

        importer = ImportWorker()
        print "Processing archive..."
        try:
            opPost = importer.fileImport(name, not(self.options.noDates),
                                         not(self.options.noIds), tags, thread)
            print "Imported into thread #%s" % opPost.id
        except Exception, e:
            print "An error occured while trying to import thread: %s" % str(e)
