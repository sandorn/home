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
@LastEditors: Even.Sand
@LastEditTime: 2020-04-03 19:33:12
'''

from .dbRouter import db_conf
import MySQLdb  # mysqlclient
import pymysql
import pandas
import mysql.connector


class SqlHelper(object):
    '''
    def __new__(cls, *args, **kwargs):
        print("In __new__()")
        # #单实例模式
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    '''

    def __init__(self, dbName='default', odbc='mysqlclient'):
        self.dbName = dbName
        self.odbc = odbc

        if dbName not in db_conf:
            raise('错误提示：检查数据库配置：' + dbName)

        _dbconf = db_conf[dbName]
        if 'type' in _dbconf:
            _dbconf.pop('type')

        try:
            if odbc == 'connector':
                self.conn = mysql.connector.connect(**_dbconf)
            elif odbc == 'pymysql':
                self.conn = pymysql.connect(**_dbconf)
            else:   # mysqlclient
                self.conn = MySQLdb.connect(**_dbconf)

            self.cur = self.conn.cursor()
            #! pandasData = pandas.read_sql(sql, connect.conn)  # 读MySQL数据,connect.conn
            print("获取数据库连接对象成功,连接池:{}".format(str(self.conn)))
        except Exception as error:
            print('\033[connect Error:\n', error, ']\033', sep='')  # repr(error)
            return None  # raise  # exit(1)

    '''
    对with的处理:所求值的对象必须有一个__enter__()方法，一个__exit__()方法。
    跟with后面的语句被求值后，返回对象的__enter__()方法被调用，这个方法的返回值将被赋值给as后面的变量。当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。
    '''

    def __enter__(self):
        print(self.dbName, self.odbc, "In __enter__()")
        return self

    def __exit__(self):
        self.__del__()
        print(self.dbName, self.odbc, "In __exit__()")

    def __del__(self):
        print(self.dbName, self.odbc, "In __del__()")
        if hasattr(self, 'cur') and (self.odbc != 'connector'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def __str__(self):
        """返回一个对象的描述信息"""
        return f'mysql数据库对象，<dbName：[{self.dbName}] , odbc：[{self.odbc}]>\n可选驱动：[mysql.connector]；[pymysql]；[mysqlclient]；\n默认驱动[mysqlclient：MySQLdb]。'

    def has_tables(self, table_name):
        """判断数据库是否包含某个表,包含返回True"""
        self.cur.execute("show tables")
        tablerows = self.cur.fetchall()
        if len(tablerows) == 0:
            return False
        if table_name in tablerows[0]:
            return True
        return False

    def init_db(self):
        self.db = self.client.proxy
        self.proxys = self.db.proxys

    def close(self):
        pass

    def worKon(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as error:
            self.conn.rollback()
            print('\033[', error, ']\033', sep='')
            return False

    def insert(self, dt, tb_name):
        # 以字典形式提交插入
        ls = [(k, dt[k]) for k in dt if dt[k] is not None]
        sql = 'insert %s (' % tb_name + ','.join([i[0] for i in ls]) + ') values (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        print(sql)
        self.worKon(sql)

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
            return _版本号
        else:
            return False

    def getAll(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            data = self.cur.fetchall()
        except Exception as e:
            print(e)
        return data

    def getPt(self, sql):
        #  read_sql的两个参数: sql语句， 数据库连接
        pdtable = pandas.read_sql(sql, self.conn)
        if len(pdtable):
            return pdtable
        else:
            return False

    def getDic(self, sql):
        # 重新定义游标格式
        self.cur = self.conn.cursor(cursorclass=mysql.cursors.DictCursor)
        self.cur.execute(sql)
        dic = self.cur.fetchall()
        self.cur = self.conn.cursor(cursorclass=None)
        if len(dic):
            return dic
        else:
            return False


if __name__ == '__main__':
    db = SqlHelper('TXbook', 'connector')
    db.cur.execute("SELECT VERSION()")
    print("1数据库版本：", db.cur.fetchone())

    db2 = SqlHelper('TXbook', 'pymysql')  # 'mysqlclient' ; 'pymysql' ; 'connector'
    db2.cur.execute("SELECT VERSION()")
    print("2数据库版本：", db2.cur.fetchone())

    print(id(db))
    print(id(db2))

'''
    db3 = SqlHelper('TXbook')
    db3.cur.execute("SELECT VERSION()")
    print("3数据库版本：", db3.cur.fetchone())
    db3.conn.close()
'''

'''
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


'''
# 查询语句，选出 users 表中的所有数据
sql =  "select * from users;"
# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)
# 输出 users 表的查询结果
print(df)

# 新建pandas中的DataFrame, 只有id,num两列
df = pd.DataFrame({'id': [1, 2, 3, 4], 'name': ['zhangsan', 'lisi', 'wangwu', 'zhuliu']})
# 将新建的DataFrame储存为MySQL中的数据表，储存index列
df.to_sql('mydf', engine, index=True)
print('Read from and write to Mysql table successfully!')
# 如果使用事务引擎，可以设置自动提交事务，或者在每次操作完成后手动提交事务conn.commit()
conn.autocommit(1)    # conn.autocommit(True)
# 使用cursor()方法获取操作游标
cursor = conn.cursor()
# 因该模块底层其实是调用CAPI的，所以，需要先得到当前指向数据库的指针。

# 插入单条数据
sql = 'INSERT INTO user values("%d","%s")' %(1,"jack")
#复制一条记录
sql = 'INSERT INTO user selcet * from user where id=16'
# 不建议直接拼接sql，占位符方面可能会出问题，execute提供了直接传值
value = [2,'John']
cursor.execute('INSERT INTO test values(%s,%s)',value)

# 批量插入数据
values = []
for i in range(3, 20):
    values.append((i,'kk'+str(i)))
cursor.executemany('INSERT INTO user values(%s,%s)',values)

# 查询数据条目
count = cursor.execute('SELECT * FROM %s' %TABLE_NAME)
print 'total records: %d' %count
print 'total records:', cursor.rowcount

# 获取表名信息
desc = cursor.description
print "%s %3s" % (desc[0][0], desc[1][0])

# 查询一条记录
print 'fetch one record:'
result = cursor.fetchone()
print result
print 'id: %s,name: %s' %(result[0],result[1])

# 查询多条记录
print 'fetch five record:'
results = cursor.fetchmany(5)
for r in results:
    print r

# 查询所有记录
# 重置游标位置，偏移量:大于0向后移动;小于0向前移动，mode默认是relative
# relative:表示从当前所在的行开始移动; absolute:表示从第一行开始移动
cursor.scroll(0,mode='absolute')
results = cursor.fetchall()
for r in results:
    print r
cursor.scroll(-2)
results = cursor.fetchall()
for r in results:
    print r

# 更新记录
cursor.execute('UPDATE %s SET name = "%s" WHERE id = %s' %(TABLE_NAME,'Jack',1))

# 删除记录
cursor.execute('DELETE FROM %s WHERE id = %s' %(TABLE_NAME,2))

# 如果没有设置自动提交事务，则这里需要手动提交一次
conn.commit()

except:
    import traceback
    traceback.print_exc()
    # 发生错误时会滚
    conn.rollback()
finally:
    # 关闭游标连接
    cursor.close()
    # 关闭数据库连接
    conn.close()
'''
