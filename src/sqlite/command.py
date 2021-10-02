from datetime import datetime, timedelta
import pprint
from typing import List
from sqlite.connection import conn


def addPosts(post_list: List):
    create_time = datetime.utcnow()
    sql_values = ', '.join(
        [f'({post_id}, \'{create_time}\')' for post_id in post_list])
    if sql_values:
        conn.execute(
            f'INSERT INTO POST (post_id, create_time) VALUES {sql_values}')
        conn.commit()


def get_post_id_in_hours():
    create_time = datetime.utcnow() - timedelta(hours=1)
    cursor = conn.execute(
        f'SELECT post_id FROM POST WHERE create_time >= \'{create_time}\'')
    return [row[0] for row in cursor]


def make_table():
    import sqlite.model
