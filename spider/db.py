import pymysql
from dbutils.pooled_db import PooledDB, PooledSharedDBConnection, PooledDedicatedDBConnection

from config import db_config


class DbClient:
    def __init__(self):
        """
        初始化数据库连接池，配置在config.py中
        """
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=1,
            maxcached=1,
            blocking=True,
            **db_config
        )

    def get_conn(self) -> tuple[PooledSharedDBConnection, PooledDedicatedDBConnection]:
        """
        获取数据库连接\n
        :return: (conn, cur)
        """
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    def insert(self, data):
        """
        插入数据\n
        :param data: 数据 (pid, title, urls, tags, uid, author, width, height, page_count, r18)
        """
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

    def query(self, pid) -> int:
        """
        查询指定pid是否存在\n
        :param pid: pid
        :return: 1 or 0
        """
        conn, cur = self.get_conn()
        try:
            cur.execute("SELECT COUNT(*) FROM collect WHERE pid = %s", pid)
        except Exception as e:
            print(e)
            conn.rollback()
        else:
            res = cur.fetchall()
            return res[0][0]
        finally:
            cur.close()
            conn.close()
