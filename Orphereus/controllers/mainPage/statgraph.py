# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2009 Johan Liebert, Mantycore, Hedger, Rusanon                #
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

from pylons.i18n import N_
from string import *
from array import array
from beaker.cache import CacheManager
from Orphereus.model.Picture import Picture
import datetime
import urllib2
import re
import tempfile
import sqlalchemy as sa
from sqlalchemy.sql import and_, or_, not_

from Orphereus.lib.BasePlugin import BasePlugin
from Orphereus.lib.base import *
from Orphereus.lib.constantValues import CFG_BOOL, CFG_INT, CFG_STRING, CFG_LIST
from Orphereus.model import *
from Orphereus.lib.interfaces.AbstractHomeExtension import AbstractHomeExtension

import logging
_log = logging.getLogger(__name__)

from paste.script import command
from Orphereus.config.environment import load_environment
from paste.deploy import appconfig
from pylons import config

class GraphsCommand(command.Command):
    graphsToShow = ["stat_posts_pd", "stat_posts_total", "stat_users_pd"]
    max_args = 0
    min_args = 0

    usage = ""
    summary = "Build stat graphs"
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

    parser.add_option('--onlypreparedata',
                      action = 'store_true',
                      dest = 'preparedata',
                      default = False,
                      help = 'prepare statistical data')

    parser.add_option('--solar',
                      action = 'store_true',
                      dest = 'solar',
                      default = False,
                      help = 'prepare statistical data')

    @staticmethod
    def setup_config(filename, relative_to):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[GRAPHS] %(asctime)s %(name)s:%(levelname)s: %(message)s")
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

    def plotStdGraph(self, xsvals, ysvals, name, header, labels):
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib import rc
        from matplotlib.dates import date2num

        header = "%s\n%s" % (header, h.tsFormat(datetime.datetime.now()))
        maincolor = "#6c6c6c"
        linecolor = "#2f3f3f"
        rc('axes', edgecolor = maincolor)
        fig = plt.figure(1)
        fig.patch.set_alpha(0.0)
        plt.suptitle(header)
        ax = fig.add_subplot(1, 1, 1) 
        ax.axes.grid(color = maincolor)
        colors = [linecolor, 'b', 'r', 'g', 'm', 'y']
        for dataset, linecolor in zip(ysvals, colors):
            line = plt.plot_date(xsvals, dataset, '-', color = linecolor, linewidth = 1)
        plt.grid(True)
        fig.autofmt_xdate()
        if labels:
            legend = plt.legend(labels, labelspacing = 0.1) #loc=(0.9, .95),
            plt.setp(legend.get_texts(), fontsize = 'small')

        imgdata = StringIO.StringIO()
        plt.savefig(imgdata, format = 'png')
        plt.close()
        imgdata.seek(0)
        out = imgdata.getvalue()
        path = os.path.join(g.OPT.staticPath, "%s.png" % name)
        print "Created:", path
        f = open(path, "wb+")
        f.write(out)
        f.close()
        Picture.makeThumbnail(path, os.path.join(g.OPT.staticPath, "%ss.png" % name), (200, 200))

        
    def plotMultiGraph(self, xsvals, ysvals, name, header, labels):
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib import rc
        from matplotlib.dates import date2num
        import matplotlib.font_manager as font_manager

        header = "%s\n%s" % (header, h.tsFormat(datetime.datetime.now()))
        maincolor = "#6c6c6c"
        linecolor = "#2f3f3f"
        #rc('xtick', labelsize = 12, color = 'white', direction = 'out') # x tick labels
        #rc('lines', lw = 0.5, color = maincolor) # thicker black lines
        #rc('grid', c = maincolor, lw = 0.5) # solid gray grid lines
        #rc('text', color = maincolor)
        rc('axes', edgecolor = maincolor, grid = True)
        plt.rc('grid', color = '0.75', linestyle = '-', linewidth = 0.5)

        #rc('xtick', color = maincolor)
        #rc('ytick', color = maincolor)

        fig = plt.figure(1)
        fig.set_size_inches(9, 6)
        fig.patch.set_alpha(0.0)
        plt.suptitle(header) # color = maincolor)
        #ax = fig.add_subplot(1, 1, 1) #, axisbg = "#E2E0A7")
        left, width = 0.1, 0.8
        rect1 = [left, 0.7, width, 0.2]
        rect2 = [left, 0.3, width, 0.4]
        rect3 = [left, 0.1, width, 0.2]
        ax1 = fig.add_axes(rect1)
        ax2 = fig.add_axes(rect2, sharex = ax1)
        ax3 = fig.add_axes(rect3, sharex = ax1)

        assert len(ysvals) == 5
        ax = [ax2,
              ax2,
              ax1,
              ax3,
              ax3]
        #ax.axes.grid(color = maincolor)
        #ax.set_yscale('log')
        colors = [linecolor, 'b', 'r', 'g', 'm', 'y']
        for dataset, linecolor, axc, label in zip(ysvals, colors, ax, labels):
            line = axc.plot_date(xsvals, dataset, '-', color = linecolor, linewidth = 1, label = label)

        for ax in ax1, ax2, ax3:
            if ax != ax3:
                for label in ax.get_xticklabels():
                    label.set_visible(False)
            else:
                for label in ax.get_xticklabels():
                    label.set_rotation(15)
                    label.set_horizontalalignment('right')
            yl = ax.get_yticklabels()
            yl[0].set_visible(False)
            yl[-1].set_visible(False)

        #plt.grid(True)
        #fig.autofmt_xdate()
        #if labels:
        props = font_manager.FontProperties(size=8)
        leg = ax2.legend(loc='upper left', shadow=True, fancybox=False, prop=props)
        leg.get_frame().set_alpha(0.5)
        leg = ax1.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
        leg.get_frame().set_alpha(0.5)
        leg = ax3.legend(loc='upper left', shadow=True, fancybox=True, prop=props)
        leg.get_frame().set_alpha(0.5)

        #    legend = plt.legend(labels, labelspacing = 0.1) #loc=(0.9, .95),
        #    plt.setp(legend.get_texts(), fontsize = 'small')

        imgdata = StringIO.StringIO()
        plt.savefig(imgdata, format = 'png')
        plt.close()
        imgdata.seek(0)
        out = imgdata.getvalue()
        path = os.path.join(g.OPT.staticPath, "%s.png" % name)
        print "Created:", path
        f = open(path, "wb+")
        f.write(out)
        f.close()
        Picture.makeThumbnail(path, os.path.join(g.OPT.staticPath, "%ss.png" % name), (200, 200))

    def command(self):
        #devIni = self.args[0]
        self.setup_config(self.options.config, self.options.path)

        if self.options.preparedata:
            self.prepareData(self.options.solar)
        else:
            import matplotlib
            matplotlib.use('Agg')

            xsvals = []
            ysvalsPPD = []
            ysvalsTotal = []
            ysvalsUUsers = []

            radioFlux = []
            sunspotNumber = []
            sunspotArea = []

            for sr in StatRecord.query.order_by(StatRecord.timestamp.asc()):
                xsvals.append(sr.timestamp)
                ysvalsPPD.append(sr.postsAtDay)
                ysvalsTotal.append(sr.totalPostsUntil)
                ysvalsUUsers.append(sr.uniqueUsers)
                radioFlux.append(sr.radioFlux)
                sunspotNumber.append(sr.sunspotNumber)
                sunspotArea.append(sr.sunspotArea)

            period = 6
            ppdEMA = self.calculateEMA(ysvalsPPD, period)
            ppdEMAv = [0] * (period - 1)
            ppdEMAv.extend(ppdEMA)

            uuEMA = self.calculateEMA(ysvalsUUsers, period)
            uuEMAv = [0] * (period - 1)
            uuEMAv.extend(uuEMA)

            self.plotStdGraph(xsvals, [ysvalsTotal], "stat_posts_total", "Total posts", None)
            self.plotMultiGraph(xsvals,
                              [ysvalsPPD, ppdEMAv, radioFlux, sunspotNumber, sunspotArea],
                              "stat_posts_pd",
                              "Posts per day",
                              ("Posts", "Exp MA", "Radio Flux", "Sunspot Number", "Sunspot Area"))
            self.plotMultiGraph(xsvals, [ysvalsUUsers, uuEMAv, radioFlux, sunspotNumber, sunspotArea],
                              "stat_users_pd",
                              "Unique users per day",
                              ("Posts", "Exp MA", "Radio Flux", "Sunspot Number", "Sunspot Area"))

    def prepareData(self, downloadSolarData):
        ns = g.pluginsDict['statgraph'].namespace()
        birthdate = meta.Session.query(sa.sql.functions.min(Post.date)).scalar()
        lastdate = datetime.datetime.now()
        currentdate = birthdate
        xsvals = []
        ysvalsPPD = []
        ysvalsT = []
        ysvalsUU = []
        dayscount = (lastdate - birthdate).days
        ccount = 0
        values = {}
        while currentdate < lastdate:
            nextdate = (currentdate + datetime.timedelta(days = 1))
            uniqueUidsExpr = meta.Session.query(Post.uidNumber).distinct()
            dayClause = and_(Post.date <= nextdate, Post.date >= currentdate)
            uuserscount = uniqueUidsExpr.filter(dayClause).count()
            countfordate = Post.query.filter(dayClause).count()
            countupdate = Post.query.filter(Post.date <= nextdate).count()
            xsvals.append(currentdate.date())
            ysvalsPPD.append(countfordate)
            ysvalsT.append(countupdate)
            ysvalsUU.append(uuserscount)
            print "Day %d/%d (%s): %d posts, %d total, %d uniq users" % (ccount,
                                                                    dayscount,
                                                                    currentdate.date(),
                                                                    countfordate,
                                                                    countupdate,
                                                                    uuserscount)
            dayvalues = {'postsAtDay' : countfordate,
                      'uniqueUsers' : uuserscount,
                      'totalPostsUntil' : countupdate,
                      'radioFlux' : None,
                      'sunspotNumber' : None,
                      'sunspotArea' : None,
                      }
            values[currentdate.date()] = dayvalues
            ccount += 1
            currentdate = nextdate

        if downloadSolarData:
            idxbase = 'http://www.swpc.noaa.gov/ftpdir/indices/old_indices'
            curidx = 'http://www.swpc.noaa.gov/ftpdir/indices/quar_DSD.txt'
            #tmpd = tempfile.mkdtemp()
            #print "Temporary directory: %s" % tmpd
            def download(url):
                print "Downloading %s..." % url
                response = urllib2.urlopen(url)
                html = response.read()
                """
                f = open(os.path.join(tmpd, url.split(r'/')[-1]), 'w+')
                f.write(html)
                f.close()
                """
                print "ok"
                return html
            print "Downloading index from %s..." % idxbase
            response = urllib2.urlopen(idxbase)
            oldind = response.read()
            print "ok"
            mergedData = ""
            cur_year = 2008
            while cur_year <= datetime.datetime.now().year:
                rex = re.compile(r"%d\w*_DSD\.txt" % cur_year)
                filesToDownload = list(set(re.findall(rex, oldind)))
                filesToDownload = map(lambda x: "%s/%s" % (idxbase, x), filesToDownload)
                filesToDownload.append(curidx)
                print "Files to download: %s" % str(filesToDownload)
                for ftd in filesToDownload:
                    mergedData += download(ftd)
                cur_year += 1
            mergedData = filter(lambda x: not ('#' in x or ':' in x), mergedData.splitlines())
            mergedData = sorted(mergedData)
            fmts = '%Y %m %d'
            slen = 10
            solarvalues = {}
            rex = re.compile("^\d+\s+\d+\s+\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+.+$")

            for line in mergedData:
                ts = datetime.datetime.strptime(line[:slen], fmts)
                groups = rex.match(line).groups()
                solarvalues[ts.date()] = (groups[0], groups[1], groups[2])

            print "Setting data..."
            for date in values:
                solarDayValues = solarvalues.get(date, None)
                if solarDayValues:
                    print "%s" % str(date)
                    dayvalues = values[date]
                    dayvalues['radioFlux'] = solarDayValues[0]
                    dayvalues['sunspotNumber'] = solarDayValues[1]
                    dayvalues['sunspotArea'] = solarDayValues[2]
                    values[date] = dayvalues
            print "ok"
        for date in values:
            ns.StatRecord.setFor(date, **values[date])
        meta.Session.commit()

    @staticmethod
    def calculateEMA(values_array, n):
        """
        returns an n period exponential moving average for
        the time series values_array

        values_array is a list ordered from oldest (index 0) to most recent (index
        -1) n is an integer

        returns a numeric array of the exponential moving average
        """
        values_array = array('d', values_array)
        exponential_moving_average_array = []
        j = 1
        #get n sma first and calculate the next n period ema
        sma = sum(values_array[:n]) / n
        multiplier = 2 / float(1 + n)
        exponential_moving_average_array.append(sma)
        #EMA(current) = ( (Price(current) - EMA(prev) ) xMultiplier) + EMA(prev)
        exponential_moving_average_array.append(((values_array[n] - sma) * multiplier) + sma)
        #now calculate the rest of the values
        for i in values_array[n + 1:]:
            tmp = ((i - exponential_moving_average_array[j]) * multiplier) + exponential_moving_average_array[j]
            j = j + 1
            exponential_moving_average_array.append(tmp)
        return exponential_moving_average_array

