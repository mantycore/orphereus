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

        params = None
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
    else:
      buffer += token
  if buffer:
    newElement = lineClass(buffer)
    topBlock.children.append(newElement)

  return topBlock
