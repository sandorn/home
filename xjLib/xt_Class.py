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

from typing import Any

# 生成器的类型提示： Generator[yield_type, send_type, return_type]
# from typing import List, Dict, Tuple, Set,Union,Any,Sequence
# from typing import Type,TypeVar,Generic,Callable,Iterable,Iterator,Mapping,Pattern
# from typing import Generator,ClassVar,Annotated,Optional


class ItemGetMixin:
    """下标调用（索引操作）[key]"""

    def __getitem__(self, key: str) -> Any:
        # return getattr(self, key, None)
        return self.__dict__.get(key, None)


class ItemSetMixin:
    """下标调用（索引操作）[key]"""

    def __setitem__(self, key: str, value: Any) -> None:
        # return setattr(self, key, value)
        self.__dict__[key] = value


class ItemDelMixin:
    """下标调用（索引操作）[key]"""

    def __delitem__(self, key: str) -> None:
        # return delattr(self, key)
        return self.__dict__.pop(key)


class ItemMixin(ItemGetMixin, ItemSetMixin, ItemDelMixin): ...


class AttrGetMixin:
    """原点调用（属性访问）cls.key"""

    def __getattr__(self, key: str) -> Any:
        # return getattr(self, key, None)
        # return super().__getattribute__(key)
        return self.__dict__.get(key, None)


class AttrSetMixin:
    """原点调用（属性访问）cls.key"""

    def __setattr__(self, key: str, value: Any) -> None:
        return super().__setattr__(key, value)


class AttrDelMixin:
    """原点调用（属性访问）cls.key"""

    def __delattr__(self, key: str) -> None:
        return super().__delattr__(key)


class AttrMixin(AttrGetMixin, AttrSetMixin, AttrDelMixin): ...


class ReDictMixin:
    """get_dict重新生成 __dict__ 类字典,主要用于readonly限制"""

    def get_dict(self) -> dict[str, Any]:
        """把对象转换成字典"""
        if not hasattr(self, "__dict__") or len(self.__dict__) == 0:
            self.__dict__ = {
                key: getattr(self, key)
                for key in dir(self)
                if not key.startswith("__") and not callable(getattr(self, key))
            }
        return self.__dict__


class IterMixin:
    """
    # #迭代类,用于继承,不支持next
    from collections import Iterable
    isinstance(a, Iterable)
    """

    def __iter__(self) -> Any:
        yield from self.__dict__.items()
        # return iter(self.get_dict().items())


class ReprMixin:
    """用于打印显示"""

    def __repr__(self) -> str:
        dic = self.__dict__ | self.get_dict()
        return f"{self.__class__.__qualname__}({', '.join([f'{k}={v!r}' for k, v in dic.items()])})"


# 基类,支持下标,迭代,打印
class BaseCls(AttrMixin, ItemMixin, IterMixin, ReprMixin): ...


