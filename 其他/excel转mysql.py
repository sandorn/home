# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   excel转mysql.py
@Time    :   2019/04/17 12:27:10
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
选择excel文件，用xlrd读取，然后在数据库中创建表，并插入数据
要求excel表格规范，第一行为列标题
'''

import xlrd
import MySQLdb

import win32ui

dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
dlg.SetOFNInitialDir('d:/')  # 设置打开文件对话框中的初始显示目录
dlg.DoModal()

filename = dlg.GetPathName()  # 获取选择的文件名称
print(filename)
data = xlrd.open_workbook(filename)  #读取表格
db = "baoxianjihuashu"  #需要操作的数据库

conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', charset='utf8')  #连接mysql
cur = conn.cursor()
# cur.execute("drop database if exists " + db)
# cur.execute("create database " + db)
conn.select_db(db)  # 初始化数据库

sheet_names = data.sheet_names()
for sheet_name in sheet_names:
    sheet = data.sheet_by_name(sheet_name)
    row_data = sheet.row_values(0)
    # print(row_data)
    row_data = ' varchar(256) DEFAULT NULL, '.join(row_data)
    row_data = row_data + ' varchar(256) DEFAULT NULL'
    print('create table ' + sheet_name + '(' + row_data + ')')  #数据库中创建表格
    cur.execute('DROP TABLE IF EXISTS ' + sheet_name)
    cur.execute('create table ' + sheet_name + '(' + row_data + ')')  #数据库中创建表格
    ss = ''
    for index in range(sheet.ncols):
        ss = ss + '%s, '
    ss = ss.rstrip(', ')
    sql = "insert " + sheet_name + " values(" + ss + ")"
    param = []
    for index in range(1, sheet.nrows):
        row_values = sheet.row_values(index)
        param.append(row_values)
    cur.executemany(sql, param)  #插入数据
    conn.commit()

cur.close()
conn.close()
