# !/usr/bin/env python3
"""
==============================================================
Description  : SQLORM使用示例 - 基于factory.py的重写版本
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-11-05 10:45:00
LastEditTime : 2024-11-05 10:45:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/examples/example_usage.py
Github       : https://github.com/sandorn/home

本文件展示如何使用factory.py提供的工厂函数创建数据库连接和ORM操作对象，
包括模型创建、表反射、数据增删改查等功能。
==============================================================
"""

from __future__ import annotations

from typing import Any

from xt_sqlorm.core.connection import SqlConnection
from xt_sqlorm.core.factory import create_orm_operations, create_sqlconnection, reflect_table
from xt_sqlorm.examples.user import UserModel
from xt_wraps.log import mylog as log


# 配置数据库连接
class UserService:
    """用户服务类
    
    封装用户相关的业务逻辑
    """

    def __init__(self, db_conn: SqlConnection | None = None, **conn_kwargs):
        """初始化用户服务
        
        Args:
            db_conn: 数据库连接对象，如果为None则创建新连接
            **conn_kwargs: 创建连接时的参数，会传递给create_sqlconnection
        """
        # 创建ORM操作对象
        self.user_ops = create_orm_operations(UserModel, db_conn=db_conn, **conn_kwargs)
        self.db_conn = self.user_ops.db

    def create_user(self, user_data: dict[str, Any]) -> UserModel:
        """创建新用户
        
        Args:
            user_data: 用户数据字典
            
        Returns:
            创建的用户模型对象
        """
        with self.user_ops.db.session_scope() as session:
            user = self.user_ops.create(user_data, session)
            log.info(f'Created user: {user.username}')
            return user

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        """根据ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户模型对象，如果不存在则返回None
        """
        user = self.user_ops.get_by_id(user_id)
        if user:
            log.info(f'Found user: {user.username}')
        else:
            log.warning(f'User with ID {user_id} not found')
        return user

    def get_user_by_username(self, username: str) -> UserModel | None:
        """根据用户名获取用户
        
        Args:
            username: 用户名
            
        Returns:
            用户模型对象，如果不存在则返回None
        """
        user = self.user_ops.get_one({'username': username})
        if user:
            log.info(f'Found user: {username}')
        else:
            log.warning(f'User {username} not found')
        return user

    def update_user(self, user_id: int, update_data: dict[str, Any]) -> UserModel | None:
        """更新用户信息
        
        Args:
            user_id: 用户ID
            update_data: 更新数据字典
            
        Returns:
            更新后的用户模型对象，如果用户不存在则返回None
        """
        with self.user_ops.db.session_scope() as session:
            user = self.user_ops.update_by_id(user_id, update_data, session)
            if user:
                log.info(f'Updated user: {user.username}')
            else:
                log.warning(f'Failed to update user with ID {user_id}: user not found')
            return user

    def delete_user(self, user_id: int) -> bool:
        """删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除成功返回True
        """
        with self.user_ops.db.session_scope() as session:
            success = self.user_ops.delete_by_id(user_id, session)
            if success:
                log.info(f'Deleted user with ID {user_id}')
            else:
                log.warning(f'Failed to delete user with ID {user_id}: user not found')
            return success

    def get_all_users(self, page: int = 1, page_size: int = 10) -> list[dict[str, Any]]:
        """分页获取所有用户
        
        Args:
            page: 页码
            page_size: 每页记录数
            
        Returns:
            用户数据字典列表
        """
        users, total = self.user_ops.get_paginated(
            page=page,
            page_size=page_size,
            order_by='created_at',
            order_dir='desc'
        )

        # 转换为字典列表
        user_dicts = [user.to_dict() for user in users]
        log.info(f'Retrieved page {page} of users, total: {total}')

        return user_dicts

    def search_users(self, keyword: str) -> list[dict[str, Any]]:
        """搜索用户
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            用户数据字典列表
        """
        # 这里只是简单示例，实际项目中可能需要更复杂的搜索逻辑
        users = self.user_ops.get_all()

        # 简单过滤
        filtered_users = [
            user for user in users
            if keyword.lower() in user.username.lower() or
               keyword.lower() in user.email.lower()
        ]

        # 转换为字典列表
        user_dicts = [user.to_dict() for user in filtered_users]
        log.info(f"Found {len(user_dicts)} users matching keyword '{keyword}'")

        return user_dicts


# MySQL连接配置选项
# 选项1: 使用db_key连接
DB_KEY = 'TXbx'

# 选项2: 使用连接URL连接
DB_URL = 'mysql://sandorn:123456@localhost:3306/bxflb?charset=utf8mb4'

# 当前使用的连接方式
USE_DB_KEY = True  # 设置为True使用db_key，False使用URL


