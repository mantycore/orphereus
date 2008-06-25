import logging
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
from fc.lib.fuser import FUser

log = logging.getLogger(__name__)

class FcaController(BaseController):
    def boardsManagement(self):
        return render('/wakaba.boardsManage.mako')
