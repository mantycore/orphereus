import sqlalchemy as sa
from sqlalchemy import orm
from Orphereus.model import meta
from Orphereus.lib.constantValues import *
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

    #create mappings
    meta.Session.mapper(LoginTracker, t_logins)
    meta.Session.mapper(Captcha, t_captchas)
    meta.Session.mapper(Oekaki, t_oekaki)
    meta.Session.mapper(Invite, t_invites)
    meta.Session.mapper(Setting, t_settings)
    meta.Session.mapper(Ban, t_bans)

    meta.Session.mapper(UserOptions, t_userOptions)
    meta.Session.mapper(UserFilters, t_userFilters)
    meta.Session.mapper(User, t_users, properties = {
            'options' : orm.relation(UserOptions, uselist = False, backref = 'user', cascade = "all, delete, delete-orphan"),
            'filters' : orm.relation(UserFilters, backref = 'user', cascade = "all, delete, delete-orphan")
        })

    meta.Session.mapper(Extension, t_extension)
    meta.Session.mapper(Picture, t_piclist, properties = {
        'extension' : orm.relation(Extension)
        })

    meta.Session.mapper(TagOptions, t_tagOptions)
    meta.Session.mapper(Tag, t_tags, properties = {
            'options' : orm.relation(TagOptions, uselist = False, backref = 'tag', cascade = "all, delete, delete-orphan")
        })
    meta.Session.mapper(Post, t_posts, properties = {
        'tags' : orm.relation(Tag, secondary = t_tagsToPostsMap),
        'file': orm.relation(Picture),
        'parentPost' : orm.relation(Post, remote_side = [t_posts.c.id]),
        })

    meta.Session.mapper(LogEntry, t_log, properties = {
        'user' : orm.relation(User)
        })

    gvars = config['pylons.app_globals']
    log.info('Initialzing ORM, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        orminit = plugin.ormInit()
        if orminit:
            log.info('calling ORM initializer %s from: %s' % (str(orminit), plugin.pluginId()))
            orminit(orm, plugin.namespace())
    log.info('COMPLETED ORM INITIALIZATION STAGE')

def init_globals(globalObject, setupMode):
    meta.globj = globalObject
    settingsMap = {}

    if not setupMode:
        settings = False
        settings = Setting.getAll()
        if settings:
            for s in settings:
                #log.debug('Option: %s==%s ' % (s.name, s.value))
                if s.name in settingsDef:
                    settingsMap[s.name] = s

        for s in settingsDef:
            if not s in settingsMap:
                option = Setting.create(s, settingsDef[s])
                settingsMap[s] = option
    else:
        from Orphereus.lib.miscUtils import empty
        for s in settingsDef:
            option = empty()
            option.name = s
            option.value = settingsDef[s]
            settingsMap[s] = option

    meta.globj.settingsMap = settingsMap
    if not setupMode:
        adminTagsLine = meta.globj.settingsMap['adminOnlyTags'].value
        meta.globj.forbiddenTags = Tag.csStringToExTagIdList(adminTagsLine)

        meta.globj.additionalLinks = []
        linksstr = meta.globj.settingsMap['additionalLinks'].value
        links = linksstr.split('|')
        if links:
            for link in links:
                meta.globj.additionalLinks.append(link.split(','))

        meta.globj.sectionNames = meta.globj.settingsMap['sectionNames'].value.split('|')

        disabledTagsLine = meta.globj.settingsMap['disabledTags'].value
        meta.globj.disabledTags = disabledTagsLine.lower().split('|')

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