def run_example():
    """运行示例
    
    展示factory.py中各工厂函数的使用方法，包括：
    1. 创建数据库连接
    2. 创建ORM操作对象
    3. 反射现有表
    4. 执行CRUD操作
    """
    db_conn = None
    
    try:
        # 创建数据库连接配置
        conn_config = {'db_key': DB_KEY} if USE_DB_KEY else {'url': DB_URL}
        
        # 1. 示例1: 直接创建数据库连接
        log.info('=== 示例1: 创建数据库连接 ===')
        db_conn = create_sqlconnection(**conn_config, echo=False)
        log.info('成功创建数据库连接')
        
        # 2. 示例2: 通过UserService创建ORM操作对象
        log.info('\n=== 示例2: 通过UserService创建ORM操作 ===')
        user_service = UserService(**conn_config)
        log.info('成功创建UserService，连接状态: 可用')
        
        # 创建表（如果不存在）
        log.info('\n=== 初始化数据库表 ===')
        # UserModel.metadata.create_all(db_conn.engine)
        log.info('数据库表初始化完成')

        # 3. 示例3: 执行CRUD操作
        log.info('\n=== 示例3: 执行CRUD操作 ===')
        
        # 创建新用户（使用唯一用户名）
        import time
        unique_suffix = str(int(time.time()))[-6:]
        username = f'test_user_{unique_suffix}'
        email = f'test_{unique_suffix}@example.com'
        log.info(f'创建新用户... 用户名: {username}')
        new_user = user_service.create_user({
            'username': username,
            'password': 'hashed_password',
            'email': email,
            'nickname': 'Test User',
            'is_active': True
        })
        log.info(f'创建用户成功:{new_user.to_dict()}')

        # 获取用户（根据用户名而不是ID）
        log.info('\n根据用户名获取用户...')
        user_record = user_service.get_user_by_username(username)
        if user_record:
            log.info(f'用户详情: {user_record.to_dict()}')

        # 更新用户（根据用户名而不是ID）
        log.info('\n更新用户信息...')
        # 先根据用户名获取用户ID
        user_for_update = user_service.get_user_by_username(username)
        if user_for_update:
            updated_user = user_service.update_user(
                user_for_update.ID,
                {'nickname': 'Updated Test User', 'email': 'updated@example.com'}
            )
            if updated_user:
                log.info(f'更新后的用户详情: {updated_user.to_dict()}')

        # 分页获取用户
        log.info('\n分页获取用户列表...')
        users = user_service.get_all_users(page=1, page_size=5)
        log.info(f'第1页用户列表: {users}')

        # 搜索用户
        log.info('\n搜索用户...')
        search_results = user_service.search_users('test')
        log.info(f"搜索'test'的结果: {search_results}")

        # 4. 示例4: 直接使用create_orm_operations创建ORM操作对象
        log.info('\n=== 示例4: 直接使用create_orm_operations ===')
        direct_user_ops = create_orm_operations(UserModel, db_conn=db_conn)
        log.info('成功直接创建ORM操作对象')
        
        # 验证直接创建的ORM操作对象
        all_users_count = len(direct_user_ops.get_all())
        log.info(f'使用直接创建的ORM操作获取用户总数: {all_users_count}')

        # 5. 示例5: 反射现有表（如果用户表已经存在）
        log.info('\n=== 示例5: 反射现有表 ===')
        try:
            # 假设用户表名是'users'，实际项目中需要根据数据库中的表名调整
            reflected_model = reflect_table('users', db_conn=db_conn)
            log.info(f'成功反射表users，创建模型类: {reflected_model.__name__}')
            
            # 使用反射的模型创建ORM操作
            reflected_ops = create_orm_operations(reflected_model, db_conn=db_conn)
            reflected_users_count = len(reflected_ops.get_all())
            log.info(f'使用反射模型获取用户总数: {reflected_users_count}')
        except Exception as e:
            log.warning(f'表反射示例失败: {e!s}')

        # 清理: 删除创建的测试用户
        log.info('\n=== 清理测试数据 ===')
        # 先根据用户名获取用户ID
        user_for_delete = user_service.get_user_by_username(username)
        if user_for_delete:
            success = user_service.delete_user(user_for_delete.ID)
            log.info(f"删除测试用户结果: {'成功' if success else '失败'}")
        else:
            log.warning('未找到要删除的测试用户')

        log.ok('\n示例运行完成')

    except Exception as e:
        log.fail(f'示例运行失败: {e!s}')
        raise

    finally:
        # 释放资源
        if db_conn is not None:
            db_conn.dispose()
            log.stop('数据库连接已关闭')


if __name__ == '__main__':

    # 运行示例
    run_example()
