import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_settings = sa.Table("settings", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("name"     , sa.types.String(64), nullable=False),
    sa.Column("value"    , sa.types.UnicodeText, nullable=False)
    )

class Setting(object):
    @staticmethod
    def getSetting(name):
        return Setting.query().filter(Setting.name==name).first()

    def setValue(self, value):
        self.value = value
        meta.Session.commit()
