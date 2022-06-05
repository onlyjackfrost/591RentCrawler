import os

from psycopg2 import pool


class PostgresBaseManager:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        database = os.getenv('POSTGRES_DATABASE', None)
        user = os.getenv('POSTGRES_USER', None)
        password = os.getenv('POSTGRES_PASSWORD', None)
        host = os.getenv('POSTGRES_host', None)
        port = '5432'
        database_url = os.getenv('DATABASE_URL', None)
        # self.conn = self.connectServerPostgresDb()
        self.pool = self.createPool(database=database,
                                    user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database_url=database_url)

    def createPool(self, database, user, password, host, port, database_url):
        """
        :return: 連接 Heroku Postgres SQL 認證用
        """
        if database_url:
            print('connection with url')
            pq_pool = pool.SimpleConnectionPool(
                1,
                10,
                database_url,
                sslmode='require',minconn=2, maxconn=5
            )

        else:
            print('connection with user')
            pq_pool = pool.SimpleConnectionPool(1,10,
                                                database=database,
                                                user=user,
                                                password=password,
                                                host=host,
                                                port=port)
        return pq_pool


postgres_manager = PostgresBaseManager()


def runTest():
    """
    :return: 測試是否可以連線到 Heroku Postgres SQL
    """
    conn = postgres_manager.pool.getconn()
    # test
    cur = conn.cursor()
    cur.execute('SELECT VERSION()')
    results = cur.fetchall()
    print("Database version : {0} ".format(results))
    conn.commit()
    cur.close()

    postgres_manager.pool.putconn(conn)


def initSchema(self):
    conn = postgres_manager.pool.getconn()
    # create schema
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS POST(
            id serial PRIMARY KEY,
            post_id INT NOT NULL,
            create_time TIMESTAMP 
        );''')
    # cur.execute('''
    #     CREATE INDEX idx_POST_post_id
    #     ON POST(post_id);
    #     ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Line_users(
            id serial PRIMARY KEY,
            user_id VARCHAR(300) NOT NULL UNIQUE,
            create_time TIMESTAMP
        )
    ''')
    self.conn.commit()
    print('database schema initialization done')
    cur.close()

    postgres_manager.pool.putconn(conn)


if __name__ == '__main__':
    postgres_manager = PostgresBaseManager()
    postgres_manager.runTest()
    postgres_manager.initSchema()
    postgres_manager.closePostgresConnection()