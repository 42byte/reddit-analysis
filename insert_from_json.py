import functools
import json
import multiprocessing
import sys
import time
from datetime import datetime

from models import Author, Comment, CommentParent, Subreddit, database


BATCH_SIZE = 5000


def insert(records):
    with database.execution_context():
        Comment.insert_many(records).execute()


def make_comment_dict(record):
    return dict(reddit_id=record['id'],
                reddit_name=record['name'],
                subreddit=None,
                author=None,
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
    records = []
    with open(filepath) as f:
        with multiprocessing.Pool() as p:
            for line in f:
                records.append(make_comment_dict(json.loads(line)))
                if len(records) == BATCH_SIZE:
                    msg = ('Inserted records {} to {}'
                            .format(count - BATCH_SIZE + 1, count))
                    callback = functools.partial(print, msg)
                    p.apply_async(insert, (records,), callback=callback)
                    records = []
                count += 1
            p.close()
            p.join()
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

