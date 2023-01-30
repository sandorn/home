# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-21 00:08:37
LastEditTime : 2023-01-24 20:59:03
FilePath     : /CODE/xjLib/xt_DAO/xt_SqlTwisted.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from copy import deepcopy

from twisted.enterprise import adbapi
from xt_DAO.cfg import DB_CONFIG


class SqlTwisted(object):

    def __init__(self, key='default'):
        config = deepcopy(DB_CONFIG[key])
        if 'type' in config: config.pop('type')
        # cp_reconnect=True  #连接持久化
        self.dbpool = adbapi.ConnectionPool('pymysql', **config)
        # "MySQLdb"
    def close(self):
        self.dbpool.close()

    def run(self, sql):
        defer = yield self.dbpool.runQuery(sql)
        defer.addErrback(self.handle_error, sql)

    def insert(self, item, table_name):
        defer = self.dbpool.runInteraction(self._do_insert, item, table_name)
        defer.addErrback(self.handle_error, item)  # 处理异常

    def update(self, item, condition, table_name):
        defer = self.dbpool.runInteraction(self._do_update, item, condition, table_name)
        defer.addErrback(self.handle_error, item)  # 处理异常

    def handle_error(self, failure, item):
        print(f'SqlTwisted 异步操作异常 | {failure} | item:{item}')

    @staticmethod
    def get_update_sql(item, condition, table_name):
        #@ sql语句表名、字段名均需用``表示
        item_kv = ", ".join([f"`{k}`='{item[k]}'" for k in item])
        cond_kv = ", ".join([f"`{k}`='{condition[k]}'" for k in condition])
        sql = f"UPDATE `{table_name}` SET {item_kv} WHERE {cond_kv}"
        return sql.replace('%', '%%')

    @staticmethod
    def get_insert_sql(item, table_name):
        #@ sql语句表名、字段名均需用``表示
        cols = ", ".join(f"`{k}`" for k in item.keys())
        vals = ", ".join(f"'{v}'" for v in item.values())
        sql = f"insert into `{table_name}`({cols}) values({vals})"
        return sql.replace('%', '%%')

    def _do_insert(self, cursor, item, table_name):
        sql = self.get_insert_sql(item, table_name)
        return cursor.execute(sql)

    def _do_update(self, cursor, item, condition, table_name):
        sql = self.get_update_sql(item, condition, table_name)
        return cursor.execute(sql)


if __name__ == "__main__":
    from twisted.internet import reactor
    engine = SqlTwisted('TXbx')
    item = {'username': '刘新军'}
    item1 = {'ID': 2, 'username': '刘新军', 'password': '234567', '手机': '13910118122', '代理人编码': '10005393', '会员级别': 'SSS', '会员到期日': '9999-12-31 00:00:00'}
    e = engine.run('SELECT * from `users2`')
    print(e)
    # engine.insert(item1, 'users2')
    # engine.update(item, {'ID': 2}, 'users2')
    # reactor.suggestThreadPoolSize(8)
    # reactor.callLater(0.01, reactor.stop)
    # reactor.callWhenRunning(work)
    reactor.run()
