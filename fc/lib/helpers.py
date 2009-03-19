"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config
import datetime
import os
import miscUtils as utils
from routes.util import url_for

import logging
log = logging.getLogger(__name__)

def expandName(name):
    #log.debug("expanding: %s" % name)
    if name:
        parts = name.split('.')
        if parts and utils.isNumber(parts[-2].replace('s', '')): #TODO: is the second condition really needed?
            ext = parts[-1].lower()
            prefix = name[0:4]
            #log.debug('%s/%s/%s' % (ext, prefix, name))
            return '%s/%s/%s' % (ext, prefix, name)
    #log.debug('passed: %s' % name)
    return name

def modLink(filePath, secid, hidePrefixes = False):
    #log.debug("mod: %s" % (filePath))
    if filePath and config['pylons.app_globals'].OPT.secureLinks:
        baseName = os.path.basename(filePath)
        prefix = os.path.dirname(filePath)
        #log.debug(baseName)
        #log.debug(prefix)
        if utils.isNumber(baseName.split('.')[-2].replace('s', '')):
            p1 = baseName[0:4]
            p2 = baseName[4:8]
            p3 = baseName[8:len(baseName)]
            retval = '%s%s%s%s' % (p1, str(secid), p2, p3)
            if prefix and not hidePrefixes:
                retval = prefix + '/' + retval
            return retval
    #log.debug('not modified: %s' % filePath)

    if hidePrefixes:
         baseName = os.path.basename(filePath)
         if baseName:
            return baseName

    return filePath

def modMessage(message, user, f):
    if f:
        gv = config['pylons.app_globals']
        uval = gv.uniqueVals[user.uidNumber % (len(gv.uniqueVals) - 1)]
        return message.replace('[SECURITY:UNIQUE_VAL]', uval)
    else:
        return message

def modifyTime(sourceTime, user, f):
    if f:
        x = user.uidNumber
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

def staticFile(fileName):
    gv = config['pylons.app_globals']
    spw = gv.OPT.staticPathWeb
    spl = gv.OPT.staticPath
    ext = fileName.split('.')[-1]
    relFileName = "%s/%s" % (ext, fileName)
    localFileName = os.path.join(spl, relFileName)
    version = gv.caches.get(localFileName, False)
    if not version:
        version = os.path.getmtime(localFileName)
        gv.caches[localFileName] = version
    return u"%s%s?version=%s" % (spw, relFileName, str(version))


