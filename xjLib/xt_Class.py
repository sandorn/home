# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-30 14:25:16
FilePath     : /xjLib/xt_Class.py
LastEditTime : 2021-04-14 19:35:50
#Github       : https://github.com/sandorn/home
#==============================================================
'''


class item_get_Mixin:
    '''下标obj[key]'''

    def __getitem__(self, key):
        # return getattr(self, key)
        return self.__dict__.get(key)


class item_set_Mixin:
    '''下标obj[key]'''

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class item_del_Mixin:
    '''下标obj[key]'''

    def __delitem__(self, key):
        return self.__dict__.pop(key)


class item_Mixin(item_get_Mixin, item_set_Mixin, item_del_Mixin):
    '''下标obj[key]'''
    pass


class attr_get_Mixin:
    '''原点调用obj.key'''

    def __getattr__(self, key):
        # return super().__getattribute__(key)
        return self.__dict__.get(key)


class attr_set_Mixin:
    '''原点调用obj.key'''

    def __setattr__(self, key, value):
        return super().__setattr__(key, value)


class attr_del_Mixin:
    '''原点调用obj.key'''

    def __delattr__(self, key):
        return super().__delattr__(key)


class attr_Mixin(attr_get_Mixin, attr_set_Mixin, attr_del_Mixin):
    '''原点调用obj.key'''
    pass


class dict_mothed_Mixin:
    '''get_dict重新生成__dict__类字典,主要用于readonly限制'''

    def get_dict(self):
        '''把对象转换成字典'''
        if not hasattr(self, '__dict__') or len(self.__dict__) == 0:
            self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}
        return self.__dict__


class iter_Mixin(dict_mothed_Mixin):
    '''
    # #迭代类,用于继承,不支持next
    from collections import Iterable
    isinstance(a, Iterable)
    '''

    def __iter__(self):
        # for attr, value in self.__dict__.items():
        #     yield attr, value
        return iter(self.get_dict().items())


class repr_Mixin(dict_mothed_Mixin):
    '''用于打印显示'''

    # __str__ = __repr__
    def __repr__(self):
        dic = self.__dict__
        # # __class__.__name__
        return f"{self.__class__.__qualname__}({', '.join([f'{k}={v!r}' for k, v in dic.items()])})"


class Class_Meta(item_Mixin, iter_Mixin, repr_Mixin):
    '''metaclass=abc.ABCMeta'''
    pass


class SetOnce_Mixin:
    """限制key赋值一次,key不存在时可赋值"""
    __slots__ = ()

    def __setitem__(self, key, value):
        if key not in self:
            return super().__setitem__(key, value)
        raise Exception(str(key) + ' already set')


class SetOnceDict(SetOnce_Mixin, dict):
    """自定义字典,限制key只能赋值一次,key不存在时可添加"""
    pass


def typeassert(**kwargs):
    '''Descriptor for a type-checked attribute
    #限制属性赋值的类型,因使用__dict__,与slots冲突'''

    class Typed:

        def __init__(self, name, expected_type):
            self.name = name
            self.expected_type = expected_type

        def __get__(self, instance, cls):
            return self if instance is None else instance.__dict__[self.name]

        def __set__(self, instance, value):
            assert isinstance(value, self.expected_type)
            # raise TypeError('Expected ' + str(self.expected_type))
            instance.__dict__[self.name] = value

        def __delete__(self, instance):
            del instance.__dict__[self.name]

    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls, name, Typed(name, expected_type))
        return cls

    return decorate


def typed_property(name, expected_type):
    '''class类property属性生成器,限制赋值类型'''
    storage_name = f'_{name}'

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
        '''赋值:无操作,直接返回'''
        return

    return prop


if __name__ == "__main__":

    def one():
        my_dict = SetOnceDict()
        try:
            my_dict['username'] = '1111'
            my_dict['me'] = 'sandorn'
            my_dict['username'] = 'hellokitty'
        except Exception as err:
            print(err)
        print(99999, my_dict)

    def itre():

        class Animal(iter_Mixin, repr_Mixin):

            def __init__(self):
                self.name = 'na98888me'
                self.age = 12
                self._i = 787
                self.姓名 = '行云流水'

        bb = Animal()
        print(bb)
        for k, v in bb:
            print(k.ljust(6), ':', v)

    def itat():

        class Anima(item_Mixin, attr_Mixin):

            def __init__(self):
                self.name = 'na98888me'
                self.age = 12
                self._i = 787
                self.姓名 = '行云流水'

        a = Anima()
        a['name'] = '张三李四'
        print(a['names'])
        del a['_i']
        b = Anima()
        b._i = 567
        print(a.name555s)
        del b.name
        print(a.__dict__, a['age'], id(a))
        print(id(b.__dict__), b.__dict__, b.age, id(b))

    # one()
    itre()
    # itat()
'''
参考见Alispeech/xt_Pygame.py
xt_Thread/Custom.py
xt_Singleon.py

# 方法1:工厂函数
def createClass(cls):
    class CustomizedClass(cls):
        .......
    return CustomizedClass

ClassList = createClass(list)

# 方法2:type完全动态构造
# 方法3:type混入继承,动态修改
# 方法4:class 混入继承

# 方法3:明示重置class.__bases__  = (指定父类,) class 要隔代继承object,QThread出错

print(QThread.__mro__)
(<class 'PyQt5.QtCore.QThread'>, <class 'PyQt5.QtCore.QObject'>, <class 'sip.wrapper'>, <class 'sip.simplewrapper'>, <class 'object'>)

'''
