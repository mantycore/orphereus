from Orphereus.lib.OrphieMark.BlockFormatting import parseBlockFormattingElements

import logging
log = logging.getLogger(__name__)

def printTree(root, level = 0):
    shift = "  " * level

    print "%s%s" % (shift, str(root))
    for item in root.children:
        printTree(item, level + 1)

class OrphieParser(object):
    def __init__(self, globj, callbackSource):
        self.globj = globj
        self.callbackSource = callbackSource
        #log.debug(self.callbackSource)

    def parseMessage(self, messageText, parentId, maxLines, maxLen):
        rootElement = parseBlockFormattingElements(messageText)
        fullMessage = rootElement.format(callbackSource = self.callbackSource,
                                  globj = self.globj,
                                  parentId = parentId)
        return (fullMessage, None)
