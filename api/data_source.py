import pymysql
from dbutils.pooled_db import PooledDB


class DbClient:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=1,
            maxcached=1,
            blocking=True,
            host=...,
            port=...,
            user=...,
            password=...,
            database=...,
            charset='utf8mb4'
        )

    def get_conn(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    def query(self, sql):
        conn, cur = self.get_conn()
        try:
            cur.execute(sql)
            conn.commit()
            return cur.fetchall()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
