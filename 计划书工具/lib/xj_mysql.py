# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   xj_mysql.py
@Time    :   2019/04/29 12:04:24
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

try:
    import MySQLdb as myodbc  # 与  pymysql 相同
except ImportError:
    import pymysql as myodbc
import pandas
import db_router
dbr = db_router.DBSERVER


class MysqlHelp(object):

    def __new__(cls, *args, **kwargs):
        #print("__new__方法被调用")
        return object.__new__(cls)

    def __init__(self, name='default'):

        if name not in dbr:
            print('错误提示：\n        检查数据库路由名称！')
            #self.__del__()
            exit(1)

        try:
            self.conn = myodbc.connect(**dbr[name])
            # 使用cursor()获取操作游标
            self.cur = self.conn.cursor()
        except Exception as error:
            print(
                '\033[connect Error:\n', error, ']\033', sep='')  # repr(error)
            return None  # raise  # exit(1)

    def __del__(self):
        #print("__del__方法被调用")
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def __str__(self):
        """返回一个对象的描述信息"""
        return 'MySQLdb数据库对象'

    def worKon(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as error:
            self.conn.rollback()
            print('\033[', error, ']\033', sep='')
            return False

    def insert(self, dt):
        #以字典形式提交插入
        ls = [(k, dt[k]) for k in dt if dt[k] is not None]
        sql = 'insert %s (' % self.tb + ','.join([
            i[0] for i in ls
        ]) + ') values (' + ','.join(['%r' % i[1] for i in ls]) + ');'
        self.worKon(sql)

    def update(self, dt_update, dt_condition, table):
        #dt_update,更新的数据
        #dt_condition，匹配的数据
        #table,表名
        sql = 'UPDATE %s SET ' % table + ','.join([
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
        #重新定义游标格式
        self.cur = self.conn.cursor(cursorclass=myodbc.cursors.DictCursor)
        self.cur.execute(sql)
        dic = self.cur.fetchall()
        self.cur = self.conn.cursor(cursorclass=None)
        if len(dic):
            return dic
        else:
            return False


def getVer(db_name):
    #  使用execute执行SQL语句
    db_name.cur.execute("SELECT VERSION()")
    #  使用 fetchone() 方法获取一条数据库。
    版本号 = db_name.cur.fetchone()
    if 版本号:
        return 版本号[0]
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
