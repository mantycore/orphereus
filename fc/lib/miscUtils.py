import re
class FieldStorageLike(object):
    def __init__(self,filename,filepath):
        self.filename = filename
        self.file = open(filepath,'rb')

def filterText(text):
    return text.replace('<','&lt;').replace('>','&gt;').replace("'",'&#39;').replace('"','&quot;').replace('(c)','&copy;').replace('---','&#151;').replace('--','&#8722;').replace('(tm)','&#153;').replace('...','&#8230;')

def isNumber(n):
    if n and isinstance(n, basestring):
        if re.match("^[-+]?[0-9]+$", n):
            return True
        else:
            return False
    else:
        return False
