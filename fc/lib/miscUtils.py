from pylons import config
from pylons import c, cache, config, g, request, response, session
from pylons.i18n import _, ungettext, N_

import re
import os
import logging
import datetime

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

from fc.model import LogEntry
from fc.lib.constantValues import *

class empty(object):
    pass

class FieldStorageLike(object):
    def __init__(self,filename,filepath):
        self.filename = filename
        self.file = open(filepath, 'rb')

def filterText(text):
    return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace("'",'&#39;') \
               .replace('"','&quot;').replace('(c)','&copy;').replace('--','&#151;') \
               .replace('(tm)','&#153;').replace('...','&#8230;')

def isNumber(n):
    if isinstance(n, int):
        return True
    if n and isinstance(n, basestring):
        if re.match("^[-+]?[0-9]+$", n):
            return True
        else:
            return False
    else:
        return False

def currentUID():
    try:
        if c.userInst:
            return c.userInst.uidNumber()
    except:
        pass
    return -1

def toLog(event, text, commit = True):
    LogEntry.create(currentUID(), event, filterText(text), commit)

def adminAlert(alertStr):
    g = config['pylons.app_globals']
    server = smtplib.SMTP(g.OPT.alertServer, g.OPT.alertPort)
    if g.OPT.alertPort == 587: #fix for google
        server.ehlo()
        server.starttls()
        server.ehlo()
    server.login(g.OPT.alertSender, g.OPT.alertPassword)

    for mail in g.OPT.alertEmail:
        msg = MIMEMultipart()
        msg['From'] = g.OPT.alertSender
        msg['To'] = mail
        msg['Subject'] =  '%s: Security alert by %d: ' % (g.OPT.baseDomain, currentUID())
        msg.attach(MIMEText(alertStr))

        server.sendmail(g.OPT.alertSender, mail, msg.as_string())
    server.close()

def getUserIp():
    if g.OPT.useXRealIP:
        return request.headers["X-Real-IP"]
    return request.environ["REMOTE_ADDR"]

def checkAdminIP():
    if g.OPT.useAnalBarriering and getUserIp() != '127.0.0.1':
        msg = _("Access attempt from %s for admin account!") % getUserIp()
        toLog(LOG_EVENT_SECURITY_IP, msg)
        adminAlert(msg)
        session['uidNumber'] = -1
        session.save()
        return False
    else:
        return True

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

