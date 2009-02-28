import os

import logging
log = logging.getLogger(__name__)

class AngryFileHolder:
    def __init__(self, filenames):
        self.__files = filenames
        self.__deleteOnDestroy = True

    def disableDeletion(self):
        self.__deleteOnDestroy = False

    def paths(self):
        return self.__files

    def __del__(self):
        if self.__deleteOnDestroy:
            for file in self.__files:
                if file:
                    os.unlink(file)
                    #log.debug("File %s deleted" % file)


