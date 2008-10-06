"""The application's Globals object"""
from pylons import config
import sys
import os
 
import logging
log = logging.getLogger(__name__)


class OptHolder(object):
    def __init__(self):
        #in most cases you don't need to change these paths
        self.appPath = os.path.dirname(__file__).replace('/fc/lib', '').replace('\\fc\\lib', '')  #sys.path[0] #os.path.dirname(__file__) 
        self.templPath= os.path.join(self.appPath, 'fc/templates/')
        self.uploadPath = os.path.join(self.appPath, 'fc/uploads/')
        self.captchaFont = os.path.join(self.appPath, 'fc/cfont.ttf')
        self.markupFile = os.path.join(self.appPath, 'wakabaparse/mark.def')                   
        
        # Basic IB settings
        self.devMode = (config['core.devMode'] == 'true')        
        self.hashSecret = config['core.hashSecret']
        self.baseDomain = config['core.baseDomain'] 
        self.minPassLength = int(config['core.minPassLength'])
        self.filesPathWeb=config['core.filesPathWeb']
        
        # Security settings
        #self.refControlList = ['anoma.ch', 'anoma.li', 'localhost', '127.0.0.1']
        #self.fakeLinks = ['http://www.youtube.com/watch?v=oHg5SJYRHA0', 'http://meatspin.com/', 'http://youtube.com/watch?v=Uqot33mczsw', 'http://youtube.com/watch?v=dZBU6WzBrX8']

        self.alertEmail = config['security.alertEmail'] 
        self.alertServer = config['security.alertServer']
        self.alertPort = int(config['security.alertPort'])
        self.alertSender = config['security.alertSender']
        self.alertPassword = config['security.alertPassword']

        self.refControlEnabled = (config['security.refControlEnabled'] == 'true') 
        self.refControlList = config['security.refControlList'].split(',')
        self.fakeLinks = config['security.fakeLinks'].split(',')

        self.obfuscator = config['security.obfuscator']
        
class Globals(object):   
    def __init__(self):
        self.OPT = OptHolder() 
 
