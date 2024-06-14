# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-21 00:08:37
LastEditTime : 2024-06-13 21:19:32
FilePath     : /CODE/xjLib/xt_DAO/xt_SqlTwisted.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from copy import deepcopy

from twisted.enterprise import adbapi
from twisted.internet import reactor
from xt_DAO.cfg import DB_CONFIG


class SqlTwisted:
    def __init__(self, key='default', table_name=None):
        self.table_name = table_name
        config = deepcopy(DB_CONFIG[key])
        if 'type' in config:
            config.pop('type')
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **config)  # 'MySQLdb' , 'pymysql'
        reactor.callWhenRunning(self.close)

    def close(self):
        self.dbpool.close()
        reactor.stop()  # 终止reactor

    def query_success(self, results):
        print('【perform_query 查询成功】:', results)

    def query_failure(self, error):
        print('【perform_query 查询失败】:', error)

    # 异步执行SQL查询
    def perform_query(self, query):
        self.dbpool.runQuery(query).addCallbacks(self.query_success, self.query_failure)

    def query(self, sql):
        defer = self.dbpool.runInteraction(self._do_query, sql)
        defer.addBoth(self.handle_back, sql, 'query')

    def insert(self, item, table_name=None):
        table_name = table_name or self.table_name
        defer = self.dbpool.runInteraction(self._do_insert, item, table_name)
        defer.addBoth(self.handle_back, item, 'insert')

    def update(self, item, condition, table_name=None):
        table_name = table_name or self.table_name
        defer = self.dbpool.runInteraction(self._do_update, item, condition, table_name)
        defer.addBoth(self.handle_back, item, 'update')

    def handle_back(self, result, item, *args):
        [arg] = args
        print(f'【SqlTwisted异步回调 [{arg}] 】: {result} | item:{item}')
        return result

    @staticmethod
    def get_insert_sql(item, table_name):
        cols = ', '.join(f'`{k}`' for k in item.keys())
        vals = ', '.join(f"'{v}'" for v in item.values())
        sql = f'INSERT INTO `{table_name}`({cols}) VALUES({vals})'
        return sql.replace('%', '%%')

    @staticmethod
    def get_update_sql(item, condition, table_name):
        item_kv = ', '.join([f"`{k}`='{item[k]}'" for k in item])
        cond_k = ', '.join([f'`{k}`' for k in condition.keys()])
        cond_v = ', '.join([f"'{v}'" for v in condition.values()])
        sql = f'UPDATE `{table_name}` SET {item_kv} WHERE ({cond_k})=({cond_v})'
        return sql.replace('%', '%%')

    def _do_query(self, cursor, sql):
        cursor.execute(sql)  # self.dbpool 自带cursor
        return cursor.fetchall()

    def _do_insert(self, cursor, item, table_name):
        sql = self.get_insert_sql(item, table_name)
        return cursor.execute(sql)  # self.dbpool 自带cursor

    def _do_update(self, cursor, item, condition, table_name):
        sql = self.get_update_sql(item, condition, table_name)
        return cursor.execute(sql)


if __name__ == '__main__':
    SQ = SqlTwisted('TXbx', 'users2')
    update_item = {'username': '刘新军'}
    insert_item = {'username': '刘新军99', 'password': '234567', '手机': '13910118122', '代理人编码': '10008888', '会员级别': 'SSS', '会员到期日': '9999-12-31 00:00:00'}
    sql = ''
    # SQ.insert(insert_item, 'users2')
    # SQ.update(update_item, {'ID': 2})
    SQ.query('select * from users2')
    SQ.perform_query('select * from users2')
    reactor.run()
