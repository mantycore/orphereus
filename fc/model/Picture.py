import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime
import os
import Image

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_piclist = sa.Table("piclist", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("thumpath" , sa.types.String(255), nullable=False),
    sa.Column("width"    , sa.types.Integer, nullable=False),
    sa.Column("height"   , sa.types.Integer, nullable=False),
    sa.Column("thwidth"  , sa.types.Integer, nullable=False),
    sa.Column("thheight" , sa.types.Integer, nullable=False),
    sa.Column("size"     , sa.types.Integer, nullable=False),
    sa.Column("md5"      , sa.types.String(32), nullable=False),
    sa.Column("extid"    , sa.types.Integer, sa.ForeignKey('extlist.id'))
    )

class Picture(object):
    def __init__(self, relativeFilePath, thumbFilePath, fileSize, picSizes, extId, md5):
       self.path = relativeFilePath
       self.thumpath = thumbFilePath
       self.width = picSizes[0]
       self.height = picSizes[1]
       self.thwidth = picSizes[2]
       self.thheight = picSizes[3]
       self.extid = extId
       self.size = fileSize
       self.md5 = md5

    @staticmethod
    def create(relativeFilePath, thumbFilePath, fileSize, picSizes, extId, md5):
        pic = Picture(relativeFilePath, thumbFilePath, fileSize, picSizes, extId, md5)
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

    def deletePicture(self, commit = True):
        from fc.model.Post import Post
        log.debug(Post.pictureRefCount(self.id))
        if Post.pictureRefCount(self.id) == 1:
            filePath = os.path.join(meta.globj.OPT.uploadPath, self.path)
            thumPath = os.path.join(meta.globj.OPT.uploadPath, self.thumpath)
            if os.path.isfile(filePath):
                os.unlink(filePath)

            ext = self.extension
            if not ext.path:
                if os.path.isfile(thumPath):
                    os.unlink(thumPath)

            meta.Session.delete(self)
            if commit:
                meta.Session.commit()

