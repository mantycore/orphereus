import sqlalchemy as sa
from sqlalchemy import orm
from fc.model import meta
def init_model(engine):
    sm = orm.sessionmaker(autoflush=True, transactional=True, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

t_posts = sa.Table("posts", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("parentid", sa.types.Integer, nullable=False),
    sa.Column("message", sa.types.UnicodeText, nullable=True),
    sa.Column("date", sa.types.Date, nullable=False),
    sa.Column("last_date", sa.types.Date, nullable=True)
    )

t_tags = sa.Table("tags", meta.metadata,
    sa.Column("id", sa.types.Integer, primary_key=True),
    sa.Column("tag", sa.types.UnicodeText, nullable=False)
    )

t_post_tags = sa.Table("post_tags", meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('post_id', sa.types.Integer, sa.ForeignKey('posts.id')),
    sa.Column('tag_id', sa.types.Integer, sa.ForeignKey('tags.id'))
    )

class Post(object):
    pass

class Tag(object):
    def __init__(self, tag):
        self.tag = tag

orm.mapper(Tag, t_tags, properties = {
    'posts' : orm.relation(Post, secondary = t_post_tags)
    })
orm.mapper(Post, t_posts, properties = {
    'tags' : orm.relation(Tag, secondary = t_post_tags)
    })
