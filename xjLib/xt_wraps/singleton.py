# !/usr/bin/env python
"""
==============================================================
Description  : 单例模式工具模块 - 提供多种线程安全的单例实现方式
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-06 12:00:00
FilePath     : /CODE/xjlib/xt_wraps/singleton.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- SingletonMeta：线程安全的单例元类实现
- SingletonMixin：线程安全的单例混入类实现
- SingletonWraps：增强型单例类装饰器实现
- singleton：基于SingletonWraps的简单单例装饰器函数

主要特性：
- 线程安全：通过双重检查锁机制确保在多线程环境下的安全性
- 内存优化：使用弱引用避免内存泄漏
- 实例管理：支持重置、检查和获取实例的功能
- 异常处理：提供完善的错误捕获和处理机制
- 类型支持：完整的类型注解支持
- 自动垃圾回收：通过弱引用实现实例的自动清理
==============================================================
"""

from __future__ import annotations

from threading import RLock
from typing import Any
from weakref import WeakKeyDictionary, WeakValueDictionary

# 类型别名定义
T = type[Any]
S = type[Any]


class SingletonMeta(type):
    """线程安全的单例元类实现

    核心功能：
    - 通过元类方式实现单例模式
    - 双重检查锁机制确保线程安全
    - 支持实例重置和状态检查
    - 使用弱引用字典避免内存泄漏
    - 完善的异常处理机制

    方法说明：
    - __call__: 获取单例实例，带异常处理
    - reset_instance: 重置单例实例
    - has_instance: 检查是否存在单例实例
    - get_instance: 获取当前单例实例（不创建新实例）

    类属性：
    - _instances: 弱引用字典，存储类与实例的映射关系
    - _instance_lock: 可重入锁，确保线程安全

    使用示例：
        # 基本用法
        class DatabaseConnection(metaclass=SingletonMeta):
            def __init__(self, connection_string: str):
                print(f"初始化数据库连接: {connection_string}")
                self.connection_string = connection_string

        # 创建实例
        db1 = DatabaseConnection("mysql://localhost:3306/db1")
        db2 = DatabaseConnection("mysql://localhost:3306/db2")

        # db1和db2是同一个实例
        print(f"是同一个实例: {db1 is db2}")  # 输出: True
        print(f"连接字符串: {db1.connection_string}")  # 输出: mysql://localhost:3306/db1

        # 实例管理
        print(f"存在实例: {DatabaseConnection.has_instance()}")  # 输出: True

        # 重置实例
        DatabaseConnection.reset_instance()
        print(f"重置后存在实例: {DatabaseConnection.has_instance()}")  # 输出: False

        # 重置后创建新实例
        db3 = DatabaseConnection("mysql://localhost:3306/db3")
        print(f"新连接字符串: {db3.connection_string}")  # 输出: mysql://localhost:3306/db3
    """

    _instances: WeakValueDictionary[type, Any] = WeakValueDictionary()  # 使用弱引用字典来存储实例
    _instance_lock: RLock = RLock()  # 使用可重入锁，避免递归调用问题

    def __call__(cls: T, *args: Any, **kwargs: Any) -> Any:
        """获取单例实例（带异常处理）"""
        # 第一次检查（无锁）
        if cls in cls._instances:
            return cls._instances[cls]

        # 获取锁
        with cls._instance_lock:
            # 第二次检查（有锁）
            if cls in cls._instances:
                return cls._instances[cls]

            try:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
                return instance
            except Exception as e:
                raise RuntimeError(f'SingletonMeta __call__ failed for {cls.__name__}: {e}') from e

    def reset_instance(cls: T) -> None:
        """重置单例实例（通过类调用）"""
        with cls._instance_lock:
            cls._instances.pop(cls, None)  # 移除该类的实例引用

    def has_instance(cls: T) -> bool:
        """检查是否存在单例实例"""
        return cls in cls._instances

    def get_instance(cls: T) -> Any | None:
        """获取当前单例实例（不创建新实例）"""
        return cls._instances.get(cls) if cls in cls._instances else None


