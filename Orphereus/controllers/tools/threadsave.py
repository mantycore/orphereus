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

import re, shutil, tarfile
from tempfile import mkdtemp

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.MenuItem import MenuItem
from Orphereus.lib.base import *
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

class UserTagsPlugin(BasePlugin, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('Thread saving pluging'),
                 }
        BasePlugin.__init__(self, 'threadsave', config)

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('saveThread', '/saveThread/:post', controller = 'tools/threadsave', action = 'save', requirements = dict(post = '\d+'))

    # AbstractPageHook
    def threadPanelCallback(self, thread, userInst):
        from webhelpers.html.tags import link_to
        return link_to(_("[Save]"), h.url_for('saveThread', post = thread.id), target = "_blank")

# this import MUST be placed after public definitions to avoid loop importing
from OrphieBaseController import OrphieBaseController

class ThreadsaveController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)
        self.initiate()
        
    def __del__(self):
        shutil.rmtree(self.path, True)

    def _prepareHtml(self, html):
        staticFiles = list(set(re.findall('%s([^"]+)"' % meta.globj.OPT.staticPathWeb, html)))
        staticFiles = map(lambda s: s.split('?')[0], staticFiles)
        dirs = list(set(map(lambda fn: (fn.find('/') > -1) and fn.split('/')[0] or '',  staticFiles)))
        dirs.append('files')
        html = re.sub('%s([^"]+)"' % meta.globj.OPT.staticPathWeb, r'\1"', html)
        
        postFiles = list(set(re.findall('%s([^"]+)"' % meta.globj.OPT.filesPathWeb, html)))
        html = re.sub('%s[^"]+/([^"]+)"' % meta.globj.OPT.filesPathWeb, r'files/\1"', html)
        
        #html = re.sub('f="/\d+(#i\d+)', r'f="\1', html)
        map(lambda dir: dir and os.mkdir('%s/%s' %(self.path, dir)), dirs)
        map(lambda fn: shutil.copyfile('%s/%s' %(meta.globj.OPT.staticPath, fn), '%s/%s' %(self.path, fn)) , staticFiles)
        map(lambda fn: shutil.copyfile('%s/%s' %(meta.globj.OPT.uploadPath, fn), '%s/files/%s' %(self.path, os.path.basename(fn))), postFiles)
        return html
    
    def loadThread(self):
        try:
            thread = Post.buildThreadFilter(self.userInst, self.tid).one()
        except:
            return self.error(_(u"Post not found."))
        thread.hideFromBoards = False
        thread.hidden = thread.hideFromBoards
        thread.Replies = thread.filterReplies().all()
        thread.omittedPosts = 0
        tagDescr = Post.tagLine(thread.tags)
        c.boardName = tagDescr[1]
        c.tagLine = tagDescr[0]
        c.count = 1
        c.threads = [thread]
        c.currentUserCanPost = False
        c.disableMenu = True
        page = self.render('posts')
        page = self._prepareHtml(page)
        f = open('%s/%s.htm' % (self.path, self.tid), 'w')
        f.write(page)
        f.close()
        return redirect_to(str('%ssave/%s' % (meta.globj.OPT.filesPathWeb, self.compress())))

    def compress(self):
        files = os.listdir(self.path)
        os.chdir(self.path)
        mark = (self.userInst.Anonymous and 0) or (str(self.userInst.secid())*4)[-4:]
        arcName = '%s.%s.tar.gz' % (self.tid, mark)
        arcPath = '%s/save/' % meta.globj.OPT.uploadPath
        tar = tarfile.open(arcName, 'w:gz')
        for file in files:
            tar.add(file)
        tar.close()
        if not(os.path.exists(arcPath)):
            os.makedirs(arcPath)
        shutil.move(arcName, arcPath)
        return arcName
    
    def save(self, post):
        self.path = mkdtemp()
        self.tid = post
        return self.loadThread()