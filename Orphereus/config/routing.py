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
log = logging.getLogger("ROUTING")

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

    gvars = config['pylons.app_globals']
    log.info('Initialzing routes, registered plugins: %d' % (len(gvars.plugins)),)
    for plugin in gvars.plugins:
        plugin.initRoutes(map)
    for plugin in gvars.plugins:
        plugin.postInitRoutes(map)
    log.info('COMPLETED ROUTING INITIALIZATION STAGE')

    map.connect('*url', controller = 'Orphie_Public', action = 'UnknownAction')
    return map
