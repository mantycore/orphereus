import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_logins = sa.Table("loginStats", meta.metadata,
    sa.Column("id"          , sa.types.Integer, primary_key=True),
    sa.Column("ip"          , sa.types.String(16), nullable=False),
    sa.Column("attempts"    , sa.types.Integer, nullable=False),    
    sa.Column("cid"         , sa.types.Integer, nullable=True), 
    sa.Column("lastAttempt" , sa.types.DateTime, nullable=True)
    )

class LoginTracker(object):
    def __init__(self, ip):
        self.ip = ip
        self.attempts = 0
        self.lastAttempt =  datetime.datetime.now()
        
    def getTracker(ip):
        tracker = LoginTracker.query.filter(LoginTracker.ip==ip).first()
        if not tracker:
            tracker = LoginTracker(ip)
            meta.Session.add(tracker)
            meta.Session.commit()
        return tracker
    getTracker = staticmethod(getTracker)
