import re

from Orphereus.lib.OrphieMark.MarkupHierarchy import RootElement, ComplexLine, MarkupElement, PlainText

def processChildren(buffer, blockClass, currentElement):
  if buffer:
    if blockClass:
      newElement = blockClass(buffer)
      currentElement.children.append(newElement)
    else:
      currentElement.children.extend(map(lambda line: ComplexLine(line), buffer))
    buffer = []
  return buffer

def  parseBlockFormattingElements(input):
  itemizers = [r"\123", r"\***"]
  tagDelimiters = ['%%', '``', '**', '*', '__', '$$']
  tagDelimiters.extend(itemizers)
  tagRegex = {
              '``' : re.compile("``(=\w+){0,1}")
             }
  plainTextMode = False
  blockClass = None
  codeToken = "``"
  lines = input.splitlines()
  lines = map(lambda line: line.rstrip(), lines)
  tagStack = []
  buffer = []
  topBlock = RootElement()
  currentBlocks = [topBlock]
  currentElement = topBlock

  for line in lines:
    #print ">> " + line
    tokenWithParams = False
    lineIsToken = line in tagDelimiters
    token = line
    if not lineIsToken:
      token = line[0:2]
      tokenWithParams = (token in tagDelimiters and  token in tagRegex.keys() and tagRegex[token].match(line))

    if (lineIsToken or tokenWithParams) and (not plainTextMode or token == codeToken):
      if not token in tagStack:
        tagStack.append(token)
        currentElement = currentBlocks[-1]

        buffer = processChildren(buffer, blockClass, currentElement)
        if token == codeToken:
          plainTextMode = True
          blockClass = PlainText

        params = None
        if token != line:
          params = line[len(token):]
        newElement = MarkupElement(token, params)

        newElement.params = line

        currentElement.children.append(newElement)
        currentBlocks.append(newElement)
      else:
        while token in tagStack:
          tag = tagStack.pop()
        currentElement = currentBlocks.pop()

        buffer = processChildren(buffer, blockClass, currentElement)

        if token == codeToken:
          plainTextMode = False
          blockClass = None
    else:
      if len(line) > 0 or (buffer and len(buffer[-1]) > 0): #ignore more than 1 empty lines, also ignore first empty line # or not buffer:
        buffer.append(line)

  buffer = processChildren(buffer, blockClass, currentElement)
  return topBlock
