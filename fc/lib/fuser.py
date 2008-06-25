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

class FUser(object):
    def __init__(self, uid_number = -1):
        self.__uidNumber = uid_number
        self.__valid = False
        
        if uid_number>-1:
            self.__user = meta.Session.query(User).options(eagerload('options')).filter(User.uid_number==uid_number).first()
            
            #log.debug(self.__user) 
            
            if self.__user:
                self.__valid = True                

                if not self.__user.options:
                    self.__user.options = UserOptions()
                    self.__user.options.threads_per_page = 10
                    self.__user.options.replies_per_thread = 10
                    self.__user.options.style = 'photon'
                    self.__user.options.template = 'wakaba'
                    self.__user.options.bantime = 0
                    self.__user.options.canDeleteAllPosts = 0                       
                    self.__user.options.canMakeInvite = 0                     
                    meta.Session.commit()                  

                #it could be replaced by __user.* ... But it can reduce performance in case of using AutoCommit... So I'm using additional fields
                self.__threadsPerPage = self.__user.options.threads_per_page #session['options']['threads_per_page']
                self.__repliesPerThread = self.__user.options.replies_per_thread #session['options']['replies_per_thread']
                self.__style = self.__user.options.style #session['options']['style']
                self.__template =  self.__user.options.template #session['options']['template']
                self.__canDeleteAllPosts = self.__user.options.canDeleteAllPosts
                self.__canMakeInvite = self.__user.options.canMakeInvite
                self.__valid = True
                
    def isValid(self):
        return self.__valid
    def isAuthorized(self):
        return self.isValid() and (session.get('uid_number', -1) == self.__uidNumber)
    def uidNumber(self):
        return self.__uidNumber
    def uid(self):
        return self.__user.uid
    def threadsPerPage(self, value = False):
    	if value:
    	    self.__user.options.threads_per_page = value
    		self.__threadsPerPage = value        
        return self.__threadsPerPage
    def repliesPerThread(self, value = False):
    	if value:
    	    self.__user.options.replies_per_thread = value
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
    def bantime(self):   
        return self.__user.bantime
    def banreason(self):
        return self.__user.banreason 
