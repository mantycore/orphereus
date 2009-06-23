from pylons.i18n import N_
from string import *

from Orphereus.lib.pluginInfo import PluginInfo
from Orphereus.lib.menuItem import MenuItem
from Orphereus.lib.miscUtils import *
from Orphereus.lib.base import *
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class UserTag(object):
    def __init__(self, name, comment, uidNumber):
        self.tag = name
        self.comment = comment
        self.userId = uidNumber

    @staticmethod
    def get(tagName, userInst):
        return UserTag.query().filter(and_(UserTag.tag == tagName, UserTag.userId == userInst.uidNumber)).first()

    @staticmethod
    def getById(tagid, userInst):
        return UserTag.query().filter(and_(UserTag.id == int(tagid), UserTag.userId == userInst.uidNumber)).first()

    @staticmethod
    def getPostTags(postid, userId):
        ns = g.pluginsDict['usertags'].pnamespace
        return ns.UserTag.query().filter(and_(ns.UserTag.userId == userId, ns.UserTag.posts.any(Post.id == postid))).all()

    def addToThread(self, thread):
        if not thread in self.posts:
            self.posts.append(thread)
            meta.Session.commit()
            return True
        return False
    """
        @staticmethod
        def getMappingTable():
            if not UserTag.userTagsToPostsMappingTable:
                UserTag.userTagsToPostsMappingTable = sa.Table("usertagsToPostsMap", meta.metadata,
                sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id')),
                sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('usertag.id')),
                )
            return UserTag.userTagsToPostsMappingTable
    """
def ormPropChanger(orm, propDict, namespace):
    pass
    #propDict['Post']['userTags'] = orm.relation(namespace.UserTag, secondary = namespace.UserTag.getMappingTable())

def ormInit(orm, namespace, propDict):
    t_usertags = sa.Table("usertag", meta.metadata,
        sa.Column("id"       , sa.types.Integer, primary_key = True),
        sa.Column('userId'  , sa.types.Integer, sa.ForeignKey('user.uidNumber')),
        sa.Column("tag"      , sa.types.UnicodeText, nullable = False),
        sa.Column("comment"  , sa.types.UnicodeText, nullable = True),
        )

    t_userTagsToPostsMappingTable = sa.Table("usertagsToPostsMap", meta.metadata,
        sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('post.id')),
        sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('usertag.id')),
        )

    #orm.mapper
    meta.Session.mapper(namespace.UserTag, t_usertags, properties = {
        'user' : orm.relation(User),
        'posts' : orm.relation(Post, secondary = t_userTagsToPostsMappingTable),
        })

def routingInit(map):
    map.connect('userTagsMapper', '/postTags/:post/:act/:tagid', controller = 'usertags', action = 'postTags', act = 'show', tagid = 0, requirements = dict(post = '\d+', tagid = '\d+'))
    map.connect('userTagsManager', '/userProfile/manageUserTags/:act/:tagid', controller = 'usertags', action = 'postTagsManage', act = 'show', tagid = 0, requirements = dict(tagid = '\d+'))

def requestHook(baseController):
    pass

def threadPanelCallback(thread, userInst):
    from webhelpers.html.tags import link_to
    if not userInst.Anonymous:
        return link_to(_("[My tags]"), h.url_for('userTagsMapper', post = thread.id), target = "_blank")
    return ''

def threadInfoCallback(thread, userInst):
    ns = g.pluginsDict['usertags'].pnamespace
    from webhelpers.html.tags import link_to
    result = ''
    if not userInst.Anonymous:
        tags = ns.UserTag.getPostTags(thread.id, userInst.uidNumber)
        result = " "
        for t in tags:
            result += ("%s ") % link_to("/$%s/" % t.tag, h.url_for('boardBase', board = '$' + t.tag), title = t.comment)
    return result

def tagHandler(tag, userInst):
    ns = g.pluginsDict['usertags'].pnamespace
    if not userInst.Anonymous:
        tag = ns.UserTag.query().filter(and_(ns.UserTag.tag == tag[1:], ns.UserTag.userId == userInst.uidNumber)).first()
        if tag:
            ids = []
            for post in tag.posts:
                ids.append(post.id)
            #log.critical(ids)
            if ids:
                return Post.id.in_(ids)
    return None

def profileLinks():
    links = (('userTagsManager', {}, _('User tags')),)
    return links

def tagCheckHandler(tagName, userInst):
    ns = g.pluginsDict['usertags'].pnamespace
    name = tagName
    if name.startswith('$'):
        name = tagName[1:]
    if not userInst.Anonymous:
        return ns.UserTag.get(name, userInst)
    else:
         return name != tagName

