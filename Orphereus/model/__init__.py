import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import mapper as sqla_mapper

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

def session_mapper(scoped_session):
    def mapper(cls, *arg, **kw):
        validate = kw.pop('validate', False)

        if cls.__init__ is object.__init__:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    if validate:
                        if not cls_mapper.has_property(key):
                            raise TypeError(
                                "Invalid __init__ argument: '%s'" % key)
                    setattr(self, key, value)
            cls.__init__ = __init__
        cls.query = scoped_session.query_property()
        return sqla_mapper(cls, *arg, **kw)
    return mapper

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

def adjust_dialect(engine, name = 'default'):
    log.info("Trying to adjust %s engine to current dialect..." % name)
    target = meta

    def logAndChange(var, newType):
        log.info("Using %s instead of %s" % (str(newType), str(var)))
        return newType

    if (engine.dialect.name.lower() == "postgresql"):
        log.info("Currently using MySQL dialect, adjusting types...")
        from sqlalchemy.databases import mysql
        target.FloatType = logAndChange(meta.FloatType, mysql.MSDouble)
        target.BlobType = logAndChange(meta.BlobType, sa.databases.mysql.MSLongBlob)
        target.UIntType = logAndChange(meta.UIntType, sa.databases.mysql.MSInteger(unsigned = True))
    elif (engine.dialect.name.lower() == "mysql"):
        log.info("Currently using PostgreSQL dialect, adjusting types...")
        from sqlalchemy.databases import postgresql
        target.FloatType = logAndChange(meta.FloatType, postgresql.DOUBLE_PRECISION)
        target.BlobType = logAndChange(meta.BlobType, postgresql.BYTEA)
        target.UIntType = logAndChange(meta.UIntType, postgresql.BIGINT)
    else:
        log.warning("Unknown SQL Dialect!")
    log.info("Adjusting completed")

def init_model(engine):
    adjust_dialect(engine)

    sm = orm.sessionmaker(autoflush = False, autocommit = False, bind = engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    meta.mapper = session_mapper(meta.Session)
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
            'options' : orm.relation(UserOptions, uselist = False, backref = 'user', cascade = "all, delete, delete-orphan", lazy = False),
            'filters' : orm.relation(UserFilters, backref = 'user', cascade = "all, delete, delete-orphan", lazy = False)
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
        plugin.extendORMProperties(orm, propDict)

        pconfig = plugin.config
        ormPropChanger = pconfig.get('ormPropChanger', None)
        if ormPropChanger:
            log.error('config{} is deprecated')
            log.info('calling ORM extender %s from: %s' % (str(ormPropChanger), plugin.pluginId()))
            ormPropChanger(orm, propDict, plugin.namespace())
    log.info('COMPLETED ORM EXTENDING STAGE')

    #create mappings
    meta.mapper(LoginTracker, t_logins, properties = LoginTrackerProps)
    meta.mapper(Captcha, t_captchas, properties = CaptchaProps)
    meta.mapper(Oekaki, t_oekaki, properties = OekakiProps)
    meta.mapper(Invite, t_invites, properties = InviteProps)
    meta.mapper(Setting, t_settings, properties = SettingProps)
    meta.mapper(Ban, t_bans, properties = BanProps)

    meta.mapper(UserOptions, t_userOptions, properties = UserOptionsProps)
    meta.mapper(UserFilters, t_userFilters, properties = UserFiltersProps)
    meta.mapper(User, t_users, properties = UserProps)

    meta.mapper(Extension, t_extension, properties = ExtensionProps)
    meta.mapper(Picture, t_piclist, properties = PictureProps)

    meta.mapper(TagOptions, t_tagOptions, properties = TagOptionsProps)
    meta.mapper(Tag, t_tags, properties = TagProps)
    meta.mapper(Post, t_posts, properties = PostProps)

    meta.mapper(LogEntry, t_log, properties = LogEntryProps)

    gvars = config['pylons.app_globals']
    log.info('Initialzing ORM, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        plugin.initORM(orm, propDict)

        """
        orminit = plugin.ormInit()
        if orminit:
            log.error('config{} is deprecated')
            log.info('calling ORM initializer %s from: %s' % (str(orminit), plugin.pluginId()))
            orminit(orm, plugin.namespace(), propDict)
        """
    log.info('COMPLETED ORM INITIALIZATION STAGE')

def upd_globals():
    adminTagsLine = meta.globj.OPT.adminOnlyTags
    meta.globj.forbiddenTags = Tag.csStringToExTagIdList(adminTagsLine)
    meta.globj.additionalLinks = [link.split('|') for link in meta.globj.OPT.additionalLinks]
    meta.globj.sectionNames = meta.globj.OPT.sectionNames
    meta.globj.disabledTags = meta.globj.OPT.disabledTags
    meta.globj.OPT.memcachedServers = [str(server) for server in meta.globj.OPT.memcachedServers]
    meta.globj.OPT.cachePrefix = str(meta.globj.OPT.cachePrefix)
    if meta.globj.mc:
        meta.globj.mc.disconnect_all()
        meta.globj.mc.set_servers(meta.globj.OPT.memcachedServers)
    else:
        meta.globj.mc = MCache(meta.globj.OPT.memcachedServers, debug = 0,
                                        key = meta.globj.OPT.cachePrefix,
                                        meta = meta)
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
