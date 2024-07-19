import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from xt_database.cfg import connect_str

# 创建连接引擎
engine = create_async_engine(connect_str(key="TXbx", odbc="aiomysql"))
# 创建DBSession类型:
DBSession = async_sessionmaker(bind=engine)


async def query_data(sql):
    # 创建session对象:
    async with DBSession() as session:
        # 执行sql语句：
        result = await session.execute(text(sql))  # 返回结果为ResultProxy类型，可以通过fetchall()获取全部数据，fetchone()获取一条数据。
        return result.fetchall()  # 返回全部数据


async def main():  # 定义一个main函数用于测试代码是否正常执行。
    sql = "select * from users2"  # 查询table表中的所有数据
    return await query_data(sql)


if __name__ == "__main__":  # 判断当前文件是否为主文件，如果是则执行下面的代码。
    loop = asyncio.get_event_loop()  # 获取事件循环对象loop。
    res = loop.run_until_complete(main())  # 执行main函数
    print(res)
