"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config
import datetime
import os

import logging
log = logging.getLogger(__name__)

def modLink(string, secid, f):
    if f:
        p1 = string[0:4]
        p2 = string[4:8]
        p3 = string[8:len(string)]
        return p1 + str(secid) + p2 + p3
    else:
        return string

def modMessage(message, user, f):  
    if f:
        gv = config['pylons.app_globals']
        uval = gv.uniqueVals[user.uidNumber() % (len(gv.uniqueVals) - 1)]
        return message.replace('[SECURITY:UNIQUE_VAL]', uval)
    else:
        return message
    
def modifyTime(sourceTime, user, f):
    if f:
        x = user.uidNumber()
        return sourceTime - datetime.timedelta(seconds=((-1)**x)*int(x/2))
    else:
        return sourceTime
    
def modTime(post, user, f):
    return modifyTime(post.date, user, f)

def templateExists(relName):
    #log.debug(config['pylons.g'].OPT.templPath)
    #log.debug(relName)
    #log.debug(os.path.join(config['pylons.g'].OPT.templPath, relName))
    #log.debug(os.path.exists(os.path.join(config['pylons.g'].OPT.templPath, relName)))
    return os.path.exists(os.path.join(config['pylons.app_globals'].OPT.templPath, relName))

