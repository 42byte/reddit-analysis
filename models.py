from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase


database = PooledPostgresqlExtDatabase(
            'postgres',
            max_connections=32,
            stale_timeout=300,  # 5 minutes.
            host='localhost', 
            port=8888,
            user='postgres', 
            register_hstore=False)


class BaseModel(Model):
    class Meta:
        database = database


class Subreddit(BaseModel):
    reddit_id = CharField()
    name = CharField()


class Author(BaseModel):
    name = CharField()
    comments = IntegerField(default=0)


class Comment(BaseModel):
    reddit_id = CharField()
    reddit_name = CharField()
    subreddit = ForeignKeyField(Subreddit, null=True)
    author = ForeignKeyField(Author, null=True)
    parent_id = CharField()
    link_id = CharField()
    created_utc = DateTimeField()
    ups = IntegerField()
    downs = IntegerField()
    score = IntegerField()
    body = TextField()


class CommentParent(BaseModel):
    comment = ForeignKeyField(Comment, related_name='comment')
    parent_comment = ForeignKeyField(Comment, null=True,
                                     related_name='parent_comment')

