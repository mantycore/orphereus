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
                   'prooflink' : re.compile('##((\d+)(,\d+)*)'),
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