class SingletonMixin:
    """线程安全的单例混入类实现

    核心功能：
    - 通过混入方式实现单例模式
    - 支持与其他类的多重继承
    - 双重检查锁确保线程安全
    - 使用弱引用字典避免内存泄漏
    - 提供完整的实例管理接口

    类方法：
    - get_instance: 获取当前单例实例（不创建新实例）
    - reset_instance: 重置单例实例
    - has_instance: 检查是否存在单例实例

    类属性：
    - _instances: 弱引用字典，存储类与实例的映射关系
    - _instance_lock: 可重入锁，确保线程安全

    使用示例：
        # 基本用法
        class ConfigService(SingletonMixin):
            def __init__(self, config_file: str | None = None):
                print(f"加载配置文件: {config_file or '默认配置'}")
                self.config = config_file or 'default_config'

        # 创建实例
        config1 = ConfigService("app_config.json")
        config2 = ConfigService("user_config.json")

        # config1和config2是同一个实例
        print(f"是同一个实例: {config1 is config2}")  # 输出: True
        print(f"配置文件: {config1.config}")  # 输出: app_config.json

        # 实例管理
        print(f"存在实例: {ConfigService.has_instance()}")  # 输出: True

        # 重置实例
        ConfigService.reset_instance()

        # 重置后创建新实例
        config3 = ConfigService("new_config.json")
        print(f"新配置文件: {config3.config}")  # 输出: new_config.json

        # 多重继承示例
        class Loggable:
            def log(self, message: str) -> None:
                print(f"[LOG] {message}")

        class LoggedConfigService(ConfigService, Loggable):
            pass

        logged_config = LoggedConfigService("logged_config.json")
        logged_config.log(f"当前配置: {logged_config.config}")
    """

    _instance_lock: RLock = RLock()  # 使用可重入锁，避免递归调用问题
    _instances: WeakValueDictionary[type, Any] = WeakValueDictionary()

    def __new__(cls: T, *args: Any, **kwargs: Any) -> Any:
        """实例化处理（带错误日志和双重检查锁）"""
        # 第一次检查（无锁）
        if cls in cls._instances:
            return cls._instances[cls]

        # 获取锁
        with cls._instance_lock:
            # 第二次检查（有锁）
            if cls in cls._instances:
                return cls._instances[cls]

            try:
                # 创建实例
                instance = super().__new__(cls)
                # 存储实例引用
                cls._instances[cls] = instance
                # 注意：不手动调用__init__，让Python正常流程处理初始化
                return instance
            except Exception as e:
                # 清理失败的实例
                if cls in cls._instances:
                    del cls._instances[cls]
                # 改进错误处理，记录异常并重新抛出
                raise RuntimeError(f'SingletonMixin {cls.__name__} __new__ failed: {e}') from e

    @classmethod
    def reset_instance(cls: T) -> None:
        """重置单例实例"""
        with cls._instance_lock:
            cls._instances.pop(cls, None)  # 移除该类的实例引用

    @classmethod
    def has_instance(cls: T) -> bool:
        """检查是否存在单例实例"""
        return cls in cls._instances

    @classmethod
    def get_instance(cls: T) -> Any | None:
        """获取当前单例实例（不创建新实例）"""
        return cls._instances.get(cls) if cls in cls._instances else None


