import sqlalchemy as sa
from sqlalchemy import orm
from fc.model import meta
from pylons import config
from fc.lib.constantValues import *

import logging
log = logging.getLogger(__name__)

def init_model(engine):
    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)
    #logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
    
    settings = False
    try:
        settings = meta.Session.query(Setting).all()
        #log.debug(settingsDef)
        settingsMap = {}
        if settings:
            for s in settings:
                #log.debug(s.name+ ' : ' +s.value)
                if s.name in settingsDef:
                    settingsMap[s.name] = s
        
        for s in settingsDef: 
            if not s in settingsMap:
                #log.debug(s) 
                settingsMap[s] = Setting()
                settingsMap[s].name = s
                settingsMap[s].value = settingsDef[s]
                meta.Session.save(settingsMap[s])
                meta.Session.commit()
        config['pylons.g'].settingsMap = settingsMap
        
        
    except:
        pass             
    """
    gv = config['pylons.g']
    gv.tagCache = {}
    tags = meta.Session.query(Tag).all()
    for tag in tags:
        gv.tagCache[tag.tag] = tag.id
        
    log.debug(gv.tagCache)
    """        

t_settings = sa.Table("settings", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("name"     , sa.types.String(64), nullable=False),
    sa.Column("value"    , sa.types.UnicodeText, nullable=False)
    )

t_invites = sa.Table("invites", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("invite"   , sa.types.String(128), nullable=False),
    sa.Column("date"     , sa.types.DateTime,  nullable=False)
    )

t_users = sa.Table("users", meta.metadata,
    sa.Column("uidNumber",sa.types.Integer, primary_key=True),
    sa.Column("uid"      , sa.types.String(128), nullable=False)
    )

t_userOptions = sa.Table("userOptions", meta.metadata,
    sa.Column("optid"    ,sa.types.Integer, primary_key=True),
    sa.Column("uidNumber",sa.types.Integer, sa.ForeignKey('users.uidNumber')),
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
    sa.Column("mixOldThreads", sa.types.Boolean, nullable=True),
    sa.Column("defaultGoto", sa.types.Integer, nullable=True),
    sa.Column("isAdmin"  , sa.types.Boolean, nullable=True),
    sa.Column("canDeleteAllPosts", sa.types.Boolean, nullable=True),
    sa.Column("canMakeInvite", sa.types.Boolean, nullable=True),
    sa.Column("canChangeRights", sa.types.Boolean, nullable=True)
    )

t_userFilters = sa.Table("userFilters", meta.metadata,
    sa.Column("id"        , sa.types.Integer    , primary_key=True),
    sa.Column("uidNumber" , sa.types.Integer    , sa.ForeignKey('users.uidNumber')),
    sa.Column("filter"    , sa.types.UnicodeText, nullable=False)
    )

t_log = sa.Table("log", meta.metadata,
    sa.Column("id"    , sa.types.Integer, primary_key=True),
    sa.Column("uidNumber", sa.types.Integer, sa.ForeignKey('users.uidNumber')),
    sa.Column("date"  , sa.types.DateTime, nullable=False),
    sa.Column("event" , sa.types.Integer, nullable=False),
    sa.Column("entry" , sa.types.UnicodeText, nullable=False)
    )

t_extlist = sa.Table("extlist", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("thwidth"  , sa.types.Integer, nullable=False),
    sa.Column("thheight" , sa.types.Integer, nullable=False),
    sa.Column("ext"      , sa.types.String(16), nullable=False),
    sa.Column("type"     , sa.types.String(16), nullable=False)
    )

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

t_oekaki = sa.Table("oekaki", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tempid"   , sa.types.String(20), nullable=False),
    sa.Column("picid"    , sa.types.Integer, nullable=False),
    sa.Column("time"     , sa.types.Integer, nullable=False),
    sa.Column("source"   , sa.types.Integer, nullable=False),
    sa.Column("uidNumber",sa.types.Integer, nullable=False),
    sa.Column("type"     , sa.types.String(255), nullable=False),
    sa.Column("path"     , sa.types.String(255), nullable=False),
    sa.Column("timeStamp", sa.types.DateTime, nullable=False)
    )

t_posts = sa.Table("posts", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("secondaryIndex",sa.types.Integer, nullable=True),
    sa.Column("parentid" , sa.types.Integer, sa.ForeignKey('posts.id')),
    sa.Column("message"  , sa.types.UnicodeText, nullable=True),
    sa.Column("messageShort", sa.types.UnicodeText, nullable=True),
    sa.Column("messageRaw"  , sa.types.UnicodeText, nullable=True),
    sa.Column("title"    , sa.types.UnicodeText, nullable=True),
    sa.Column("sage"     , sa.types.Boolean, nullable=True),
    sa.Column("uidNumber",sa.types.Integer,nullable=True),
    sa.Column("picid"    , sa.types.Integer, sa.ForeignKey('piclist.id')),
    sa.Column("date"     , sa.types.DateTime, nullable=False),
    sa.Column("bumpDate", sa.types.DateTime, nullable=True),
    sa.Column("spoiler"  , sa.types.Boolean, nullable=True),
    sa.Column("replyCount" , sa.types.Integer, nullable=False, server_default='0'),   
    )

