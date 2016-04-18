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
    comments = IntegerField(default=0)


class Comment(BaseModel):
    reddit_id = CharField()
    reddit_name = CharField()
    subreddit = ForeignKeyField(Subreddit)
    author = ForeignKeyField(Author)
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

