import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_oekaki = sa.Table("oekaki", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tempid"   , sa.types.String(20), nullable=False),
    sa.Column("time"     , sa.types.Integer, nullable=False),
    sa.Column("source"   , sa.types.Integer, nullable=False),
    sa.Column("uidNumber",sa.types.Integer, nullable=False),
    sa.Column("type"     , sa.types.String(255), nullable=False),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("timeStamp", sa.types.DateTime, nullable=False),
    sa.Column("selfy", sa.types.Boolean, nullable=False, server_default='0'),
    )

class Oekaki(object):
    def __init__(self, tempid, uidNumber, type, source, selfy):
        self.timeStamp = datetime.datetime.now()
        self.time = -1
        self.path = ''
        self.type = type
        self.uidNumber = uidNumber
        self.source = source
        self.tempid = tempid
        self.selfy = selfy

    @staticmethod
    def create(tempid, uidNumber, type, source, selfy):
        oekaki = Oekaki(tempid, uidNumber, type, source, selfy)
        meta.Session.add(oekaki)
        meta.Session.commit()

    @staticmethod
    def get(tempid):
        return Oekaki.query.filter(Oekaki.tempid==tempid).first()

    def setPathAndTime(self, path, time):
        self.path = path
        self.time = time
        meta.Session.commit()

    def delete(self):
        meta.Session.delete(self)
        meta.Session.commit()
