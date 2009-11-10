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

import sqlalchemy as sa
from sqlalchemy import orm

from Orphereus.model import meta
import os
import Image

import logging
log = logging.getLogger(__name__)

t_piclist = sa.Table("picture", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key = True),
    sa.Column("path"     , sa.types.String(255), nullable = False),
    sa.Column("thumpath" , sa.types.String(255), nullable = False),
    sa.Column("width"    , sa.types.Integer, nullable = True),
    sa.Column("height"   , sa.types.Integer, nullable = True),
    sa.Column("thwidth"  , sa.types.Integer, nullable = False),
    sa.Column("thheight" , sa.types.Integer, nullable = False),
    sa.Column("size"     , sa.types.Integer, nullable = False),
    sa.Column("md5"      , sa.types.String(32), nullable = False),
    sa.Column("extid"    , sa.types.Integer, sa.ForeignKey('extension.id')),
    sa.Column("animpath" , sa.types.String(255), nullable = True), #TODO: XXX: dirty solution
    )

class Picture(object):
    def __init__(self, relativeFilePath, thumbFilePath, fileSize, picSizes, extId, md5, animPath):
        self.path = relativeFilePath
        self.thumpath = thumbFilePath
        self.width = picSizes[0]
        self.height = picSizes[1]
        self.thwidth = picSizes[2]
        self.thheight = picSizes[3]
        self.extid = extId
        self.size = fileSize
        self.md5 = md5
        if animPath:
            self.animpath = animPath

    @staticmethod
    def create(relativeFilePath, thumbFilePath, fileSize, picSizes, extId, md5, animPath = None, commit = False):
        pic = Picture(relativeFilePath, thumbFilePath, fileSize, picSizes, extId, md5, animPath)
        if commit:
            meta.Session.add(pic)
            meta.Session.commit()
        return pic

    @staticmethod
    def getPicture(id):
        return Picture.query.filter(Picture.id == id).first()

    @staticmethod
    def getByMd5(md5):
        return Picture.query.filter(Picture.md5 == md5).first()

    @staticmethod
    def makeThumbnail(source, dest, maxSize):
        sourceImage = Image.open(source)
        size = sourceImage.size
        if sourceImage:
            sourceImage.thumbnail(maxSize, Image.ANTIALIAS)
            sourceImage.save(dest)
            return size + sourceImage.size
        else:
            return []

    def pictureRefCount(self):
        from Orphereus.model.Post import Post
        return Post.query.filter(Post.file == self).count()

    def deletePicture(self, commit = True):
        if self.pictureRefCount() == 1:
            filePath = os.path.join(meta.globj.OPT.uploadPath, self.path)
            thumPath = os.path.join(meta.globj.OPT.uploadPath, self.thumpath)
            if os.path.isfile(filePath):
                os.unlink(filePath)

            if self.animpath:
                animPath = os.path.join(meta.globj.OPT.uploadPath, self.animpath)
                if os.path.isfile(animPath):
                    os.unlink(animPath)

            ext = self.extension
            if not ext.path:
                if os.path.isfile(thumPath):
                    os.unlink(thumPath)

            meta.Session.delete(self)
            if commit:
                meta.Session.commit()
