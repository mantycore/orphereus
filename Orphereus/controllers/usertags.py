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
    def get(name):
        return UserTag.query().filter(UserTag.name == name).first()

    @staticmethod
    def getPostTags(postid, userId):
        ns = g.pluginsDict['usertags'].pnamespace
        return ns.UserTag.query().filter(and_(ns.UserTag.userId == userId, ns.UserTag.posts.any(Post.id == postid))).all()

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
    map.connect('userTagsManager', '/managePostTags/:act/:tagid', controller = 'usertags', action = 'postTagsManage', act = 'show', tagid = 0, requirements = dict(tagid = '\d+'))

def requestHook(baseController):
    pass

def threadPanelCallback(thread, userInst):
    from webhelpers.html.tags import link_to
    if not userInst.Anonymous:
        return link_to(_("[My tags]"), h.url_for('userTagsMapper', post = thread.id))

def threadInfoCallback(thread, userInst):
    ns = g.pluginsDict['usertags'].pnamespace
    from webhelpers.html.tags import link_to
    tags = ns.UserTag.getPostTags(thread.id, userInst.uidNumber)
    result = " "
    for t in tags:
        result += ("%s ") % link_to("/%s/" % t.tag, h.url_for('userTagsFilter', filter = t.tag), title = t.comment)
    return result

def pluginInit(globj = None):
    if globj:
        h.threadPanelCallbacks.append(threadPanelCallback)
        h.threadInfoCallbacks.append(threadInfoCallback)

    config = {'basehook' : requestHook, # hook for base controller constructor
             'routeinit' : routingInit, # routing initializer
             'orminit' : ormInit, # ORM initializer
             'name' : N_('Personal tags module'),
             'ormPropChanger' : ormPropChanger
             }

    return PluginInfo('usertags', config)

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import *

class UsertagsController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__init__(self)

    def postTags(self, post, act, tagid):
        if self.userInst.Anonymous:
            return self.error(_("User tags allowed only for registered users"))
        thread = Post.query().get(int(post))
        if thread:
            if act == 'delete':
                tag = UserTag.query().filter(and_(UserTag.id == int(tagid), UserTag.userId == self.userInst.uidNumber)).first()
                if tag:
                    if thread in tag.posts:
                        tag.posts.remove(thread)
                        meta.Session.commit()
                    else:
                        return self.error(_("This tag isn't mapped to this post"))
                else:
                    return self.error(_("Incorrect tag id"))

            if act == 'add':
                tagName = filterText(request.params.get('tagName', ''))
                tag = UserTag.query().filter(and_(UserTag.tag == tagName, UserTag.userId == self.userInst.uidNumber)).first()
                if not tag:
                    return self.error(_("Tag doesn't exists"))
                tag.posts.append(thread)
                meta.Session.commit()
            c.thread = thread
            c.userTags = UserTag.getPostTags(thread.id, self.userInst.uidNumber)
            return self.render('userTagsForPost')
        else:
            return self.error(_("Incorrect thread id"))

    def postTagsManage(self, act, tagid):
        if self.userInst.Anonymous:
            return self.error(_("User tags allowed only for registered users"))

        if act == 'add':
            tagName = filterText(request.params.get('tagName', ''))
            tag = UserTag.query().filter(and_(UserTag.tag == tagName, UserTag.userId == self.userInst.uidNumber)).first()
            tagDescr = filterText(request.params.get('tagDescr', ''))
            if tagName:
                if not tag:
                    tag = UserTag(tagName, tagDescr, self.userInst.uidNumber)
                    meta.Session.commit()
                else:
                    return self.error(_("Tag already exists"))
        elif act == 'delete':
            tag = UserTag.query().filter(and_(UserTag.id == int(tagid), UserTag.userId == self.userInst.uidNumber)).first()
            if tag:
                meta.Session.delete(tag)
                meta.Session.commit()
            else:
                return self.error(_("Incorrect tag id"))

        c.userTags = UserTag.query().filter(UserTag.userId == self.userInst.uidNumber).all()
        return self.render('userTags')
