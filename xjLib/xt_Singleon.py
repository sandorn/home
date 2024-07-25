# !/usr/bin/env python
"""
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-23 17:41:52
FilePath     : /xjLib/xt_Singleon.py
LastEditTime : 2020-12-08 12:30:49
#Github       : https://github.com/sandorn/home
#==============================================================
单例，与线程无关
"""

from functools import wraps
from threading import Lock


class SingletonMetaCls(type):
    """
    单例元类，构建类时：metaclass=SingletonMetaCls
    有重新__init__方法，可多次init
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


class SingletonMeta(type):
    """
    单例模式元类,构建类时调用
    class cls(parent_cls,metaclass=SingletonMeta):,
    @ 单次init,可用类调用classmethod
    """

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


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
    # 可通过self._intialed判断,设定初始化次数"""

    class Class_Wrapper(_cls):
        _lock = Lock()
        _instance = None

        def __new__(cls, *args, **kwargs):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
                    cls._instance.__qualname__ = _cls.__name__
                    cls._instance._intialed = False
            return cls._instance

        def __del__(self):
            self.__class__._instance = None
            self.__class__._intialed = False

    return Class_Wrapper


def singleton_wraps_class(cls_obj):
    """单例装饰器,返回类，#@未测试"""
    _instance_dic = {}
    _instance_lock = Lock()

    @wraps(cls_obj)
    def wrapper(*args, **kwargs):
        if cls_obj in _instance_dic:
            return _instance_dic.get(cls_obj)

        with _instance_lock:
            if cls_obj not in _instance_dic:
                _instance_dic[cls_obj] = cls_obj(*args, **kwargs)
        return _instance_dic.get(cls_obj)

    return wrapper


if __name__ == "__main__":

    class sss:
        def __init__(self, string, age=12):
            self.name = string
            self.age = age

    super_sss = type("super_sss", (sss, SingletonMixin), {})

    class sample(sss, metaclass=SingletonMeta): ...

    class sample_mixin(sss, SingletonMixin): ...

    @singleton_wraps_class
    class sample_class_wrap(sss): ...

    @singleton_decorator_class
    class singleton_decorator_class_f(sss): ...

    singleton_decorator_class_f_line = singleton_decorator_class(sss)

    a = sss("习近平")
    t = super_sss("毛泽东")
    b = sample("胡锦涛")
    c = sample_mixin("江泽民")
    d = sample_class_wrap("李鹏")
    z = singleton_decorator_class_f("邓小平")
    e = singleton_decorator_class_f_line("朱镕基")

    print(id(a), id(t), id(b), id(c), id(d))
    print(e is z, id(e), id(z))
