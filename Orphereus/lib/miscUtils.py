################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

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

from Orphereus.lib.constantValues import *

class empty(object):
    pass

class FieldStorageLike(object):
    def __init__(self, filename, filepath):
        self.filename = filename
        self.file = open(filepath, 'rb')

def natsort(list_):
    tmp = [ (int(re.search('\d+', i).group(0)), i) for i in list_ ]
    tmp.sort()
    return [ i[1] for i in tmp ]

from Orphereus.lib.OrphieMark.tools import filterText as filterText

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

def toNumber(n, default = 0, minimum = None):
    if isNumber(n) and (not minimum or int(n) >= minimum):
        return int(n)
    return default

def currentUID():
    try:
        if c.userInst:
            return c.userInst.uidNumber
    except:
        pass
    return - 1

def toLog(event, text, commit = True):
    from Orphereus.model import LogEntry
    LogEntry.create(currentUID(), event, text, commit)

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
        msg['Subject'] = '%s: Security alert by %d: ' % (g.OPT.baseDomain, currentUID())
        msg.attach(MIMEText(alertStr))

        server.sendmail(g.OPT.alertSender, mail, msg.as_string())
    server.close()

def getUserIp():
    if g.OPT.useXRealIP:
        return request.headers["X-Real-IP"]
    return request.environ["REMOTE_ADDR"]

def checkAdminIP():
    import ipcalc
    if g.OPT.useAnalBarriering:
        userip = getUserIp()
        for range in g.OPT.trustedIPRanges:
            if userip in ipcalc.Network(range):
                return True
        msg = _("Access attempt from %s for admin account!") % getUserIp()
        toLog(LOG_EVENT_SECURITY_IP, msg)
        adminAlert(msg)
        session['uidNumber'] = -1
        session.save()
        return False
    return True

def getRPN(text, operators):
    whitespace = [' ', "\t", "\r", "\n", "'", '"', '\\', '<', '>']
    stack = []
    temp = []
    result = []
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
