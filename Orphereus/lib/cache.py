# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Hedger                                                   #
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
        '''Extended memcache.Client, with automatic key prefixing and SQLA \
        objects storing capabilities'''
        valid = True
        uniqeKey = ''
        meta = None
        def __init__(self, *args, **kwargs):
            self.uniqeKey = kwargs.get('key', '')
            self.meta = kwargs.get('meta', '')
            del kwargs['key'], kwargs['meta']
            Client.__init__(self, *args, **kwargs)

        def delete(self, key, **kwargs):
            return Client.delete(self, self.uniqeKey + str(key), **kwargs)

        def set(self, key, val, **kwargs):
            return Client.set(self, self.uniqeKey + str(key), val, **kwargs)

        def get(self, key):
            return Client.get(self, self.uniqeKey + str(key))

        def get_multi(self, keys, **kw):
            kw['key_prefix'] = "%s%s" % (self.uniqeKey, kw.get('key_prefix', ''))
            return Client.get_multi(self, keys, **kw)

        def set_multi(self, mapping, **kw):
            kw['key_prefix'] = "%s%s" % (self.uniqeKey, kw.get('key_prefix', ''))
            return Client.set_multi(self, mapping, **kw)

        def set_sqla(self, key, obj, **kwargs):
            '''Saves SQLAlchemy object in a session-restorable form'''
            return self.set(key, dumps(obj), **kwargs)

        def get_sqla(self, key):
            '''Reads SQLAlchemy object and restores session metadata'''
            serial = self.get(key)
            if serial:
                return loads(serial, self.meta.metadata, self.meta.Session)
            return None

        def setdefaultEx(self, key, function, *args, **kwargs):
            '''extended dict-like setdefault, returns stored key value, if it exists.\
            Otherwise, executes function(), saves and returns the result'''
            res = self.get(key)
            if not(res):
                res = function(*args)
                self.set(key, res, **kwargs)
            return res

        def setdefault_sqlaEx(self, key, function, *args, **kwargs):
            '''setdefaultEx modification for functions, returning Alchemy objects'''
            res = self.get_sqla(key)
            if not(res):
                res = function(*args)
                self.set_sqla(key, res, **kwargs)
            return res

else:
    class MCache():
        '''Fake class with stub implementation of all methods.
        It is used when memcache package is unavaliable.'''
        valid = False
        __init__ = set = get = delete = set_multi = set_sqla = get_sqla = disconnect_all = set_servers = \
             lambda *args, **kwargs: None
        get_multi = lambda *args, **kwargs: {}
        setdefaultEx = setdefault_sqlaEx = \
             lambda key, function, *args, **kwargs: function(*args)

class CacheDict(dict):
    def setdefaultEx(self, key, function, *args):
        '''extended setdefault, returns stored value, if it exists.\
        Otherwise, executes function(), saves and returns the result'''
        if key in self:
            return self[key]
        else:
            log.debug("Key '%s' not found in cache, calling %s to fill in" % (key, function))
            return self.setdefault(key, function(*args))
