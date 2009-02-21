import sqlalchemy as sa

from fc.model import meta
import datetime
import time
import hashlib

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_invites = sa.Table("invites", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("invite"   , sa.types.String(128), nullable=False),
    sa.Column("date"     , sa.types.DateTime,  nullable=False)
    )

class Invite(object):
    def __init__(self, code):
        self.date = datetime.datetime.now()
        self.invite = code

    @staticmethod
    def getId(code):
        invite = Invite.query.filter(Invite.invite==code).first()
        ret = False
        if invite:
            ret = invite.id
            meta.Session.delete(invite)
            meta.Session.commit()
        return ret

    @staticmethod
    def create(secret):
        invite = Invite(Invite.generateId(secret))
        meta.Session.add(invite)
        meta.Session.commit()
        return invite

    @staticmethod
    def generateId(secret):
        return hashlib.sha512(str(long(time.time() * 10**7)) + hashlib.sha512(secret).hexdigest()).hexdigest()