# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-30 14:25:16
#FilePath     : /xjLib/xt_Class.py
#LastEditTime : 2020-06-23 17:42:25
#Github       : https://github.com/sandorn/home
#==============================================================
'''


class item_MixIn:
    '''下标obj[key]'''
    def __getitem__(self, attr):
        return getattr(self, attr)

    def __setitem__(self, attr, value):
        return setattr(self, attr, value)

    def __delitem__(self, attr):
        return delattr(self, attr)


class attr_MixIn:
    '''
    原点调用obj.key
    不可使用init
    '''
    def __getattr__(self, attr):
        return super().__getattribute__(attr)
        # return getattr(self, attr)

    def __setattr__(self, attr, value):
        return super().__setattr__(attr, value)
        # return setattr(self, attr, value)

    def __delattr__(self, attr, value):
        return delattr(self, attr)


class dict_MixIn:
    '''生成类字典'''
    def __init__(self):
        self.__dict__ = {
            key: getattr(self, key)
            for key in dir(self)
            if not key.startswith('__') and not callable(getattr(self, key))
        }


class iter_MixIn:
    '''
    # #迭代类，用于继承
    from collections import Iterable
    print(isinstance(a, Iterable))
    '''
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class repr_MixIn:
    '''用于打印显示'''
    def __repr__(self):
        tmp = str(self.__dict__).replace('{', '').replace('}', '')
        return self.__class__.__name__ + '(' + tmp + ')'

    __str__ = __repr__


class Class_Meta(dict_MixIn, item_MixIn, attr_MixIn, iter_MixIn, repr_MixIn):
    '''metaclass=abc.ABCMeta'''
    pass


def typeassert(**kwargs):
    '''Descriptor for a type-checked attribute
    #限制属性赋值的类型，因使用__dict__,与slots冲突'''
    class Typed:
        def __init__(self, name, expected_type):
            self.name = name
            self.expected_type = expected_type

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return instance.__dict__[self.name]

        def __set__(self, instance, value):
            if not isinstance(value, self.expected_type):
                raise TypeError('Expected ' + str(self.expected_type))
            instance.__dict__[self.name] = value

        def __delete__(self, instance):
            del instance.__dict__[self.name]

    # Class decorator that applies it to selected attributes
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls, name, Typed(name, expected_type))
        return cls

    return decorate


def typed_property(name, expected_type):
    '''class类property属性生成器,限制赋值类型'''
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError('{} must be a {}'.format(name, expected_type))
        setattr(self, storage_name, value)

    return prop


def readonly(name):
    '''
    class类property只读属性生成器,隐藏真实属性名:name,
    #不在__dict__内,需要使用class_to_dict函数生成类__dict__
    #可配合@dataclass(init=False)
    '''
    storage_name = name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        '''赋值：无操作，直接返回'''
        return

    return prop
