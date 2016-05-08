import sys
import json
import time
from datetime import datetime

from models import Author, Comment, CommentParent, Subreddit, database

BATCH_SIZE = 1000

def insert(records):
    with database.atomic():
        for record in records:
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


def create_heirarchy():
    # Create the heirarchy between the Comments using a join
    pass


def insert_from_json(filepath):
    count = 0
    with open(filepath) as f:
        records = []
        for line in f:
            record = json.loads(line)
            records.append(record)
            if len(records) == BATCH_SIZE:
                insert(records)
                records.clear()
                print('Inserted records {} to {}'.format(
                    count - BATCH_SIZE + 1, 
                    count))
            count += 1
    return count


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('USAGE: python insert_from_json.py <json file path>')

    start = time.time()
    database.create_tables(
            [Author, Comment, CommentParent, Subreddit],
            safe=True
    )
    inserted = insert_from_json(sys.argv[1])
    end = time.time()
    elapsed = end - start 
    print('Inserted {} records in {}s'.format(inserted, elapsed))

