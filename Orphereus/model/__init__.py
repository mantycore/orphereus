import sqlalchemy as sa
from sqlalchemy import orm
from Orphereus.model import meta
from Orphereus.lib.constantValues import *
from Orphereus.lib.cache import MCache
from pylons import config

from FCCaptcha import *
from Extension import *
from Invite import *
from LogEntry import *
from LoginTracker import *
from Oekaki import *
from Picture import *
from Post import *
from Setting import *
from Tag import *
from TagOptions import *
from User import *
from UserFilters import *
from UserOptions import *
from Ban import *

import logging
log = logging.getLogger("ORM (%s)" % __name__)

def batchProcess(query, routine, packetSize = 1000):
    currentPacket = 0
    totalSize = query.count()
    while currentPacket < totalSize:
        maxId = currentPacket + packetSize
        if maxId > totalSize:
            maxId = totalSize
        routine(query[currentPacket:maxId])
        currentPacket += packetSize
        meta.Session.commit()

def init_model(engine):
    log.info("Trying to adjust engine to current dialect...")
    def logAndChange(var, newType):
        log.info("Using %s instead of %s" % (str(newType), str(var)))
        return newType
    if (isinstance(engine.dialect, sa.databases.mysql.MySQLDialect)):
        log.info("Currently using MySQL dialect, adjusting types...")
        meta.FloatType = logAndChange(meta.FloatType, sa.databases.mysql.MSDouble)
        meta.BlobType = logAndChange(meta.BlobType, sa.databases.mysql.MSLongBlob)
        meta.UIntType = logAndChange(meta.UIntType, sa.databases.mysql.MSInteger(unsigned = True))
    elif (isinstance(engine.dialect, sa.databases.postgres.PGDialect)):
        log.info("Currently using PostgreSQL dialect, adjusting types...")
        meta.FloatType = logAndChange(meta.FloatType, sa.databases.postgres.PGFloat)
        meta.BlobType = logAndChange(meta.BlobType, sa.databases.postgres.PGBinary)
        meta.UIntType = logAndChange(meta.UIntType, sa.databases.postgres.PGBigInteger)
    else:
        log.info("[WARNING] Unknown SQL Dialect!")
    log.info("Adjusting completed")

    sm = orm.sessionmaker(autoflush = False, autocommit = False, bind = engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    #log.debug(dir(engine))
    #log.debug(dir(engine.logger))
    #engine.echo = True
    #engine.logger.setLevel('debug')
    #import logging

    #logging.basicConfig()
    #logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.DEBUG)
    #logging.getLogger('sqlalchemy.orm.logging').setLevel(logging.DEBUG)


    LoginTrackerProps = {}
    CaptchaProps = {}
    OekakiProps = {}
    InviteProps = {}
    SettingProps = {}
    BanProps = {}

    UserOptionsProps = {}
    UserFiltersProps = {}
    UserProps = {
            'options' : orm.relation(UserOptions, uselist = False, backref = 'user', cascade = "all, delete, delete-orphan", lazy=False),
            'filters' : orm.relation(UserFilters, backref = 'user', cascade = "all, delete, delete-orphan", lazy=False)
                }

    ExtensionProps = {}
    PictureProps = {
        'extension' : orm.relation(Extension)
        }
    TagOptionsProps = {}
    TagProps = {
            'options' : orm.relation(TagOptions, uselist = False, backref = 'tag', cascade = "all, delete, delete-orphan")
        }
    PostProps = {
        'tags' : orm.relation(Tag, secondary = t_tagsToPostsMap),
        'file': orm.relation(Picture),
        'parentPost' : orm.relation(Post, remote_side = [t_posts.c.id]),
        }
    LogEntryProps = {
        'user' : orm.relation(User)
        }

    propDict = {
                "LoginTracker" : LoginTrackerProps,
                "Captcha" : CaptchaProps,
                "Oekaki" : OekakiProps,
                "Invite" : InviteProps,
                "Settings" : SettingProps,
                "Ban" : BanProps,
                "UserOptions": UserOptionsProps,
                "UserFilters" : UserFiltersProps,
                "User" : UserProps,
                "Extension" : ExtensionProps,
                "Picture" : PictureProps,
                "TagOptions" : TagOptionsProps,
                "Tag" : TagProps,
                "Post" : PostProps,
                "LogEntry" : LogEntryProps,
                }

    gvars = config['pylons.app_globals']
    log.info('Extending ORM properties, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        pconfig = plugin.config
        ormPropChanger = pconfig.get('ormPropChanger', None)
        if ormPropChanger:
            log.info('calling ORM extender %s from: %s' % (str(ormPropChanger), plugin.pluginId()))
            ormPropChanger(orm, propDict, plugin.namespace())
    log.info('COMPLETED ORM EXTENDING STAGE')

    #create mappings
    meta.Session.mapper(LoginTracker, t_logins, properties = LoginTrackerProps)
    meta.Session.mapper(Captcha, t_captchas, properties = CaptchaProps)
    meta.Session.mapper(Oekaki, t_oekaki, properties = OekakiProps)
    meta.Session.mapper(Invite, t_invites, properties = InviteProps)
    meta.Session.mapper(Setting, t_settings, properties = SettingProps)
    meta.Session.mapper(Ban, t_bans, properties = BanProps)

    meta.Session.mapper(UserOptions, t_userOptions, properties = UserOptionsProps)
    meta.Session.mapper(UserFilters, t_userFilters, properties = UserFiltersProps)
    meta.Session.mapper(User, t_users, properties = UserProps)

    meta.Session.mapper(Extension, t_extension, properties = ExtensionProps)
    meta.Session.mapper(Picture, t_piclist, properties = PictureProps)

    meta.Session.mapper(TagOptions, t_tagOptions, properties = TagOptionsProps)
    meta.Session.mapper(Tag, t_tags, properties = TagProps)
    meta.Session.mapper(Post, t_posts, properties = PostProps)

    meta.Session.mapper(LogEntry, t_log, properties = LogEntryProps)

    gvars = config['pylons.app_globals']
    log.info('Initialzing ORM, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        orminit = plugin.ormInit()
        if orminit:
            log.info('calling ORM initializer %s from: %s' % (str(orminit), plugin.pluginId()))
            orminit(orm, plugin.namespace(), propDict)
    log.info('COMPLETED ORM INITIALIZATION STAGE')
    
def upd_globals():
    adminTagsLine = meta.globj.OPT.adminOnlyTags
    meta.globj.forbiddenTags = Tag.csStringToExTagIdList(adminTagsLine)

    meta.globj.additionalLinks = []
    links = meta.globj.OPT.additionalLinks
    if links:
        for link in links:
            meta.globj.additionalLinks.append(link.split('|'))

    meta.globj.sectionNames = meta.globj.OPT.sectionNames 
    meta.globj.disabledTags = meta.globj.OPT.disabledTags
    meta.globj.OPT.memcachedServers = list([str(server) for server in meta.globj.OPT.memcachedServers])
    meta.globj.OPT.cachePrefix = str(meta.globj.OPT.cachePrefix) 
    if meta.globj.mc:
        del meta.globj.mc
    meta.globj.mc = MCache(meta.globj.OPT.memcachedServers, debug=0, key=meta.globj.OPT.cachePrefix)

    log.info('UPDATING GLOBALS COMPLETED')
    
def init_globals(globalObject, setupMode):
    meta.globj = globalObject

    if not setupMode:
        log.info('LOADING CONFIGURATION DATA')
        meta.globj.OPT.initValues(Setting)
        log.info('LOAD COMPLETED')
        
        upd_globals()

    """
    gv = config['pylons.g']
    gv.tagCache = {}
    tags = meta.Session.query(Tag).all()
    for tag in tags:
        gv.tagCache[tag.tag] = tag.id

    log.debug(gv.tagCache)
    """

# Code below is incorrect because key filed doesn't exists
# Note: TagMapping deletion is correct
#class TagMapping(object):
#    pass
#orm.mapper(TagMapping, t_tagsToPostsMap)

