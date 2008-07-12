import re
import logging
import datetime
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
from fc.lib.constantValues import *
from fc.lib.settings import *

class FieldStorageLike(object):
    def __init__(self,filename,filepath):
        self.filename = filename
        self.file = open(filepath,'rb')

def filterText(text):
    return text.replace('<','&lt;').replace('>','&gt;').replace("'",'&#39;').replace('"','&quot;').replace('(c)','&copy;').replace('---','&#151;').replace('--','&#8722;').replace('(tm)','&#153;').replace('...','&#8230;')

def isNumber(n):
    if n and isinstance(n, basestring):
        if re.match("^[-+]?[0-9]+$", n):
            return True
        else:
            return False
    else:
        return False
        
def addLogEntry(event,entry):
    logEntry = LogEntry()
    logEntry.uidNumber = c.userInst.uidNumber()
    logEntry.date = datetime.datetime.now()
    logEntry.event = event
    logEntry.entry = entry
    meta.Session.save(logEntry)
    meta.Session.commit()
    
def initEnvironment():
    c.settingsMap = getSettingsMap()
    c.title = c.settingsMap['title'].value
    boards = meta.Session.query(Tag).join('options').filter(TagOptions.persistent==True).order_by(TagOptions.sectionId).all()
    c.boardlist = []
    sectionId = 0
    section = []
    for b in boards:
        if not sectionId:
            sectionId = b.options.sectionId
            section = []
        if sectionId != b.options.sectionId:
            c.boardlist.append(section)
            sectionId = b.options.sectionId
            section = []
        section.append(b.tag)
    if section:
        c.boardlist.append(section)

def checkAdminIP():
    if request.environ["REMOTE_ADDR"] != '127.0.0.1':
        addLogEntry(LOG_EVENT_SECURITY_IP,_("Access attempt from %s for admin account!")%request.environ["REMOTE_ADDR"])
        session['uidNumber'] = -1
        session.save()
        return False
    else:
        return True

def getTagsListFromString(string):
    result = []
    tags = string.split(',')
    for tag in tags:
        aTag = meta.Session.query(Tag).options(eagerload('options')).filter(Tag.tag==tag).first()
        if aTag:
            result.append(aTag.id)
    return result