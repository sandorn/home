# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-10-20 10:47:17
FilePath     : /CODE/xjLib/xt_Class.py
Github       : https://github.com/sandorn/home
==============================================================
"""


class ItemGetMixin:
    """下标调用（索引操作）[key]"""

    def __getitem__(self, key):
        # return getattr(self, key, None)
        return self.__dict__.get(key, None)


class ItemSetMixin:
    """下标调用（索引操作）[key]"""

    def __setitem__(self, key, value):
        # return setattr(self, key, value)
        self.__dict__[key] = value


class ItemDelMixin:
    """下标调用（索引操作）[key]"""

    def __delitem__(self, key):
        # return delattr(self, key)
        return self.__dict__.pop(key)


class ItemMixin(ItemGetMixin, ItemSetMixin, ItemDelMixin): ...


class AttrGetMixin:
    """原点调用（属性访问）cls.key"""

    def __getattr__(self, key):
        # return getattr(self, key, None)
        # return super().__getattribute__(key)
        return self.__dict__.get(key, None)


class AttrSetMixin:
    """原点调用（属性访问）cls.key"""

    def __setattr__(self, key, value):
        return super().__setattr__(key, value)


class AttrDelMixin:
    """原点调用（属性访问）cls.key"""

    def __delattr__(self, key):
        return super().__delattr__(key)


class AttrMixin(AttrGetMixin, AttrSetMixin, AttrDelMixin): ...


class ReDictMixin:
    """get_dict重新生成 __dict__ 类字典,主要用于readonly限制"""

    def get_dict(self):
        """把对象转换成字典"""
        if not hasattr(self, "__dict__") or len(self.__dict__) == 0:
            self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith("__") and not callable(getattr(self, key))}
        return self.__dict__


class IterMixin:
    """
    # #迭代类,用于继承,不支持next
    from collections import Iterable
    isinstance(a, Iterable)
    """

    def __iter__(self):
        yield from self.__dict__.items()
        # return iter(self.get_dict().items())


class ReprMixin(ReDictMixin):
    """用于打印显示"""

    def __repr__(self):
        dic = self.get_dict()
        return f"{self.__class__.__qualname__}({', '.join([f'{k}={v!r}' for k, v in dic.items()])})"


class BaseCls(AttrMixin, ItemMixin, IterMixin, ReprMixin): ...  # 基类,支持下标,迭代,打印


class SetOnceMixin(ItemGetMixin, AttrGetMixin):
    """限制下标[key]赋值,key不存在时可赋值；对属性访问无用"""

    __slots__ = ()

    def __setitem__(self, key, value):
        if key not in self:
            return super().__setitem__(key, value)
        raise ValueError(f"key:`{key}` is already set,cannot reset value to `{value}`!")

    def __setattr__(self, key, value):
        if key not in self:
            return super().__setattr__(key, value)
        raise ValueError(f"key:`{key}` is already set,cannot reset value to `{value}`!")


class SetOnceDict(SetOnceMixin, dict): ...  # 自定义字典,限制key只能赋值一次,key不存在时可添加


class LogMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")


class ClsMeta(type):
    """
    更智能的元类，根据类属性动态选择Mixin
    class BaseClsMeta(metaclass=ClsMeta):
        MixinAttr = True
        MixinItem = True
        MixinIter = True
        MixinRepr = True
        MixinLog = True
    """

    def __new__(cls, name, bases, dct):
        bases_mixins = ()  # 用于存放要应用的Mixin类
        bases_mixins += (bases,) if bases else ()
        bases_mixins += (ItemMixin,) if "MixinItem" in dct and dct["MixinItem"] else ()
        bases_mixins += (AttrMixin,) if "MixinAttr" in dct and dct["MixinAttr"] else ()
        bases_mixins += (IterMixin,) if "MixinIter" in dct and dct["MixinIter"] else ()
        bases_mixins += (ReprMixin,) if "MixinRepr" in dct and dct["MixinRepr"] else ()
        bases_mixins += (LogMixin,) if "MixinLog" in dct and dct["MixinLog"] else ()
        # mixins_to_apply = []
        # if "MixinAttr" in dct and dct["MixinAttr"]:
        #     mixins_to_apply.append(AttrMixin)

        # for mixin in mixins_to_apply:
        #     dct.update(mixin.__dict__)  # 动态添加属性和方法
        # return super().__new__(cls, name, bases, dct)

        # print(99999999999999999999999999, f"name:{name}, bases_mixins:{bases_mixins}, dct:{dct}")
        return type(name, bases_mixins, dct)


def typeassert(**kwargs):
    """Descriptor for a type-checked attribute
    #限制属性赋值的类型,因使用__dict__,与slots冲突"""

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
    """class类property属性生成器,限制赋值类型"""
    storage_name = f"_{name}"

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be a {expected_type}")
        setattr(self, storage_name, value)

    return prop


