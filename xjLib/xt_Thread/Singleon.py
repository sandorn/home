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


class Singleton_Mixin:
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
                instance = super().__new__(cls)
                # 为实例添加一个标志，用于跟踪是否初始化
                instance._intialed = False
                cls._instance[cls] = instance

        return cls._instance[cls]

    def __del__(self):
        self.__class__._instance[self] = None


class Singleton_Meta(type):
    """
    单例模式元类,构建类时调用
    class cls(parent_cls,metaclass=Singleton_Meta):,
    @ 单次init,可用类调用classmethod
    """

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class singleton_wrap_class:
    """单例类装饰器,单次init,只能实例调用classmethod
    # @QThread可用
    """

    _lock = Lock()

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        with self._lock:
            if self._instance is None:
                self._instance = self._cls(*args, **kwargs)
        return self._instance


def singleton_wrap_return_class(_cls):
    """单例类装饰器,多次init,返回类,类属性及方法通用
    # 可通过self._intialed判断,设定初始化次数"""

    class class_wrapper(_cls):
        _lock = Lock()
        _instance = None

        def __new__(cls, *args, **kwargs):
            with cls._lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super().__new__(cls)
                    cls._instance.__qualname__ = _cls.__name__
                    cls._instance._intialed = False
            return cls._instance

        def __del__(self):
            self.__class__._instance = None
            self.__class__._intialed = False

    return class_wrapper


def singleton_wrap(cls):
    """单例装饰器,单次init,只能实例调用classmethod
    命令行可用,装饰器形式需要类有parent_cls"""
    _instance = {}
    _lock = Lock()

    @wraps(cls)
    def _singleton(*args, **kwargs):
        with _lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


if __name__ == '__main__':

    class sss:
        def __init__(self, string, age=12):
            self.name = string
            self.age = age

    super_sss = type('super_sss', (sss, Singleton_Mixin), {})

    class sample(sss, metaclass=Singleton_Meta):
        pass

    class sample_mixin(sss, Singleton_Mixin):
        pass

    @singleton_wrap_class
    class sample_class_wrap(sss):
        pass

    @singleton_wrap_return_class
    class singleton_wrap_return_class_f(sss): ...

    singleton_wrap_return_class_f_line = singleton_wrap_return_class(sss)

    @singleton_wrap
    class singleton_wrap_f(sss): ...

    # singleton_wrap_f_line = singleton_wrap(sss)

    # aa = singleton_wrap_return_class_f('张三')
    # bb = singleton_wrap_return_class_f('李四', 28)
    # bb.old = 99
    # # print(aa)
    # print(bb)
    # # print(bb.__name__)
    # print(aa is bb, id(aa), id(bb), aa.__dict__, bb.__dict__)
    # cc = t()
    # cc.a = 88
    # dd = tt()
    # ee = tt()
    # ee.b = 987
    # dd.a = 4444
    # print(aa is bb, ee is dd, id(aa), id(bb), id(cc), id(dd), aa.__dict__, bb.__dict__, cc.__dict__, dd.__dict__)
    # print(11111, sample.__mro__)
    # print(22222, sample.__base__)
    # print(33333, sample.__bases__)
    # print(44444, sample.__mro__)
    t1 = singleton_wrap_f('习近平')
    t2 = super_sss('胡锦涛')
    print(t1 is t2, t1.__dict__, t2.__dict__)