def tagCreationHandler(tagstring, userInst, textFilter):
    afterPostCallbackParams = []
    newTagString = tagstring
    from Orphereus.controllers.Orphie_Main import OrphieMainController
    ns = g.pluginsDict['usertags'].pnamespace
    tags, dummy, nonexistent = Tag.stringToTagLists(tagstring, False)
    for usertag in nonexistent:
        if usertag.startswith('$'):
            nonexistent.remove(usertag)
            if not userInst.Anonymous:
                usertag = usertag[1:]
                tag = ns.UserTag.get(usertag, userInst)
                if not tag:
                    descr = OrphieMainController.getTagDescription(usertag, textFilter)
                    tag = ns.UserTag(usertag, descr, userInst.uidNumber)
                    meta.Session.commit()
                afterPostCallbackParams.append(tag)
    newTagString = ''
    for tag in tags:
        newTagString += '%s ' % tag.tag
    newTagString += ' '.join(nonexistent)
    return (newTagString, afterPostCallbackParams)

def afterPostCallback(post, userInst, params):
    for tag in params:
        tag.addToThread(post)

def pluginInit(globj = None):
    if globj:
        h.threadPanelCallbacks.append(threadPanelCallback)
        h.threadInfoCallbacks.append(threadInfoCallback)
        if not getattr(globj, 'tagHandlers', None):
            globj.tagHandlers = []
        globj.tagHandlers.append(tagHandler)

    config = {'basehook' : requestHook, # hook for base controller constructor
             'routeinit' : routingInit, # routing initializer
             'orminit' : ormInit, # ORM initializer
             'name' : N_('Personal tags module'),
             'ormPropChanger' : ormPropChanger,
             'additionalProfileLinks' : profileLinks,
             'tagCreationHandler' : tagCreationHandler,
             'tagCheckHandler' : tagCheckHandler,
             'afterPostCallback' : afterPostCallback,
             }

    return PluginInfo('usertags', config)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import *

class UsertagsController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    def postTags(self, post, act, tagid):
        if self.userInst.Anonymous:
            return self.error(_("User tags allowed only for registered users"))
        c.boardName = _('User tags of thread')
        thread = Post.query().get(int(post))
        if thread:
            doRedir = False
            if act == 'delete':
                tag = UserTag.query().filter(and_(UserTag.id == int(tagid), UserTag.userId == self.userInst.uidNumber)).first()
                if tag:
                    if thread in tag.posts:
                        tag.posts.remove(thread)
                        meta.Session.commit()
                        doRedir = True
                    else:
                        return self.error(_("This tag isn't mapped to this post"))
                else:
                    return self.error(_("Incorrect tag id"))

            if act == 'add':
                tagName = filterText(request.params.get('tagName', ''))
                tag = UserTag.get(tagName, self.userInst) #UserTag.query().filter(and_(UserTag.tag == tagName, UserTag.userId == self.userInst.uidNumber)).first()
                if not tag:
                    tag = UserTag.getById(tagid, self.userInst) #UserTag.query().filter(and_(UserTag.id == int(tagid), UserTag.userId == self.userInst.uidNumber)).first()
                if not tag:
                    return self.error(_("Tag doesn't exists"))
                if tag.addToThread(thread):
                    doRedir = True
                else:
                    return self.error(_("This tag already mapped to this post"))
            if doRedir:
                return redirect_to('userTagsMapper', post = thread.id)
            c.thread = thread
            c.userTags = UserTag.getPostTags(thread.id, self.userInst.uidNumber)
            c.allTags = UserTag.query().filter(UserTag.userId == self.userInst.uidNumber).all()
            return self.render('userTagsForPost')
        else:
            return self.error(_("Incorrect thread id"))

    def postTagsManage(self, act, tagid):
        if self.userInst.Anonymous:
            return self.error(_("User tags allowed only for registered users"))

        c.boardName = _('User tags management')
        doRedir = False
        if act == 'add':
            tagName = filterText(request.params.get('tagName', ''))
            tag = UserTag.get(tagName, self.userInst)
            tagDescr = filterText(request.params.get('tagDescr', ''))
            if tagName:
                if not tag:
                    tag = UserTag(tagName, tagDescr, self.userInst.uidNumber)
                    meta.Session.commit()
                    doRedir = True
                else:
                    return self.error(_("Tag already exists"))
        elif act == 'delete' or act == 'removefromall':
            tag = UserTag.getById(tagid, self.userInst) #UserTag.query().filter(and_(UserTag.id == int(tagid), UserTag.userId == self.userInst.uidNumber)).first()
            if tag:
                if act == 'delete':
                    if not tag.posts:
                        meta.Session.delete(tag)
                        meta.Session.commit()
                        doRedir = True
                    else:
                        return self.error(_("Can't delete mapped tag"))
                elif act == 'removefromall':
                    tag.posts = []
                    meta.Session.commit()
                    doRedir = True
            else:
                return self.error(_("Incorrect tag id"))
        if doRedir:
            return redirect_to('userTagsManager')
        c.userTags = UserTag.query().filter(UserTag.userId == self.userInst.uidNumber).all()
        return self.render('userTags')
