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

"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

import logging
log = logging.getLogger("ROUTING (%s)" % __name__)

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory = config['pylons.paths']['controllers'],
                 always_scan = config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller = 'error')

    # CUSTOM ROUTES HERE
    # debug route
    gvars = config['pylons.app_globals']
    framedMain = gvars.OPT.framedMain

    log.info('Initialzing routes, registered plugins: %d' % (len(gvars.plugins)),)
    # Calling routing initializers from plugins
    for plugin in gvars.plugins:
        plugin.initRoutes(map)

        #rinit = plugin.routingInit()
        #if rinit:
        #    log.error('config{} is deprecated')
        #    log.info('calling routing initializer %s from: %s' % (str(rinit), plugin.pluginId()))
        #    rinit(map)
    log.info('COMPLETED ROUTING INITIALIZATION STAGE')

    ## VIEW
    map.connect('makeFwdTo', '/makeFwdTo', controller = 'Orphie_View', action = 'makeFwdTo')
    map.connect('frameMenu', '/frameMenu', controller = 'Orphie_View', action = 'frameMenu')
    map.connect('viewLogBase', '/viewLog', controller = 'Orphie_View', action = 'viewLog', page = 0, requirements = dict(page = '\d+'))
    map.connect('viewLog', '/viewLog/page/:page', controller = 'Orphie_View', action = 'viewLog', requirements = dict(page = '\d+'))
    map.connect('viewAnimation',
                '/viewAnimation/:source/:animid',
                controller = 'Orphie_View',
                action = 'viewAnimation',
                animid = '0',
                requirements = dict(source = '\d+', animid = '\d+'))
    ## VIEW: END


    # Special routes
    map.connect('authorize', '/authorize', controller = 'Orphie_Public', action = 'authorize', url = '')
    map.connect('authorizeToUrl', '/*url/authorize', controller = 'Orphie_Public', action = 'authorize', url = '')
    map.connect('logout', '/logout', controller = 'Orphie_Public', action = 'logout', url = '')
    map.connect('captcha', '/captcha/:cid', controller = 'Orphie_Public', action = 'captchaPic', cid = 0)
    map.connect('register', '/register/:invite', controller = 'Orphie_Public', action = 'register')
    map.connect('banned', '/youAreBanned', controller = 'Orphie_Public', action = 'banned')
    map.connect('ipBanned', '/ipBanned', controller = 'Orphie_Public', action = 'ipBanned')

    map.connect('static', '/static/:page', controller = 'Orphie_Main', action = 'showStatic', page = 'rules')
    map.connect('searchBase', '/search/:text', controller = 'Orphie_Main', action = 'search', text = '', page = 0, requirements = dict(page = '\d+'))
    map.connect('search', '/search/:text/page/:page', controller = 'Orphie_Main', action = 'search', requirements = dict(page = '\d+'))

    # Users subsystem
    map.connect('userProfile', '/userProfile', controller = 'Orphie_Main', action = 'showProfile')

    # Oekaki
    map.connect('oekakiDraw',
                '/oekakiDraw/:url/:sourceId/:selfy/:anim/:tool',
                controller = 'Orphie_Main',
                action = 'oekakiDraw',
                selfy = None,
                anim = None,
                tool = None,
                sourceId = '0',
                requirements = dict(sourceId = '\d+'))
    map.connect('oekakiSave',
                '/oekakiSave/:url/:tempid',
                controller = 'Orphie_Public',
                action = 'oekakiSave',
                url = '',
                requirements = dict(tempid = '\d+'))

    # Threads
    map.connect('postReply', '/:post', controller = 'Orphie_Main', action = 'PostReply', conditions = dict(method = ['POST']), requirements = dict(post = '\d+'))
    map.connect('delete', '/:board/delete', controller = 'Orphie_Main', action = 'DeletePost', conditions = dict(method = ['POST']))
    map.connect('postThread', '/:board', controller = 'Orphie_Main', action = 'PostThread', conditions = dict(method = ['POST']))

    ## VIEW
    map.connect('thread', '/:post/:tempid', controller = 'Orphie_View', action = 'GetThread', tempid = 0, requirements = dict(post = '\d+', tempid = '\d+'))
    # Generic filter
    map.connect('boardBase', '/:board/:tempid', controller = 'Orphie_View', action = 'GetBoard', board = not framedMain and defaultBoard or None, tempid = 0, page = 0, requirements = dict(tempid = '\d+'))
    map.connect('board', '/:board/page/:page', controller = 'Orphie_View', action = 'GetBoard', tempid = 0, requirements = dict(page = '\d+'))
    ## VIEW: END

    # traps for bots
    map.connect('botTrap1', '/ajax/stat/:confirm', controller = 'Orphie_Bot_Trap', action = 'selfBan', confirm = '')
    map.connect('botTrap2', '/holySynod/stat/:confirm', controller = 'Orphie_Bot_Trap', action = 'selfBan', confirm = '')

    map.connect('*url', controller = 'Orphie_Public', action = 'UnknownAction')
    return map
