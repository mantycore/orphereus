import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_captchas = sa.Table("captchas", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("text"     , sa.types.String(32), nullable=False),
    sa.Column("content"  , sa.types.Binary, nullable=True)
    )

class Captcha(object):
    pass