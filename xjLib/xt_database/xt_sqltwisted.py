# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-21 00:08:37
LastEditTime : 2024-08-20 14:19:36
FilePath     : /CODE/xjLib/xt_database/xt_sqltwisted.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from twisted.enterprise import adbapi
from twisted.internet import reactor
from xt_database.cfg import DB_CFG
from xt_database.xt_untilsql import make_insert_sql, make_update_sql


class SqlTwisted:
    def __init__(self, db_key="default", table_name=None):
        self.table_name = table_name
        if not hasattr(DB_CFG, db_key):
            raise ValueError(f"错误提示:检查数据库配置:{db_key}")
        cfg = DB_CFG[db_key].value
        cfg.pop("type", None)
        self.dbpool = adbapi.ConnectionPool("MySQLdb", **cfg)  # 'MySQLdb' , 'pymysql'
        reactor.callWhenRunning(self.close)

    def close(self):
        self.dbpool.close()
        reactor.stop()  # 终止reactor

    def perform_query_success(self, results):
        print("【perform_query 查询成功】:", results)

    def perform_query_failure(self, error):
        print("【perform_query 查询失败】:", error)

    # 异步执行SQL查询
    def perform_query(self, query):
        self.dbpool.runQuery(query).addCallbacks(
            self.perform_query_success, self.perform_query_failure
        )

    def query(self, sql):
        defer = self.dbpool.runInteraction(self._do_query, sql)
        defer.addBoth(self.handle_back, sql, "query")

    def insert(self, item, table_name=None):
        table_name = table_name or self.table_name
        defer = self.dbpool.runInteraction(self._do_insert, item, table_name)
        defer.addBoth(self.handle_back, item, "insert")

    def update(self, item, condition, table_name=None):
        table_name = table_name or self.table_name
        defer = self.dbpool.runInteraction(self._do_update, item, condition, table_name)
        defer.addBoth(self.handle_back, item, "update")

    def handle_back(self, result, item, *args):
        print(f"【SqlTwisted异步回调 [{args[0]}] 】: {result} | item:{item}")
        return result

    def _do_query(self, cursor, sql):
        cursor.execute(sql)  # self.dbpool 自带cursor
        return cursor.fetchall()

    def _do_insert(self, cursor, item, table_name):
        sql = make_insert_sql(item, table_name)
        return cursor.execute(sql)  # self.dbpool 自带cursor

    def _do_update(self, cursor, item, condition, table_name):
        sql = make_update_sql(item, condition, table_name)
        return cursor.execute(sql)


if __name__ == "__main__":
    SQ = SqlTwisted("TXbx", "users2")
    update_item = {"username": "刘新军"}
    insert_item = {
        "username": "刘新军99",
        "password": "234567",
        "手机": "13910118122",
        "代理人编码": "10008888",
        "会员级别": "SSS",
        "会员到期日": "9999-12-31 00:00:00",
    }
    sqlstr = ["select * from users2 where ID=2", "select * from users2"]
    # SQ.insert(insert_item, "users2")
    # SQ.update(update_item, {"ID": 2})
    # SQ.query(sqlstr)
    SQ.perform_query(sqlstr[1])
    reactor.run()
