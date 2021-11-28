import datetime
from postgres.connection import postgres_manager

conn = postgres_manager.conn


def addPosts(post_ids):
    create_time = datetime.datetime.utcnow()
    cur = conn.cursor()
    sql_values = ', '.join(
        [f'({post_id}, \'{create_time}\')' for post_id in post_ids])
    if sql_values:
        cur.execute(
            f'INSERT INTO POST (post_id, create_time) VALUES {sql_values}')
        conn.commit()


def get_post_ids(post_ids):
    cur = conn.cursor()
    val_str = ",".join([f'{id}' for id in post_ids])
    cur.execute(f'SELECT post_id FROM POST WHERE post_id IN ({val_str})')
    cursor = cur.fetchall()
    return [row[0] for row in cursor]


def get_all_post_id():
    cur = conn.cursor()
    cur.execute(f'SELECT post_id FROM POST')
    cursor = cur.fetchall()
    print('current number of post_id:', len(cursor))


def add_user(user_id):
    cur = conn.cursor()
    cur.execute(f'INSERT INTO Line_users (user_id) VALUES "{user_id}"')
    conn.commit()


def get_user_id():
    cur = conn.cursor()
    cur.execute(f'SELECT user_id FROM Line_users LIMIT 1')
    cursor = cur.fetchall()
    if not cursor:
        return None
    else:
        return cursor[0]['user_id']
