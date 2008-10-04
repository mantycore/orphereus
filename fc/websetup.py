"""Setup the FC application"""
import logging

from paste.deploy import appconfig
from pylons import config
from fc.model import * 
import hashlib

from fc.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup fc here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    from fc.model import meta
    log.info("Creating tables")
    meta.metadata.create_all(bind=meta.engine)
    log.info("Successfully setup")
            
    uc = meta.Session.query(User).count()
    log.debug('users: %d' % uc) 
    if True or uc == 0:
        log.info("Adding user with password 'first'")
        log.debug(config['core.hashSecret'])
        user = User()
        user.uid = hashlib.sha512('first' + hashlib.sha512(config['core.hashSecret']).hexdigest()).hexdigest()
        log.debug(user.uid)        
        meta.Session.save(user)
        meta.Session.commit()
        log.info("Completed")