# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Hedger                                                   #
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

import re

from Orphereus.lib.OrphieMark.InlineFormatting import parseInlineFormattingElements
from Orphereus.lib.OrphieMark.EntitiesFormatting import parseEntities
from Orphereus.lib.OrphieMark.tools import *

from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter

import logging
log = logging.getLogger(__name__)

class MessageElement(object):
    def format(self, level = 0, **kwargs):
        childrensData = ''
        for child in self.children:
            childrensData = "%s%s" % (childrensData, child.format(level + 1, **kwargs))
        return childrensData

class PlainText(MessageElement):
    def __init__(self, text):
        if (isinstance(text, list)):
            text = '\n'.join(text)
        self.text = text
        self.children = []

    def __repr__(self):
        return "<PlainText =%s>" % self.text

    def format(self, level, **kwargs):
        if kwargs.get('insideCode', False):
            return self.text # replaceEntities(self.text)
        return filterText(self.text)

class RootElement(MessageElement):
    def __init__(self):
        self.children = []

    def __repr__(self):
        return "<root>"

class MarkupElement(RootElement):
    def __init__(self, tag, paramString = ""):
        RootElement.__init__(self)
        self.tag = tag
        self.paramString = paramString

    def __repr__(self):
        return "<Tag=%s, params=%s>" % (str(self.tag), self.paramString)

    def format(self, level, **kwargs):
        childrensData = ''

        begin = "<div>"
        end = "</div>"
        itemize = False
        childrensKwargs = {}
        childrensKwargs.update(kwargs)
        if self.tag == '*':
            begin = '<div style="font-style: italic;">'
        elif self.tag == '**':
            begin = '<div style="font-weight: bold;">'
        elif self.tag == '__':
            begin = '<div style="text-decoration: underline;">'
        elif self.tag == '$$':
            begin = '<div style="text-decoration: line-through;">'
        elif self.tag == '%%':
            begin = '<div class="spoiler">'
        elif self.tag == '``':
            begin = '<div class="code">'
            end = '</div>'
            childrensKwargs['insideCode'] = True
        elif self.tag == r'\123':
            begin = '<ol>'
            end = '</ol>'
            itemize = True
        elif self.tag == r'\***':
            begin = '<ul>'
            end = '</ul>'
            itemize = True

        if itemize:
            for child in self.children:
                childrensData = "%s<li>%s</li>\n" % (childrensData, child.format(level + 1, insideList = True))
        else:
            for child in self.children:
                childrensData = "%s%s" % (childrensData, child.format(level + 1, **childrensKwargs))

        if childrensKwargs.get('insideCode', False):
            lexer = None
            lexersDict = {'=lua' : LuaLexer,
            '=perl' : PerlLexer,
            '=python' : PythonLexer,
            '=python3' : Python3Lexer,
            '=ruby' : RubyLexer,
            '=tcl' : TclLexer,
            '=c' : CLexer,
            '=cpp' : CppLexer,
            '=d' : DLexer,
            '=delphi' : DelphiLexer,
            '=fortran' : FortranLexer,
            '=java' : JavaLexer,
            '=objectivec' : ObjectiveCLexer,
            #'=scala' : ScalaLexer,
            #'=vala' : ValaLexer,
            '=csharp' : CSharpLexer,
            '=vbnet' : VbNetLexer,
            '=clisp' : CommonLispLexer,
            '=erlang' : ErlangLexer,
            '=haskell' : HaskellLexer,
            '=ocaml' : OcamlLexer,
            '=scheme' : SchemeLexer,
            '=bash' : BashLexer,
            '=mysql' : MySqlLexer,
            '=sql' : SqlLexer,
            '=ini' : IniLexer,
            '=tex' : TexLexer,
            '=html' : HtmlLexer,
            '=js' : JavascriptLexer,
            '=php' : PhpLexer,
            '=xml' : XmlLexer,
            }
            lexername = ''
            if self.paramString:
                lexername = self.paramString.lower()
            lexer = lexersDict.get(lexername, None)

            if lexer:
                lexer = lexer()
                childrensData = highlight(childrensData, lexer, HtmlFormatter(cssclass = "sourcecode", linenos = 'table'))
            else:
                childrensData = replaceEntities(childrensData) # Don't forget, PlainText returns unsafe strings inside code blocks!
                begin += '<pre>'
                end = '%s%s' % ('</pre>', end)

        return '%s%s%s' % (begin, childrensData, end)

class InlineMarkupElement(RootElement):
    def __init__(self, tag):
        RootElement.__init__(self)
        self.tag = tag

    def __repr__(self):
        return "<InlineTag=%s>" % (str(self.tag))

    def format(self, level, **kwargs):
        childrensData = ''

        begin = "<span>"
        end = "</span>"
        childrensKwargs = {}
        childrensKwargs.update(kwargs)
        if self.tag == '*':
            begin = '<span style="font-style: italic;">'
        elif self.tag == '**':
            begin = '<span style="font-weight: bold;">'
        elif self.tag == '__':
            begin = '<span style="text-decoration: underline;">'
        elif self.tag == '$$':
            begin = '<span style="text-decoration: line-through;">'
        elif self.tag == '%%':
            begin = '<span class="spoiler">'
        elif self.tag == '``':
            begin = '<span class="code"><pre>'
            end = '</pre></span>'
            childrensKwargs['insideCode'] = True

        for child in self.children:
            childrensData = "%s%s" % (childrensData, child.format(level + 1, **childrensKwargs))
        return '%s%s%s' % (begin, childrensData, end)

