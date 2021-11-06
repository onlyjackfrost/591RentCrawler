import psycopg2
import os


class PostgresBaseManager:
    def __init__(self):
        self.database = os.getenv('POSTGRES_DATABASE', None)
        self.user = os.getenv('POSTGRES_USER', None)
        self.password = os.getenv('POSTGRES_PASSWORD', None)
        self.host = os.getenv('POSTGRES_host', None)
        self.port = '5432'
        self.database_url = os.getenv('DATABASE_URL', None)
        self.conn = self.connectServerPostgresDb()

    def connectServerPostgresDb(self):
        """
        :return: 連接 Heroku Postgres SQL 認證用
        """
        if self.database_url:
            print('connection with url')
            conn = psycopg2.connect(self.database_url, sslmode='require')
        else:
            print('connection with user')
            conn = psycopg2.connect(database=self.database,
                                    user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port)
        return conn

    def closePostgresConnection(self):
        """
        :return: 關閉資料庫連線使用
        """
        self.conn.close()

    def runTest(self):
        """
        :return: 測試是否可以連線到 Heroku Postgres SQL
        """
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()

    def initSchema(self):
        cur = self.conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS POST(
                id serial PRIMARY KEY,
                post_id INT NOT NULL,
                create_time TIMESTAMP 
            );''')
        cur.execute('''
            CREATE INDEX idx_POST_post_id 
            ON POST(post_id);
            ''')
        self.conn.commit()
        print('database schema initialization done')
        cur.close()


postgres_manager = PostgresBaseManager()

if __name__ == '__main__':
    postgres_manager = PostgresBaseManager()
    postgres_manager.runTest()
    postgres_manager.initSchema()
    postgres_manager.closePostgresConnection()