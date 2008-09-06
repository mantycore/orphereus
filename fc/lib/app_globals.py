"""The application's Globals object"""
from pylons import config
import sys
import os
 
"""
from fc.lib.miscUtils import getSettingsMap
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
from fc.lib.constantValues import *
from fc.lib.settings import *
from miscUtils import *
"""

class OptHolder(object):
    def __init__(self):
        #in most cases you don't need to change these paths
        self.appPath = os.path.dirname(__file__).replace('/fc/lib', '').replace('\\fc\\lib', '')  #sys.path[0] #os.path.dirname(__file__) 
        self.templPath= os.path.join(self.appPath, 'fc/templates/')
        self.uploadPath = os.path.join(self.appPath, 'fc/uploads/')
        self.captchaFont = os.path.join(self.appPath, 'fc/cfont.ttf')
        self.markupFile = os.path.join(self.appPath, 'wakabaparse/mark.def')
        self.devMode = os.path.exists(os.path.join(self.appPath, 'fc/development.dummy'))           

        #basic IB settings
        self.hashSecret = 'paranoia' # We will hash it by sha512, so no need to have it huge
        self.baseDomain='anoma.ch' 
        self.minPassLength=12

        self.filesPathWeb='http://wut.anoma.ch/img1/'
        if self.devMode:
            self.filesPathWeb='http://wut.anoma.ch/img2/'
                            
        # Anoma.ch-specific settings
        self.refControlList = ['anoma.ch', 'anoma.li', 'localhost', '127.0.0.1']
        self.fakeLinks = ['http://www.youtube.com/watch?v=oHg5SJYRHA0', 'http://meatspin.com/', 'http://youtube.com/watch?v=Uqot33mczsw', 'http://youtube.com/watch?v=dZBU6WzBrX8']
        self.alertEmail='lamo@sms.megafonsib.ru'
        self.alertServer='smtp.gmail.com'
        self.alertPort=587
        self.alertSender='alert@anoma.ch'
        self.alertPassword='60J266'

class Globals(object):   
    def __init__(self):
        self.OPT = OptHolder() 
 