t_tags = sa.Table("tags", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tag"      , sa.types.UnicodeText, nullable=False),
    sa.Column("replyCount" , sa.types.Integer, nullable=False, server_default='0'),
    sa.Column("threadCount" , sa.types.Integer, nullable=False, server_default='0'),
    )

t_tagOptions = sa.Table("tagOptions", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tagId"   , sa.types.Integer,  sa.ForeignKey('tags.id')),
    sa.Column("comment"  , sa.types.UnicodeText, nullable=True),
    sa.Column("sectionId", sa.types.Integer, nullable=False),
    sa.Column("persistent", sa.types.Boolean, nullable=False),
    sa.Column("imagelessThread", sa.types.Boolean, nullable=False),
    sa.Column("imagelessPost", sa.types.Boolean, nullable=False),
    sa.Column("images"   , sa.types.Boolean, nullable=False),
    sa.Column("maxFileSize" , sa.types.Integer, nullable=False),
    sa.Column("minPicSize" , sa.types.Integer, nullable=False),
    sa.Column("thumbSize", sa.types.Integer, nullable=False),
    sa.Column("enableSpoilers", sa.types.Boolean, nullable=False),
    sa.Column("canDeleteOwnThreads", sa.types.Boolean, server_default='1'),
    sa.Column("specialRules"  , sa.types.UnicodeText, nullable=True),
    )

t_tagsToPostsMap = sa.Table("tagsToPostsMap", meta.metadata,
#    sa.Column("id"          , sa.types.Integer, primary_key=True),                            
    sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('posts.id')),
    sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('tags.id')),
    )
    
t_logins = sa.Table("loginStats", meta.metadata,
    sa.Column("id"          , sa.types.Integer, primary_key=True),
    sa.Column("ip"          , sa.types.String(16), nullable=False),
    sa.Column("attempts"    , sa.types.Integer, nullable=False),    
    sa.Column("cid"         , sa.types.Integer, nullable=True), 
    sa.Column("lastAttempt" , sa.types.DateTime, nullable=True)
    )    
    
t_captchas = sa.Table("captchas", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("text"     , sa.types.String(32), nullable=False),
    sa.Column("content"  , sa.types.Binary, nullable=True)
    )     

class Captcha(object):
    pass
    
class LoginTracker(object):
    pass
    
class Oekaki(object):
    pass
    
class Invite(object):
    pass

class User(object):
    pass
    
class UserOptions(object):
    pass
    
class UserFilters(object):
    pass
    
class Extension(object):
    pass

class Picture(object):
    pass

class Post(object):
    pass

class Tag(object):
    def __init__(self, tag): # xxx???  Liebert
        self.tag = tag

class TagOptions(object):
    pass
    
class Setting(object):
    pass

class LogEntry(object):
    pass

orm.mapper(Captcha, t_captchas)        
orm.mapper(LoginTracker, t_logins)    
orm.mapper(Oekaki, t_oekaki)
orm.mapper(Invite, t_invites)
orm.mapper(UserOptions, t_userOptions)
orm.mapper(UserFilters, t_userFilters)
orm.mapper(User, t_users, properties = {    
        'options' : orm.relation(UserOptions, uselist=False, backref='t_users', cascade="all, delete, delete-orphan"),
        'filters' : orm.relation(UserFilters, backref='t_users', cascade="all, delete") #, delete-orphan
    })

orm.mapper(Extension, t_extlist)

orm.mapper(Picture, t_piclist, properties = {
    'extlist' : orm.relation(Extension)
    })

orm.mapper(TagOptions, t_tagOptions)
orm.mapper(Tag, t_tags, properties = {
        'options' : orm.relation(TagOptions, uselist=False, backref='t_tags', cascade="all, delete, delete-orphan")
    })
orm.mapper(Post, t_posts, properties = {
    'tags' : orm.relation(Tag, secondary = t_tagsToPostsMap),
    'file': orm.relation(Picture, cascade="all, delete" ), #, delete-orphan
    'parentPost' : orm.relation(Post, remote_side=[t_posts.c.id]),
    })

orm.mapper(Setting, t_settings)

orm.mapper(LogEntry, t_log, properties = {
    'user' : orm.relation(User)
    })

#class TagMapping(object):
#    pass
#orm.mapper(TagMapping, t_tagsToPostsMap)


