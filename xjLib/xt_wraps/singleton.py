# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-05 17:22:07
FilePath     : /CODE/xjLib/xt_wraps/singleton.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from threading import RLock
from typing import Any, Generic, Optional, Type, TypeVar
from weakref import WeakKeyDictionary, WeakValueDictionary

T = TypeVar("T")


class SingletonMeta(type):
    """
    线程安全的单例元类实现（优化版）

    Features:
    - 双重检查锁确保线程安全
    - 支持重新初始化实例属性
    - 自动垃圾回收（通过弱引用实现）
    - 提供实例管理和重置功能

    Usage:
    class MyClass(metaclass=SingletonMeta):
        def __init__(self, config):
            self.config = config
    """

    _instances = WeakValueDictionary()  # 使用弱引用字典来存储实例
    _instance_lock = RLock()  # 使用可重入锁，避免递归调用问题

    def __call__(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
        """获取单例实例（带异常处理）"""
        # 第一次检查（无锁）
        instance = cls._instances.get(cls)
        if instance is not None:
            return instance

        # 获取锁
        with cls._instance_lock:
            # 第二次检查（有锁）
            instance = cls._instances.get(cls)
            if instance is None:
                try:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
                except Exception as e:
                    raise RuntimeError(
                        f"SingletonMeta __call__ failed for {cls.__name__}: {e}"
                    ) from e
        return instance

    def reset_instance(cls) -> None:
        """重置单例实例（通过类调用）"""
        with cls._instance_lock:
            cls._instances.pop(cls, None)  # 移除该类的实例引用

    def has_instance(cls) -> bool:
        """检查是否存在单例实例"""
        return cls in cls._instances

    def get_instance(cls) -> Optional[Any]:
        """获取当前单例实例（不创建新实例）"""
        return cls._instances.get(cls)


class SingletonMixin:
    """线程安全的单例混入类（带内存优化）

    Features:
    - 使用弱引用避免内存泄漏
    - 支持多继承场景
    - 自动清理实例引用
    - 双重检查锁确保线程安全
    - 异常处理和日志记录

    Usage:
    class MyCls(SingletonMixin):
        def __init__(self, conn_str):
            self.connection = create_connection(conn_str)
    """

    _instance_lock = RLock()  # 使用可重入锁，避免递归调用问题
    _instances = WeakValueDictionary()

    def __new__(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
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
                # 初始化实例
                instance.__init__(*args, **kwargs)
                return instance
            except Exception as e:
                # 清理失败的实例
                if cls in cls._instances:
                    del cls._instances[cls]
                # 改进错误处理，记录异常并重新抛出
                raise RuntimeError(
                    f"SingletonMixin {cls.__name__} __new__ failed: {e}"
                ) from e

    @classmethod
    def reset_instance(cls) -> None:
        """重置单例实例"""
        with cls._instance_lock:
            cls._instances.pop(cls, None)  # 移除该类的实例引用

    @classmethod
    def has_instance(cls) -> bool:
        """检查是否存在单例实例"""
        return cls in cls._instances

    @classmethod
    def get_instance(cls) -> Optional[Any]:
        """获取当前单例实例（不创建新实例）"""
        return cls._instances.get(cls)


class SingletonWraps(Generic[T]):
    """
    增强型单例类装饰器（线程安全+重新初始化支持）

    Features:
    - 双重检查锁提升性能
    - 支持通过 `reinit` 参数重新初始化实例
    - 异常处理机制
    - 类型注解
    - 实例状态检查方法

    Usage:
    @SingletonWraps
    class Database:
        def __init__(self, conn_str):
            self.conn = create_connection(conn_str)
    """

    def __init__(self, cls: Type[T]) -> None:
        self._cls = cls
        self._instance_rlock = RLock()  # 使用可重入锁
        self._instances = WeakKeyDictionary()  # 使用弱键字典存储类与实例的关联

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """获取/创建单例实例"""
        reinit = kwargs.pop("reinit", False)  # 支持重新初始化

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
                    raise RuntimeError(
                        f"SingletonWraps __call__ failed for {self._cls.__name__}: {e}"
                    ) from e

        return instance

    def reset_instance(self) -> None:
        """重置单例实例"""
        with self._instance_rlock:
            self._instances.pop(self._cls, None)

    def has_instance(self) -> bool:
        """检查是否存在单例实例"""
        return self._cls in self._instances

    def get_instance(self) -> Optional[T]:
        """安全获取实例（处理弱引用,不创建新实例）"""
        return self._instances.get(self._cls)

def singleton(cls: Type[T]) -> T:
    """简单的单例装饰器函数（基于SingletonWraps）

    这是一个语法糖，等同于 @SingletonWraps

    Example:
    @singleton
    class AppConfig:
        def __init__(self):
            self.settings = load_config()
    """
    return SingletonWraps(cls)
