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

import socket, struct

import logging
log = logging.getLogger(__name__)

def postUrl(threadId, postId):
    return '%s#i%s' % (url_for('thread', post = threadId and threadId or postId), postId)

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
    #log.debug("gen link %s for id %s" %(filePath,secid))
    if hidePrefixes:
         baseName = os.path.basename(filePath)
         if baseName:
            return baseName

    return filePath

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

def dottedToInt(ipStr):
    return struct.unpack('!L',socket.inet_aton(ipStr))[0]

def intToDotted(n):
    return socket.inet_ntoa(struct.pack('!L',n))




