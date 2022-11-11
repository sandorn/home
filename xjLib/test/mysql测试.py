# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-17 09:26:49
#FilePath     : /xjLib/xt_DAO/test/mysql测试.py
#LastEditTime : 2020-06-17 10:17:58
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import pandas
from xt_DAO.xt_mysql import engine

with engine('Jkdoc', 'pymysql') as myDb:
    a = myDb.has_tables('jkdoc')
    print(11111, a)
    sql = "select * from jkdoc;"

    df = pandas.read_sql_query(sql, myDb.conn)
    print(22222, df)
    dic = myDb.get_dict(sql)
    print(type(dic[0]))
    for i in dic[0]:
        print(33333, i, type(dic[0][i]))  # .decode('utf-8'))


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
