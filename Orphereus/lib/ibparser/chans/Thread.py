# coding: utf-8
from Post import *
from lxml.builder import E
from lxml import etree
import time

class Thread():
    source = parser = u''
    creator = u'真~IBparser'
    version = u'0.3'
    dateCreated = time.time()
    id = -1
    posts = []
    
    def toXml(self):
        postsXml = list([post.toXml() for post in self.posts])
        dateStr = "%s" %self.dateCreated
        return E('thread',
                    parser="%s" %self.parser,
                    id="%s" %self.id,
                    source=self.source,
                    dateCreated=dateStr.split('.')[0],
                    creator=self.creator,
                    version=self.version,
                 *postsXml)
    
    def toXmlString(self):
        return etree.tostring(self.toXml())

    def fromXml(self, xml):
        self.posts = []
        for param in list(['parser','id','source','version','dateCreated']):
            setattr(self, param, xmlGetter(xml, None, param))
        self.dateCreated = int(self.dateCreated)
        for postXml in xml.iterchildren():
            self.posts.append(Post.createFromXml(postXml))
    
    def fromXmlString(self, xmlStr):
        xml = etree.fromstring(xmlStr, etree.XMLParser())
        self.fromXml(xml)
    
    def fixupParentIds(self):
        for post in self.posts[1:]:
            post.parent = self.posts[0].id
        self.id = self.posts[0].id
    
    @staticmethod 
    def createFromXmlString(xmlStr):
        thread = Thread()
        thread.fromXmlString(xmlStr)
        return thread

    @staticmethod 
    def createFromPostArray(posts):
        thread = Thread()
        thread.posts = posts
        thread.fixupParentIds()
        return thread    

class ThreadInfo():
    board = u''
    thread = 0
    archive = False
    
    def __init__(self, **kwargs):
        map(lambda arg: setattr(self, arg, kwargs[arg]), kwargs)