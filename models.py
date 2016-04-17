from peewee import *

database = SqliteDatabase('reddit_comments.db')


class BaseModel(Model):
    class Meta:
        database = database


class Subreddit(BaseModel):
    reddit_id = CharField()
    name = CharField()


class Author(BaseModel):
    name = CharField()
    comments = IntegerField()


class Comment(BaseModel):
    reddit_id = CharField()
    reddit_name = CharField()
    subreddit_id = ForeignKeyField(Subreddit)
    parent_id = CharField()
    link_id = CharField()
    author_id = ForeignKeyField(Author)
    created_utc = DateTimeField()
    ups = IntegerField()
    downs = IntegerField()
    score = IntegerField()
    body = CharField()


class CommentParent(BaseModel):

