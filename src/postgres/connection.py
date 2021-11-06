import psycopg2


class PostgresBaseManager:
    def __init__(self):

        self.database = 'ddgqsob1cb7grd'
        self.user = 'numycwzotvesnu'
        self.password = 'fd2c43fca696a12eee0d80ee88eb6f7a8f654a2107670cab896c98936b3f6028'
        self.host = 'ec2-3-221-140-141.compute-1.amazonaws.com'
        self.port = '5432'
        self.conn = self.connectServerPostgresDb()

    def connectServerPostgresDb(self):
        """
        :return: 連接 Heroku Postgres SQL 認證用
        """
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