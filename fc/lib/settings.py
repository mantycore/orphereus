import logging
from fc.lib.base import *
from fc.model import *
from sqlalchemy.orm import eagerload
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql import and_, or_, not_
from fc.lib.constantValues import *

def getSettingsMap():
    settings = meta.Session.query(Setting).all()
    settingsMap = {}
    if settings:
        for s in settings:
            if s.name in settingsDef:
                settingsMap[s.name] = s
    for s in settingsDef:
        if not s in settingsMap:
            settingsMap[s] = Setting()
            settingsMap[s].name = s
            settingsMap[s].value = settingsDef[s]
            meta.Session.save(settingsMap[s])
            meta.Session.commit()
    return settingsMap
 