class SetOnceDict:
    """限制下标[key]赋值,key不存在时可赋值；对属性访问无用"""

    # __slots__ = ("_dict",)

    def __init__(self):
        self._dict: dict[Any, Any] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self._dict.keys():
            raise ValueError(f"Key '{key}' already exists:{value}")
        self._dict[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._dict[key]

    def __repr__(self):
        return repr(self._dict)

    # def __setitem__(self, key: str, value: Any) -> None:
    #     if not hasattr(self, key):
    #         return super().__setitem__(key, value)
    #     raise ValueError(f"key:`{key}` is already set,cannot reset value to `{value}`!")


class MixinClsMeta(type):
    """
    智能元类，根据类属性动态选择Mixin
    class BaseClsMeta(metaclass=MixinClsMeta):
        MixinAttr = True
        MixinItem = True
        MixinIter = True
        MixinRepr = True
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
        **kwds: dict[str, Any],
    ) -> type:
        bases_mixins = ()  # 用于存放要应用的Mixin类
        bases_mixins += bases if bases else ()
        bases_mixins += (ItemMixin,) if "MixinItem" in dct and dct["MixinItem"] else ()
        bases_mixins += (AttrMixin,) if "MixinAttr" in dct and dct["MixinAttr"] else ()
        bases_mixins += (IterMixin,) if "MixinIter" in dct and dct["MixinIter"] else ()
        bases_mixins += (
            (
                ReDictMixin,
                ReprMixin,
            )
            if "MixinRepr" in dct and dct["MixinRepr"]
            else ()
        )
        return type(name, bases_mixins, dct, **kwds)


class BaseClsMeta(type):
    """
    智能元类，根据类属性动态选择Mixin,字典__dict__有冲突，
    原因是mixin.__dict__包含了特殊的方法（如__get__, __set__, __delete__等），
    这些方法不能直接应用到类实例上。
    class BaseClsMeta(metaclass=BaseClsMeta):
        MixinAttr = True
        MixinItem = True
        MixinIter = True
        MixinRepr = True

    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        dct: dict[str, Any],
        **kwds: dict[str, Any],
    ) -> type:
        bases_mixins = []
        if "MixinItem" in dct and dct["MixinItem"]:
            bases_mixins.append(ItemMixin)
        if "MixinAttr" in dct and dct["MixinAttr"]:
            bases_mixins.append(AttrMixin)
        if "MixinIter" in dct and dct["MixinIter"]:
            bases_mixins.append(IterMixin)

        for mixin in bases_mixins:
            dct.update(mixin.__dict__)  # 动态添加属性和方法
        return super().__new__(cls, name, bases, dct)


def typeassert(**kwargs: dict[str, Any]) -> object:
    """Descriptor for a type-checked attribute
    #限制属性赋值的类型,因使用__dict__,与slots冲突"""

    class Typed:
        def __init__(self, name: str, expected_type: Any) -> None:
            self.name = name
            self.expected_type = expected_type

        def __get__(self, instance: object, cls: type) -> Any:
            return self if instance is None else instance.__dict__[self.name]

        def __set__(self, instance: object, value: Any):
            assert isinstance(value, self.expected_type)
            # raise TypeError('Expected ' + str(self.expected_type))
            instance.__dict__[self.name] = value

        def __delete__(self, instance: object) -> None:
            del instance.__dict__[self.name]

    def decorate(cls: object) -> object:
        for name, expected_type in kwargs.items():
            setattr(cls, name, Typed(name, expected_type))
        return cls

    return decorate


def typed_property(name: str, expected_type: Any) -> property:
    """class类property属性生成器,限制赋值类型"""
    storage_name = f"_{name}"

    @property
    def prop(self: object) -> Any:
        return getattr(self, storage_name)

    @prop.setter
    def prop(self: object, value: Any) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be a {expected_type}")
        setattr(self, storage_name, value)

    return prop


def readonly(name: str) -> property:
    """
    class类property只读属性生成器,隐藏真实属性名:name,
    #不在__dict__内,需要使用class_to_dict函数生成类__dict__
    #可配合@dataclass(init=False)
    # from dataclasses import asdict, dataclass
    @dataclass(frozen=True) #frozen=True,不可修改
    """
    storage_name = name

    @property
    def prop(self: object):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self: object, value: Any):
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
            my_dict.me = 9009
            my_dict["me"] = "49"

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
                self.pi = 787
                self.姓名 = "行云流水"

        a = Anima()
        a["name"] = "张三李四"
        print(a["names99"])
        del a["姓名"]
        b = Anima()
        b.pi = 567
        print(a.name555s)
        del b.name
        print(a.__dict__, id(a))
        print(b.__dict__, id(b))

    def 动态元类():
        class MyBaseClsMeta(metaclass=BaseClsMeta):
            MixinAttr = True
            MixinItem = True
            MixinIter = True
            MixinRepr = True

            def __init__(self):
                self.name = "liuxinjun"
                self.age = 12
                self._i = 787
                self.姓名 = "行云流水"

            def ddd(self, value):
                print("ddd")

        bb = MyBaseClsMeta()
        print(bb)  # , bb.__dict__)

    # 赋值一次的字典()
    # 可迭代对象()
    # itat()
    动态元类()

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
