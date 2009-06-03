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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #                                                                         #
################################################################################

import cgi
import os.path

from paste.urlparser import PkgResourcesParser
from pylons import request
from pylons.controllers.util import forward
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal

"""
from paste.urlparser import StaticURLParser
from pylons.middleware import error_document_template, media_path
from OrphieBaseController import OrphieBaseController
"""
from Orphereus.lib.base import *

import logging
log = logging.getLogger(__name__)

class ErrorController(BaseController):
    def document(self):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        message = literal(resp.status) or cgi.escape(request.GET.get('message'))
        params = dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                 code=cgi.escape(request.GET.get('code', str(resp.status_int))),
                 message=message,
                 errorPic="%serror.png" % g.OPT.staticPathWeb,
                 )
        """
        params = dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                 code=cgi.escape(request.params.get('code', '')),
                 message=cgi.escape(request.params.get('message', '')),
                 errorPic="%serror.png" % g.OPT.staticPathWeb,
                 )
        """
        #page = error_document_template % params
        #return page
        out = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>Orphereus: misfunction. %(code)s</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta name="robots" content="noarchive" />
        <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
    </head>
    <body style='background-color: #eb6d00;'>
    <div style="text-align:center;">
        <img src='%(errorPic)s' alt = 'Orphie-kun' style="border: 2px solid #820000;"/>
        <h1 style='color: #ffffff;'>I'm awfully sorry, my dear user.</h1>
        <h2 style='color: #ffffff;'>I'm feeling</h2>
        <h1 style="color: #820000; background-color: #FADDDD;">%(message)s
        <br/>
        <a href="http://trac.anoma.ch">Visit Bugtracker</a></h1>
        <br/>
        %(prefix)s
    </div>
    </body>
</html>
"""
        out = out % params
        return out

