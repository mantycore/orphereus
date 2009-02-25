"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
from pylons.error import handle_mako_error
from pylons import config

import fc.lib.app_globals as app_globals
import fc.lib.helpers
from fc.config.routing import make_map
from fc.lib.miscUtils import adminAlert

#from fc.model import meta
from sqlalchemy import engine_from_config
from fc.model import init_model, init_globals

import logging
log = logging.getLogger(__name__)

def load_environment(global_conf, app_conf, setupMode):
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='fc',
                    template_engine='mako', paths=paths)

    #config['pylons.strict_c'] = False
    #config['pylons.c_attach_args'] = True

    #config['pylons.g'] = app_globals.Globals()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = fc.lib.helpers
    config['routes.map'] = make_map()

    # Customize templating options via this variable
    #tmpl_options = config['buffet.template_options']

    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=paths['templates'],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', output_encoding='utf-8',
        imports=['from webhelpers.html import escape'],
        default_filters=['escape'])

    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

    #if not setupMode:
    init_globals(config['pylons.app_globals'])
    #adminAlert("Orphie-kun: Hello, I'm respawned")
