from lxml.builder import E
from lxml import etree
import datetime

_Version = '0.2'

def xmlGetter(xml, item, key='val'):
    """item - child's name"""
    if item:
        return xml.find(item).get(key)
    return xml.get(key)

class Post():
    topic = text = name = trip = link = u''
    rawDate = file = localName = preview = previewLocalName = localName = u''
    parent = id = date = 0
    
    def __repr__(self):
        return '<Post #%s (p: %s), %s>' %(self.id, self.parent, self.date)

    def toXml(self):
        return E('post',
                 E('parent',id="%s" %self.parent),
                 E('topic',val=self.topic),
                 E('date',val="%s" %self.date),
                 E('name',val=self.name),
                 E('trip',val=self.trip),
                 E('link',val=self.link),
                 E('file',val=self.file,localname=self.localName),
                 E('text',val=self.text),
                 E('preview',val=self.preview,localname=self.previewLocalName),
                 id="%s" %self.id)
        
    def toXmlString(self):
        return etree.tostring(self.toXml())
    
    def fromXml(self, xml):
        self.id = xmlGetter(xml, None, 'id')
        self.parent = xmlGetter(xml, 'parent', 'id')
        for param in list(['topic','date','name','trip','link','file','preview','text']):
            setattr(self, param, xmlGetter(xml, param))
        self.previewLink = xmlGetter(xml, 'preview')        
        self.localName = xmlGetter(xml, 'file', 'localname')        
        self.previewLocalName = xmlGetter(xml, 'preview', 'localname')    
        self.date = datetime.datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S') #omg.
        #print etree.dump(xml)
    
    def fromXmlString(self, xmlStr):
        xml = etree.fromstring(xmlStr, etree.XMLParser())
        self.fromXml(xml)
    
    def test(self):
        #print self.toXmlString()
        testPost = Post.createFromXmlString(self.toXmlString())
        print "%s => %s" % (self, testPost)

    @staticmethod
    def createFromXml(xml):
         post = Post()
         post.fromXml(xml)
         return post
    
    @staticmethod
    def createFromXmlString(xml):
         post = Post()
         post.fromXmlString(xml)
         return post    