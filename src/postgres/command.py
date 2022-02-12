import datetime
from postgres.connection import postgres_manager

pool = postgres_manager.pool


def addPosts(post_ids):
    create_time = datetime.datetime.utcnow()
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        sql_values = ', '.join(
            [f'({post_id}, \'{create_time}\')' for post_id in post_ids])
        if sql_values:
            cur.execute(
                f'INSERT INTO POST (post_id, create_time) VALUES {sql_values}')
            conn.commit()
    finally:
        pool.putconn(conn)


def get_post_ids(post_ids):
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        val_str = ",".join([f'{id}' for id in post_ids])
        cur.execute(f'SELECT post_id FROM POST WHERE post_id IN ({val_str})')
        cursor = cur.fetchall()
    finally:
        pool.putconn(conn)
    return [row[0] for row in cursor]


def get_all_post_id():
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT post_id FROM POST')
        cursor = cur.fetchall()
        print('current number of post_id:', len(cursor))
    finally:
        pool.putconn(conn)


def add_user(user_id):
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(f'INSERT INTO Line_users (user_id) VALUES (\'{user_id}\')')
        conn.commit()
    finally:
        pool.putconn(conn)


def get_user_id():
    conn = pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM Line_users LIMIT 1')
        cursor = cur.fetchall()
    finally:
        pool.putconn(conn)

    if not cursor:
        return None
    else:
        return [row[0] for row in cursor]
