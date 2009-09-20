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

def parseInlineFormattingElements(tokens, topBlock):
  from Orphereus.lib.OrphieMark.MarkupHierarchy import LineWithEntities, PlainText, InlineMarkupElement
  tagDelimiters = ['%%', '``', '**', '*', '__', '$$']
  plainTextMode = False
  lineClass = LineWithEntities
  codeToken = "``"
  tagStack = []
  buffer = ""
  currentBlocks = [topBlock]
  #print tokens
  for token in tokens:
    if token in tagDelimiters and (not plainTextMode or token == codeToken):
      if not token in tagStack:
        tagStack.append(token)
        currentElement = currentBlocks[-1]

        if buffer:
          newElement = lineClass(buffer)
          currentElement.children.append(newElement)
          buffer = ""

        if token == codeToken:
          plainTextMode = True
          lineClass = PlainText

        newElement = InlineMarkupElement(token)
        currentElement.children.append(newElement)
        currentBlocks.append(newElement)
      else:
        while token in tagStack:
          tag = tagStack.pop()
        currentElement = currentBlocks.pop()

        if buffer:
          newElement = lineClass(buffer)
          currentElement.children.append(newElement)
          buffer = ""

        if token == codeToken:
          plainTextMode = False
          lineClass = LineWithEntities
        #currentElement = currentBlocks[-1]
    else:
      buffer += token
  if buffer:
    newElement = lineClass(buffer)
    topBlock.children.append(newElement)

  return topBlock
