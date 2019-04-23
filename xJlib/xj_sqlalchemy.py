#！/usr/bin/env python
#-*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   sql交互--sqlalchemy.py
@Time    :   2019/04/15 18:52:43
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas
import database_router


class MysqlHelp:

    def __init__(self, name='default'):
        connect_info = 'mysql://{}:{}@{}:{}/{}?charset={}'.format(
            database_router.DBSERVER[name]['user'],
            database_router.DBSERVER[name]['passwd'],
            database_router.DBSERVER[name]['host'],
            database_router.DBSERVER[name]['port'],
            database_router.DBSERVER[name]['db'],
            database_router.DBSERVER[name]['charset'])
        try:
            self.engine = create_engine(
                connect_info, encoding="utf-8", echo=True)
            # 创建session对象:
            _DB_Session = sessionmaker(bind=self.engine)
            self.session = _DB_Session()
        except Exception as error:
            print(
                '\033[create_engine Error:\n', error, ']\033',
                sep='')  # repr(error)
            raise
            exit(1)

    def __del__(self):
        self.session.close()
        self.engine.dispose()

    def close(self):
        self.session.close()
        self.engine.dispose()

    def workon(self, sql):
        try:
            self.session.execute(sql)
            self.session.commit()
            return True
        except Exception as error:
            self.session.ROLLBACK()
            print('\033[', error, ']\033', sep='')  # repr(error)
            return False, e

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
    print("ver:", myDb.ver())
    print("getVer:", getVer(myDb))
    sql = " select * from users ;"
    pdtable = myDb.getPt(sql)
    print("pdtable.values[1][1]:", pdtable.values[1][1])
    print("pdtable[1:2]:", pdtable[1:2])
    print("pdtable.iloc[0]:", pdtable.iloc[0])
    data = myDb.getAll(sql)
    print(data)
    print("data[0]:", data[0], "++++++++++data[1][1]:", data[1][1])
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
