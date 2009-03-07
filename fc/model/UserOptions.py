import sqlalchemy as sa
from sqlalchemy import orm

from fc.model import meta
import datetime
import re
import pickle

import logging
log = logging.getLogger(__name__)

from fc.model import meta

t_userOptions = sa.Table("userOptions", meta.metadata,
    sa.Column("optid"    ,sa.types.Integer, primary_key=True),
    sa.Column("uidNumber",sa.types.Integer, sa.ForeignKey('user.uidNumber')),
    sa.Column("threadsPerPage", sa.types.Integer, nullable=False),
    sa.Column("repliesPerThread", sa.types.Integer, nullable=False),
    sa.Column("style"    , sa.types.String(32), nullable=False),
    sa.Column("template" , sa.types.String(32), nullable=False),
    sa.Column("homeExclude", sa.types.String(256), nullable=False),
    sa.Column("hideThreads", sa.types.Text, nullable=True),
    sa.Column("bantime"  , sa.types.Integer, nullable=False),
    sa.Column("banreason", sa.types.UnicodeText(256), nullable=True),
    sa.Column("banDate", sa.types.DateTime, nullable=True),
    sa.Column("hideLongComments", sa.types.Boolean, nullable=True),
    sa.Column("useAjax", sa.types.Boolean, nullable=True),
    sa.Column("expandImages", sa.types.Boolean, nullable=True, server_default='1'),
    sa.Column("maxExpandWidth", sa.types.Integer, nullable=True, server_default='1024'),
    sa.Column("maxExpandHeight", sa.types.Integer, nullable=True, server_default='768'),
    sa.Column("mixOldThreads", sa.types.Boolean, nullable=True),
    sa.Column("defaultGoto", sa.types.Integer, nullable=True),
    sa.Column("oekUseSelfy", sa.types.Boolean, nullable=True, server_default='0'),
    sa.Column("oekUseAnim", sa.types.Boolean, nullable=True, server_default='0'),
    sa.Column("oekUsePro", sa.types.Boolean, nullable=True, server_default='0'),
    sa.Column("isAdmin"  , sa.types.Boolean, nullable=True),
    sa.Column("canDeleteAllPosts", sa.types.Boolean, nullable=True),
    sa.Column("canMakeInvite", sa.types.Boolean, nullable=True),
    sa.Column("canChangeRights", sa.types.Boolean, nullable=True),
    sa.Column("canChangeSettings", sa.types.Boolean, nullable=True),
    sa.Column("canManageBoards", sa.types.Boolean, nullable=True),
    sa.Column("canManageUsers", sa.types.Boolean, nullable=True),
    sa.Column("canManageExtensions", sa.types.Boolean, nullable=True),
    sa.Column("canManageMappings", sa.types.Boolean, nullable=True),
    sa.Column("canRunMaintenance", sa.types.Boolean, nullable=True),
    )

class UserOptions(object):
    @staticmethod
    def optionsDump(optionsObject):
        optionsNames = dir(optionsObject)
        ret = {}
        retest = re.compile("^(<.*(at (0x){0,1}[0-9a-fA-F]+)+.*>)|(__.*__)$")
        for name in optionsNames:
            attr = str(getattr(optionsObject, name))
            if not (retest.match(name) or retest.match(attr)):
                ret[name] = attr
        return ret

    @staticmethod
    def initDefaultOptions(optionsObject, globalOptHolder):
        optionsObject.style = globalOptHolder.styles[0]
        optionsObject.template = globalOptHolder.templates[0]
        optionsObject.threadsPerPage = 10
        optionsObject.repliesPerThread = 10
        optionsObject.bantime = 0
        optionsObject.isAdmin = False
        optionsObject.hideLongComments = True
        optionsObject.useAjax = True
        optionsObject.mixOldThreads = True
        optionsObject.defaultGoto = 0
        optionsObject.expandImages = True
        optionsObject.oekUseSelfy = False
        optionsObject.oekUseAnim = False
        optionsObject.oekUsePro = False
        optionsObject.maxExpandWidth = 1024
        optionsObject.maxExpandHeight = 768
        optionsObject.homeExclude = pickle.dumps([])
        optionsObject.hideThreads = pickle.dumps([])
        optionsObject.canDeleteAllPosts = False
        optionsObject.canMakeInvite = False
        optionsObject.canChangeRights = False
        optionsObject.canChangeSettings = False
        optionsObject.canManageBoards = False
        optionsObject.canManageUsers = False
        optionsObject.canManageExtensions = False
        optionsObject.canManageMappings = False
        optionsObject.canRunMaintenance = False
