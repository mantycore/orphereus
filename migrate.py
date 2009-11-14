import logging

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
formatter = logging.Formatter("[Migration] %(asctime)s %(levelname)s: %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)
log.info("Migration")

userOptMembers = ["optid",
"uidNumber",
"threadsPerPage",
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

    log.info("Initializing old model")
    engine = create_engine(sourceModelUrl)
    OM.init_model(engine)

    log.info("Migrating users...")
    oldUsers = OM.User.query.all()
    log.info("Users count: %d" % len(oldUsers))

    for user in oldUsers:
        log.info("Creating [%d] %s" % (user.uidNumber, user.uid))
        newUser = User(user.uid, user.uidNumber)
        if user.options:
            log.info("Copying options...")
            newUser.options = UserOptions()
            copyMembers(userOptMembers, user.options, newUser.options)
            meta.Session.add(newUser.options)
        meta.Session.add(newUser)
        meta.Session.commit()
        log.info("Creating filters...")
        for filter in user.filters:
            newUser.addFilter(filter.filter)
        log.info("Ok")
migrate("development.ini", "mysql://root:@127.0.0.1/orphieold?use_unicode=0&charset=utf8")
