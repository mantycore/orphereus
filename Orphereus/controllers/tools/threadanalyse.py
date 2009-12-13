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

import re, os
from tempfile import mkdtemp
from webhelpers.html.tags import link_to

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.lib.interfaces.AbstractPageHook import AbstractPageHook
from Orphereus.model import *

import logging
log = logging.getLogger(__name__)

from paste.script import command
from Orphereus.config.environment import load_environment
from paste.deploy import appconfig
from pylons import config

class AnalyseCommand(command.Command):
    max_args = 0
    min_args = 0

    usage = ""
    summary = "Build analyse graphs"
    group_name = "Orphereus"

    parser = command.Command.standard_parser(verbose = True)
    parser.add_option('--config',
                      action = 'store',
                      dest = 'config',
                      help = 'config name (e.g. "development.ini")')

    parser.add_option('--path',
                      action = 'store',
                      dest = 'path',
                      help = 'working dir (e.g. ".")')

    @staticmethod
    def setup_config(filename, relative_to):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[ANALYSE] %(asctime)s %(name)s:%(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        corelog = logging.getLogger("CORE")
        ormlog = logging.getLogger("ORM")
        corelog.addHandler(ch)
        ormlog.addHandler(ch)

        if not relative_to or not os.path.exists(relative_to):
            relative_to = "."
        print 'Loading config "%s" at path "%s"...' % (filename, relative_to)
        conf = appconfig('config:' + filename, relative_to = relative_to)
        load_environment(conf.global_conf, conf.local_conf, False)
        g._push_object(meta.globj) #zomg teh h4x

    def command(self):
        #devIni = self.args[0]
        self.setup_config(self.options.config, self.options.path)
        print "Saved to:", self.analyse([])[0]

    @staticmethod
    def analyse(postIds, algo = 'neato', opt = '-Kneato'): # algo = 'neato', opt='-Kneato' \\ algo = 'dot', opt = ''
        if not postIds:
            allThreads = meta.Session.query(Post.id).filter(Post.parentid == None).all()
            postIds = map(lambda x: x[0], allThreads)
        saveName = '%s.gv' % str(long(time.time() * 10 ** 7))
        savePath = os.path.join(meta.globj.OPT.uploadPath, 'save')
        saveTo = os.path.join(savePath, saveName)
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        f = open(saveTo, 'w+')
        header = """digraph Orphie {
ranksep=3;\n
ratio=auto;\n
overlap=false;\n
node [style=filled];
"""
        f.write(header)

        rex = re.compile(r'&gt;&gt;(\d+)')
        #def colorFor(post, postPos, postsCount):
        #    hexcolor = '#%02x%02x%02x' % (170, 170, 170 + (255 - 170) * postPos / postsCount)
        #    return hexcolor

        def gradient(start, end, length):
            __sr = int(start[0:2].upper(), 16) # 0
            __sg = int(start[2:4].upper(), 16) # 0
            __sb = int(start[4:6].upper(), 16) # 0
            __er = int(end[0:2].upper(), 16) # 255
            __eg = int(end[2:4].upper(), 16) # 255
            __eb = int(end[4:6].upper(), 16) # 255
            stepr = (__er - __sr) / (length - 1) # 63
            stepg = (__eg - __sg) / (length - 1) # 63
            stepb = (__eb - __sb) / (length - 1) # 63
            colors = [0] * length
            for i in range(0, length):
                if i == 0:
                    # first color
                    r = '%02X' % __sr
                    g = '%02X' % __sg
                    b = '%02X' % __sb
                elif i == length - 1:
                    # last color
                    r = '%02X' % __er
                    g = '%02X' % __eg
                    b = '%02X' % __eb
                else:
                    # middle color
                    r = '%02X' % (__sr + int(stepr) * i)
                    g = '%02X' % (__sg + int(stepg) * i)
                    b = '%02X' % (__sb + int(stepb) * i)

                colors[i] = r + g + b

            return colors

        for threadId in postIds:
            thread = Post.getPost(threadId)
            if not thread.parentid:
                f.write("node [shape=box, color=red];\n")
                f.write('"%d";\n' % thread.id)
                #f.write("node [shape=ellipse, color=lightblue2];\n")
                posts = Post.getThread(threadId)
                previd = None
                postsCount = len(posts)
                grad = gradient('995555', '5555ff', postsCount)
                for postPos, post in enumerate(posts):
                    if postPos == postsCount - 1:
                        f.write('node [shape=ellipse, color="blue"];\n')
                    else:
                        f.write('node [shape=ellipse, color="#%s"];\n' % grad[postPos])
                    if previd:
                        #f.write('"%d" -> "%d" [dir=none, color=green];\n' % (previd, post.id))
                        f.write('"%d" -> "%d" [color=green];\n' % (previd, post.id))
                    previd = post.id
                    links = re.findall(rex, post.message)
                    links = map(lambda x: int(x), links)
                    for link in links:
                        target = post.getPost(link)
                        if target:
                            if target.parentid == thread.id or target.id == thread.id:
                                f.write('"%d" -> "%d" [color=blue];\n' % (post.id, link))
                            elif target.parentid:
                                f.write('"%d" -> "%d" [color=red];\n' % (post.id, link))
                            else:
                                f.write("node [shape=box, color=lightblue2];\n")
                                f.write('"%d" -> "%d" [color=red];\n' % (post.id, link))
                                #f.write("node [shape=ellipse, color=lightblue2];\n")
                                #f.write('node [shape=ellipse, color="%s"];\n' % colorFor(post, postPos, postsCount))
        f.write('}')
        f.close()
        cmd = '%s -v %s -Tpng "%s" -o"%s.png"' % (algo, opt, saveTo, saveTo)
        print cmd
        os.system(cmd)
        return (saveTo, saveName + ".png")

class ThreadAnalysisPlugin(BasePlugin, AbstractPageHook):
    def __init__(self):
        config = {'name' : N_('Show thread as graph plugin'),
                  'deps' : ('base_view',)
                 }
        BasePlugin.__init__(self, 'threadanalyse', config)

    def entryPointsList(self):
        return [('graph', "AnalyseCommand"), ]

    # Implementing BasePlugin
    def initRoutes(self, map):
        map.connect('graphForThread', '/graph/{post}',
                     controller = 'tools/threadanalyse', action = 'graph',
                     requirements = dict(post = r'\d+'))

    # AbstractPageHook
    def threadPanelCallback(self, thread, userInst):
        return link_to(_("[Graph]"), h.url_for('graphForThread', post = thread.id), target = "_blank")

from Orphereus.controllers.OrphieBaseController import OrphieBaseController

class ThreadanalyseController(OrphieBaseController):
    def __init__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    #def __del__(self):
    #    shutil.rmtree(self.path, True)

    def graph(self, post):
        self.path = mkdtemp()
        self.tid = post
        filename = 'save/%s' % AnalyseCommand.analyse([int(post)])[1]
        return redirect_to(str('%s%s' % (meta.globj.OPT.filesPathWeb, filename)))

