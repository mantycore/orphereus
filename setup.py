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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. # #                                                                              #
################################################################################

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from Orphereus.lib.app_globals import Globals
from Orphereus.lib.constantValues import decimalVersion
globj = Globals(eggSetupMode = True)

print ""

eplist = ""
for plugin in globj.plugins:
    for ep in plugin.entryPointsList():
        eplist += "%s = %s:%s\n" % (ep[0], plugin.namespaceName(), ep[1])

entry_points = """
    [paste.app_factory]
    main = Orphereus.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

"""

if eplist:
    print "Plugins provides these entry points:"
    print eplist
    entry_points += "[paste.paster_command]\n"
    entry_points += eplist

setup(
    name = 'Orphereus',
    version = decimalVersion,
    description = 'Powerful imageboard engine',
    author = 'Anoma Chan',
    license = 'GPL 2',
    author_email = 'anoma.team@gmail.com',
    url = 'http://orphereus.anoma.ch',
    install_requires = ["Pylons>=0.9.7",
                        "sqlalchemy>=0.6b",
                        "ipcalc>=0.1",
                        "mutagen>=1.15",
                        "pil>=1.1.6",
                        "pygments>=1.0",
                        "lxml>=2.0",
                        "pycaptcha>=0.4",
                        "html5lib>=0.11.0",
                      ],
    packages = find_packages(exclude = ['ez_setup']),
    include_package_data = True,
    test_suite = 'nose.collector',
    package_data = {'Orphereus': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors = {'Orphereus': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('templates/**.js', 'mako', None),
            ('public/**', 'ignore', None)]},

    entry_points = entry_points,
)
