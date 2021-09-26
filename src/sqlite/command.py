from typing import List
from sqlite.connection import conn


def addPosts(post_list: List):
    sql_values = ', '.join([f'({post_id})' for post_id in post_list])
    print(sql_values)
    if sql_values:
        conn.execute(f'INSERT INTO POST (post_id) VALUES {sql_values}')
        conn.commit()


def make_table():
    import sqlite.model