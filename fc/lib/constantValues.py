hashSecret = 'paranoia' # We will hash it by sha512, so no need to have it huge
uploadPath = 'fc/public/uploads/'
uploadPathWeb = '/uploads/'

settingsDef = {
    "title" : "ANOMA.Ch",
    "uploadPathLocal" : 'fc/public/uploads/',
    "uploadPathWeb" :  '/uploads/',
    "invisibleBump" : 'true'
}

LOG_EVENT_INVITE       = 0x00010001
LOG_EVENT_BOARD_EDIT   = 0x00020001
LOG_EVENT_BOARD_DELETE = 0x00020002
LOG_EVENT_USER_EDIT    = 0x00030001
LOG_EVENT_USER_DELETE  = 0x00030002
LOG_EVENT_USER_ACCESS  = 0x00030003
LOG_EVENT_USER_BAN     = 0x00030004
LOG_EVENT_USER_UNBAN   = 0x00030005
LOG_EVENT_SETTINGS_EDIT= 0x00040001