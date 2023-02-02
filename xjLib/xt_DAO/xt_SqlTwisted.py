# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-21 00:08:37
LastEditTime : 2023-02-02 11:52:27
FilePath     : /CODE/xjLib/xt_DAO/xt_SqlTwisted.py
Github       : https://github.com/sandorn/home
==============================================================
insert update不能连续运行,因为第一个执行完reactor.stop()就停止了
'''

from copy import deepcopy

from twisted.enterprise import adbapi
from twisted.internet import reactor
from xt_DAO.cfg import DB_CONFIG


class SqlTwisted(object):

    def __init__(self, key='default'):
        config = deepcopy(DB_CONFIG[key])
        if 'type' in config: config.pop('type')
        # cp_reconnect=True  #连接持久化
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **config)  # 'MySQLdb'  'pymysql'

    def close(self):
        self.dbpool.close()

    def insert(self, item, table_name):
        defer = self.dbpool.runInteraction(self._do_insert, item, table_name)
        defer.addBoth(self.handle_back, item)
        reactor.run()
        return defer.result  # 返回回调结果

    def update(self, item, condition, table_name):
        defer = self.dbpool.runInteraction(self._do_update, item, condition, table_name)
        defer.addBoth(self.handle_back, item)
        reactor.run()
        return defer.result  # 返回回调结果

    def handle_back(self, result, item):
        print(f'SqlTwisted 异步回调 | {result} | item:{item}')
        # reactor.callWhenRunning(lambda: reactor.stop())  # 终止reactor
        # reactor.calllater(0.1, reactor.stop())  # 终止reactor
        reactor.stop()  # 终止reactor
        return result

    @staticmethod
    def get_insert_sql(item, table_name):
        cols = ", ".join(f"`{k}`" for k in item.keys())
        vals = ", ".join(f"'{v}'" for v in item.values())
        sql = f"INSERT INTO `{table_name}`({cols}) VALUES({vals})"
        return sql.replace('%', '%%')

    @staticmethod
    def get_update_sql(item, condition, table_name):
        item_kv = ", ".join([f"`{k}`='{item[k]}'" for k in item])
        cond_k = ", ".join([f"`{k}`" for k in condition.keys()])
        cond_v = ", ".join([f"'{v}'" for v in condition.values()])
        sql = f"UPDATE `{table_name}` SET {item_kv} WHERE ({cond_k})=({cond_v})"
        return sql.replace('%', '%%')

    def _do_insert(self, cursor, item, table_name):
        sql = self.get_insert_sql(item, table_name)
        return cursor.execute(sql)

    def _do_update(self, cursor, item, condition, table_name):
        sql = self.get_update_sql(item, condition, table_name)
        return cursor.execute(sql)


if __name__ == "__main__":
    engine = SqlTwisted('TXbx')
    item = {'username': '刘新军123'}
    item1 = {'username': '刘新军', 'password': '234567', '手机': '13910118122', '代理人编码': '10008888', '会员级别': 'SSS', '会员到期日': '9999-12-31 00:00:00'}
    # ress = engine.insert(item1, 'users2')
    # print(ress)
    ress = engine.update(item, {'ID': 2}, 'users2')
    print(ress)
