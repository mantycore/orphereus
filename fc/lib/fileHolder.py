import os

import logging
log = logging.getLogger(__name__)

class AngryFileHolder:
    def __init__(self, filename):
        self.__file = filename
        self.__deleteOnDestroy = True

    def disableDeletion(self):
        self.__deleteOnDestroy = False

    def path(self):
        return self.__file

    def __del__(self):
        if self.__deleteOnDestroy:
            #log.debug("File deleted")
            os.unlink(self.__file)


