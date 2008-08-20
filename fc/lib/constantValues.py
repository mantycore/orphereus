import sys
import os 

hashSecret = 'paranoia' # We will hash it by sha512, so no need to have it huge
appPath = sys.path[0]
templPath= os.path.join(appPath, 'fc/templates/')
uploadPath = os.path.join(appPath, 'fc/uploads/')
#u#ploadPathWeb = '/uploads/'
baseDomain='anoma.ch'
markupFile = os.path.join(appPath, 'wakabaparse/mark.def')
devMode = os.path.exists(os.path.join(appPath, 'fc/development.dummy'))    
filesPathWeb='http://wut.anoma.ch/img1/'
if devMode:
    filesPathWeb='http://wut.anoma.ch/img2/'
refControlList = ['anoma.ch', 'anoma.li', 'localhost', '127.0.0.1']
fakeLinks = ['http://www.youtube.com/watch?v=oHg5SJYRHA0', 'http://meatspin.com/']

settingsDef = {
    "title"         : "ANOMA.Ch",
    "invisibleBump" : 'true',
    "maxTagsCount"  : '5',
    "maxTagLen"     : '6',
    "disabledTags"  : 'logout,authorize,register,youAreBanned,userProfile,holySynod',
    "adminOnlyTags" : 'synod,logs',
    "maxLinesInPost": '15',
    "cutSymbols"    : '5000',
    "usersCanViewLogs"  : 'false'
}

LOG_EVENT_SECURITY_IP   = 0x00000001
LOG_EVENT_INVITE        = 0x00010001
LOG_EVENT_INVITE_USED   = 0x00010002
LOG_EVENT_BOARD_EDIT    = 0x00020001
LOG_EVENT_BOARD_DELETE  = 0x00020002
LOG_EVENT_USER_EDIT     = 0x00030001
LOG_EVENT_USER_DELETE   = 0x00030002
LOG_EVENT_USER_ACCESS   = 0x00030003
LOG_EVENT_USER_BAN      = 0x00030004
LOG_EVENT_USER_UNBAN    = 0x00030005
LOG_EVENT_USER_GETUID   = 0x00030006
LOG_EVENT_SETTINGS_EDIT = 0x00040001
LOG_EVENT_POSTS_DELETE  = 0x00050001
LOG_EVENT_EXTENSION_EDIT= 0x00060001
LOG_EVENT_MTN_BEGIN     = 0x00070001
LOG_EVENT_MTN_END       = 0x00070002
LOG_EVENT_MTN_UNBAN     = 0x00070002
LOG_EVENT_RICKROLLD     = 0x00080001