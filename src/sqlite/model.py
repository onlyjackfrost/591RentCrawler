from sqlite.connection import conn

conn.execute('''CREATE TABLE IF NOT EXISTS POST
       (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
       post_id         INT     NOT NULL,
       create_time    TEXT     DEFAULT (datetime('now'))
       );''')

print("Create Table successfully")