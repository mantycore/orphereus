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
    
    log.info("Adding user with password 'first'")        
    if meta.Session.query(User).count() == 0:
        user = User()
        user.uid = hashlib.sha512('first' + hashlib.sha512(config['core.hashSecret']).hexdigest()).hexdigest()
        meta.Session.save(user)
    log.info("Completed")