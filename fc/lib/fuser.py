import logging

from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
import os
import cgi
import shutil
import datetime
import time
import Image
import os
import hashlib
import re
import pickle

class FUser(object):
    def __init__(self, uidNumber = -1):
        self.__uidNumber = uidNumber
        self.__valid = False
        
        if uidNumber>-1:
            self.__user = meta.Session.query(User).options(eagerload('options')).filter(User.uidNumber==uidNumber).first()
                        
            if self.__user:
                self.__valid = True                

                if not self.__user.options:
                    self.__user.options = UserOptions()
                    self.__user.options.threadsPerPage = 10
                    self.__user.options.repliesPerThread = 10
                    self.__user.options.style = 'photon'
                    self.__user.options.template = 'wakaba'
                    self.__user.options.bantime = 0
                    self.__user.options.canDeleteAllPosts = 0                       
                    self.__user.options.canMakeInvite = 0                     
                    self.__user.options.canChangeRights = 0  
                    self.__user.options.isAdmin = False
                    self.__user.options.hideLongComments = True
                    self.__user.options.homeExclude = pickle.dumps([])
                    meta.Session.commit()                  
                
                if not self.__user.options.homeExclude:
                    self.__user.options.homeExclude = pickle.dumps([])
                    meta.Session.commit()
                
                #it could be replaced by __user.* ... But it can reduce performance in case of using AutoCommit... So I'm using additional fields
                self.__threadsPerPage = self.__user.options.threadsPerPage #session['options']['threadsPerPage']
                self.__repliesPerThread = self.__user.options.repliesPerThread #session['options']['repliesPerThread']
                self.__style = self.__user.options.style #session['options']['style']
                self.__template =  self.__user.options.template #session['options']['template']
                self.__isAdmin = self.__user.options.isAdmin                
                self.__hideLongComments = self.__user.options.hideLongComments
                self.__canDeleteAllPosts = self.__user.options.canDeleteAllPosts
                self.__canMakeInvite = self.__user.options.canMakeInvite and self.__isAdmin
                self.__canChangeRights = self.__user.options.canChangeRights and self.__isAdmin
                self.__homeExclude = pickle.loads(self.__user.options.homeExclude)
                self.__filters = self.__user.filters
                self.__valid = True
                
    def isValid(self):
        return self.__valid
    def isAuthorized(self):
        return self.isValid() and (session.get('uidNumber', -1) == self.__uidNumber)
    def isBanned(self):
        return self.__user.options.bantime > 0
    def isAdmin(self):
        return self.__isAdmin
    def uidNumber(self):
        return self.__uidNumber
    def secid(self):
        return (2*self.__uidNumber + 3) * (self.__uidNumber + 10) * (self.__uidNumber - 1)
        #(2*x+3)*(x+10)*(x-1)=
    def uid(self, value=None):        
        if value != None and not meta.Session.query(User).options(eagerload('options')).filter(User.uid==value).first():
            self.__user.uid = value
        return self.__user.uid        
    def filters(self):
        return self.__filters
    def hideLongComments(self, value=None):
        if value != None:
            self.__user.options.hideLongComments = value
            self.__hideLongComments = self.__user.options.hideLongComments
        return self.__hideLongComments
    def homeExclude(self, value = None):
        if value != None:
            self.__user.options.homeExclude = pickle.dumps(value)
            self.__homeExclude = pickle.loads(self.__user.options.homeExclude)
        return self.__homeExclude
    def threadsPerPage(self, value = False):
    	if value:
    	    self.__user.options.threadsPerPage = value
            self.__threadsPerPage = value        
        return self.__threadsPerPage
    def repliesPerThread(self, value = False):
    	if value:
    	    self.__user.options.repliesPerThread = value
    	    self.__repliesPerThread = value        
        return self.__repliesPerThread
    def style(self, value = False):
    	if value:
    	    self.__user.options.style = value
    	    self.__style = value        
        return self.__style
    def template(self, value = False):
    	if value:
    	    self.__user.options.template = value
    	    self.__template = value
        return self.__template
    def canDeleteAllPosts(self):
        return self.__canDeleteAllPosts
    def canMakeInvite(self):
        return self.__canMakeInvite    
    def canChangeRights(self):
        return self.__canChangeRights            
    def bantime(self):   
        return self.__user.options.bantime
    def banreason(self):
        return self.__user.options.banreason 
