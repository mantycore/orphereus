import sqlalchemy as sa
from sqlalchemy import orm
from fc.model import meta
def init_model(engine):
    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

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
    sa.Column("bantime"  , sa.types.Integer, nullable=False),
    sa.Column("banreason", sa.types.String(256), nullable=True),
    sa.Column("isAdmin"  , sa.types.Boolean, nullable=True),
    sa.Column("canDeleteAllPosts", sa.types.Boolean, nullable=True),
    sa.Column("canMakeInvite", sa.types.Boolean, nullable=True),   
    sa.Column("canChangeRights", sa.types.Boolean, nullable=True)
    )
t_userFilters = sa.Table("userFilters", meta.metadata,
    sa.Column("id"    ,sa.types.Integer, primary_key=True),
    sa.Column("uidNumber",sa.types.Integer, sa.ForeignKey('users.uidNumber')),
    sa.Column("filter"    , sa.types.String(64), nullable=False)
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
    sa.Column("path"     , sa.types.String(255), nullable=False)
    )

t_posts = sa.Table("posts", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("parentid" , sa.types.Integer, nullable=False),
    sa.Column("message"  , sa.types.UnicodeText, nullable=True),
    sa.Column("messageShort", sa.types.UnicodeText, nullable=True),
    sa.Column("title"    , sa.types.UnicodeText, nullable=True),
    sa.Column("sage"     , sa.types.Boolean, nullable=True),
    sa.Column("uidNumber",sa.types.Integer,nullable=True),
    sa.Column("picid"    , sa.types.Integer, sa.ForeignKey('piclist.id')),
    sa.Column("date"     , sa.types.DateTime, nullable=False),
    sa.Column("bumpDate", sa.types.DateTime, nullable=True),
    sa.Column("spoiler"  , sa.types.Boolean, nullable=True)   
    )

t_tags = sa.Table("tags", meta.metadata,
    sa.Column("id"       , sa.types.Integer, primary_key=True),
    sa.Column("tag"      , sa.types.UnicodeText, nullable=False)
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
    sa.Column("enableSpoilers", sa.types.Boolean, nullable=False)
    )

t_tagsToPostsMap = sa.Table("tagsToPostsMap", meta.metadata,
    #sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('postId'  , sa.types.Integer, sa.ForeignKey('posts.id')),
    sa.Column('tagId'   , sa.types.Integer, sa.ForeignKey('tags.id')),
    sa.Column('isMain'  , sa.types.Boolean, nullable=True)
    )
    
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

orm.mapper(Oekaki, t_oekaki)
orm.mapper(Invite, t_invites)
orm.mapper(UserOptions, t_userOptions)
orm.mapper(UserFilters, t_userFilters)
orm.mapper(User, t_users, properties = {    
        'options' : orm.relation(UserOptions, uselist=False, backref='t_users'),
        'filters' : orm.relation(UserFilters)
    })

orm.mapper(Extension, t_extlist)
orm.mapper(Picture, t_piclist, properties = {
    'extlist' : orm.relation(Extension)
    })
orm.mapper(TagOptions, t_tagOptions)
orm.mapper(Tag, t_tags, properties = {
        'options' : orm.relation(TagOptions, uselist=False, backref='t_tags')
    })
orm.mapper(Post, t_posts, properties = {
    'tags' : orm.relation(Tag, secondary = t_tagsToPostsMap),
    'file': orm.relation(Picture)
    })

orm.mapper(Setting, t_settings)
orm.mapper(LogEntry, t_log, properties = {
    'user' : orm.relation(User)
    })