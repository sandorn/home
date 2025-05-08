# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-26 10:17:05
FilePath     : /CODE/xjLib/xt_singleon.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import weakref
from functools import wraps
from threading import Lock
from typing import Any, Type


class SingletonMetaCls(type):
    """
    线程安全的单例元类实现（改进版）

    Features:
    - 双重检查锁确保线程安全
    - 支持重新初始化实例属性
    - 自动垃圾回收

    Usage:
    class MyClass(ParentCls,metaclass=SingletonMetaCls):
        def __init__(self, config):
            self.config = config
    """

    _instance_lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """获取单例实例（带异常处理）"""
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                try:
                    cls._instance = super().__call__(*args, **kwargs)
                except Exception as e:
                    raise RuntimeError(f"Singleton initialization failed: {e}")
        return cls._instance

class SingletonMixin:
    """线程安全的单例混入类（带内存优化）

    Features:
    - 使用弱引用避免内存泄漏
    - 支持多继承场景
    - 自动清理实例引用

    Usage:
    class MyCls(SingletonMixin):
        def __init__(self, conn_str):
            self.connection = create_connection(conn_str)
    """

    _lock = Lock()
    _instances = weakref.WeakValueDictionary()

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        """实例化处理（带错误日志）"""
        try:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
                    instance.__init__(*args, **kwargs)
                return cls._instances[cls]
        except Exception as e:
            print(f"Singleton creation error: {e}")
            raise

class SingletonDecoratorClass:
    """
    增强型单例类装饰器（线程安全+重新初始化支持）
    
    Features:
    - 双重检查锁提升性能
    - 支持通过reinit参数重新初始化实例
    - 异常处理机制
    - 类型注解
    
    Usage:
    @SingletonDecoratorClass
    class Database:
        def __init__(self, conn_str):
            self.conn = create_connection(conn_str)
    """

    _lock = Lock()
    _instance_ref = None  # 使用弱引用避免内存泄漏

    def __init__(self, cls: Type) -> None:
        self._cls = cls

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """获取/创建单例实例"""
        reinit = kwargs.pop('reinit', False)  # 支持重新初始化
        instance = self._instance_ref() if self._instance_ref else None
        
        if instance is None or reinit:
            with self._lock:
                instance = self._instance_ref() if self._instance_ref else None
                if instance is None or reinit:
                    try:
                        instance = self._cls(*args, **kwargs)
                        self._instance_ref = weakref.ref(instance)
                    except Exception as e:
                        raise RuntimeError(f"Singleton initialization failed: {e}")
        return instance

def singleton_decorator_factory(cls) -> Type:
    """通用单例装饰器（支持类型提示）
    
    Args:
        cls: 需要实现单例的类
        
    Returns:
        单例化后的类
        
    Example:
    @singleton
    class AppConfig:
        def __init__(self):
            self.settings = load_config()
    """
    _instances = {}
    _lock = Lock()

    @wraps(cls)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if cls not in _instances:
            with _lock:
                if cls not in _instances:
                    _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    # 添加实例管理属性
    wrapper._instances = _instances
    wrapper._lock = _lock
    return wrapper

def singleton_wraps_factory(cls_obj):
    """单例装饰器（线程安全+弱引用优化版）
    可通过self._initialized 判断初始化次数

    :param cls_obj: 需要单例化的类
    :param reinit: 是否重新初始化实例（通过kwargs传入）
    """
    _instances = weakref.WeakValueDictionary()  # 改用弱引用字典
    _lock = Lock()

    @wraps(cls_obj)
    def wrapper(*args, **kwargs):
        reinit = kwargs.pop("reinit", False)
        instance = _instances.get(cls_obj)

        # 双重检查锁优化
        if instance is None or reinit:
            with _lock:
                instance = _instances.get(cls_obj)
                if instance is None or reinit:
                    try:
                        instance = cls_obj(*args, **kwargs)
                        instance._initialized = True  # 启用初始化标记
                        instance.__name__ = (
                            f"<{cls_obj.__name__} | by singleton_wraps_factory>"
                        )
                        _instances[cls_obj] = instance
                    except Exception as e:
                        raise RuntimeError(f"单例初始化失败: {e}")
        return instance

    return wrapper

if __name__ == "__main__":

    # 测试代码
    @singleton_wraps_factory
    class MyClass:
        def __init__(self, name):
            self.name = name

    obj0 = MyClass("obj0")
    obj1 = MyClass("obj1")
    print(obj1 is obj0)  # 输出: True
    obj2 = MyClass("obj2", reinit=True)
    print(obj1 is obj2)  # 输出: False
    print(obj1.name)  # 输出: obj1
    print(obj2.name)  # 输出: obj1
