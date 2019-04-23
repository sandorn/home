# -*- coding:utf-8 -*-
__author__ = 'mayi'

#导入模块
import pypyodbc

#定义conn
def mdb_conn(db_name, password = ""):
    """
    功能：创建数据库连接
    :param db_name: C:\Users\刘新军\Desktop\展业\计划书工具\res\db.mdb
    :param db_name: 数据库密码，默认为空
    :return: 返回数据库连接
    """
    str = 'Driver={Microsoft Access Driver (*.mdb)};PWD' + password + ";DBQ=" + db_name
    conn = pypyodbc.win_connect_mdb(str)

    return conn

#增加记录
def mdb_add(conn, cur, sql):
    """
    功能：向数据库插入数据
    :param conn: 数据库连接
    :param cur: 游标
    :param sql: sql语句
    :return: sql语句是否执行成功
    """
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        return False

#删除记录
def mdb_del(conn, cur, sql):
    """
    功能：向数据库删除数据
    :param conn: 数据库连接
    :param cur: 游标
    :param sql: sql语句
    :return: sql语句是否执行成功
    """
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        return False

#修改记录
def mdb_modi(conn, cur, sql):
    """
    功能：向数据库修改数据
    :param conn: 数据库连接
    :param cur: 游标
    :param sql: sql语句
    :return: sql语句是否执行成功
    """
    try:
        cur.execute(sql)
        conn.commit()
        return True
    except:
        return False

#查询记录
def mdb_sel(cur, sql):
    """
    功能：向数据库查询数据
    :param cur: 游标
    :param sql: sql语句
    :return: 查询结果集
    """
    try:
        cur.execute(sql)
        return cur.fetchall()
    except:
        return []

if __name__ == '__main__':
    pathfile = 'test.mdb'
    tablename = 'prov'
    conn = mdb_conn(pathfile)
    cur = conn.cursor()

    #增
    sql = "Insert Into " + tablename + " Values (33, 12, '天津', 0)"
    if mdb_add(conn, cur, sql):
       print("插入成功！")
    else:
       print("插入失败！")

    #删
    sql = "Delete * FROM " + tablename + " where id = 32"
    if mdb_del(conn, cur, sql):
       print("删除成功！")
    else:
       print("删除失败！")

    #改
    sql = "Update " + tablename + " Set IsFullName = 1 where ID = 33"
    if mdb_modi(conn, cur, sql):
       print("修改成功！")
    else:
       print("修改失败！")

    #查
    sql = "SELECT * FROM " + tablename + " where id > 10"
    sel_data = mdb_sel(cur, sql)
    print(sel_data)

cur.close()    #关闭游标
conn.close()   #关闭数据库连接
