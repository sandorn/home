# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-09-05 09:53:31
FilePath     : /CODE/xjLib/xt_database/mysql.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import MySQLdb
import pymysql
from xt_database.cfg import DB_CFG
from xt_database.untilsql import make_insert_sql, make_update_sql


class DbEngine:
    """
    mysql数据库对象,参数:db_key , odbc
    可选驱动:[mysql.connector 出错禁用]、[pymysql]、[MySQLdb]
    """

    def __init__(self, db_key="default", odbc="pymysql"):
        self.db_key = db_key
        self.odbc = odbc
        if not hasattr(DB_CFG, db_key):
            raise ValueError(f"错误提示:检查数据库配置:{db_key}")
        self.cfg = DB_CFG[db_key].value.copy()
        self.cfg.pop("type", None)

        try:
            if odbc == "pymysql":
                self.conn = pymysql.connect(**self.cfg)
                self.DictCursor = pymysql.cursors.DictCursor
            else:  # mysqlclient
                self.conn = MySQLdb.connect(**self.cfg)
                self.DictCursor = MySQLdb.cursors.DictCursor
            self.conn.autocommit(True)  # #自动提交
        except Exception as error:
            print(f"{self.odbc} connect<{self.db_key}> error:{repr(error)}")
            return None
        finally:
            self.cur = self.conn.cursor()
            print(f"{self.odbc}  connect<{self.db_key}> Ok!")

    def __enter__(self):
        print(f"{ self.odbc}\t{self.db_key}\tIn __enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with自动调用,不必调用del"""
        print(f"{ self.odbc}\t{self.db_key}\tIn __exit__()")
        if exc_tb is not None:
            print(f"exc_type:{exc_type}, exc_val:{exc_val}, exc_tb:{exc_tb}")

    def __del__(self):
        print(f"{ self.odbc}\t{self.db_key}\tClosed\tIn __del__()")
        if hasattr(self, "cur"):
            self.cur.close()
        if hasattr(self, "conn"):
            self.conn.close()

    def __str__(self):
        """返回一个对象的描述信息"""
        return f"""
        mysql数据库对象,<odbc:[{self.odbc}],db_key:[{self.db_key}] >,
        可选驱动:[[pymysql | MySQLdb];默认[pymysql]。
        """

    def has_tables(self, table_name):
        """判断数据库是否包含某个表,包含返回True"""
        self.cur.execute("show tables")
        tablerows = self.cur.fetchall()
        if len(tablerows) == 0:
            return False
        return any(rows[0] == table_name for rows in tablerows)

    def close(self):
        pass

    def execute(self, sql, args=None):
        args = args or []
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as error:
            return self.__handler_err(f"{self.odbc} error |  [", error, sql)

    def insertMany(self, datas, tb_name, keys=None):
        if not isinstance(datas, (list, tuple)):
            raise TypeError("must list|tuple type")

        if keys is None:
            keys = list(datas[0].keys())
        cols = ", ".join(f"`{k}`" for k in keys)
        val_cols = ", ".join(f"%({k})s" for k in keys)
        res_sql = f"insert into `{tb_name}`({cols}) values({val_cols})"

        try:
            self.cur.executemany(res_sql, datas)
            self.conn.commit()
            return True
        except Exception as error:
            return self.__handler_err(f"{self.odbc} error | [", error, res_sql)

    # TODO Rename this here and in `execute` and `insertMany`
    def __handler_err(self, arg0, error, arg2):
        self.conn.rollback()
        print(f"{arg0}{error}] \n sql:{arg2}", sep="")
        return False

    def insert(self, data, tb_name):
        if not isinstance(data, dict):
            raise ValueError("must dict type")
        res_sql = make_insert_sql(data, tb_name)
        self.execute(res_sql)

    def update(self, new_data, condition, tb_name):
        if not isinstance(new_data, dict):
            raise ValueError("must dict type")
        sql = make_update_sql(new_data, condition, tb_name)
        self.execute(sql)

    def ver(self):
        sql = "SELECT VERSION()"
        #  使用execute方法执行SQL语句
        self.cur.execute(sql)
        #  使用 fetchone() 方法获取一条数据库。
        _版本号 = self.cur.fetchone()
        return _版本号[0] if _版本号 else None

    def query(self, sql, args=None):
        try:
            self.cur.execute(sql, args)
            return self.cur.fetchall()
        except Exception as e:
            print(e)

    def get_all_from_db(self, table_name, args=None):
        sql = f" select * from {table_name}"
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    def get_dict(self, sql):
        # 重新定义游标格式
        if self.DictCursor is None:
            self.cursorDict = self.conn.cursor(dictionary=True)
            # #mysql.connector独有
        elif isinstance(self.DictCursor, int):
            self.cursorDict = self.conn.cursor(self.DictCursor)

        self.cursorDict.execute(sql)
        dic = self.cursorDict.fetchall()
        return dic or False


if __name__ == "__main__":
    db_clent = DbEngine("TXbx", "MySQLdb")
    print(1111111111, db_clent.query("select * from users2"))
    print(2222222222, db_clent.get_all_from_db("users2"))
