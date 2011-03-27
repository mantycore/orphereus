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

from html5lib.html5parser import HTMLParser
from html5lib import treebuilders, treewalkers, serializer
from lxml import etree

#todo: write plugin to regenerate, backgrounds
def codeHighlightCss(background):
    from pygments.formatters import HtmlFormatter
    return HtmlFormatter().get_style_defs('.sourcecode')

def generateHighlightCSS(path, background = None):
    f = open(path, 'w')
    f.write(codeHighlightCss(background))
    f.close()

def fixHtml(html):
    p = HTMLParser()
    return ''.join([token.toxml() for token in p.parseFragment(html).childNodes])

def replaceEntities(text):
    return text.replace('&', '&amp;') \
               .replace('<', '&lt;') \
               .replace('>', '&gt;') \
               .replace("'", '&#39;') \
               .replace('"', '&quot;')

def replaceAcromyns(text):
    return text.replace('(c)', '&copy;') \
               .replace(' -- ', ' &mdash; ') \
               .replace('(tm)', '&#153;') \
               .replace('... ', '&#8230; ') \

def filterText(text):
    return replaceAcromyns(replaceEntities(text))

def processItem(node, sentinel, level = 0):
    def processText(text, sentinel):
        if text:
            if sentinel.slen < sentinel.maxlen:
                delta = sentinel.maxlen - sentinel.slen
                if len(text) > delta:
                    text = u"%s…" % text[:delta]
                sentinel.slen += len(text)
            else:
                text = ''
        return text

    node.text = processText(node.text, sentinel)

    subs = node.getchildren()
    for subitem in subs:
        if not sentinel.stop:
            processItem(subitem, sentinel, level + 1)
        else:
            node.remove(subitem)

    node.tail = processText(node.tail, sentinel)

"""
#python 2.6 only
class Sentinel(object):
    def __init__(self, maxlen):
        self.maxlen = maxlen
        self._slen = 0

    @property
    def stop(self):
        return self.maxlen <= self.slen

    @property
    def slen(self):
        return self._slen

    @slen.setter
    def slen(self, slen):
        self._slen = slen
"""

class Sentinel(object):
    def __init__(self, maxlen):
        self.maxlen = maxlen
        self._slen = 0

    def stopGet(self):
        return self.maxlen <= self.slen

    def slenGet(self):
        return self._slen

    def slenSet(self, slen):
        self._slen = slen
    slen = property(fget = slenGet, fset = slenSet)
    stop = property(fget = stopGet)

def cutHtml(text, max_len):
    parser = HTMLParser(tree = treebuilders.getTreeBuilder("lxml"))
    etree_document = parser.parse(text)
    sentinel = Sentinel(max_len)
    processItem(etree_document.getroot(), sentinel)

    if sentinel.stop:
        walker = treewalkers.getTreeWalker("lxml")
        stream = walker(etree_document.getroot().getchildren()[1])
        s = serializer.htmlserializer.HTMLSerializer(omit_optional_tags = False)
        output_generator = s.serialize(stream)

        output = []
        for item in output_generator:
            output.append(item)
        output = output[1:-1] # remove <body></body>
        return ''.join(output)
    return None
