################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
#  < anoma.team@gmail.com ; http://orphereus.anoma.ch >                        #
#                                                                              #
#  This file is part of Orphereus, an imageboard engine.                       #
#                                                                              #
#  This program is free software; you can redistribute it and/or               #
#  modify it under the terms of the GNU General Public License                 #
#  as published by the Free Software Foundation; either version 2              #
#  of the License, or (at your option) any later version.                      #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program; if not, write to the Free Software                 #
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
################################################################################

import os
import sys

from simpleparse import generator
from mx.TextTools import TextTools
from Orphereus.lib.miscUtils import *
from Orphereus.lib.constantValues import *
import re
from urllib import quote
from html5lib.html5parser import HTMLParser

import logging
log = logging.getLogger(__name__)

def fixHtml(html):
    p = HTMLParser()
    return ''.join([token.toxml() for token in p.parseFragment(html).childNodes])

class WakabaParser(object):
    def __init__(self, optHolder, replyingId = -1, baseProd = 'all'):
        self.plain = ['safe_text', 'symbol', 'whitespace', 'strikedout', 'symbol_mark', 'symbol_mark_noa', 'symbol_mark_nop', 'symbol_mark_nou', 'accent_code', 'noaccent_code', 'punctuation']
        self.simple = {'strong':'strong', 'emphasis':'em', 'strikeout':'del', 'inline_spoiler':'span class="spoiler"', 'inline_code':'code'}
        self.complex = ['reference', 'signature', 'link']
        self.block = {'block_code':'code', 'block_spoiler':'div class="spoiler"'}
        self.line = ['inline_full', 'text']
        self.mline = ['block_cite', 'block_list']
        self.input = u''
        self.calledBy = None
        self.baseProd = baseProd
        self.defl = open(optHolder.markupFile).read()
        self.replyingId = replyingId
        self.boardWideProoflabels = optHolder.boardWideProoflabels

        self.parser = generator.buildParser(self.defl).parserbyname(baseProd)

    def PrintTree(self, Node, Depth):
        for tag, beg, end, parts in Node:
            print ''.ljust(Depth, "\t") + tag + '=' + self.input[beg:end]
            if parts:
                self.PrintTree(parts, Depth + 1)

    def link(self, tag, beg, end, parts):
        linkString = self.input[beg:end]
        linkHref = linkString
        trusted = False

        for trLink in g.OPT.refControlList:
            if trLink in linkString:
                trusted = True
                break

        if not (trusted):
            linkHref = g.OPT.obfuscator % {'url' : linkHref}

        return '<a href="%s">%s</a>' % (linkHref, linkString)

    def reference(self, tag, beg, end, parts):
        n, i, j, p = parts[0]
        number = self.input[i:j]
        return self.calledBy.formatPostReference(number)

    def signature(self, tag, beg, end, parts):
        valid = {}
        invalid = {}
        unknown = {}
        result = u''
        for nn, i, j, p in parts:
            postId = self.input[i:j]
            info = self.calledBy.cbGetPostAndUser(postId) #self.calledBy.isPostOwner(self.input[i:j])
            post = info[0]
            uidNumber = info[1]
            if post:
                disablePL = (not self.boardWideProoflabels) and \
                            (self.replyingId == -1 or \
                            (post.parentid != self.replyingId and post.id != self.replyingId))
                if post.uidNumber < 1 or uidNumber < 1 or disablePL:
                    unknown[postId] = post.id
                elif post.uidNumber == uidNumber:
                    valid[postId] = post.id
                else:
                    invalid[postId] = post.id

        def addSpan(className, idList, result):
            retval = u''
            if result:
                retval += ","
                retval += '<span class="%s">' % className
            else:
                retval += '<span class="%s">##' % className
            sep = u''
            for i in idList:
                retval += sep + self.calledBy.formatPostReference(i, False)
                sep = ','
            retval += '</span>'
            return retval

        if invalid:
            result += addSpan("badsignature", invalid, result)
        if valid:
            result += addSpan("signature", valid, result)
        if unknown:
            result += addSpan("nonsignature", unknown, result)
        return result

    def openTag(self, tag, quantity = 1):
        tagName = tag.split()[0]
        for i in range(0, quantity):
            self.result += "<%s>" % tag
            self.tags.append(tagName)

    def fixCloseTag(self, tag):
        ret = tag
        retest = re.compile("^(\w+)\s+.*$")
        reret = retest.match(ret)
        if reret:
            ret = reret.group(1)
        return ret

    def closeTag(self, quantity = 1):
        for i in range(0, quantity):
            tag = self.tags.pop()
            tag = self.fixCloseTag(tag)
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
                self.openTag('blockquote', i - depth)
                depth = i
            elif i < depth:
                self.closeTag(depth - i)
                depth = i
            elif n:
                self.result += '<br />'
            self.result += ('&gt; ' * (depth + 1))
            self.formatInHTML(clparts)
            n += 1
        self.closeTag(depth + 1)
        return u''

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
        return u''

    def formatInHTML(self, Nodes):
        result = u''
        fP = False
        fC = False
        for tag, beg, end, parts in Nodes:
            if tag in self.plain:
                #result += filterText(self.input[beg:end])
                result += self.input[beg:end]
            elif tag in self.simple and parts:
                tagName = tag.split()[0]
                result += '<%s>%s' % (self.simple[tag], self.formatInHTML(parts))
                result += '</' + self.fixCloseTag(self.simple[tagName]) + '>'
            elif tag in self.complex:
                result += getattr(self, tag)(tag, beg, end, parts)

            elif tag in self.line:
                self.lines += 1
                if parts:
                    self.result += self.formatInHTML(parts)
                else:
                    #self.result += filterText(self.input[beg:end])
                    self.result += self.input[beg:end]
                if not self.linesFlag and (self.lines > self.maxLines or len(self.result) > self.maxLen):
                    self.linesFlag = True
                    self.short = self.result
                    self.linesCutted = self.lines
                    if self.tags:
                        for t in self.tags[::-1]:
                            self.short += "</%s>" % self.fixCloseTag(t)
            elif tag in self.block:
                self.openTag(self.block[tag])
                if parts:
                    self.formatInHTML(parts)
                self.closeTag()
            elif tag in self.mline:
                if fP:
                    fP = False
                    self.result += '</p>'
                getattr(self, tag)(tag, beg, end, parts)
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

    def parseWakaba(self, message, o, lines = 20, maxLen = 5000):
        self.input = "\n" + message + "\n"
        self.calledBy = o
        self.maxLines = lines
        self.maxLinesTolerance = 2
        self.maxLen = maxLen
        self.lines = 0
        self.linesCutted = 0
        self.linesFlag = False
        self.result = u''
        self.short = u''
        self.tags = []
        taglist = TextTools.tag(self.input, self.parser)
        result = self.formatInHTML(taglist[1])
        if self.short and ((self.linesCutted + self.maxLinesTolerance) >= self.lines):
            self.short = u''

        self.result = fixHtml(self.result)
        #XXX: TODO: very dirty fix
        if self.short:
            self.short = fixHtml(self.short)
        return (self.result, self.short)

    def getTagList(self, message):
        self.input = "\n" + message + "\n"
        taglist = TextTools.tag(self.input, self.parser)
        return taglist
