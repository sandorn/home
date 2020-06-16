# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-16 16:37:34
#FilePath     : /xjLib/test/class__doc__.py
#LastEditTime : 2020-06-16 16:37:36
#Github       : https://github.com/sandorn/home
#==============================================================
'''
'''
    Python 类的__getattr__ __setattr__ __getitem__ __setitem__ - Vincen_shen - 博客园
    https://www.cnblogs.com/vincenshen/articles/7107522.html

    python中以双下划线的是一些系统定义得名称，让python以更优雅得语法实行一些操作，本质上还是一些函数和变量，与其他函数和变量无二。
    比如x.__add__(y) 等价于 x+y
    有一些很常见，有一些可能比较偏，在这里罗列一下，做个笔记，备忘。
    x.__contains__(y) 等价于 y in x, 在list,str, dict,set等容器中有这个函数
    __base__, __bases__, __mro__, 关于类继承和函数查找路径的。
    class.__subclasses__(), 返回子类列表
    x.__call__(...) == x(...)
    x.__cmp__(y) == cmp(x,y)
    x.__getattribute__('name') == x.name == getattr(x, 'name'),  比__getattr__更早调用
    x.__hash__() == hash(x)
    x.__sizeof__(), x在内存中的字节数, x为class得话， 就应该是x.__basicsize__
    x.__delattr__('name') == del x.name
    __dictoffset__ attribute tells you the offset to where you find the pointer to the __dict__ object in any instance object that has one. It is in bytes.
    __flags__, 返回一串数字，用来判断该类型能否被序列化（if it's a heap type), __flags__ & 512
    S.__format__, 有些类有用
    x.__getitem__(y) == x[y], 相应还有__setitem__, 某些不可修改类型如set，str没有__setitem__
    x.__getslice__(i, j) == x[i:j], 有个疑问，x='123456789', x[::2],是咋实现得
    __subclasscheck__(), check if a class is subclass
    __instancecheck__(), check if an object is an instance

    你真的了解__instancecheck__、__subclasscheck__、__subclasshook__三者的用法吗 - 古明地盆 - 博客园
    https://www.cnblogs.com/traditional/p/11731676.html

    __itemsize__, These fields allow calculating the size in bytes of instances of the type. 0是可变长度， 非0则是固定长度
    x.__mod__(y) == x%y, x.__rmod__(y) == y%x
    x.__module__ , x所属模块
    x.__mul__(y) == x*y,  x.__rmul__(y) == y*x

    __reduce__, __reduce_ex__ , for pickle

    __slots__ 使用之后类变成静态一样，没有了__dict__, 实例也不可新添加属性

    __getattr__ 在一般的查找属性查找不到之后会调用此函数

    __setattr__ 取代一般的赋值操作，如果有此函数会调用此函数， 如想调用正常赋值途径用 object.__setattr__(self, name, value)

    __delattr__ 同__setattr__, 在del obj.name有意义时会调用
'''
