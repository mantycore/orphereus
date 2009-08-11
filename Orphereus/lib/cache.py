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
try:
    from memcache import Client
except:
    Client = None

if Client:
    class MCache(Client):
        valid = True
            
else:
    class MCache():
        valid = False
        def __init__(self, *args, **kwargs):
            pass
        def set(self, *args, **kwargs):
            pass
        def get(self, *args, **kwargs):
            return None
        def set_multi(self, *args, **kwargs):
            pass
        def get_multi(self, *args, **kwargs):
            return {}
    
if (__name__ == '__main__'):
    key = 'nya_1'
    mc = MCache()
    mc.connect(['127.0.0.2:11211'])
    mc.set(key,'^_^')
    print mc.get(key)
    print mc.get_multi([key])