from datetime import datetime
from typing import List
from sqlite.connection import conn


def addPosts(post_ids: List):
    create_time = datetime.utcnow()
    sql_values = ', '.join(
        [f'({post_id}, \'{create_time}\')' for post_id in post_ids])
    if sql_values:
        conn.execute(
            f'INSERT INTO POST (post_id, create_time) VALUES {sql_values}')
        conn.commit()


def get_post_ids(post_ids):
    val_str = ",".join([f'"{id}"' for id in post_ids])
    cursor = conn.execute(
        f'SELECT post_id FROM POST WHERE post_id in ({val_str})')
    return [row[0] for row in cursor]


def make_table():
    import sqlite.model
