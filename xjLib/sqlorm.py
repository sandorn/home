# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-03 23:26:06
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-14 23:47:26
__Author__ = 'Even.Sand'
'''
from xjLib.dBrouter import dbconf
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas


class MySQLConnection(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(MySQLConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, DBname='master'):
        if DBname not in dbconf:
            print('错误提示：检查数据库配置：' + DBname)
            # self.__del__()
            exit(1)

        _connect_info = 'mysql://{}:{}@{}:{}/{}?charset={}'.format(dbconf[DBname]['user'], dbconf[DBname]['passwd'], dbconf[DBname]['host'], dbconf[DBname]['port'], dbconf[DBname]['db'], dbconf[DBname]['charset'])
        try:
            self.engine = create_engine(_connect_info, encoding="utf-8", echo=True)
            self.metadata = MetaData(self.engine)  # 绑定元信息
            # 创建session对象:
            _DB_Session = sessionmaker(bind=self.engine)
            self.session = _DB_Session()
            print("获取数据库连接对象成功,连接池:{}".format(str(self.metadata)))
        except Exception as error:
            print('\033[create_engine Error:\n', error, ']\033', sep='')  # repr(error)
            return None  # raise  # exit(1)

    def __enter__(self):
        print("In __enter__()")
        return self

    def __exit__(self, args):
        self.__del__()
        print("In __exit__()")

    def __del__(self):
        # print("__del__方法被调用")
        if hasattr(self, 'session'):
            self.session.close()
        if hasattr(self, 'engine'):
            self.engine.dispose()

    def __str__(self):
        """返回一个对象的描述信息"""
        return 'sqlalchemy_mysql数据库对象'

    def workon(self, sql):
        try:
            self.session.execute(sql)
            self.session.commit()
            return True
        except Exception as error:
            self.session.ROLLBACK()
            print('\033[', error, ']\033', sep='')  # repr(error)
            return False, error

    def insert(self, dt):
        ls = [(k, dt[k]) for k in dt if dt[k] is not None]
        sql = 'insert %s (' % self.tb + ','.join([i[0] for i in ls]) + ') values (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        self.workon(sql)

    def update(self, dt_update, dt_condition, table):
        sql = 'UPDATE %s SET ' % table + ','.join(['%s=%r' % (k, dt_update[k]) for k in dt_update]) + ' WHERE ' + ' AND '.join(['%s=%r' % (k, dt_condition[k]) for k in dt_condition]) + ';'
        self.workon(sql)

    def ver(self):
        sql = "SELECT VERSION()"
        # 使用execute方法执行SQL语句
        _cur = self.engine.execute(sql)
        # _cur = self.conn.execute(sql)
        版本号 = _cur.fetchone()
        _cur.close()
        if 版本号:
            return 版本号
        else:
            return False

    def getAll(self, sql, args=[]):
        try:
            _cur = self.session.execute(sql, args)
            data = _cur.fetchall()
            _cur.close()
        except Exception as e:
            print(e)
        return data

    def getPt(self, sql):
        #  read_sql的两个参数: sql语句， 数据库连接
        pdtable = pandas.read_sql(sql, self.engine)
        if len(pdtable):
            # print('getable , ok')
            return pdtable
        else:
            return False

    def getDic(self, sql):
        _cur = self.engine.execute(sql)
        dic = _cur.fetchall()
        if len(dic):
            return dic
        else:
            return False


if __name__ == '__main__':
    myDb = MySQLConnection()
    print(myDb)
    if myDb:
        print("ver:", myDb.ver())
        sql = " select * from users ;"
        pdtable = myDb.getPt(sql)
        print("pdtable.values[1][1]:", pdtable.values[1][1])
        print("pdtable[1:2]:", pdtable[1:2])
        print("pdtable.iloc[0]:", pdtable.iloc[0])
        dic = myDb.getDic(sql)
        print('dic:', dic)
        data = myDb.getAll(sql)
        print('data:', data)
        print("data[0]:", data[0], "++++++++++data[1][1]:", data[1][1])
        del myDb
'''
    # 方式1
    res_1 = engine.execute(test_table.select())
    for re in res_1:
        # dosomething
    res_1.close()

    # 方式2
    conn = engine.connect()
    res_2 = conn.execute(test_table.select())
    for re in res_2:
        # dosomething
    res_2.close()

    # 方式3
    session_db = sessionmaker(bind=engine)
    session = session_db()
    res_3 = session.execute(test_table.select())
    for re in res_3:
        # dosomething
    session.close()

    class ThingOne(object):
    def go(self, session):
        session.query(FooBar).update({"x": 5})

class ThingTwo(object):
    def go(self, session):
        session.query(Widget).update({"q": 18})

def run_my_program():
    session = Session()
    try:
        ThingOne().go(session)
        ThingTwo().go(session)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
'''
