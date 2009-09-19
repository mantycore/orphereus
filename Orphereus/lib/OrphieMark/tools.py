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
               .replace('--', '&mdash;') \
               .replace('(tm)', '&#153;') \
               .replace('...', '&#8230;') \

def filterText(text):
    generateHighlightCSS('d:/highlight.css')
    return replaceAcromyns(replaceEntities(text))


