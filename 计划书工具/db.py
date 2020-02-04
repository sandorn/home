# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   db.py
@Time    :   2019/04/16 13:06:42
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''
import pymysql as mys
#  import MySQLdb as mys  # 与  pymysql 相同
import pandas


class MysqlHelp:

    def __init__(
            self,
            database='baoxianjihuashu',
            host='localhost',
            #  host='db4free.net',
            user='root',
            password='root',
            #  'eeM3sh4KPkp4sJ8A',
            charset='utf8mb4',
            port=3306):

        self.port = port
        self.charset = charset
        self.user = user
        self.host = host
        self.password = password
        self.database = database

        self.conn = mys.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            charset=self.charset,
            port=self.port,
            database=self.database)
        #  使用cursor()获取操作游标
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def ver(self):
        sql = "SELECT VERSION()"
        #  使用execute方法执行SQL语句
        self.cur.execute(sql)
        #  使用 fetchone() 方法获取一条数据库。
        版本号 = self.cur.fetchone()
        if 版本号 == ('8.0.15',):
            return True
        else:
            return False

    def workon(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            print('workon , ok')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False

    def getall(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            print('getall , ok')
            data = self.cur.fetchall()
            return data
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False

    def getable(self, sql):
        #  read_sql的两个参数: sql语句， 数据库连接
        sql = "select * from " + sql
        table = pandas.read_sql(sql, self.conn)
        if len(table):
            # print('getable , ok')
            return table
        else:
            return False


def getver(db_name):
    #  使用execute执行SQL语句
    db_name.cur.execute("SELECT VERSION()")
    #  使用 fetchone() 方法获取一条数据库。
    版本号 = db_name.cur.fetchone()
    if 版本号:
        return 版本号[0]
    else:
        return False


if __name__ == '__main__':
    myDb = MysqlHelp('baoxianjihuashu')
    print("getver:", getver(myDb))
    sql = " select * from users ;"
    print("ver:", myDb.ver())
    data = myDb.getall(sql)
    print("data[0]:", data[0], "++++++++++data[1][1]:", data[1][1])
    table = myDb.getable("users")
    print("table.values[1][1]:", table.values[1][1])
    print("table[1:2]:", table[1:2])
    print("table.iloc[0]:", table.iloc[0])
    '''
    myDb.workon(
        # "ALTER TABLE  users DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8mb4_0900_ai_ci"  # 设置默认编码
        #"ALTER TABLE  意外险分解 AUTO_INCREMENT=6"
        #" ALTER TABLE  users AUTO_INCREMENT=3201"  # 设定自增ID
        # "insert into users(username, password,手机) values('%s','%s','%s')" % ('gaogao', '1234567', '17610786502')
    )

    query = "INSERT INTO users(username, password,手机) values ('%s','%s','%s')"
    val = ('gaogao', '1234567', '17610786502')
    curs.execute(
        "insert into users(username, password,手机) values('%s','%s','%s')" %
        ('gaogao', '1234567', '17610786502'))
    db2.commit()
    sql = " select * from users; "
    # read_sql_query的两个参数: sql语句， 数据库连接

    df = pd.read_sql(sql, db2)
    print(df)
    print(type(df))
    '''
