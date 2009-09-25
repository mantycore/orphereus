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

__PLAINTEXTID = 'plaintext'

def tokenizeInput(input, rules, level = 0):
  if not rules:
    return []

  entitiesList = []
  lastEnd = 0
  strEnd = ''
  val = rules[0]
  deltaList = rules[1:]

  tokenid = val[0]
  regex = val[1]
  for ent in regex.finditer(input):
    start = ent.start(0)
    end = ent.end(0)
    strBefore = input[lastEnd:start]
    down = tokenizeInput(strBefore, deltaList, level + 1)
    if down:
      entitiesList.extend(down)
    else:
      entitiesList.append((__PLAINTEXTID, strBefore))
    strCurrent = input[start : end]
    entitiesList.append((tokenid, regex.match(strCurrent).group(1)))
    lastEnd = end
  if lastEnd != len(input):
    strEnd = input[lastEnd:]
    down = tokenizeInput(strEnd, deltaList, level + 1)
    if down:
      entitiesList.extend(down)
    else:
      entitiesList.append((__PLAINTEXTID, strEnd))
  return entitiesList

def parseEntities(input, topBlock):
  from Orphereus.lib.OrphieMark.MarkupHierarchy import PlainText, InlineEntity
  entitiesRegexps = {'reference' : re.compile('>>(\d+)'),
                   'prooflink' : re.compile('##((\d+|(op))(,(\d+|(op)))*)'),
                   'htmlchar' : re.compile('&(\w+);'),
                   'htmlcode' : re.compile('&#(\d+);'),
                   'url' : re.compile(r"(\b(http|https)://([-A-Za-z0-9+&@#/%?=~_()|!:,.;]*[-A-Za-z0-9+&@#/%=~_()|]))"),
      }

  rules = []
  for key in entitiesRegexps.keys():
    rules.append((key, entitiesRegexps[key]))
  result = tokenizeInput(input, rules)
  #print result
  for token in result:
    tokenid = token[0]
    tokenval = token[1]
    if tokenid == __PLAINTEXTID:
      topBlock.children.append(PlainText(tokenval))
    else:
      topBlock.children.append(InlineEntity(tokenid, tokenval))
  #print ''.join(result) == input
  return True

