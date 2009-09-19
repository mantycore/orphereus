import re

from Orphereus.lib.OrphieMark.InlineFormatting import parseInlineFormattingElements
from Orphereus.lib.OrphieMark.EntitiesFormatting import parseEntities
from Orphereus.lib.OrphieMark.tools import *

from pygments import highlight
from pygments.lexers import PythonLexer
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
            if self.paramString and self.paramString.lower() == "=python":
                lexer = PythonLexer()
            if lexer:
                childrensData = highlight(childrensData, lexer, HtmlFormatter(cssclass = "sourcecode"))
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
        #print
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
            #print ret
            return ret

        tokens = disambiguate(tokens)
        #print ''.join(tokens) == input
        #print
        parseInlineFormattingElements(tokens, self)

    def format(self, level, **kwargs):
        childrensData = ''
        for child in self.children:
            childrensData += child.format(level + 1, **kwargs)
        begin = ''
        end = ''
        if not kwargs.get('insideList', False):
            begin = '<div class="textBlock">'
            end = '</div>'
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
        #for nn, i, j, p in parts:
        for postId in postIds:
            #postId = self.input[i:j]
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
        #log.debug(kwargs)
        self.globj = kwargs.get('globj', None)
        self.parentId = kwargs.get('parentId', None)

        if self.entype == 'reference' and self.callbackSource:
            return self.callbackSource.formatPostReference(int(self.value))
        elif self.entype == 'prooflink':
            return self.formatSignature(self.value) #'<a href="link">prooflink</a>'
        elif self.entype == 'htmlchar':
            #TODO: check entities for existence
            return '&%s;' % self.value
        elif self.entype == 'htmlcode':
            #TODO: check entities for existence
            return '&#%s;' % self.value
        elif self.entype == 'url':
            if self.value.startswith('(') and self.value.endswith(')'):
                self.value = self.value[1:-1]
            return self.formatLink(self.value)
#            return '<a href="%s" target="_blank">%s</a>' % (self.value, self.value)
