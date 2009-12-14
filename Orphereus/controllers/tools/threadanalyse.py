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
    def analyse(postIds, **kwargs): # algo = 'neato', opt='-Kneato' \\ algo = 'dot', opt = ''
        algo = kwargs.get('algo', 'neato')
        opt = kwargs.get('opt', '-Kneato')
        showThreadLines = kwargs.get('showThreadLines', True)
        format = kwargs.get('format', 'png')
        if not format in ['svg', 'png', 'jpg', 'gif']:
            format = 'png'

        if not postIds:
            allThreads = meta.Session.query(Post.id).filter(Post.parentid == None).all()
            postIds = map(lambda x: x[0], allThreads)
        gvName = '%s.gv' % str(long(time.time() * 10 ** 7))
        savePath = os.path.join(meta.globj.OPT.uploadPath, 'save')
        writeGvTo = os.path.join(savePath, gvName)
        if not os.path.exists(savePath):
            os.mkdir(savePath)
        f = open(writeGvTo, 'w+')
        #overlap=false;\n model=circuit;
        header = """digraph Orphie {
ranksep=3;\n
ratio=auto;\n
pack=true;\n
overlap=orthoxy;\n
node [style=filled];
"""
        f.write(header)

        rex = re.compile(r'&gt;&gt;(\d+)')
        def colorFor(post, postPos, postsCount):
            hexcolor = '#0900c1%02x' % (40 + ((255 - 40) * postPos / postsCount))
            return hexcolor


        for threadId in postIds:
            thread = Post.getPost(threadId)
            if not thread.parentid:
                f.write('node [shape=doublecircle, color="green"];\n')
                f.write('"%d";\n' % thread.id)
                #f.write("node [shape=ellipse, color=lightblue2];\n")
                posts = Post.getThread(threadId)
                previd = None
                postsCount = len(posts)
                #grad = gradient('3000b9', 'b90000', postsCount)
                for postPos, post in enumerate(posts):
                    if postPos == postsCount - 1:
                        f.write('node [shape=circle, color="red"];\n')
                    else:
                        f.write('node [shape=box, color="%s"];\n' % colorFor(post, postPos, postsCount))
                    if previd and showThreadLines:
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

        picturePath = "%s.%s" % (writeGvTo, format)
        pictureName = "%s.%s" % (gvName, format)
        cmd = '%s -v %s -T%s "%s" -o"%s"' % (algo, opt, format, writeGvTo, picturePath)
        log.debug(cmd)
        os.system(cmd)
        if os.path.exists(picturePath):
            return (picturePath, pictureName)
        else:
            log.error("Can't create graph: <%s>, <%s>" % (cmd, picturePath))
            return (writeGvTo, gvName)

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
    def __before__(self):
        OrphieBaseController.__before__(self)
        self.initiate()

    #def __del__(self):
    #    shutil.rmtree(self.path, True)

    def graph(self, post):
        self.path = mkdtemp()
        self.tid = post
        c.postId = post
        if 'proceed' in request.POST:
            showThreadLines = bool(request.POST.get('showThreadLines', False))
            format = filterText(request.POST.get('format', 'png')).strip()
            format = format[:3] # excessive restrictions applied because this string will be sent to commandline
            if not re.compile("^\w+$").match(format):
                format = 'png'
            filename = 'save/%s' % AnalyseCommand.analyse([int(post)], format = format, showThreadLines = showThreadLines)[1]
            return redirect_to(str('%s%s' % (meta.globj.OPT.filesPathWeb, filename)))
        return self.render('threadgraph')
