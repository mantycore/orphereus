import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql import and_, or_, not_

from fc.model import meta
from fc.model.Picture import Picture
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_extlist = sa.Table("extlist", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("thwidth"  , sa.types.Integer, nullable=False),
    sa.Column("thheight" , sa.types.Integer, nullable=False),
    sa.Column("ext"      , sa.types.String(16), nullable=False, unique=True),
    sa.Column("type"     , sa.types.String(16), nullable=False),
    sa.Column("enabled"  , sa.types.Boolean, server_default='1'),
    sa.Column("newWindow", sa.types.Boolean, server_default='1'),
    )

#TODO: rewrite Extension
class Extension(object):
    def __init__(self, name, enabled, newWindow, type, path, thwidth, thheight):
        self.ext = name
        self.setData(enabled, newWindow, type, path, thwidth, thheight)

    def setData(self, enabled, newWindow, type, path, thwidth, thheight):
        self.path = path
        self.enabled = enabled
        self.newWindow = newWindow
        self.type = type
        self.path = path
        self.thwidth = thwidth
        self.thheight = thheight
        meta.Session.commit()

    def delete(self):
        boundPictures = Picture.query.filter(Picture.extension.has(Extension.id == self.id)).count()
        if boundPictures == 0:
            meta.Session.delete(self)
            meta.Session.commit()
            return True
        else:
            return False

    @staticmethod
    def getList(enabledOnly):
        filter = Extension.query.order_by(Extension.type)
        if enabledOnly:
            filter = filter.filter(Extension.enabled == True)
        return filter.all()

    @staticmethod
    def getExtension(ext):
        return Extension.query.filter(Extension.ext==ext).first()

    @staticmethod
    def create(name, enabled, newWindow, type, path, thwidth, thheight):
        if not Extension.getExtension(name):
            ext = Extension(name, enabled, newWindow, type, path, thwidth, thheight)
            meta.Session.add(ext)
            meta.Session.commit()
            return ext
        else:
            return False
