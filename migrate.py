import logging
import datetime

from paste.deploy import appconfig
from pylons import config
from Orphereus.model import *
import Orphereus.oldmodel as OM
import hashlib
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper

from Orphereus.config.environment import load_environment
import Orphereus.lib.app_globals as app_globals

from sqlalchemy import create_engine

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s: %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)
log.info("Migration")

userOptMembers = ["threadsPerPage",
"repliesPerThread",
"style",
"template",
"homeExclude",
"hideThreads",
"bantime",
"banreason",
"banDate",
"useFrame",
"hideLongComments",
"useAjax",
"expandImages",
"maxExpandWidth",
"maxExpandHeight",
"mixOldThreads",
"useTitleCollapse",
"hlOwnPosts",
"invertSortingMode",
"defaultGoto",
"oekUseSelfy",
"oekUseAnim",
"oekUsePro",
"isAdmin",
"canDeleteAllPosts",
"canMakeInvite",
"canChangeRights",
"canChangeSettings",
"canManageBoards",
"canManageUsers",
"canManageExtensions",
"canManageMappings",
"canRunMaintenance",
"lang",
"cLang", ]

tagOptMembers = ["comment",
"sectionId",
"persistent",
"service",
"imagelessThread",
"imagelessPost",
"images",
"maxFileSize",
"minPicSize",
"thumbSize",
"enableSpoilers",
"canDeleteOwnThreads",
"specialRules",
"selfModeration",
"showInOverview",
"bumplimit", ]

banMembers = ["ip",
"mask",
"type",
"reason",
"date",
"period",
"enabled", ]

def copyMembers(membersList, source, target):
    for member in membersList:
        setattr(target, member, getattr(source, member))

def migrate(targetConfig, sourceModelUrl):
    """Place any commands to setup Orphereus here"""
    conf = appconfig('config:' + os.path.abspath(targetConfig))
    load_environment(conf.global_conf, conf.local_conf, True)

    log.info("Dropping tables")
    meta.metadata.drop_all(bind = meta.engine)
    log.info("Successfully dropped")
    log.info("Creating tables")
    meta.metadata.create_all(bind = meta.engine)
    log.info("Successfully setup")

    init_globals(meta.globj, False)

    log.info("=================================================================")
    log.info("Initializing old model")
    engine = create_engine(sourceModelUrl)
    OM.init_model(engine)
    log.info("-----------------------------------------------------------------")

    log.info("=================================================================")
    log.info("Migrating users...")
    log.info("-----------------------------------------------------------------")
    oldUsers = OM.User.query.all()
    log.info("Users count: %d" % len(oldUsers))

    for user in oldUsers:
        log.info("Creating [%d] %s" % (user.uidNumber, user.uid))
        newUser = User(user.uid, None)
        meta.Session.add(newUser)
        meta.Session.commit()
        newUser.uidNumber = user.uidNumber
        if user.options:
            log.info("Copying options for %d..." % newUser.uidNumber)
            newUser.options = UserOptions()
            copyMembers(userOptMembers, user.options, newUser.options)
            meta.Session.add(newUser.options)
        else:
            log.error("No options for user %d" % user.uidNumber)
        meta.Session.commit()
        log.info("Creating filters for %d..." % newUser.uidNumber)
        for filter in user.filters:
            newUser.addFilter(filter.filter)

    log.info("=================================================================")
    log.info("Migrating tags...")
    log.info("-----------------------------------------------------------------")
    oldTags = OM.Tag.query.all()
    log.info("Tags count: %d" % len(oldTags))

    for tag in oldTags:
        log.info("Creating /%s/" % (tag.tag,))
        newTag = Tag(tag.tag)
        if tag.options:
            log.info("Copying options for /%s/..." % tag.tag)
            copyMembers(tagOptMembers, tag.options, newTag.options)
        else:
            log.error("No options for tag /%s/" % tag.tag)
        meta.Session.add(newTag)
        meta.Session.commit()

    log.info("=================================================================")
    log.info("Migrating settings...")
    log.info("-----------------------------------------------------------------")
    oldSettings = OM.Setting.query.all()
    log.info("Settings count: %d" % len(oldSettings))

    for setting in oldSettings:
        log.info("Creating %s=%s" % (setting.name, setting.value))
        Setting.create(setting.name, setting.value)

    log.info("=================================================================")
    log.info("Migrating bans...")
    log.info("-----------------------------------------------------------------")
    oldBans = OM.Ban.query.all()
    log.info("Bans count: %d" % len(oldBans))

    for ban in oldBans:
        log.info("Creating ban for %d" % (ban.ip,))
        newBan = Ban(0, 0, 0, '', datetime.datetime.now(), 0, False)
        copyMembers(banMembers, ban, newBan)
        meta.Session.add(newBan)
        meta.Session.commit()

migrate("development.ini", "mysql://root:@127.0.0.1/orphieold?use_unicode=0&charset=utf8")
