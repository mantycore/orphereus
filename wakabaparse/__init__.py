import os
import sys

from simpleparse import generator
from mx.TextTools import TextTools
from fc.lib.miscUtils import *
from fc.lib.constantValues import *

class WakabaParser(object):
    def __init__(self, definition = markupFile, baseProd = 'all'):
        self.plain  = ['safe_text','symbol','whitespace','strikedout','symbol_mark','symbol_mark_noa','symbol_mark_nou']
        self.simple = {'strong':'strong','emphasis':'em','strikeout':'del','inline_spoiler':"span class='spoiler'"}
        self.complex= ['reference','signature','link']
        self.block  = {'block_code':'code','block_spoiler':"div class='spoiler'"}
        self.line   = ['inline_full','text']
        self.mline  = ['block_cite','block_list']
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
        
    def reference(self, tag, beg, end, parts):
        n,i,j,p = parts[0]
        number = self.input[i:j]
        pid = self.calledBy.getParentID(number)
        if pid == -1:
            return '<a href="/%s">&gt;&gt;%s</a>' % (number,number)
        else:
            return '<a href="/%s#%s" onclick="highlight(%s)">&gt;&gt;%s</a>' % (pid,number,number,number)

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
                result += sep + '<a href="/%s#i%s">%s</a>' % (valid[i],i,i)
                sep = ','
            result += '</span>'
        return result

    def openTag(self, tag, quantity=1):
        tagName = tag.split()[0]
        for i in range(0,quantity):
            self.result += "<%s>" % tag
            self.tags.append(tagName)

    def closeTag(self,quantity=1):
        for i in range(0,quantity):
            tag = self.tags.pop()
            self.result += "</%s>" % tag

    def block_cite(self, tag, beg, end, parts):
        depth = 0
        n = 0
        self.openTag('blockquote')
        for citeline, clbeg, clend, clparts in parts:
            if len(clparts) > 1:
                i = 1
                while clparts[i][0] == 'sub_cite':
                    i += 1
                i -= 1
            else:
                i = 0
            if i > depth:
                self.openTag('blockquote',i - depth)
                depth = i
            elif i < depth:
                self.closeTag(depth - 1)
                depth = i
            elif n:
                self.result += '<br />'
            self.result += ('&gt; ' * (depth + 1))
            self.formatInHTML(clparts)
            n += 1
        self.closeTag(depth + 1)
        return ''
    def block_list(self, tag, beg, end, parts):
        fNL = (parts[0][3][1][0] == 'numlist')
        if fNL:
            self.openTag('ol')
        else:
            self.openTag('ul')
        for citeline, clbeg, clend, clparts in parts:
            if fNL != (clparts[1][0] == 'numlist'):
                fNL = not fNL
                if fNL:
                    self.closeTag()
                    self.openTag('ol')
                else:
                    self.closeTag()
                    self.openTag('ul')
            self.openTag('li')
            if clparts:
                self.formatInHTML(clparts)
            self.closeTag()
        self.closeTag()
        return ''
        
    def formatInHTML(self, Nodes):
        result = ''
        fP = False
        fC = False
        for tag, beg, end, parts in Nodes:
            if tag in self.plain:
                result += filterText(self.input[beg:end])
            elif tag in self.simple and parts:
                tagName = tag.split()[0]
                result += '<' + self.simple[tag]+ '>' + self.formatInHTML(parts) + '</' + self.simple[tagName]+ '>'
            elif tag in self.complex and parts:
                result += getattr(self,tag)(tag, beg, end, parts)

            elif tag in self.line:
                self.lines += 1
                if parts:
                    self.result += self.formatInHTML(parts)
                else:
                    self.result += filterText(self.input[beg:end])
                if not self.linesFlag and (self.lines > self.maxLines or len(self.result) > self.maxLen):
                    self.linesFlag = True
                    self.short = self.result
                    if self.tags:
                        for t in self.tags[::-1]:
                            self.short += "</%s>" % t
            elif tag in self.block:
                self.openTag(self.block[tag])
                if parts:
                    self.formatInHTML(parts)
                self.closeTag()
            elif tag in self.mline:
                if fP:
                    fP = False
                    self.result += '</p>'
                getattr(self,tag)(tag, beg, end, parts)
            elif tag == 'line' or tag == 'spoiler_line':
                if fP and len(parts) > 1:
                    self.result += '<br />'
                elif len(parts) > 1:
                    fP = True
                    self.result += '<p>'
                elif fP:
                    fP = False
                    self.result += '</p>'
                if parts:
                    self.formatInHTML(parts)
            elif tag == 'code':
                if fC:
                    self.result += '<br />'
                else:
                    fC = True
                self.formatInHTML(parts)
            elif tag == 'newline':
                self.result += "\r\n"
            elif parts:
                result += self.formatInHTML(parts)
        if fP:
            fP = False
            self.result += '</p>'
        return result

    def parseWakaba(self, message, o, lines=20, maxLen=5000):
        self.input = "\n" + message
        self.calledBy = o
        self.maxLines = lines
        self.maxLen = maxLen
        self.lines = 0
        self.linesFlag = False
        self.result = ''
        self.short = ''
        self.tags = []
        taglist = TextTools.tag(self.input, self.parser)
        result = self.formatInHTML(taglist[1])
        return (self.result,self.short)

    def getTagList(self, message):
    	self.input = "\n" + message
    	taglist = TextTools.tag(self.input, self.parser)
    	return taglist
