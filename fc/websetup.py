"""Setup the FC application"""
import logging

from paste.deploy import appconfig
from pylons import config
from fc.model import *
import hashlib
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper

from fc.config.environment import load_environment
import fc.lib.app_globals as app_globals

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup fc here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf, True)
    from fc.model import meta
    log.info("Creating tables")
    meta.metadata.create_all(bind=meta.engine)
    log.info("Successfully setup")

    try:
        uc = meta.Session.query(User).count()
    except:
        uc = 0
    log.debug('users: %d' % uc)

    if uc == 0:
        log.info("Adding user with password 'first'")
        log.debug(config['core.hashSecret'])
        uid = hashlib.sha512('first' + hashlib.sha512(config['core.hashSecret']).hexdigest()).hexdigest()
        user = User.create(uid)
        log.debug(uid)
        uidNumber = user.uidNumber
        log.debug(uidNumber)
        user.options.isAdmin = True
        user.options.canChangeRights = True
        meta.Session.commit()
    try:
        ec = meta.Session.query(Extension).count()
    except:
        ec = 0
    log.debug('extenions: %d' % ec)

    if ec == 0:
        log.info("Adding extensions")

        Extension.create('jpeg', True, True, 'image', '', 0, 0)
        Extension.create('jpg', True, True, 'image', '', 0, 0)
        Extension.create('gif', True, True, 'image', '', 0, 0)
        Extension.create('bmp', True, True, 'image-jpg', '', 0, 0)
        Extension.create('png', True, True, 'image', '', 0, 0)
        Extension.create('zip', True, True, 'archive', '../generic/archive.png', 0, 0)
        Extension.create('7z', True, True, 'archive', '../generic/archive.png', 0, 0)
        Extension.create('mp3', True, True, 'image', '../generic/sound.png', 0, 0)
        Extension.create('ogg', True, True, 'image', '../generic/sound.png', 0, 0)


    try:
        tc = meta.Session.query(Tag).count()
    except:
        tc = 0
    log.debug('tags: %d' % tc)

    if tc == 0:
        log.info("Adding tag /b/")

        tag = Tag('b')
        tag.options = TagOptions()
        tag.options.comment = 'Random'
        tag.options.sectionId = 2
        tag.options.persistent = True
        tag.options.specialRules = u''
        tag.options.imagelessThread = False
        tag.options.imagelessPost = True
        tag.options.enableSpoilers = False
        tag.options.canDeleteOwnThreads = True
        tag.options.images = True
        tag.options.maxFileSize = 3000000
        tag.options.minPicSize = 50
        tag.options.thumbSize = 180
        meta.Session.add(tag)

        meta.Session.commit()

    log.info("Completed")
