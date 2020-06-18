# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-17 13:46:12
#FilePath     : /xjLib/test/meta_class--test.py
#LastEditTime : 2020-06-17 15:38:10
#Github       : https://github.com/sandorn/home
#==============================================================
深刻理解Python中的元类(metaclass)以及元类实现单例模式 - 苍松 - 博客园
https://www.cnblogs.com/tkqasn/p/6524879.html
'''


# 元类会自动将你通常传给‘type’的参数作为自己的参数传入
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items()
             if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    #通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents,
                uppercase_attr)  #返回一个类


class Foo1(metaclass=upper_attr):
    __metaclass__ = upper_attr
    bar = 'bip'


class UpperAttrMetaclass(type):
    def __new__(cls, cls_name, bases, attr_dict):
        uppercase_attr = {}
        for name, val in attr_dict.items():
            if name.startswith('__'):
                uppercase_attr[name] = val
            else:
                uppercase_attr[name.upper()] = val
        return super(UpperAttrMetaclass, cls).__new__(cls, cls_name, bases,
                                                      uppercase_attr)


class Foo(metaclass=UpperAttrMetaclass):
    # this __metaclass__ will affect the creation of this new style class
    __metaclass__ = UpperAttrMetaclass
    bar = 'bar'


print(hasattr(Foo, 'bar'))  # False

print(hasattr(Foo, 'BAR'))  # True

f = Foo()
print(f.BAR)
f1 = Foo1()
print(f1.BAR)
# 'bar'

#coding: utf-8
'''
python编程题(继承和元类)_yz764127031的博客-CSDN博客
https://blog.csdn.net/yz764127031/article/details/79099456?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-2
2.自动注册子类
实现一个名为 Base 的类，且任何继承自 Base 子类将被记录，且可以通过迭代 Base 输出所有的子类名称。
'''


class IterableBase(type):
    def __iter__(cls):
        return iter(cls.__subclasses__())

    def __str__(cls):
        return cls.__name__


class Base(metaclass=IterableBase):
    pass


class Lab(Base):
    pass


class Course(Base):
    pass


for cls in Base:
    print(cls)


class selfreigster(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'subclasses'):
            cls.subclasses = []
        else:
            cls.subclasses.append(cls)
        super(selfreigster, cls).__init__(name, bases, dct)

    def __iter__(self):
        return iter(self.subclasses)

    def __str__(self):
        return self.__name__


class Bases(object, metaclass=selfreigster):
    """docstring for Base"""
    pass


class Labs(Bases):
    pass


class Courses(Bases):
    pass


for cls in Bases:
    print(cls)


def namedtuple(tuple_name, attrs):
    class Meta(type):
        def __call__(self, *args):
            return type.__call__(self, args)

    attrs_set = set(attrs)

    def __init__(self, args):
        print('__init__', args)
        for key, value in zip(attrs, args):
            self.__dict__[key] = value

    def __str__(self):
        values = [str(x) for x in self.__dict__.values()]
        return tuple_name + '(' + ', '.join(values) + ')'

    def to_dict(self):
        return self.__dict__

    return Meta(
        tuple_name, (tuple, ), {
            'attr_keys': attrs_set,
            '__init__': __init__,
            '__str__': __str__,
            'to_dict': to_dict
        })


Point = namedtuple('PX', ['x', 'y'])
p = Point(1, 2)
print(p)
