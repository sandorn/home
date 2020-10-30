# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2019-05-03 23:26:06
#FilePath     : /xjLib/xt_DAO/xt_mysql.py
#LastEditTime : 2020-07-08 20:40:16
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import MySQLdb
import pandas
import pymysql
from copy import deepcopy
from .dbconf import db_conf


class engine(object):
    """
    mysql数据库对象，参数：db_name , odbc
    可选驱动：[mysql.connector 出错禁用]、[pymysql]、[MySQLdb]
    """
    def __init__(self, key='default', odbc='MySQLdb'):
        self.db_name = key
        self.odbc = odbc
        if key not in db_conf:
            raise ('错误提示：检查数据库配置：' + self.db_name)
        else:
            self.conf = deepcopy(db_conf[self.db_name])

        if 'type' in self.conf: self.conf.pop('type')

        try:
            if odbc == 'pymysql':
                self.conn = pymysql.connect(**self.conf)
                self.DictCursor = pymysql.cursors.DictCursor
            else:  # mysqlclient
                self.conn = MySQLdb.connect(**self.conf)
                self.DictCursor = MySQLdb.cursors.DictCursor
            # self.conn.autocommit(True)  # #自动提交
        except Exception as error:
            print(f'{self.odbc} connect<{self.db_name}> error:{repr(error)}')
            return None  # raise  # exit(1)
        else:
            self.cur = self.conn.cursor()
            print(f'{self.odbc}  connect<{self.db_name}> Ok!')

    '''
    对with的处理:所求值的对象必须有一个__enter__()方法，一个__exit__()方法。
    跟with后面的语句被求值后，返回对象的__enter__()方法被调用，这个方法的返回值将被赋值给as后面的变量。当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。
    '''

    def __enter__(self):
        print(f"{ self.odbc}\t{self.db_name}\tIn __enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with自动调用,不必调用del"""
        print(f"{ self.odbc}\t{self.db_name}\tIn __exit__()")
        if exc_tb is not None:
            print(f'exc_type:{exc_type}, exc_val:{exc_val}, exc_tb:{exc_tb}')

    def __del__(self):
        print(f"{ self.odbc}\t{self.db_name}\tIn __del__()")
        '''hasattr(self, 'conn')'''
        if self.odbc != 'connector':
            self.cur.close()
        self.conn.close()

    def __str__(self):
        """返回一个对象的描述信息"""
        return f'mysql数据库对象，<odbc：[{self.odbc}],db_name:[{self.db_name}] >\n可选驱动：[[pymysql | MySQLdb]；默认[MySQLdb]。'

    def has_tables(self, table_name):
        """判断数据库是否包含某个表,包含返回True"""
        self.cur.execute("show tables")
        tablerows = self.cur.fetchall()
        if len(tablerows) == 0:
            return False
        for rows in tablerows:
            if rows[0] == table_name:
                return True
        return False

    def close(self):
        pass

    def worKon(self, sql, args=None):
        args = args or []
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as error:
            self.conn.rollback()
            print(f'\033[{error}]\033', f'sql:{sql}', sep='')
            return False

    def insertMany(self, datas, tb_name, keys=None):
        if not isinstance(datas, (list, tuple)):
            raise "must send list|tuple object for me"

        if keys is None: keys = [k for k in datas[0].keys()]
        cols = ", ".join("`{}`".format(k) for k in keys)
        val_cols = ", ".join("%({})s".format(k) for k in keys)
        sql = "insert into `%s`(%s) values(%s)"
        res_sql = sql % (tb_name, cols, val_cols)

        try:
            self.cur.executemany(res_sql, datas)
            self.conn.commit()
            return True
        except Exception as error:
            self.conn.rollback()
            print(f'\033[{error}]\033', f'sql:{res_sql}', sep='')
            return False

    def insert(self, data, tb_name):
        cols = ", ".join("`{}`".format(k) for k in data.keys())
        val_cols = ", ".join("'{}'".format(v) for v in data.values())
        res_sql = f"insert into `{tb_name}`({cols}) values({val_cols})"
        self.worKon(res_sql.replace('%', '%%'))

    def update(self, dt_update, dt_condition, tb_name):
        # dt_update,更新的数据
        # dt_condition，匹配的数据
        # tb_name,表名
        sql = 'UPDATE %s SET ' % tb_name + ','.join(['%s=%r' % (k, dt_update[k]) for k in dt_update]) + ' WHERE ' + ' AND '.join(['%s=%r' % (k, dt_condition[k]) for k in dt_condition]) + ';'
        self.worKon(sql)

    def ver(self):
        sql = "SELECT VERSION()"
        #  使用execute方法执行SQL语句
        self.cur.execute(sql)
        #  使用 fetchone() 方法获取一条数据库。
        _版本号 = self.cur.fetchone()
        if _版本号:
            return _版本号[0]
        else:
            return False

    def get_all_from_db(self, form_name, args=[]):
        sql = f" select * from {form_name}"
        try:
            self.cur.execute(sql, args)
            data = self.cur.fetchall()
        except Exception as e:
            print(e)
        return data

    def get_pd_table(self, sql):
        sql = "select * from " + sql
        pdtable = pandas.read_sql(sql, self.conn)  # !第二个参数为数据库连接
        if len(pdtable):
            return pdtable
        else:
            return False

    def get_dict(self, sql):
        # 重新定义游标格式
        if self.DictCursor is None:
            self.cursorDict = self.conn.cursor(dictionary=True)
            # #mysql.connector独有
        else:
            self.cursorDict = self.conn.cursor(self.DictCursor)

        self.cursorDict.execute(sql)
        dic = self.cursorDict.fetchall()
        if dic:
            return dic
        else:
            return False
