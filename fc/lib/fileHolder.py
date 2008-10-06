import os
from fc.model import *

import logging
log = logging.getLogger(__name__)

class AngryFileHolder:
    def __init__(self, filename, pic = False):
        #log.debug('holder created')
        self.__file = filename
        self.__pic = pic
        self.__deleteOnDestroy = True
        
    def disableDeletion(self):
        self.__deleteOnDestroy = False

    def __del__(self):
        #log.debug('Destruction... ' + self.__file)
        if self.__deleteOnDestroy:
            os.unlink(self.__file)
            #log.debug('Holded file deleted!')
            
            if self.__pic:
                meta.Session.delete(self.__pic)
                meta.Session.commit()
                #log.debug('picid file deleted!')
            
