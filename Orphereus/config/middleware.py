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

"""Pylons middleware initialization"""
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool

from pylons import config
from pylons.error import error_template
"""
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, \
    StaticJavascripts

"""

from beaker.middleware import CacheMiddleware, SessionMiddleware
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from routes.middleware import RoutesMiddleware
from paste.deploy.config import PrefixMiddleware
from pylons.wsgiapp import PylonsApp

from Orphereus.config.environment import load_environment
from paste.gzipper import middleware as gzipper 

def make_app(global_conf, full_stack = True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by
        another WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """

    # Configure the Pylons environment
    load_environment(global_conf, app_conf, False)

    # The Pylons WSGI app
    app = PylonsApp()
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)
    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and 500 when debug is disabled)
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])

    # Establish the Registry for this application
    app = RegistryManager(app)

    # Static files
    if config['pylons.app_globals'].OPT.compressionEnabled:
        app = gzipper(app, config['pylons.app_globals'].OPT.compressionLevel)
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, app])
    prefix = config['pylons.app_globals'].OPT.urlPrefix
    if prefix and prefix.startswith('/') and len(prefix) > 1:
        app = PrefixMiddleware(app, global_conf, prefix = prefix)
    return app
