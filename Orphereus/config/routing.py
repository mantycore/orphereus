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

    map.explicit = True
    map.minimization = True

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller = 'error')
    map.connect('/error/{action}/{id}', controller = 'error')

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
    map.connect('thread', '/{post}/{tempid}',
                controller = 'Orphie_View',
                action = 'GetThread',
                tempid = 0,
                requirements = dict(post = r'\d+', tempid = r'\d+'))
    # Generic filter
    map.connect('boardBase', '/{board}/{tempid}',
                controller = 'Orphie_View',
                action = 'GetBoard',
                board = not framedMain and defaultBoard or None,
                tempid = 0, page = 0,
                requirements = dict(tempid = r'\d+'))
    map.connect('board', '/{board}/page/{page}',
                controller = 'Orphie_View',
                action = 'GetBoard',
                tempid = 0,
                requirements = dict(page = r'\d+'))
    ## VIEW: END

    map.connect('*url', controller = 'Orphie_Public', action = 'UnknownAction')
    return map
