import re
import os
import logging
import datetime
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
from fc.lib.constantValues import *
from fc.lib.settings import *
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

class empty(object):
    pass

class FieldStorageLike(object):
    def __init__(self,filename,filepath):
        self.filename = filename
        self.file = open(filepath,'rb')

def filterText(text):
    return text.replace('<','&lt;').replace('>','&gt;').replace("'",'&#39;').replace('"','&quot;').replace('(c)','&copy;').replace('--','&#151;').replace('(tm)','&#153;').replace('...','&#8230;')

def isNumber(n):
    if n and isinstance(n, int):
        return True
    if n and isinstance(n, basestring):
        if re.match("^[-+]?[0-9]+$", n):
            return True
        else:
            return False
    else:
        return False
        
def currentUID():
    if c.userInst:
        return c.userInst.uidNumber()
    else:
        return -1        
        
def addLogEntry(event,entry):
    logEntry = LogEntry()
    logEntry.uidNumber = currentUID()
    logEntry.date = datetime.datetime.now()
    logEntry.event = event
    logEntry.entry = entry
    meta.Session.save(logEntry)
    meta.Session.commit()
    
def adminAlert(alertStr):
    server = smtplib.SMTP(g.OPT.alertServer, g.OPT.alertPort)
    if g.OPT.alertPort == 587:
        server.ehlo()
        server.starttls()
        server.ehlo()    
    server.login(g.OPT.alertSender, g.OPT.alertPassword)

    msg = MIMEMultipart()
    msg['From'] = g.OPT.alertSender
    msg['To'] = g.OPT.alertEmail
    msg['Subject'] = _(g.OPT.baseDomain + (' ALERT by %d: ' % currentUID()))
    msg.attach(MIMEText(alertStr))
   
    server.sendmail(g.OPT.alertSender, g.OPT.alertEmail, msg.as_string())
    server.close()    
    
def checkAdminIP():
    if request.environ["REMOTE_ADDR"] != '127.0.0.1':
        msg = _("Access attempt from %s for admin account!") % request.environ["REMOTE_ADDR"]
        addLogEntry(LOG_EVENT_SECURITY_IP, msg)
        adminAlert(msg)
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

def getRPN(text, operators):
    whitespace = [' ',"\t","\r","\n","'",'"','\\','<','>']
    stack = []
    temp  = []
    result= []
    for i in text:
        if i == '(':
            if temp:
                result.append(''.join(temp))
                temp = []
            stack.append('(')
        elif i == ')':
            if temp:
                result.append(''.join(temp))
                temp = []                
            while (stack and stack[-1] != '('):
                result.append(stack.pop())
            if stack:
                stack.pop()
        elif i in operators:
            if temp:
                result.append(''.join(temp))
                temp = []
            while (stack and (stack[-1] in operators) and (operators[i] <= operators[stack[-1]])):
                result.append(stack.pop())
            stack.append(i)
        elif not i in whitespace:
            temp.append(i)
    if temp:
        result.append(''.join(temp))
        temp = []
    while stack:
        result.append(stack.pop())
    return result


 