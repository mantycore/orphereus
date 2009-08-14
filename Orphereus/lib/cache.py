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

"""
Implements MCache class and it's fake copy, if memcache is unavailable. 
"""
from sqlalchemy.ext.serializer import loads, dumps

try:
    from memcache import Client
except:
    Client = None

import logging
log = logging.getLogger(__name__)

if Client:
    class MCache(Client):
        valid = True
        uniqeKey = ''
        meta = None
        def __init__(self, *args, **kwargs):
            self.uniqeKey = kwargs.get('key', '')
            self.meta = kwargs.get('meta', '')
            del kwargs['key'], kwargs['meta']
            Client.__init__(self, *args, **kwargs)
            
        def delete(self, key, **kwargs):
            return Client.delete(self, self.uniqeKey+str(key), **kwargs)
        
        def set(self, key, val, **kwargs):
            #log.debug('writing cache entry %s with exp time=%s' %(key,kwargs.get('time', 0)))
            return Client.set(self, self.uniqeKey+str(key), val, **kwargs)

        def get(self, key):
            return Client.get(self, self.uniqeKey+str(key))

        def set_sqla(self, key, obj, **kwargs):
            #log.debug('writing sql cache %s' %key)
            return self.set(key, dumps(obj), **kwargs)

        def get_sqla(self, key):
            #log.debug('getting sql cache %s' %key)
            serial = self.get(key)
            if serial:
                return loads(serial, self.meta.metadata, self.meta.Session)
            return None
        
        def setdefaultEx(self, key, function, *args, **kwargs): 
            res = self.get(key)
            if not(res):
                res = function(*args)
                self.set(key, res, **kwargs)
            return res

        #def setdefault_sqlEx(self, key, query, **kwargs): 
        #    res = self.get_sqla(key)
        #    if not(res):
        #        res = query
        #        self.set(key, res, **kwargs)
        #    return res

else:
    class MCache():
        valid = False
        __init__ = set = get = delete = set_multi = set_sqla = get_sqla = lambda *args, **kwargs: None
        get_multi = lambda *args, **kwargs: {}
        

class CacheDict(dict):
    def setdefaultEx(self, key, function, *args):
        try:
            return self[key]
        except:
            log.debug("Key '%s' not found in cache, calling %s to fill in" %(key, function))
            return self.setdefault(key, function(*args))