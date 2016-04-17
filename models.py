from peewee import *


class Subreddit(Model):
    reddit_id = CharField()
    name = CharField()


class Author(Model):
    name = CharField()
    comments = IntegerField()


class Comment(Model):
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


class CommentParent(Model):
    comment_id = ForeignKeyField(Comment)
    parent_comment_id = ForeignKeyField(Comment)

