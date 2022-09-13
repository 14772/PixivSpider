import pymysql
from DBUtils.PooledDB import PooledDB

from config import db_config


class DbClient:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=1,
            maxcached=1,
            blocking=True,
            **db_config
        )

    def get_conn(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    def insert(self, data):
        sql = "INSERT INTO collect(pid, title, urls, tags, uid, author, width, height, page_count, r18) VALUES (%s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        conn, cur = self.get_conn()
        try:
            cur.execute(sql, data)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()
