import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime
import hashlib
from pylons import config

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_users = sa.Table("users", meta.metadata,
    sa.Column("uidNumber",sa.types.Integer, primary_key=True),
    sa.Column("uid"      , sa.types.String(128), nullable=False)
    )

class User(object):
    def genUid(key):
        return hashlib.sha512(key + hashlib.sha512(config['pylons.app_globals'].OPT.hashSecret).hexdigest()).hexdigest()
    genUid = staticmethod(genUid)