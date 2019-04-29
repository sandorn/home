# ！/usr/bin/env python
# -*-coding:utf-8-*-

import xj_mysql


def 连接数据库(name):
    global db
    db = xj_mysql.MysqlHelp(name)
    # 使用execute方法执行SQL语句
    db.cur.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取一条数据库。
    print("数据库版本：", db.cur.fetchone())


def 列表():
    sel_sql = "SELECT  *  FROM  费率结构   "  # SQL语句
    db.cur.execute(sel_sql)
    global 产品结构列表
    产品结构列表 = []
    # 使用 fetchall() 方法获取数据
    results = db.cur.fetchall()
    for row in results:
        res = []
        for cell in row:
            (cell != '') and res.append(
                cell)  # 等同于# if row != '':\n    res.append(row)
        产品结构列表.append(res)
    return True


def 构建视图sql():
    sel_sql_begin = "Create or Replace  VIEW  `v{}` AS SELECT `ID`,`产品名称`,`保险公司`,`产品大类`,`产品小类`"
    sel_sql_end = " FROM `费率表` WHERE  `产品名称` = '{}' "
    视图sql_list = []
    for row in 产品结构列表:
        sel_sql = sel_sql_begin
        sel_sql = sel_sql.format(row[1])

        for i in range(len(row)):
            if i > 4:
                #print(row[1],row[i])
                sel_sql = sel_sql + ",`" + row[i] + "`"

        sel_sql = sel_sql + sel_sql_end.format(row[1])
        视图sql_list.append(sel_sql)
    return 视图sql_list


def 执行视图sql(sql):
    for i in range(len(sql)):
        db.worKon(sql[i])  # 执行SQL语句
        #print('执行|', i, '|', sql[i])


def main(name="default"):
    连接数据库(name)
    if 列表():
        temp_list = 构建视图sql()
        for i in range(len(temp_list)):
            print(temp_list[i])
    执行视图sql(temp_list)


if __name__ == '__main__':
    main()
    print("产品结构列表[1]:", 产品结构列表[1])
