import sqlalchemy as sa
import sqlalchemy.databases as databases
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
#from TagOptions import *
from User import *
from UserFilters import *
from UserOptions import *
from Ban import *

import logging
_log = logging.getLogger("ORM")
_log.setLevel(logging.DEBUG)

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

def adjust_dialect(engine, meta):
    _log.info("Trying to adjust engine to current dialect...")
    target = meta

    def logAndChange(var, newType):
        _log.info("Using %s instead of %s" % (str(newType), str(var)))
        return newType

    props = {'disableTextIndexing' : None,
             'tagLengthHardLimit' : 24,
             'userFilterLengthLimit' : 512}

    dialectName = engine.dialect.name
    diam = __import__("sqlalchemy.dialects.%s.base" % dialectName, globals(), locals(), ['base'], -1)

    if (isinstance(engine.dialect, databases.mysql.MySQLDialect)):
        _log.info("Currently using MySQL dialect, adjusting types...")
        target.FloatType = logAndChange(meta.FloatType, diam.MSDouble)
        target.BlobType = logAndChange(meta.BlobType, diam.MSLongBlob)
        target.UIntType = logAndChange(meta.UIntType, diam.MSInteger(unsigned = True))
        props['disableTextIndexing'] = True
        props['disableInstantIdSetting'] = True
    elif (isinstance(engine.dialect, databases.postgres.PGDialect)):
        _log.info("Currently using PostgreSQL dialect, adjusting types...")
        target.FloatType = logAndChange(meta.FloatType, diam.DOUBLE_PRECISION)
        target.BlobType = logAndChange(meta.BlobType, diam.BYTEA)
        target.UIntType = logAndChange(meta.UIntType, diam.BIGINT)
    elif (isinstance(engine.dialect, databases.sqlite.SQLiteDialect)):
        _log.info("Currently using SQLite dialect, adjusting doesn't required ^_^")
    elif (isinstance(engine.dialect, databases.mssql.MSSQLDialect)):
        _log.info("O_o ZOMG TEH ENTERPRISE! o_O")
        _log.info("Currently using Microsoft SQL dialect, adjusting types...")
        target.UIntType = logAndChange(meta.UIntType, diam.BIGINT)
        props['disableTextIndexing'] = True
    elif (isinstance(engine.dialect, databases.oracle.OracleDialect)):
        _log.info("Currently using Oracle dialect, ZOMG TEH ENTERPRISE!")
        props['disableTextIndexing'] = True
        raise Exception("Too enterprise for me")
    else:
        _log.warning("\n\nUnknown SQL Dialect %s!\n\n" % dialectName)
    _log.info("Adjusting completed")
    meta.dialectProps = props
    return props

def init_model(engine, meta):
    dialectProps = adjust_dialect(engine, meta)

    t_logins = t_loginTracker_init(dialectProps)
    t_captchas = t_captcha_init(dialectProps)
    t_oekaki = t_oekaki_init(dialectProps)
    t_invites = t_invite_init(dialectProps)
    t_settings = t_settings_init(dialectProps)
    t_userOptions = t_useroptions_init(dialectProps)
    t_userFilters = t_userfilters_init(dialectProps)
    t_users = t_user_init(dialectProps)
    t_extension = t_extension_init(dialectProps)
    t_piclist, t_filesToPostsMap = t_picture_init(dialectProps)
    t_tags, t_tagsToPostsMap = t_tags_init(dialectProps)
    t_log = t_log_init(dialectProps)
    t_posts = t_posts_init(dialectProps)
    t_bans = t_bans_init(dialectProps)

    sm = orm.sessionmaker(autoflush = False, autocommit = False, bind = engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    meta.mapper = session_mapper(meta.Session)
    #_log.debug(dir(engine))
    #_log.debug(dir(engine.logger))
    """
    engine.echo = True
    engine.logger.setLevel('info')

    import logging

    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    #logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.orm.logging').setLevel(logging.INFO)
    """

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
    #TagOptionsProps = {}
    TagProps = {}
    #        'options' : orm.relation(TagOptions, uselist = False, backref = 'tag', cascade = "all, delete, delete-orphan")
    #    }

    PictureAssociationProps = {'attachedFile' : orm.relation(Picture)}

    PostProps = {
        'tags' : orm.relation(Tag, secondary = t_tagsToPostsMap),
        #'file': orm.relation(Picture),
        #'attachments'  : orm.relation(Picture, secondary = t_filesToPostsMap),
        'attachments'  : orm.relation(PictureAssociation, cascade = "all, delete, delete-orphan"),
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
                #"TagOptions" : TagOptionsProps,
                "Tag" : TagProps,
                "Post" : PostProps,
                "LogEntry" : LogEntryProps,
                "PictureAssociation" : PictureAssociationProps,
                }

    gvars = config['pylons.app_globals']
    _log.info('Extending ORM properties, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        plugin.extendORMProperties(orm, engine, dialectProps, propDict)
    _log.info('COMPLETED ORM EXTENDING STAGE')

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

    #meta.mapper(TagOptions, t_tagOptions, properties = TagOptionsProps)
    meta.mapper(Tag, t_tags, properties = TagProps)
    meta.mapper(PictureAssociation, t_filesToPostsMap, properties = PictureAssociationProps)
    meta.mapper(Post, t_posts, properties = PostProps)

    meta.mapper(LogEntry, t_log, properties = LogEntryProps)

    gvars = config['pylons.app_globals']
    _log.info('Initialzing ORM, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        plugin.initORM(orm, engine, dialectProps, propDict)

        """
        orminit = plugin.ormInit()
        if orminit:
            _log.error('config{} is deprecated')
            _log.info('calling ORM initializer %s from: %s' % (str(orminit), plugin.pluginId()))
            orminit(orm, plugin.namespace(), propDict)
        """
    _log.info('COMPLETED ORM INITIALIZATION STAGE')

def upd_globals():
    #adminTagsLine = meta.globj.OPT.adminOnlyTags
    #meta.globj.forbiddenTags = Tag.csStringToExTagIdList(adminTagsLine)
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
    _log.info('UPDATING GLOBALS COMPLETED')

def init_globals(globalObject, deployMode):
    meta.globj = globalObject

    if not deployMode:
        _log.info('LOADING CONFIGURATION DATA')
        meta.globj.OPT.initValues(Setting)
        _log.info('LOAD COMPLETED')

        upd_globals()

    """
    gv = config['pylons.g']
    gv.tagCache = {}
    tags = meta.Session.query(Tag).all()
    for tag in tags:
        gv.tagCache[tag.tag] = tag.id

    _log.debug(gv.tagCache)
    """
