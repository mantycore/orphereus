import os
import sys

from simpleparse import generator
from mx.TextTools import TextTools

def PrintTree(Node,Depth):
   for tag, beg, end, parts in Node:
      print ''.ljust(Depth,"\t") + tag + '=' + input[beg:end]
      if parts:
         PrintTree(parts,Depth + 1)

plain  = ['safe_text','text','symbol','whitespace','strikedout']
simple = {'strong':'strong','emphasis':'em','strikeout':'del','block_code':'code'}
complex= ['reference','signature','block_cite','block_list']

input = u''
calledBy = ''

def block_cite(tag, beg, end, parts):
   depth = 0
   n = 0
   result = '<blockquote>'
   for citeline, clbeg, clend, clparts in parts:
      if len(clparts) > 1:
         i = 1
         while clparts[i][0] == 'sub_cite':
            i += 1
         i -= 1
      else:
         i = 0
      if i > depth:
         result += ('<blockquote>' * (i - depth))
         depth = i
      elif i < depth:
         result += ('</blockquote>' * (depth - i))
         depth = i
      elif n:
         result += '<br />'
      result += ('&gt; ' * (depth + 1)) + formatInHTML(clparts)
      n += 1
   result += ('</blockquote>' * (depth + 1)) 
   return result
   
def block_list(tag, beg, end, parts):
   fNL = (parts[0][3][1][0] == 'numlist')
   if fNL:
      result = '<ol>'
   else:
      result = '<ul>'
   for citeline, clbeg, clend, clparts in parts:
      if fNL != (clparts[1][0] == 'numlist'):
         fNL = not fNL
         if fNL:
            result += '</ul><ol>'
         else:
            result += '</ol><ul>'
      result += '<li>' + formatInHTML(clparts) + '</li>'
   if fNL:
      result += '</ol>'
   else:
      result += '</ul>'
   return result

def reference(tag, beg, end, parts):
   n,i,j,p = parts[0]
   number = input[i:j]
   pid = calledBy.getParentID(number)
   if pid == -1:
      pid = number
   if pid:
      return '<a href="%s#i%s">&gt;&gt;%s</a>' % (pid,number,number)
   else:
      return '&gt;&gt;%s' % number

def signature(tag, beg, end, parts):
   valid = {}
   result = ''
   for nn, i, j, p in parts:
      pid = calledBy.isPostOwner(input[i:j])
      if pid == -1:
         pid = input[i:j]
      if pid:
         valid[input[i:j]]=pid
   if valid:
      result = '<span class="signature">##'
      sep = ''
      for i in valid:
         result += sep + '<a href="%s#i%s">%s</a>' % (valid[i],i,i)
         sep = ','
      result += '</span>'
   return result

def formatInHTML(Nodes):
   result = ''
   fP = False
   fC = False
   for tag, beg, end, parts in Nodes:
      if tag in plain:
         result += input[beg:end]
      elif tag in simple and parts:
         result += '<' + simple[tag]+ '>' + formatInHTML(parts) + '</' + simple[tag]+ '>'
      elif tag in complex:
         if fP:
            fP = False
            result += '</p>'
         result += globals()[tag](tag, beg, end, parts)
      elif tag == 'line':
         if fP and len(parts) > 1:
            result += '<br />'
         elif len(parts) > 1:
            fP = True
            result += '<p>'
         elif fP:
            fP = False
            result += '</p>'
         result += formatInHTML(parts)
      elif tag == 'code':
         if fC:
            result += '<br />'
         else:
            fC = True
         result += formatInHTML(parts)
      elif tag == 'newline':
         result += "\r\n"
      elif parts:
         result += formatInHTML(parts)
   if fP:
      fP = False
      result += '</p>'                                    
   return result

def parseWakaba(message,o):
   globals()['input'] = "\n" + message
   globals()['calledBy'] = o
   decl = open('wakabaparse/mark.def').read()
   parser = generator.buildParser(decl).parserbyname('all')
   taglist = TextTools.tag(globals()['input'], parser)
   result = formatInHTML(taglist[1])
   return result
