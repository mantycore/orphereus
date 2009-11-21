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

"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons.error import handle_mako_error
from pylons import config

import Orphereus.lib.app_globals as app_globals
import Orphereus.lib.helpers
from Orphereus.config.routing import make_map
from Orphereus.lib.miscUtils import adminAlert

#from Orphereus.model import meta
from sqlalchemy import engine_from_config
from Orphereus.model import init_model, init_globals
from Orphereus.model import meta

import logging
log = logging.getLogger(__name__)

def load_environment(global_conf, app_conf, deployMode):
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root = root,
                 controllers = os.path.join(root, 'controllers'),
                 static_files = os.path.join(root, 'public'),
                 templates = [os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package = 'Orphereus',
                    template_engine = 'mako', paths = paths)

    #config['pylons.strict_c'] = False
    #config['pylons.c_attach_args'] = True

    #config['pylons.g'] = app_globals.Globals()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = Orphereus.lib.helpers
    if not deployMode:
        config['routes.map'] = make_map()

    # Customize templating options via this variable
    #tmpl_options = config['buffet.template_options']

    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories = paths['templates'],
        error_handler = handle_mako_error,
        module_directory = os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding = 'utf-8', output_encoding = 'utf-8',
        imports = ['from webhelpers.html import escape'],
        default_filters = ['unicode', 'trim', ]) # 'escape', ])
        #TODO:turn escape filter on and use h.literal for all strings in templates

    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine, meta)

    #if not setupMode:
    init_globals(config['pylons.app_globals'], deployMode)
    #adminAlert("Orphie-kun: Hello, I'm respawned")
