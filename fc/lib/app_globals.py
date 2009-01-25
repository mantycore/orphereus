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
        proposedPath = config['core.uploadPath']
        if os.path.exists(proposedPath):
            self.uploadPath = proposedPath
        self.devMode = (config['core.devMode'] == 'true')
        self.hashSecret = config['core.hashSecret']
        self.baseDomain = config['core.baseDomain'] 
        self.minPassLength = int(config['core.minPassLength'])
        self.staticPathWeb=config['core.staticPathWeb']
        self.filesPathWeb=config['core.filesPathWeb']
        self.templates = config['core.templates'].split(',')
        self.styles = config['core.styles'].split(',')
        self.actuator = config['core.actuator']
        self.secondaryIndex = (config['core.secondaryIndex'] == 'true')
        self.vitalSigns = (config['core.vitalSigns'] == 'true')
        self.allowPosting = (config['core.allowPosting'] == 'true')
        self.allowAnonymous = (config['core.allowAnonymous'] == 'true')
        self.allowAnonymousPosting = (config['core.allowAnonymousPosting'] == 'true')
        self.allowRegistration = (config['core.allowRegistration'] == 'true')
        self.statsCacheTime = int(config['core.statsCacheTime'])
        
        # Security settings
        self.alertEmail = config['security.alertEmail'] 
        self.alertServer = config['security.alertServer']
        self.alertPort = int(config['security.alertPort'])
        self.alertSender = config['security.alertSender']
        self.alertPassword = config['security.alertPassword']

        self.refControlEnabled = (config['security.refControlEnabled'] == 'true') 
        self.refControlList = config['security.refControlList'].split(',')
        self.fakeLinks = config['security.fakeLinks'].split(',')

        self.checkUAs = (config['security.checkUAs'] == 'true')
        self.badUAs = config['security.badUAs'].split(',')
        
        self.spiderTrap = (config['security.spiderTrap'] == 'true') 

        self.obfuscator = config['security.obfuscator']
        
        self.secureLinks = (config['security.secureLinks'] == 'true')
        self.secureText = (config['security.secureText'] == 'true')
        self.secureTime = (config['security.secureTime'] == 'true')
        self.interestingNumbers = (config['security.interestingNumbers'] == 'true')
        self.useAnalBarriering = (config['security.useAnalBarriering'] == 'true')
        
        self.enableFinalAnonymity = (config['security.enableFinalAnonymity'] == 'true')
        self.finalAHoursDelay = int(config['security.finalAHoursDelay'])
        self.hlAnonymizedPosts = (config['security.hlAnonymizedPosts'] == 'true')
        
class Globals(object):   
    def __init__(self):
        self.OPT = OptHolder() 
        
        f = open(os.path.join(self.OPT.appPath, 'fc/uniqueVals.txt'), "r")
        data = f.read()
        f.close() 
        
        self.uniqueVals = data.split('\n')
        
