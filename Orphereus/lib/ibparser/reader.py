import os, os.path, shutil
from tempfile import mkdtemp
import shutil
import tarfile
from lxml import etree
import datetime

from chans.Post import *
from chans.Thread import *

def read(file):
    f = open(file,'r')
    data = f.read()
    f.close()
    return data

class ThreadReader():
    fsClass = None
    def __init__(self, archive):
        self.arcName = os.path.basename(archive)
        self.archive = archive
        self.tempDir = mkdtemp()
        if archive:
            self.readArc()
        
    def __del__(self):
        shutil.rmtree(self.tempDir, True)
        
    def unpack(self):
        if not(self.tempDir in self.archive):
            shutil.copy(self.archive, self.tempDir)
        os.chdir(self.tempDir)
        arc = tarfile.open(self.arcName, 'r')
        arc.extractall('./data/')
    
    def readArc(self):
        self.unpack()
        self.thread = Thread.createFromXmlString(read('./data/thread.xml'))
        
    def fieldStorage(self, fname):
        try:
            if fname and self.fsClass:
                return self.fsClass(fname, './data/%s' %fname)
        except:
            return None
    
    def test(self):
        return (read('./data/thread.xml') == self.thread.toXmlString())
    
    @staticmethod
    def createFromPostData(data):
        reader = ThreadReader('')
        reader.arcName = 'posted.tar.gz'
        localFilePath = os.path.join(reader.tempDir, reader.arcName)
        localFile = open(localFilePath, 'w+b')
        shutil.copyfileobj(data.file, localFile)
        localFile.close()
        reader.archive = localFilePath
        reader.readArc()
        return reader

class ThreadLoader():
    def __init__(self, url):
        pass
'''
HTTP/1.1 200 OK
Date: Sat, 22 Aug 2009 17:39:35 GMT
Server: Apache/2.2.0 (Win32) DAV/2 mod_ssl/2.2.0 OpenSSL/0.9.8a mod_autoindex_color PHP/5.1.1
Last-Modified: Thu, 02 Oct 2008 07:29:06 GMT
ETag: "289fa-2d42-2bfd1480"
Accept-Ranges: bytes
Content-Length: 11586
Content-Type: text/html


months = ['', u'Jan', u'Feb', u'Mar', u'Apr', u'May', u'Jun', u'Jul', u'Aug', u'Sep', u'Oct', u'Nov', u'Dec']
regexp = re.compile(r"""\w+, (\d+) (\w+) (\d+) (\d+):(\d+):(\d+).+""")
data = regexp.findall(date)
month = months.index(data[0][1])
return datetime.datetime(int(data[0][2]),month,int(data[0][0]),int(data[0][3]),int(data[0][4]),int(data[0][5]))
'''
    
if (__name__ == '__main__'):
    tr = ThreadReader('pa_2467.tar.gz')
    print tr.test()