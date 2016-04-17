import sys
import json
from datetime import datetime

from models import Author, Comment, CommentParent, Subreddit, database

def insert(record):
    subreddit, _ = Subreddit.create_or_get(reddit_id=record['subreddit_id'],
                                           name=record['subreddit'])
    author, _ = Author.create_or_get(name=record['author'])
    author.comments += 1
    author.save()

    comment = Comment.create(reddit_id=record['id'],
                             reddit_name=record['name'],
                             subreddit=subreddit.id,
                             author=author.id,
                             parent_id=record['parent_id'],
                             link_id=record['link_id'],
                             created_utc=datetime.fromtimestamp(
                                 int(record['created_utc'])),
                             ups=record['ups'],
                             downs=record['downs'],
                             score=record['score'],
                             body=record['body'])

    parent = (Comment
                .select()
                .where(Comment.reddit_name == comment.parent_id)
                .first())
    parent_id = parent.id if parent else None
    CommentParent.create(comment=comment.id, parent_comment=parent_id)


def insert_from_json(filepath):
    count = 0
    with open(filepath) as f:
        for line in f:
            record = json.loads(line)
            insert(record)
            count += 1
    return count


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('USAGE: python insert_from_json.py <json file path>')

    database.create_tables(
            [Author, Comment, CommentParent, Subreddit],
            safe=True
    )
    inserted = insert_from_json(sys.argv[1])
    print('Inserted {} records'.format(inserted))

