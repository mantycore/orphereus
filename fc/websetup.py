"""Setup the FC application"""
import logging

from paste.deploy import appconfig
from pylons import config
from fc.model import * 
import hashlib
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from lib.fuser import FUser

from fc.config.environment import load_environment
import fc.lib.app_globals as app_globals

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup fc here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
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
        user = User()
        user.uid = hashlib.sha512('first' + hashlib.sha512(config['core.hashSecret']).hexdigest()).hexdigest()
        log.debug(user.uid)
        meta.Session.add(user)
        meta.Session.commit()
        uidNumber = user.uidNumber
        log.debug(uidNumber)
        fuser = FUser(uidNumber) # create options
        user = meta.Session.query(User).options(eagerload('options')).filter(User.uidNumber==uidNumber).first()
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
        
        ext = Extension()
        ext.path = ''
        ext.thwidth = 0
        ext.thheight = 0
        ext.ext = 'jpeg'
        ext.type = 'image'
        meta.Session.add(ext)

        
        ext = Extension()
        ext.path = ''
        ext.thwidth = 0
        ext.thheight = 0
        ext.ext = 'jpg'
        ext.type = 'image'
        meta.Session.add(ext)
        
        
        ext = Extension()
        ext.path = ''
        ext.thwidth = 0
        ext.thheight = 0
        ext.ext = 'gif'
        ext.type = 'image'
        meta.Session.add(ext)
        
        
        ext = Extension()
        ext.path = ''
        ext.thwidth = 0
        ext.thheight = 0
        ext.ext = 'bmp'
        ext.type = 'image'
        meta.Session.add(ext)
        
        
        ext = Extension()
        ext.path = ''
        ext.thwidth = 0
        ext.thheight = 0
        ext.ext = 'png'
        ext.type = 'image'
        meta.Session.add(ext)
        
        
        ext = Extension()
        ext.path = '../generic/archive.png'
        ext.thwidth = 80
        ext.thheight = 80
        ext.ext = 'zip'
        ext.type = 'archive'
        meta.Session.add(ext)
        
        
        ext = Extension()
        ext.path = '../generic/archive.png'
        ext.thwidth = 80
        ext.thheight = 80
        ext.ext = '7z'
        ext.type = 'archive'
        meta.Session.add(ext)
        
        
        ext = Extension()
        ext.path = '../generic/sound.png'
        ext.thwidth = 80
        ext.thheight = 80
        ext.ext = 'mp3'
        ext.type = 'audio'
        meta.Session.add(ext)
        
        ext = Extension()
        ext.path = '../generic/sound.png'
        ext.thwidth = 80
        ext.thheight = 80
        ext.ext = 'ogg'
        ext.type = 'audio'
        meta.Session.add(ext)
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