def readonly(name):
    """
    class类property只读属性生成器,隐藏真实属性名:name,
    #不在__dict__内,需要使用class_to_dict函数生成类__dict__
    #可配合@dataclass(init=False)
    # from dataclasses import asdict, dataclass
    @dataclass(frozen=True) #frozen=True,不可修改
    """
    storage_name = name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        """赋值:无操作,直接返回"""
        return

    return prop


if __name__ == "__main__":

    def 赋值一次的字典():
        my_dict = SetOnceDict()
        try:
            my_dict["username"] = "sand"
            my_dict["me"] = "orny"
            my_dict["efvtgn"] = "sandorny"
            my_dict.me = 99
            # my_dict["me"] = "49"

        except Exception as err:
            print(err)
        print(99999, my_dict, my_dict.me)

    def 可迭代对象():
        class Animal(IterMixin, ReprMixin):
            def __init__(self):
                self.name = "liuxinjun"
                self.age = 12
                self._i = 787
                self.姓名 = "行云流水"

        bb = Animal()
        print(bb)
        for k, v in bb:
            print(k.ljust(16), ":", v)

    def itat():
        class Anima(ItemMixin, AttrMixin):
            def __init__(self):
                self.name = "na98888me"
                self.age = 12
                self._i = 787
                self.姓名 = "行云流水"

        a = Anima()
        a["name"] = "张三李四"
        print(a["names99"])
        del a["姓名"]
        b = Anima()
        b._i = 567
        print(a.name555s)
        del b.name
        print(a.__dict__, id(a))
        print(b.__dict__, id(b))

    def metaclass():
        _registry = []

        class RegisterMixinMeta(type):
            def __new__(cls, name, bases, dct):
                new_class = super().__new__(cls, name, bases, dct)
                if "register_me" in dct and dct["register_me"]:
                    _registry.append(new_class)
                return new_class

        class IPlugin(metaclass=RegisterMixinMeta):
            """接口类 ，定义了插件应实现的方法"""

            def plugin_action(self):
                raise NotImplementedError("Subclasses must implement plugin_action.")

        class PluginA(IPlugin):
            register_me = True

            def plugin_action(self):
                print("Plugin A is active.")

        class PluginB(IPlugin):
            def plugin_action(self):
                print("Plugin B is active but not registered explicitly.")

        # 使用示例
        for plugin_class in _registry:
            plugin_class().plugin_action()
        BBB = PluginB()
        BBB.plugin_action()

        class MyBaseClsMeta(metaclass=ClsMeta):
            # MixinAttr = True
            # MixinItem = True
            # MixinIter = True
            MixinRepr = True
            MixinLog = True

            def __init__(self):
                self.name = "liuxinjun"
                self.age = 12
                self._i = 787
                self.姓名 = "行云流水"

        bb = MyBaseClsMeta()
        print(bb, bb.get_dict(), bb.__dict__)
        bb.log("hello")

    赋值一次的字典()
    # 可迭代对象()
    # itat()
    # metaclass()


"""
方法1:工厂函数
def createClass(cls):
    class CustomizedClass(cls):
        .......
    return CustomizedClass

ClassList = createClass(list)

方法2:type完全动态构造
方法3:type混入继承,动态修改
方法4:class 混入继承

方法5:明示重置class.__bases__  = (指定父类,) class 要隔代继承object,QThread出错

print(QThread.__mro__)
(<class 'PyQt5.QtCore.QThread'>, <class 'PyQt5.QtCore.QObject'>, <class 'sip.wrapper'>, <class 'sip.simplewrapper'>, <class 'object'>)

"""
