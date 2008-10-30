"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons import config
import datetime

def modLink(string, secid, f):
    if f:
        p1 = string[0:4]
        p2 = string[4:8]
        p3 = string[8:len(string)]
        return p1 + str(secid) + p2 + p3
    else:
        return string

def modMessage(message, user, f):  
    if f:
        gv = config['pylons.g']  
        uval = gv.uniqueVals[user.uidNumber() % (len(gv.uniqueVals) - 1)]
        return message.replace('[SECURITY:UNIQUE_VAL]', uval)
    else:
        return message
    
def modTime(post, user, f):
    if f:
         return post.date - datetime.timedelta(seconds=((-1)**user)*int(user/2))
    else:
        return post.date

