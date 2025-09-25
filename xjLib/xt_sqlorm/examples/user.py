#!/usr/bin/env python3
"""
==============================================================
Description  : 用户模型定义模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:20:00
LastEditTime : 2024-09-22 10:20:00
FilePath     : /code/xt_sqlorm/models/user.py
Github       : https://github.com/sandorn/home

本模块定义用户相关数据库模型
==============================================================
"""

from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from xt_sqlorm.models.base import BaseModel
from xt_sqlorm.models.mixins import IdMixin, TimestampMixin
from xt_sqlorm.models.types import JsonEncodedDict


class ValidatedJsonEncodedDict(JsonEncodedDict):
    def process_bind_param(self, value, dialect):
        if value is not None and not isinstance(value, dict):
            raise ValueError('Value must be a dictionary')
        # 可以添加更复杂的验证逻辑
        return super().process_bind_param(value, dialect)


# 或者创建专门的类型
class PreferencesType(JsonEncodedDict):
    """专门用于存储用户偏好的JSON类型"""
    pass


class UserModel(BaseModel, IdMixin, TimestampMixin):
    """用户模型
    
    定义用户表结构和字段
    """
    __tablename__ = 'users'
    
    # 基础信息
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    
    # 状态信息
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # 个人信息
    nickname = Column(String(50))
    avatar = Column(String(255))
    
    # 扩展字段
    last_login_at = Column(DateTime)
    login_count = Column(Integer, default=0)
    
    def __init__(self, **kwargs):
        """初始化用户模型"""
        super().__init__(**kwargs)
        if 'created_at' not in kwargs:
            self.created_at = func.now()
        if 'updated_at' not in kwargs:
            self.updated_at = func.now()
    
    def update_login_info(self):
        """更新登录信息"""
        self.last_login_at = func.now()
        self.login_count += 1


class UserProfileModel(BaseModel, IdMixin):
    """用户资料模型
    
    定义用户扩展资料表结构和字段
    """
    __tablename__ = 'user_profiles'
    
    user_id = Column(Integer, nullable=False)
    real_name = Column(String(50))
    gender = Column(String(10))
    birth_date = Column(DateTime)
    address = Column(String(255))
    bio = Column(String(500))
    preferences = Column(PreferencesType)  # 存储用户偏好
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


if __name__ == '__main__':
    # 使用示例
    profile = UserProfileModel(
        user_id=1, 
        preferences={
        'theme': 'dark',
        'language': 'zh-CN',
        'notifications': {
            'email': True,
            'push': False,
            'sms': True
        },
        'privacy': {
            'profile_public': True,
            'search_indexed': False
        }
    })
