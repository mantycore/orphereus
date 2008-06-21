import os
import sys

from simpleparse import generator
from mx.TextTools import TextTools

class WakabaParser(object):
    def __init__(self, definition = 'wakabaparse/mark.def', baseProd = 'all'):
        self.plain  = ['safe_text','text','symbol','whitespace','strikedout','symbol_mark','symbol_mark_noa','symbol_mark_nou']
        self.simple = {'strong':'strong','emphasis':'em','strikeout':'del','block_code':'code'}
        self.complex= ['reference','signature','block_cite','block_list','link']
        self.input  = u''
        self.calledBy = None
        self.baseProd = baseProd
        self.defl = open(definition).read()
        self.parser = generator.buildParser(self.defl).parserbyname(baseProd)
        
    def PrintTree(self, Node, Depth):
        for tag, beg, end, parts in Node:
            print ''.ljust(Depth,"\t") + tag + '=' + self.input[beg:end]
            if parts:
                self.PrintTree(parts,Depth + 1)

    def link(self, tag, beg, end, parts):
        return '<a href="%s">%s</a>' % (self.input[beg:end],self.input[beg:end])
    def block_cite(self, tag, beg, end, parts):
        depth = 0
        n = 0
        result = '<blockquote>'
        for citeline, clbeg, clend, clparts in parts:
            if len(clparts) > 1:
                i = 1
                while clparts[i][0] == 'sub_cite':
                    i += 1
                i -= 1
            else:
                i = 0
            if i > depth:
                result += ('<blockquote>' * (i - depth))
                depth = i
            elif i < depth:
                result += ('</blockquote>' * (depth - i))
                depth = i
            elif n:
                result += '<br />'
            result += ('&gt; ' * (depth + 1)) + self.formatInHTML(clparts)
            n += 1
        result += ('</blockquote>' * (depth + 1)) 
        return result
   
    def block_list(self, tag, beg, end, parts):
        fNL = (parts[0][3][1][0] == 'numlist')
        if fNL:
            result = '<ol>'
        else:
            result = '<ul>'
        for citeline, clbeg, clend, clparts in parts:
            if fNL != (clparts[1][0] == 'numlist'):
                fNL = not fNL
                if fNL:
                    result += '</ul><ol>'
                else:
                    result += '</ol><ul>'
            result += '<li>' + self.formatInHTML(clparts) + '</li>'
        if fNL:
            result += '</ol>'
        else:
            result += '</ul>'
        return result

    def reference(self, tag, beg, end, parts):
        n,i,j,p = parts[0]
        number = self.input[i:j]
        pid = self.calledBy.getParentID(number)
        if pid == -1:
            pid = number
        if pid:
            return '<a href="%s#i%s">&gt;&gt;%s</a>' % (pid,number,number)
        else:
            return '&gt;&gt;%s' % number

    def signature(self, tag, beg, end, parts):
        valid = {} 
        result = ''
        for nn, i, j, p in parts:
            pid = self.calledBy.isPostOwner(self.input[i:j])
            if pid == -1:
                pid = self.input[i:j]
            if pid:
                valid[self.input[i:j]]=pid
        if valid:
            result = '<span class="signature">##'
            sep = ''
            for i in valid:
                result += sep + '<a href="%s#i%s">%s</a>' % (valid[i],i,i)
                sep = ','
            result += '</span>'
        return result
    def filterPlain(self, text):
    	return text.replace('<','&lt;').replace('>','&gt;')
    def formatInHTML(self, Nodes):
        result = ''
        fP = False
        fC = False
        for tag, beg, end, parts in Nodes:
            if tag in self.plain:
                result += self.filterPlain(self.input[beg:end])
            elif tag in self.simple and parts:
                result += '<' + self.simple[tag]+ '>' + self.formatInHTML(parts) + '</' + self.simple[tag]+ '>'
            elif tag in self.complex:
                if fP:
                    fP = False
                    result += '</p>'
                result += getattr(self,tag)(tag, beg, end, parts)
            elif tag == 'line':
                if fP and len(parts) > 1:
                    result += '<br />'
                elif len(parts) > 1:
                    fP = True
                    result += '<p>'
                elif fP:
                    fP = False
                    result += '</p>'
                result += self.formatInHTML(parts)
            elif tag == 'code':
                if fC:
                    result += '<br />'
                else:
                    fC = True
                result += self.formatInHTML(parts)
            elif tag == 'newline':
                result += "\r\n"
            elif parts:
                result += self.formatInHTML(parts)
        if fP:
            fP = False
            result += '</p>'
        return result

    def parseWakaba(self, message, o):
        self.input = "\n" + message
        self.calledBy = o
        taglist = TextTools.tag(self.input, self.parser)
        result = self.formatInHTML(taglist[1])
        return result

    def getTagList(self, message):
    	self.input = "\n" + message
    	taglist = TextTools.tag(self.input, self.parser)
    	return taglist