class LineWithEntities(RootElement):
    def __init__(self, text):
        RootElement.__init__(self)
        #self.text = text
        #print "input=" + text
        parseEntities(text, self)

    def __repr__(self):
        return "<LineWithEntities>"

class ComplexLine(RootElement):
    def __init__(self, input):
        RootElement.__init__(self)
        self.quoteLevel = 0
        self.parseComplexLine(input)

    def __repr__(self):
        return "<ComplexLine, quoteLevel=%d>" % (self.quoteLevel)

    def parseComplexLine(self, input):
        quoteLine = ''
        quoteRe = re.compile('^((>\s*)*)((>>\d+).*)$')
        matcher = quoteRe.match(input)
        if not matcher:
            quoteRe = re.compile('^((>\s*)+)(.*)$')
            matcher = quoteRe.match(input)
        if matcher:
            quoteLine = matcher.group(1)
            input = matcher.group(3)
            self.quoteLevel = quoteLine.count('>')

        delims = re.compile("(\*|\$\$|%%|__|``)")
        tokens = delims.split(input)
        tokens = filter(lambda token: token, tokens) #remove empty
        #print tokens

        def disambiguate(tokens):
            #print tokens
            ret = []
            inAmbig = False
            for token in tokens:
                if token != '*':
                    if inAmbig:
                        ret.append('*')
                    ret.append(token)
                    inAmbig = False
                else:
                    if inAmbig:
                        ret.append('**')
                        inAmbig = False
                    else:
                        inAmbig = True
            if inAmbig:
                ret.append('*')
            return ret

        tokens = disambiguate(tokens)
        #print ''.join(tokens) == input
        parseInlineFormattingElements(tokens, self)

    def format(self, level, **kwargs):
        childrensData = ''
        for child in self.children:
            childrensData += child.format(level + 1, **kwargs)
        if not self.children:
            childrensData = u'<br/>'
        begin = ''
        end = ''
        if not kwargs.get('insideList', False):
            begin = '<div class="textBlock">'
            end = '</div>'
            i = 0
            while i < self.quoteLevel:
                begin += '<blockquote>'
                end = "%s%s" % ("</blockquote>", end)
                i += 1
            if self.quoteLevel:
                begin += "&gt; " * self.quoteLevel
        return '%s%s%s' % (begin, childrensData, end)

class InlineEntity(RootElement):
    def __init__(self, entype, value):
        RootElement.__init__(self)
        self.entype = entype
        self.value = value

    def __repr__(self):
        return "<Entity=%s, params=%s>" % (str(self.entype), self.value)

    def formatLink(self, linkString, globj):
        linkHref = linkString
        trusted = False

        for trLink in self.globj.OPT.refControlList:
            if trLink in linkString:
                trusted = True
                break

        if not (trusted):
            linkHref = self.globj.OPT.obfuscator % {'url' : linkHref}

        return '<a href="%s" target="_blank">%s</a>' % (linkHref, linkString)

    def formatSignature(self, sigString):
        valid = {}
        invalid = {}
        unknown = {}
        result = u''
        log.debug(sigString)
        postIds = sigString.split(',')
        log.debug(postIds)
        for postId in postIds:
            info = self.callbackSource.cbGetPostAndUser(postId)
            post = info[0]
            uidNumber = info[1]
            if post:
                disablePL = (not self.globj.OPT.boardWideProoflabels) and \
                            (self.parentId == -1 or \
                            (post.parentid != self.parentId and post.id != self.parentId))
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
                retval += sep + self.callbackSource.formatPostReference(i, False)
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

    def format(self, level, **kwargs):
        self.callbackSource = kwargs.get('callbackSource', None)
        self.globj = kwargs.get('globj', None)
        self.parentId = kwargs.get('parentId', None)

        if self.entype == 'reference' and self.callbackSource:
            return self.callbackSource.formatPostReference(int(self.value))
        elif self.entype == 'prooflink':
            return self.formatSignature(self.value)
        elif self.entype == 'htmlchar':
            #TODO: check entities for existence
            return '&%s;' % self.value
        elif self.entype == 'htmlcode':
            #TODO: check entities for existence
            return '&#%s;' % self.value
        elif self.entype == 'url':
            closingStr = ''
            if self.value.endswith(')'):
                openedCount = 0
                for ch in self.value:
                    if ch == '(':
                        openedCount += 1
                    elif ch == ')':
                        openedCount -= 1
                if openedCount < 0:
                    while self.value.endswith(')') and openedCount < 0:
                        self.value = self.value[0:-1]
                        closingStr += ')'
                        openedCount += 1
            return "%s%s" % (self.formatLink(self.value, self.globj), closingStr)

