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

from functools import wraps
from threading import Lock


class SingletonMetaCls(type):
    """
    单例元类,可多次init,构建类时调用
    class MyCls(ParentCls,metaclass=SingletonMetaCls)
    """

    _instance_lock = Lock()

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super().__init__(*args, **kwargs)

    def _init_instance(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance

        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    def __call__(cls, *args, **kwargs):
        reinit = kwargs.pop("reinit", False)
        instance = cls._init_instance(*args, **kwargs)
        if reinit:
            # 重新初始化单例对象属性
            instance.__init__(*args, **kwargs)
        return instance


class SingletonMixin:
    """
    单例模式基类,用于继承,可多次init,
    可用类调用 classmethod
    # 可通过self._intialed判断,设定初始化次数
    """

    _lock = Lock()  # 保护实例字典的线程锁
    _instances = {}  # 保存实例的字典

    def __new__(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances[cls]

        with cls._lock:
            if cls not in cls._instances:
                # 调用基类的__new__方法，创建实例，并将其添加到实例字典
                instance = super().__new__(cls)
                instance._initialized = False  # 为实例添加标志，用于跟踪是否初始化
                cls._instances[cls] = instance

        return cls._instances[cls]

    def __del__(self):
        # 清理实例字典中的引用
        self.__class__._instances.pop(self.__class__, None)


class SingletonDecoratorClass:
    """单例类装饰器,单次init,只能实例调用classmethod"""

    _lock = Lock()

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        with self._lock:
            if self._instance is None:
                self._instance = self._cls(*args, **kwargs)
        return self._instance


def singleton_decorator_factory(_cls):
    """单例类装饰器,多次init,返回类,类属性及方法通用
    # 可通过self._initialized判断,设定初始化次数"""

    class ClassWrapper(_cls):
        _lock = Lock()
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is not None:
                return cls._instance

            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__qualname__ = _cls.__name__
                    cls._instance.__name__ = (
                        f"<{_cls.__name__} | by singleton_decorator_factory>"
                    )
                    cls._instance._initialized = False
            return cls._instance

        def __del__(self):
            self.__class__._instance = None
            self.__class__._initialized = False

    return ClassWrapper


def singleton_wraps_factory(cls_obj):
    """单例装饰器,返回类"""
    _instance_dic = {}
    _instance_lock = Lock()

    @wraps(cls_obj)
    def wrapper(*args, **kwargs):
        # 检查实例是否已存在
        if cls_obj in _instance_dic:
            return _instance_dic[cls_obj]

        with _instance_lock:
            # 再次检查以防多个线程同时创建实例
            if cls_obj not in _instance_dic:
                instance = cls_obj(*args, **kwargs)
                instance._initialized = False
                instance.__name__ = f"<{cls_obj.__name__} | by singleton_wraps_factory>"
                _instance_dic[cls_obj] = instance

        return _instance_dic[cls_obj]

    return wrapper


if __name__ == "__main__":

    class sss:
        def __init__(self, value):
            self.value = value
            self._initialized = True

    super_sss = type("super_sss", (sss, SingletonMixin), {})

    class sample(sss, metaclass=SingletonMetaCls): ...

    class sample_mixin(sss, SingletonMixin): ...

    @singleton_wraps_factory
    class sample_class_wrap(sss): ...

    @singleton_decorator_factory
    class singleton_decorator_factory_f(sss): ...

    singleton_decorator_factory_line = singleton_decorator_factory(sss)

    a = sss("习近平")
    t = super_sss("毛泽东")
    b = sample("胡锦涛")
    c = sample_mixin("江泽民")
    d = sample_class_wrap("李鹏")
    dd = sample_class_wrap("李鹏2")
    z = singleton_decorator_factory_f("邓小平")
    e = singleton_decorator_factory_line("朱镕基")

    print(id(a), id(t), id(b), id(c), d is dd)
    print(e is z, id(e), id(z), e)
