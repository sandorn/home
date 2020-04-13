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
@LastEditTime: 2020-04-13 18:10:33
'''

import mysql.connector
import MySQLdb  # mysqlclient
import pandas
import pymysql

from xjLib.db.dbconf import db_conf


class engine(object):
    """
    mysql数据库对象，参数：db_name , odbc
    可选驱动：[mysql.connector]、[pymysql]、[mysqlclient]，
    默认驱动[mysqlclient：MySQLdb]
    """

    def __init__(self, key='default', odbc='mysqlclient'):
        self.db_name = key
        self.odbc = odbc
        if key not in db_conf:
            raise ('错误提示：检查数据库配置：' + self.db_name)
        db_conf[key].pop('type')

        self.conf = db_conf[self.db_name]

        try:
            if odbc == 'connector':
                self.conn = mysql.connector.connect(**self.conf)
                self.DictCursor = None
            elif odbc == 'pymysql':
                self.conn = pymysql.connect(**self.conf)
                self.DictCursor = pymysql.cursors.DictCursor
            else:  # mysqlclient
                self.conn = MySQLdb.connect(**self.conf)
                self.DictCursor = MySQLdb.cursors.DictCursor

            # self.conn.autocommit(True)
            self.cur = self.conn.cursor()
            print(f'connect({self.db_name}) by [{ self.odbc}] as {self.conn}.')
        except Exception as error:
            print(
                f'\033[connect({self.db_name}) by [{ self.odbc}] error:{error}]\033'
            )  # repr(error)
            return None  # raise  # exit(1)

    '''
    对with的处理:所求值的对象必须有一个__enter__()方法，一个__exit__()方法。
    跟with后面的语句被求值后，返回对象的__enter__()方法被调用，这个方法的返回值将被赋值给as后面的变量。当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。
    '''

    def __enter__(self):
        print(f"{self.db_name}\t{ self.odbc}\tIn __enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with自动调用,不必调用del"""
        print(f"{self.db_name}\t{ self.odbc}\tIn __exit__()")
        if exc_tb is not None:
            print('has error %s' % exc_tb)

    def __del__(self):
        print(f"{self.db_name}\t{ self.odbc}\tIn __del__()")
        '''hasattr(self, 'conn')'''
        if self.odbc != 'connector':
            self.cur.close()
        self.conn.close()

    def __str__(self):
        """返回一个对象的描述信息"""
        return f'mysql数据库对象，<db_name:[{self.db_name}] , odbc：[{self.odbc}]>\n可选驱动：[mysql.connector]；[pymysql]；[mysqlclient]；\n默认驱动[mysqlclient：MySQLdb]。'

    def has_tables(self, table_name):
        """判断数据库是否包含某个表,包含返回True"""
        self.cur.execute("show tables")
        tablerows = self.cur.fetchall()
        if len(tablerows) == 0:
            return False
        for rows in tablerows:
            if table_name == rows[0]:
                return True
        return False

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
        sql = 'insert into %s (' % tb_name + ','.join([
            i[0] for i in ls
        ]) + ') values (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        # print(sql)  # .replace('%', '%%')
        self.worKon(sql)

    def update(self, dt_update, dt_condition, tb_name):
        # dt_update,更新的数据
        # dt_condition，匹配的数据
        # tb_name,表名
        sql = 'UPDATE %s SET ' % tb_name + ','.join([
            '%s=%r' % (k, dt_update[k]) for k in dt_update
        ]) + ' WHERE ' + ' AND '.join(
            ['%s=%r' % (k, dt_condition[k]) for k in dt_condition]) + ';'
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


if __name__ == '__main__':
    # db = SqlHelper('TXbook', 'mysqlclient')  # 'mysqlclient' ; 'pymysql' ; 'connector'
    # db2 = SqlHelper('TXbook', 'pymysql')
    # db3 = engine('TXbx', 'connector')

    with engine('Jkdoc', 'connector') as myDb:
        a = myDb.has_tables('jkdoc')
        print(11111, a)
        sql = "select * from jkdoc;"
        if a:
            df = pandas.read_sql_query(sql, myDb.conn)
            print(22222, df)
            dic = myDb.get_dict(sql)
            print(type(dic[0]))
            for i in dic[0]:
                print(33333, i, type(dic[0][i]))  #  .decode('utf-8'))
'''
        # 查询语句，选出 users 表中的所有数据
        sql = "select * from users;"
        # read_sql_query的两个参数: sql语句， 数据库连接
        df = pandas.read_sql_query(sql, myDb.conn)
        # 输出 users 表的查询结果
        print(df)


        data = myDb.get_all_from_db("users")
        print("data[0]:", data[0], "++++++++++data[1][1]:", data[1][1])
        table = myDb.get_pd_table("users")
        print("table.values[1][1]:", table.values[1][1])
        print("table[1:2]:", table[1:2])
        print("table.iloc[0]:", table.iloc[0])

        dic = myDb.get_dict( " select * from users ;")
        for d in dic:
            print(d)

        # 查询语句，选出 users 表中的所有数据
        sql = "select * from users;"
        # read_sql_query的两个参数: sql语句， 数据库连接
        df = pandas.read_sql_query(sql, myDb.conn)
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
# 复制一条记录
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
