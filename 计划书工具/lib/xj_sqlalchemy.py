# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   xj_sqlalchemy.py
@Time    :   2019/04/29 12:04:12
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas
import db_router
dbr = db_router.DBSERVER


class MysqlHelp:

    def __new__(cls, *args, **kwargs):
        #print("__new__方法被调用")
        return object.__new__(cls)

    def __init__(self, name='default'):

        if name not in dbr:
            print('错误提示：\n        检查数据库路由名称！')
            #self.__del__()
            exit(1)

        _connect_info = 'mysql://{}:{}@{}:{}/{}?charset={}'.format(
            dbr[name]['user'], dbr[name]['passwd'], dbr[name]['host'],
            dbr[name]['port'], dbr[name]['db'], dbr[name]['charset'])
        try:
            self.engine = create_engine(
                _connect_info, encoding="utf-8", echo=True)
            self.metadata = MetaData(self.engine)  # 绑定元信息
            # 创建session对象:
            _DB_Session = sessionmaker(bind=self.engine)
            self.session = _DB_Session()
        except Exception as error:
            print(
                '\033[create_engine Error:\n', error, ']\033',
                sep='')  # repr(error)
            return None  # raise  # exit(1)

    def __del__(self):
        #print("__del__方法被调用")
        if hasattr(self, 'session'):
            self.session.close()
        if hasattr(self, 'engine'):
            self.engine.dispose()

    def __str__(self):
        """返回一个对象的描述信息"""
        # print(num)
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
        sql = 'insert %s (' % self.tb + ','.join([
            i[0] for i in ls
        ]) + ') values (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        self.workon(sql)

    def update(self, dt_update, dt_condition, table):
        sql = 'UPDATE %s SET ' % table + ','.join([
            '%s=%r' % (k, dt_update[k]) for k in dt_update
        ]) + ' WHERE ' + ' AND '.join(
            ['%s=%r' % (k, dt_condition[k]) for k in dt_condition]) + ';'
        self.workon(sql)

    def ver(self):
        sql = "SELECT VERSION()"
        # 使用execute方法执行SQL语句
        _cur = self.engine.execute(sql)
        #_cur = self.conn.execute(sql)
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


def getVer(db_name):
    #  使用execute执行SQL语句
    _cur = db_name.session.execute("SELECT VERSION()")
    #  使用 fetchone() 方法获取一条数据库。
    版本号 = _cur.fetchone()
    if 版本号:
        return 版本号
    else:
        return False


if __name__ == '__main__':
    myDb = MysqlHelp()
    print(myDb)
    if myDb:
        print("ver:", myDb.ver())
        print("getVer:", getVer(myDb))
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
