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
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #                                                                         #
################################################################################


import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta

import datetime
import string
import random
import Image, ImageDraw, ImageFilter, ImageFont
import StringIO
from Captcha.Visual import Text, Backgrounds, Distortions, ImageCaptcha

class CaptchaGenerator(ImageCaptcha):
    def __init__(self, word, font, *args, **kwargs):
        self.word = word
        self.font = font
        super(CaptchaGenerator, self).__init__(*args, **kwargs)

    def getLayers(self):
        word = self.word
        ff = Text.FontFactory(26, self.font)
        bg = random.choice([Backgrounds.SolidColor(), Backgrounds.CroppedImage(), Backgrounds.TiledImage(), ])
        bg = (bg, Backgrounds.Grid(), Distortions.SineWarp(amplitudeRange = (6, 10), periodRange = (0.1, 0.4)))
        return [ bg,
            Backgrounds.RandomDots(),
            #Distortions.WigglyBlocks(),
            Text.TextLayer(word, borderSize = 1, fontFactory = ff),
            Distortions.SineWarp()
            #Distortions.SineWarp()
            ]

import logging
log = logging.getLogger(__name__)

from fc.model import meta
from pylons.i18n import get_lang, set_lang, _

t_captchas = sa.Table("captcha", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key = True),
    sa.Column("text"     , sa.types.UnicodeText, nullable = False),
    sa.Column("content"  , sa.types.Binary, nullable = True),
    sa.Column("timestamp", sa.types.DateTime, nullable = False)
    )

def randomStr(min = 6, max = 8):
    vowels = _("euoa")
    consonants = _("qwrtypsdfghjkzxcvbnm")
    str = ''
    #log.debug('using in gen: %s' %get_lang())
    for x in range(0, random.randint(min , max) / 2):
        str += random.choice(consonants) + random.choice(vowels)

    return str

def force_unicode(string, encoding = 'utf-8'):
    try:
        if type(string) is str:
            string = string.decode(encoding)
        if type(string) is not unicode:
            string = unicode(string)
    finally:
        return string

class Captcha(object):
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.datetime.now()

    def delete(self):
        meta.Session.delete(self)
        meta.Session.commit()

    def test(self, text, removeOnlyIncorrect = False):
        ret = (force_unicode(self.text) == force_unicode(text))
        #log.debug("recieved: %s" %text)
        #log.debug("self: %s" %self.text)
        #log.debug(str(self) +  "  " + str(self.id))
        if not ret or (ret and not removeOnlyIncorrect):
            #log.debug("del id %s " %self.text)
            meta.Session.delete(self)
            meta.Session.commit()
        return ret

    @staticmethod
    def create():
        captcha = Captcha(randomStr())
        meta.Session.add(captcha)
        meta.Session.commit()
        #log.debug("created %s" %str(captcha.id))
        return captcha

    @staticmethod
    def getCaptcha(id):
        return Captcha.query.filter(Captcha.id == id).first()

    @staticmethod
    def exists(id):
        return (Captcha.query.filter(Captcha.id == id).count() == 1)

    @staticmethod
    def picture(cid, font):
        captcha = Captcha.query.filter(Captcha.id == cid).first()

        out = ""
        if captcha and captcha.content:
            return captcha.content
        elif captcha:
            text = force_unicode(captcha.text)

            size = (150, 40)
            cgen = CaptchaGenerator(text, font)
            textPic = cgen.render(size)

            f = StringIO.StringIO()
            textPic.save(f, "PNG")
            pic = f.getvalue()
            if captcha:
                captcha.content = pic
                meta.Session.commit()
            out = pic
            return str(out)
        else:
            return "Wrong ID"

    """
        pw = 300
        ph = 80
        textPic = Image.new('RGBA', (pw, ph), 'orange')
        draw = ImageDraw.Draw(textPic)
        font = ImageFont.truetype(font, 64)
        w = font.getsize(text)[0]
        h = font.getsize(text)[1]
        tcolor = (random.randrange(50, 150), random.randrange(50, 150), random.randrange(50, 150))
        draw.text(((pw - w)/2 + random.randrange(-20, 20), (ph - h)/2 + random.randrange(-10, 10)), text, font=font, fill=tcolor)

        if captcha:
            noisePic = Image.new('RGBA', (pw, ph), 'yellow')
            draw = ImageDraw.Draw(noisePic)
            pc = random.randrange(20)+10
            for c in range(pc):
                x1 = random.randrange(0, pw)
                y1 = random.randrange(0, ph)
                x2 = random.randrange(x1, pw)
                y2 = random.randrange(y1, ph)
                fcolor=(random.randrange(50,250), random.randrange(50,250), random.randrange(50,250))
                ocolor=(random.randrange(50,250), random.randrange(50,250), random.randrange(50,250))
                draw.ellipse((x1, y1, x2, y2), fill=tcolor, outline=ocolor)

            noisePic= noisePic.filter(ImageFilter.BLUR)
            #textPic = Image.blend(noisePic, textPic, 0.4)
            textPic = Image.blend(textPic, noisePic, 0.6)
            ht = Captcha.createHatchingTexture(0.5, pw, ph, tcolor)
            textPic = Image.blend(textPic, ht, 0.3)
    """

    """
        @staticmethod
        def createHatchingTexture(density, width, height, fill): # cool procedure, found in google
            # create image and drawing surface
            hatchImage = Image.new("RGBA", (width, height), 0)
            hatchDraw = ImageDraw.Draw(hatchImage)
            # set density
            spacer = int(10 * density)
            doubleSpacer = spacer * 2
            # draw lines
            y1 = 0
            y2 = height
            for x in range(0, width, spacer):
                x1 = x + random.randint(-doubleSpacer, doubleSpacer)
                x2 = x + random.randint(-doubleSpacer, doubleSpacer)
                hatchDraw.line((x1, y1, x2, y2), fill=fill)
            x1 = 0
            x2 = width
            for y in range(0, height, spacer):
                y1 = y + random.randint(-doubleSpacer, doubleSpacer)
                y2 = y + random.randint(-doubleSpacer, doubleSpacer)
                hatchDraw.line((x1, y1, x2, y2), fill=fill)
            return hatchImage
    """
