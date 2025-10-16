# !/usr/bin/env python3
"""
==============================================================
Description  : XT-SQLORM异步数据库操作示例
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-23 10:30:00
FilePath     : /CODE/xjlib/xt_sqlorm/examples/async_example.py
Github       : https://github.com/sandorn/home

异步数据库操作示例，演示如何使用AsyncSqlConnection和AsyncOrmOperations
==============================================================
"""
from __future__ import annotations

import asyncio
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, select

# 导入ORM模块
from xt_sqlorm import AsyncOrmOperations, AsyncSqlConnection, BaseModel

# 导入日志模块
from xt_wraps.log import mylog as loger


# 定义示例模型
class User(BaseModel):
    """用户模型"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class AsyncExample:
    """异步数据库操作示例类"""
    
    def __init__(self):
        """初始化示例类"""
        self.connection: AsyncSqlConnection | None = None
        self.orm_ops: AsyncOrmOperations[User] | None = None
    
    async def init_db(self) -> None:
        """初始化数据库连接"""
        try:
            # 创建异步数据库连接
            self.connection = AsyncSqlConnection(
                url='sqlite+aiosqlite:///./test_async.db',
                echo=False,  # 生产环境设为False
                pool_size=5,
                max_overflow=10
            )
            
            # 初始化数据库（创建表）
            await self.connection.create_tables([User])
            loger.ok('数据库表创建成功')
            
            # 创建ORM操作实例
            self.orm_ops = AsyncOrmOperations(User, self.connection)
            
        except Exception as e:
            loger.fail(f'数据库初始化失败: {e}')
            raise
    
    async def test_crud_operations(self) -> None:
        """测试CRUD操作"""
        if not self.orm_ops:
            raise ValueError('ORM操作实例未初始化')
        
        try:
            loger.info('开始测试CRUD操作')
            
            # 1. 插入单条记录
            user_data = {
                'username': 'async_user1',
                'email': 'async_user1@example.com'
            }
            insert_result = await self.orm_ops.insert(user_data)
            loger.ok(f'插入单条记录结果: {insert_result}')
            
            # 2. 批量插入
            batch_users = [
                {'username': 'async_user2', 'email': 'async_user2@example.com'},
                {'username': 'async_user3', 'email': 'async_user3@example.com'}
            ]
            batch_insert_result = await self.orm_ops.insert_many(batch_users)
            loger.ok(f'批量插入结果: {batch_insert_result}')
            
            # 3. 查询单条记录
            user = await self.orm_ops.get_by_id(1)
            loger.info(f'查询ID=1的用户: {user}')
            
            # 4. 条件查询
            stmt = select(User).where(User.username == 'async_user1')
            query_result = await self.orm_ops.query(stmt)
            loger.info(f'条件查询结果: {query_result}')
            
            # 5. 更新记录
            update_data = {'email': 'updated_email@example.com'}
            update_result = await self.orm_ops.update(update_data, id=1)
            loger.ok(f'更新结果: {update_result}')
            
            # 6. 批量更新
            batch_update_data = {'email': 'batch_updated@example.com'}
            batch_update_result = await self.orm_ops.update_many(
                batch_update_data, 
                User.id.in_([2, 3])
            )
            loger.ok(f'批量更新结果: {batch_update_result}')
            
            # 7. 删除记录
            delete_result = await self.orm_ops.delete(id=1)
            loger.ok(f'删除结果: {delete_result}')
            
        except Exception as e:
            loger.fail(f'CRUD操作测试失败: {e}')
            raise
    
    async def test_transaction(self) -> None:
        """测试事务操作"""
        if not self.connection or not self.orm_ops:
            raise ValueError('数据库连接或ORM操作实例未初始化')
        
        try:
            loger.info('开始测试事务操作')
            
            # 使用事务进行多个操作
            async with self.connection.transaction():
                # 插入记录
                await self.orm_ops.insert({
                    'username': 'transaction_user',
                    'email': 'transaction@example.com'
                })
                
                # 再插入一条记录
                await self.orm_ops.insert({
                    'username': 'transaction_user2',
                    'email': 'transaction2@example.com'
                })
            
            loger.ok('事务执行成功')
            
            # 测试事务回滚
            try:
                async with self.connection.transaction():
                    await self.orm_ops.insert({
                        'username': 'rollback_user',
                        'email': 'rollback@example.com'
                    })
                    # 故意引发错误触发回滚
                    raise ValueError('测试事务回滚')
            except ValueError:
                loger.warning('事务回滚成功')
                # 验证回滚后记录不存在
                stmt = select(User).where(User.username == 'rollback_user')
                result = await self.orm_ops.query(stmt)
                loger.info(f'回滚后查询结果: {result}')
                
        except Exception as e:
            loger.fail(f'事务操作测试失败: {e}')
            raise
    
    async def test_direct_sql(self) -> None:
        """测试直接执行SQL"""
        if not self.connection:
            raise ValueError('数据库连接未初始化')
        
        try:
            loger.info('开始测试直接执行SQL')
            
            # 执行查询SQL
            result = await self.connection.execute('SELECT * FROM users')
            loger.info(f'直接SQL查询结果数量: {len(result)}')
            
            # 执行插入SQL
            sql = 'INSERT INTO users (username, email) VALUES (?, ?)'
            params = ('sql_user', 'sql_user@example.com')
            insert_result = await self.connection.execute(sql, params)
            loger.ok(f'直接SQL插入结果: {insert_result}')
            
        except Exception as e:
            loger.fail(f'直接SQL执行测试失败: {e}')
            raise
    
    async def close(self) -> None:
        """关闭数据库连接"""
        if self.connection:
            await self.connection.close()
            loger.ok('数据库连接已关闭')


async def main() -> None:
    """主函数"""
    example = AsyncExample()
    
    try:
        # 初始化数据库
        await example.init_db()
        
        # 测试CRUD操作
        await example.test_crud_operations()
        
        # 测试事务操作
        await example.test_transaction()
        
        # 测试直接SQL执行
        await example.test_direct_sql()
        
    finally:
        # 确保关闭连接
        await example.close()


if __name__ == '__main__':
    # 运行主函数
    asyncio.run(main())