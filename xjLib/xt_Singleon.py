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
    单例元类,可多次init，构建类时调用
    class MyCls(ParentCls,metaclass=SingletonMetaCls)
    """

    _instance_lock = Lock()

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        super().__init__(*args, **kwargs)

    def _init_instance(cls, *args, **kwargs):
        if cls._instance:
            # 存在实例对象直接返回，减少锁竞争，提高性能
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
    _instance = {}  # 保存实例的字典

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instance:
                # 调用基类的__new__方法，创建实例，并将其添加到实例字典
                instance = super().__new__(cls)  # 为实例添加一个标志，用于跟踪是否初始化
                setattr(instance, "_initialized", False)
                cls._instance[cls] = instance

        return cls._instance[cls]

    def __del__(self):
        self.__class__._instance[self] = None


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


def singleton_decorator_class(_cls):
    """单例类装饰器,多次init,返回类,类属性及方法通用
    # 可通过self._initialized判断,设定初始化次数"""

    class Class_Wrapper(_cls):
        _lock = Lock()
        _instance = None

        def __new__(cls, *args, **kwargs):
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__qualname__ = _cls.__name__
                    cls._instance.__name__ = f"<{_cls.__name__} | by singleton_decorator_class>"
                    cls._instance._initialized = False
            return cls._instance

        def __del__(self):
            self.__class__._instance = None
            self.__class__._initialized = False

    return Class_Wrapper


def singleton_wraps_class(cls_obj):
    """单例装饰器,返回类"""
    _instance_dic = {}
    _instance_lock = Lock()

    @wraps(cls_obj)
    def wrapper(*args, **kwargs):
        if cls_obj in _instance_dic:
            cls_obj.__name__ = f"<{cls_obj.__name__} | by singleton_wraps_class>"
            return _instance_dic.get(cls_obj)

        with _instance_lock:
            if cls_obj not in _instance_dic:
                _instance_dic[cls_obj] = cls_obj(*args, **kwargs)
                _instance_dic[cls_obj]._intialed = False
                _instance_dic[cls_obj].__name__ = f"<{cls_obj.__name__} | by singleton_wraps_class>"
        return _instance_dic.get(cls_obj)

    return wrapper


if __name__ == "__main__":

    class sss:
        def __init__(self, name, age=12):
            self.name = name
            self.age = age

    super_sss = type("super_sss", (sss, SingletonMixin), {})

    class sample(sss, metaclass=SingletonMetaCls): ...

    class sample_mixin(sss, SingletonMixin): ...

    @singleton_wraps_class
    class sample_class_wrap(sss): ...

    @singleton_decorator_class
    class singleton_decorator_class_f(sss): ...

    singleton_decorator_class_line = singleton_decorator_class(sss)

    a = sss("习近平")
    t = super_sss("毛泽东")
    b = sample("胡锦涛")
    c = sample_mixin("江泽民")
    d = sample_class_wrap("李鹏")
    dd = sample_class_wrap("李鹏2")
    z = singleton_decorator_class_f("邓小平")
    e = singleton_decorator_class_line("朱镕基")

    print(id(a), id(t), id(b), id(c), d is dd)
    print(e is z, id(e), id(z), e)
