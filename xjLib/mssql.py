
from xjLib.dBrouter import dbconf
import MySQLdb as mysql
import pymysql as pmysql


class MySQLConnection(object):
    """
    数据库连接池代理对象
    查询参数主要有两种类型
    第一种：传入元祖类型,如(12,13),这种方式主要是替代SQL语句中的%s展位符号
    第二种: 传入字典类型,如{"id":13},SQL语句需要使用键来代替展位符,例如：%(name)s
    """

    def __init__(self, DBname='master', odbc='mysql'):
        if DBname not in dbconf:
            print('错误提示：检查数据库配置：' + DBname)
            # self.__del__()
            exit(1)

        try:
            if odbc == 'pmysql':
                self.conn = pmysql.connect(**dbconf[DBname])
            else:
                self.conn = mysql.connect(**dbconf[DBname])
            self.cur = self.conn.cursor()
            print("获取数据库连接对象成功,连接池:{}".format(str(self.conn)))
        except Exception as error:
            print('\033[connect Error:\n', error, ']\033', sep='')  # repr(error)
            return None  # raise  # exit(1)

    def execute(self, sql, param=None):
        """
        基础更新、插入、删除操作
        :param sql:
        :param param:
        :return: 受影响的行数
        """
        ret = None
        try:
            if param is None:
                ret = self.cur.execute(sql)
            else:
                ret = self.cur.execute(sql, param)
        except TypeError as te:
            print("类型错误:", te)
        return ret

    def query(self, sql, param=None):
        """
        查询数据库
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回集合
        """
        self.cur.execute(sql, param)
        result = self.cur.fetchall()
        return result

    def queryOne(self, sql, param=None):
        """
        查询数据返回第一条
        :param sql: 查询SQL语句
        :param param: 参数
        :return: 返回第一条数据的字典
        """
        result = self.query(sql, param)
        if result:
            return result[0]
        else:
            return None

    def listByPage(self, sql, current_page, page_size, param=None):
        """
        分页查询当前表格数据
        :param sql: 查询SQL语句
        :param current_page: 当前页码
        :param page_size: 页码大小
        :param param:参数
        :return:
        """
        countSQL = "select count(*) ct from (" + sql + ") tmp "
        print("统计SQL:{}".format(sql))
        countNum = self.count(countSQL, param)
        offset = (current_page - 1) * page_size
        totalPage = int(countNum / page_size)
        if countNum % page_size > 0:
            totalPage = totalPage + 1
        pagination = {"current_page": current_page, "page_size": page_size, "count": countNum, "total_page": totalPage}
        querySql = "select * from (" + sql + ") tmp limit %s,%s"
        print("查询SQL:{}".format(querySql))
        # 判断是否有参数
        if param is None:
            # 无参数
            pagination["data"] = self.query(querySql, (offset, page_size))
        else:
            # 有参数的情况,此时需要判断参数是元祖还是字典
            if isinstance(param, dict):
                # 字典的情况,因此需要添加字典
                querySql = "select * from (" + sql + ") tmp limit %(tmp_offset)s,%(tmp_pageSize)s"
                param["tmp_offset"] = offset
                param["tmp_pageSize"] = page_size
                pagination["data"] = self.query(querySql, param)
            elif isinstance(param, tuple):
                # 元祖的方式
                listtp = list(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"] = self.query(querySql, tuple(listtp))
            else:
                # 基础类型
                listtp = []
                listtp.append(param)
                listtp.append(offset)
                listtp.append(page_size)
                pagination["data"] = self.query(querySql, tuple(listtp))
        return pagination

    def count(self, sql, param=None):
        """
        统计当前表记录行数
        :param sql: 统计SQL语句
        :param param: 参数
        :return: 当前记录行
        """
        ret = self.queryOne(sql, param)
        count = None
        if ret:
            for k, v in ret.items():
                count = v
        return count

    def insert(self, sql, param=None):
        """
        数据库插入
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql, param)

    def update(self, sql, param=None):
        """
        更新操作
        :param sql: SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql, param)

    def delete(self, sql, param=None):
        """
        删除操作
        :param sql: 删除SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.execute(sql, param)

    def batch(self, sql, param=None):
        """
        批量插入
        :param sql: 插入SQL语句
        :param param: 参数
        :return: 受影响的行数
        """
        return self.cur.executemany(sql, param)

    def commit(self, param=None):
        """
        提交数据库
        :param param:
        :return:
        """
        if param is None:
            self.conn.commit()
        else:
            self.conn.rollback()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("释放数据库连接")
        return None


if __name__ == '__main__':
    db = MySQLConnection()
    # 使用execute方法执行SQL语句
    db.cur.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取一条数据库。
    print("数据库版本：", db.cur.fetchone())

    db2 = MySQLConnection('db4', 'pmysql')
    # 使用execute方法执行SQL语句
    db2.cur.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取一条数据库。
    print("数据库版本：", db2.cur.fetchone())

'''
https://www.cnblogs.com/yinliang/p/11784911.html
第一种方式,获取默认数据库的连接,在配置文件中配置名称为master的数据库
connect=MySQLConnect()
第二种方式,指定key名称获取数据库连接,如下：获取"db4"的数据库连接
connect=MySQLConnect("db4")

# 使用下标索引的方式插入数据
sql = "insert into user(id,name) values(%s,%s)"
connect.insert(sql, ("1", "张三"))
connect.commit()

# 使用下标索引的方式批量插入数据
sql = "insert into user(id,name) values(%s,%s)"
# 执行批量插入动作
data = []   # 放入的是元祖
data.append(("1", "张三"))
data.append(("2", "张三2"))
connect.batch(sql, data)
connect.commit()

# 使用下标索引的方式插入数据
sql="insert into user(id,name) values(%(id)s,%(name)s)"
# 执行插入动作，此时我们使用的是字典
connect.insert(sql,{"name":"张三","id":"1"})
connect.commit()

# 使用下标索引的方式批量插入数据
sql="insert into user(id,name) values(%(id)s,%(name)s)"
# 执行批量插入动作
data=[]
# 放入的是自字典
data.append({"name":"张三","id":"1"})
data.append({"name":"张三1","id":"2"})
connect.batch(sql,data)
connect.commit()
'''
