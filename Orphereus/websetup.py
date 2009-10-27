################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

"""Setup the FC application"""
import logging

from paste.deploy import appconfig
from pylons import config
from Orphereus.model import *
import hashlib
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper

from Orphereus.config.environment import load_environment
import Orphereus.lib.app_globals as app_globals

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup Orphereus here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf, True)
    from Orphereus.model import meta
    log.info("Creating tables")
    meta.metadata.create_all(bind = meta.engine)
    log.info("Successfully setup")
    init_globals(meta.globj, False)

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
        Extension.create('swf', True, True, 'flash', 'generic/flash.png', 128, 128)
        Extension.create('zip', True, True, 'archive', 'generic/archive.png', 128, 128)
        Extension.create('rar', True, True, 'archive', 'generic/archive.png', 128, 128)
        Extension.create('tar', True, True, 'archive', 'generic/archive.png', 128, 128)
        Extension.create('7z', True, True, 'archive', 'generic/archive.png', 128, 128)
        Extension.create('mp3', True, True, 'music', 'generic/sound.png', 128, 128)
        Extension.create('ogg', True, True, 'music', 'generic/sound.png', 128, 128)
        Extension.create('txt', True, True, 'text', 'generic/text.png', 128, 128)
        Extension.create('log', True, True, 'text', 'generic/text.png', 128, 128)

    try:
        tc = meta.Session.query(Tag).count()
    except:
        tc = 0
    log.debug('tags: %d' % tc)

    if tc == 0:
        log.info("Adding tag /b/")

        tag = Tag(u'b')
        tag.options = TagOptions()
        tag.options.comment = u'Random'
        tag.options.sectionId = 1
        tag.options.persistent = True
        tag.options.specialRules = u"It's /b/, there is no rules"
        meta.Session.add(tag)

        meta.Session.commit()

    log.info("Completed")

    gvars = config['pylons.app_globals']
    log.debug('Calling deploy routines, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        plugin.deployCallback()

        #dh = plugin.deployHook()
        #if dh:
        #    log.debug('calling deploy routine %s from: %s' % (str(dh), plugin.pluginId()))
        #    dh(plugin.namespace())
    log.debug('DEPLOYMENT COMPLETED')
