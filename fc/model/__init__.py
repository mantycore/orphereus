import sqlalchemy as sa
from sqlalchemy import orm
from fc.model import meta
from fc.lib.constantValues import *

import logging
log = logging.getLogger(__name__)

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

def init_model(engine):
    sm = orm.sessionmaker(autoflush=False, autocommit=False, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

    #create mappings
    meta.Session.mapper(LoginTracker, t_logins)
    meta.Session.mapper(Captcha, t_captchas)
    meta.Session.mapper(Oekaki, t_oekaki)
    meta.Session.mapper(Invite, t_invites)
    meta.Session.mapper(Setting, t_settings)

    meta.Session.mapper(UserOptions, t_userOptions)
    meta.Session.mapper(UserFilters, t_userFilters)
    meta.Session.mapper(User, t_users, properties = {
            'options' : orm.relation(UserOptions, uselist=False, backref='t_users', cascade="all, delete, delete-orphan"),
            'filters' : orm.relation(UserFilters, backref='t_users', cascade="all, delete, delete-orphan")
        })

    meta.Session.mapper(Extension, t_extlist)
    meta.Session.mapper(Picture, t_piclist, properties = {
        'extension' : orm.relation(Extension)
        })

    meta.Session.mapper(TagOptions, t_tagOptions)
    meta.Session.mapper(Tag, t_tags, properties = {
            'options' : orm.relation(TagOptions, uselist=False, backref='t_tags', cascade="all, delete, delete-orphan")
        })
    meta.Session.mapper(Post, t_posts, properties = {
        'tags' : orm.relation(Tag, secondary = t_tagsToPostsMap),
        'file': orm.relation(Picture),
        'parentPost' : orm.relation(Post, remote_side=[t_posts.c.id]),
        })

    meta.Session.mapper(LogEntry, t_log, properties = {
        'user' : orm.relation(User)
        })

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
        from fc.lib.miscUtils import empty
        for s in settingsDef:
            option = empty()
            option.name = s
            option.value = settingsDef[s]
            settingsMap[s] = option

    meta.globj.settingsMap = settingsMap
    if not setupMode:
        adminTagsLine = meta.globj.settingsMap['adminOnlyTags'].value
        meta.globj.forbiddenTags = Tag.csStringToExTagIdList(adminTagsLine)

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

