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

if (__name__ == '__main__'):
    tr = ThreadReader('pa_2467.tar.gz')
    print tr.test()