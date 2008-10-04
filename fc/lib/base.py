"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

import fc.lib.helpers as h
import fc.model as model

from fc.model import meta
import time

import logging
log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
            
    def sqlCount(self, filter, id = ''):
        if g.OPT.devMode:
            id += str(filter)
            ct = time.time()  
        result = filter.count()
        if g.OPT.devMode:
            rtime = time.time() - ct
            c.sum += rtime
            c.log.append("%s<br/>%s" %(id, str(rtime)))
        return result        

    def sqlAll(self, filter, id = ''):
        if g.OPT.devMode:
            id += str(filter)
            ct = time.time()  
        result = filter.all()
        if g.OPT.devMode:
            rtime = time.time() - ct
            c.sum += rtime
            c.log.append("%s<br/>%s" %(id, str(rtime)))
        return result                
    
    def sqlOne(self, filter, id = ''):
        if g.OPT.devMode:
            id += str(filter)
            ct = time.time()  
        result = filter.one()
        if g.OPT.devMode:
            rtime = time.time() - ct
            c.sum += rtime
            c.log.append("%s<br/>%s" %(id, str(rtime)))
        return result                 
    
    def sqlGet(self, filter, rid,  id = ''): 
        if g.OPT.devMode:
            id += str(filter)
            ct = time.time()  
        result = filter.get(rid)
        if g.OPT.devMode:
            rtime = time.time() - ct
            c.sum += rtime
            c.log.append("%s<br/>%s" %(id, str(rtime)))
        return result
 
    def sqlFirst(self, filter, id = ''):
        if g.OPT.devMode:
            id += str(filter)
            ct = time.time()  
        result = filter.first()
        if g.OPT.devMode:
            rtime = time.time() - ct
            c.sum += rtime
            c.log.append("%s<br/>%s" %(id, str(rtime)))
        return result                

    def sqlSlice(self, filter, a = None, b = None, id = ''):
        if g.OPT.devMode:
            id += str(filter)
            ct = time.time()  
        #log.debug("%s/%s" %(str(a), str(b)))
        if a == None and b != None:
            result = filter[:b]
            #log.debug('1')
        elif b == None and a != None:
            result = filter[a:]
            #log.debug('2')
        else:
            result = filter[a:b]
            #log.debug('3')
        if g.OPT.devMode:
            rtime = time.time() - ct
            c.sum += rtime
            c.log.append("%s<br/>%s" %(id, str(rtime)))
        return result          

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