class StatRecord(object):
    def __init__(self, timestamp, **kwargs):
        self.timestamp = timestamp
        StatRecord.setValues(self, **kwargs)

    @staticmethod
    def setValues(instance, **values):
        for arg in values:
            setattr(instance, arg, values[arg])

    @staticmethod
    def setFor(date, **values):
        record = StatRecord.query.filter(StatRecord.timestamp == date).first()
        if not record:
            record = StatRecord(date, **values)
            meta.Session.add(record)
        else:
            StatRecord.setValues(record, **values)

    @staticmethod
    def getFor(date):
        return StatRecord.query.filter(StatRecord.date == date).first()

class HomeStatisticsPlugin(BasePlugin, AbstractHomeExtension):
    def __init__(self):
        config = {'name' : N_('Graphical statistics for main page'),
                  'deps' : ('base_view',)
                 }

        BasePlugin.__init__(self, 'statgraph', config)
        AbstractHomeExtension.__init__(self, 'statgraph')

    def entryPointsList(self):
        return [('statgraphs', "GraphsCommand"), ]

    def initORM(self, orm, engine, dialectProps, propDict):
        namespace = self.namespace()
        t_statistics = sa.Table("statlog", meta.metadata,
            sa.Column("timestamp"       , sa.types.Date, unique = True, primary_key = True),
            sa.Column('postsAtDay'  , sa.types.Integer, nullable = True),
            sa.Column('uniqueUsers'  , sa.types.Integer, nullable = True),
            sa.Column('totalPostsUntil'  , sa.types.Integer, nullable = True),
            sa.Column('radioFlux'  , meta.FloatType, nullable = True),
            sa.Column('sunspotNumber'  , meta.FloatType, nullable = True),
            sa.Column('sunspotArea'  , meta.FloatType, nullable = True),
            )

        #orm.mapper
        meta.mapper(namespace.StatRecord, t_statistics, properties = {})

    def prepareData(self, controller, container):
        c.graphsToShow = []

        for graph in GraphsCommand.graphsToShow:
            fname = "%s.png" % graph
            tname = "%ss.png" % graph
            fpath = os.path.join(g.OPT.staticPath, fname)
            tpath = os.path.join(g.OPT.staticPath, tname)
            if os.path.exists(fpath) and os.path.exists(tpath):
                c.graphsToShow.append((tname, fname))
