#!/usr/bin/python
# -*- coding: UTF-8 -*-


import MySQLdb as mysql

db = mysql.connect(host='db4free.net', port=3306, user='sandorn', passwd='eeM3sh4KPkp4sJ8A', db='baoxianjihuashu', charset='utf8mb4')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()
print("Database version : %s " % data)

# SQL插入语句
ins_sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
        LAST_NAME, AGE, SEX, INCOME)
        VALUES ('yu', 'jie', 20, 'M', 8000)"""
ins_sql1 = 'insert into employee(first_name, last_name, age, sex, income) values (%s, %s, %s, %s, %s)'
# SQL查询语句
sel_sql = "select * from %s where 保险期间 = %s"
# SQL更新语句
upd_sql = 'update employee set age = %s where sex = %s'
# SQL删除语句
del_sql = 'delete from employee where first_name = %s'

# 使用execute方法执行SQL语句
'''
try:
    # 执行sql语句
    # insert
    cursor.execute(ins_sql)
    cursor.execute(ins_sql1, ('xu', 'f', 20, 'M', 8000))
    # select
    cursor.execute(sel_sql, ('yu',))
    values = cursor.fetchall()
    print values
    # update
    cursor.execute(upd_sql, (24, 'M',))
    # delete
    cursor.execute(del_sql, ('xu',))
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
fetchall():接收全部的返回结果行.
'''

# 构建sql语句
sel_sql = '''
SELECT
    *
FROM
    {0[0]}
WHERE
    性别 = '{0[1]}'
AND 年龄 = '{0[2]}'
AND 保险期间='{0[3]}'
'''
#"select * from {0[0]} where 性别='{0[1]}' and 年龄={0[2]} and 保险期间='{0[3]}'"
params = ["爱加倍", "女", '43', "70周岁"]
sp_sql = sel_sql.format(params)

# 执行sql语句
print(sp_sql)
cursor.execute(sp_sql)

# 使用 fetchall() 方法获取数据
results = cursor.fetchall()
for row in results:
    ID = row[0]
    保险期间 = row[1]
    性别 = row[2]
    年龄 = row[3]
    缴费期限 = row[4]
    费率 = row[5]
    print("ID={}, 保险期间={},性别={},年龄={},缴费期限={},费率={}".format(ID, 保险期间, 性别, 年龄, 缴费期限, 费率))

# 构建sql语句
sel_sql = '''
SELECT
    *
FROM
    {0[0]}
WHERE
    性别 = '{0[1]}'
AND 年龄 = '{0[2]}'
'''
#"select * from {0[0]} where 性别='{0[1]}' and 年龄={0[2]}"
params = ["多倍保至尊版", "女", '43']
sp_sql = sel_sql.format(params)
# 执行sql语句
print(sp_sql)
count = cursor.execute(sp_sql)
print("找到{}条数据".format(count))
# 使用 fetchall() 方法获取数据
results = cursor.fetchall()
for row in results:
    print(row)

# 关闭数据库连接
cursor.close()
db.commit()
db.close()


'''
基本上参考这篇文章，对原作者表示谢意：http://blog.csdn.net/whzhaochao/article/details/49126037

对文章稍有补充，因我的工作电脑环境可能和原作者的略有不同。

我的电脑环境是WIN7x64+PHPStudy2017+nginx+PHP7，数据库管理工具用的navicat。

为了避免原文失效，我这边稍作整理发一遍。（PS：实战通过）



1、生成思路

利用mysql内存表插入速度快的特点，先利用函数和存储过程在内存表中生成数据，然后再从内存表插入普通表中

2、创建内存表及普通表

CREATE TABLE `vote_record_memory` (
    `id` INT (11) NOT NULL AUTO_INCREMENT,
    `user_id` VARCHAR (20) NOT NULL,
    `vote_id` INT (11) NOT NULL,
    `group_id` INT (11) NOT NULL,
    `create_time` datetime NOT NULL,
    PRIMARY KEY (`id`),
    KEY `index_id` (`user_id`) USING HASH
) ENGINE = MEMORY AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8

CREATE TABLE `vote_record` (
    `id` INT (11) NOT NULL AUTO_INCREMENT,
    `user_id` VARCHAR (20) NOT NULL,
    `vote_id` INT (11) NOT NULL,
    `group_id` INT (11) NOT NULL,
    `create_time` datetime NOT NULL,
    PRIMARY KEY (`id`),
    KEY `index_user_id` (`user_id`) USING HASH
) ENGINE = INNODB AUTO_INCREMENT = 1 DEFAULT CHARSET = utf8

3、创建函数及存储过程
CREATE FUNCTION `rand_string`(n INT) RETURNS varchar(255) CHARSET latin1
BEGIN
DECLARE chars_str varchar(100) DEFAULT 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
DECLARE return_str varchar(255) DEFAULT '' ;
DECLARE i INT DEFAULT 0;
WHILE i < n DO
SET return_str = concat(return_str,substring(chars_str , FLOOR(1 + RAND()*62 ),1));
SET i = i +1;
END WHILE;
RETURN return_str;
END

CREATE  PROCEDURE `add_vote_memory`(IN n int)
BEGIN
  DECLARE i INT DEFAULT 1;
    WHILE (i <= n ) DO
      INSERT into vote_record_memory  (user_id,vote_id,group_id,create_time ) VALUEs (rand_string(20),FLOOR(RAND() * 1000),FLOOR(RAND() * 100) ,now() );
            set i=i+1;
    END WHILE;
END

4、调用存储过程 （这里是我在按照原文，走不通后谷歌找来的）
根据不同系统修改内存限制

修改my.ini
tmp_table_size=4000M
max_heap_table_size = 4000M
修改后重启 mysql

然后执行

CALL add_vote_memory(1000000)

修改后，一百万数据也不要很久，不到5分钟。大笑




5、从内存表插入到普通表

INSERT into vote_record SELECT * from  vote_record_memory

大笑执行这个也很快，喝口水就好了，有图有真相。


PS：数据库这一块还得多多加强啊奋斗
'''