class SingletonWraps:
    """线程安全的单例装饰器类实现（增强版）

    核心功能：
    - 作为装饰器类将普通类转换为单例类
    - 支持泛型类型注解，提供完整的类型支持
    - 双重检查锁确保线程安全
    - 使用弱引用字典避免内存泄漏
    - 支持实例重置、检查和获取功能
    - 提供重新初始化实例的选项

    方法说明：
    - __call__: 获取/创建单例实例，支持reinit参数重新初始化
    - reset_instance: 重置单例实例
    - has_instance: 检查是否存在单例实例
    - get_instance: 安全获取实例（处理弱引用，不创建新实例）

    属性说明：
    - _cls: 被装饰的原始类
    - _instance_rlock: 可重入锁，确保线程安全
    - _instances: 弱引用字典，存储类与实例的关联

    使用示例：
        # 基本用法
        @SingletonWraps
        class CacheManager:
            def __init__(self, max_size: int = 100):
                print(f"初始化缓存管理器，最大大小: {max_size}")
                self.cache: dict[Any, Any] = {}
                self.max_size = max_size

        # 创建实例
        cache1 = CacheManager(200)
        cache2 = CacheManager(300)

        # cache1和cache2是同一个实例
        print(f"是同一个实例: {cache1 is cache2}")  # 输出: True
        print(f"缓存最大大小: {cache1.max_size}")  # 输出: 200

        # 实例管理
        print(f"存在实例: {CacheManager.has_instance()}")  # 输出: True
        print(f"获取实例: {CacheManager.get_instance()}")  # 输出: <CacheManager object at ...>

        # 重新初始化实例
        cache3 = CacheManager(400, reinit=True)
        print(f"重新初始化后最大大小: {cache3.max_size}")  # 输出: 400

        # 重置实例
        CacheManager.reset_instance()
        print(f"重置后存在实例: {CacheManager.has_instance()}")  # 输出: False

        # 重置后创建新实例
        cache4 = CacheManager(500)
        print(f"新实例最大大小: {cache4.max_size}")  # 输出: 500
    """

    def __init__(self, cls: S) -> None:
        self._cls: S = cls
        self._instance_rlock: RLock = RLock()  # 使用可重入锁
        self._instances: WeakKeyDictionary[S, Any] = WeakKeyDictionary()  # 使用弱键字典存储类与实例的关联

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """获取/创建单例实例"""
        reinit: bool = kwargs.pop('reinit', False)  # 支持重新初始化

        # 第一次检查（无锁）
        instance = self.get_instance()
        if instance is not None and not reinit:
            return instance

        # 获取锁
        with self._instance_rlock:
            # 第二次检查（有锁）
            instance = self.get_instance()
            if reinit or instance is None:
                try:
                    # 创建新实例
                    instance = self._cls(*args, **kwargs)
                    self._instances[self._cls] = instance
                except Exception as e:
                    raise RuntimeError(f'SingletonWraps __call__ failed for {self._cls.__name__}: {e}') from e

        return instance

    def reset_instance(self) -> None:
        """重置单例实例"""
        with self._instance_rlock:
            self._instances.pop(self._cls, None)

    def has_instance(self) -> bool:
        """检查是否存在单例实例"""
        return self._cls in self._instances

    def get_instance(self) -> Any | None:
        """安全获取实例（处理弱引用,不创建新实例）"""
        return self._instances.get(self._cls)


def singleton(cls: S) -> SingletonWraps:
    """简单的单例装饰器函数

    这是SingletonWraps类的语法糖，提供更简洁的使用方式。
    功能上等同于 @SingletonWraps 装饰器。

    Args:
        cls: 要转换为单例的目标类

    Returns:
        装饰后的类，确保全局只有一个实例

    Example:
        # 基本用法
        @singleton
        class AppConfig:
            def __init__(self):
                print("初始化应用配置")
                self.settings = {"app_name": "MyApp", "version": "1.0"}

        # 创建实例
        config1 = AppConfig()
        config2 = AppConfig()

        # config1和config2是同一个实例
        print(f"是同一个实例: {config1 is config2}")  # 输出: True
        print(f"应用名称: {config1.settings['app_name']}")  # 输出: MyApp

        # 实例管理（通过装饰后的类访问）
        print(f"存在实例: {AppConfig.has_instance()}")  # 输出: True

        # 重置实例
        AppConfig.reset_instance()
        print(f"重置后存在实例: {AppConfig.has_instance()}")  # 输出: False

        # 重置后创建新实例
        config3 = AppConfig()
        print(f"新实例: {config3}")
    """
    return SingletonWraps(cls)
