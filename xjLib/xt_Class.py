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
#LastEditTime : 2020-07-10 13:20:29
#Github       : https://github.com/sandorn/home
#==============================================================
'''


class item_get_MixIn:
    '''下标obj[key]'''
    def __getitem__(self, attr):
        return getattr(self, attr)


class item_set_MixIn:
    '''下标obj[key]'''
    def __setitem__(self, attr, value):
        return setattr(self, attr, value)


class item_del_MixIn:
    '''下标obj[key]'''
    def __delitem__(self, attr):
        return delattr(self, attr)


class item_MixIn(item_get_MixIn, item_set_MixIn, item_del_MixIn):
    '''下标obj[key]'''
    pass


class attr_get_MixIn:
    '''原点调用obj.key'''
    def __getattr__(self, attr):
        return super().__getattribute__(attr)
        # return getattr(self, attr)


class attr_set_MixIn:
    '''原点调用obj.key'''
    def __setattr__(self, attr, value):
        return super().__setattr__(attr, value)
        # return setattr(self, attr, value)


class attr_del_MixIn:
    '''原点调用obj.key'''
    def __setattr__(self, attr, value):
        return super().__setattr__(attr, value)
        # return setattr(self, attr, value)


class attr_MixIn(attr_get_MixIn, attr_set_MixIn, attr_del_MixIn):
    '''原点调用obj.key'''
    pass


class dict_MixIn:
    '''生成类字典
    # @暂时弃用'''
    def __init__(self):
        self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}


class iter_MixIn:
    '''
    # #迭代类，用于继承，不支持next
    from collections import Iterable
    print(isinstance(a, Iterable))
    '''
    def __iter__(self):
        if not hasattr(self, '__dict__') or len(self.__dict__) == 0:
            self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}

        return iter(self.__dict__.items())
        # for attr, value in self.__dict__.items():
        #     yield attr, value


class repr_MixIn:
    '''用于打印显示'''
    def __repr__(self):
        if not hasattr(self, '__dict__') or len(self.__dict__) == 0:
            self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}

        return f"{self.__class__.__qualname__}({', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()])})"

    # __str__ = __repr__


class Class_Meta(item_MixIn, iter_MixIn, repr_MixIn):
    '''metaclass=abc.ABCMeta'''
    pass


class SetOnce_MixIn:
    """限制key赋值一次，key不存在时可赋值"""
    __slots__ = ()

    def __setitem__(self, key, value):
        if key not in self:
            return super().__setitem__(key, value)
        raise Exception(str(key) + ' already set')


class SetOnceDict(SetOnce_MixIn, dict):
    """自定义字典,限制key只能赋值一次，key不存在时可添加"""
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


if __name__ == "__main__":
    my_dict = SetOnceDict()
    try:
        my_dict['username'] = '1111'
        my_dict['me'] = 'sandorn'
        my_dict['username'] = 'hellokitty'
    except Exception as err:
        print(err)
    print(99999, my_dict)

    class Animal(iter_MixIn, repr_MixIn):
        def __init__(self):
            self.name = 'na98888me'
            self.age = 12
            self._i = 787
            self.姓名 = '行云流水'

    print(Animal().__dict__)
    print(Animal())
    for k, v in Animal():
        print(k.ljust(8), ':', v)
        pass
