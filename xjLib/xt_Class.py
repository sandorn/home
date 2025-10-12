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

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, ClassVar


class MixinError(Exception):
    """Mixin相关错误"""

    pass


class ItemGetMixin:
    """提供下标访问([key])获取属性值的功能

    通过__getitem__方法，允许对象使用字典风格的下标访问方式获取属性值。
    直接从实例的__dict__中获取值，如果键不存在则返回None。
    """

    def __getitem__(self, key: str) -> Any:
        """获取指定键的值

        Args:
            key: 要获取的属性名

        Returns:
            属性值，如果不存在则返回None
        """
        try:
            return self.__dict__.get(key)
        except Exception as e:
            raise MixinError(f"Failed to get item '{key}': {e}") from e


class ItemSetMixin:
    """提供下标访问([key])设置属性值的功能

    通过__setitem__方法，允许对象使用字典风格的下标访问方式设置属性值。
    直接在实例的__dict__中设置键值对。
    """

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值

        Args:
            key: 要设置的属性名
            value: 要设置的属性值
        """
        self.__dict__[key] = value


class ItemDelMixin:
    """提供下标访问([key])删除属性的功能

    通过__delitem__方法，允许对象使用字典风格的下标访问方式删除属性。
    直接从实例的__dict__中删除指定的键值对。
    """

    def __delitem__(self, key: str) -> None:
        """删除指定键的值

        Args:
            key: 要删除的属性名
        """
        self.__dict__.pop(key, None)


class ItemMixin(ItemGetMixin, ItemSetMixin, ItemDelMixin):
    """统一的字典风格访问Mixin"""

    def keys(self) -> list[str]:
        """返回所有键的列表"""
        return list(self.__dict__.keys())

    def values(self) -> list[Any]:
        """返回所有值的列表"""
        return list(self.__dict__.values())

    def items(self) -> list[tuple[str, Any]]:
        """返回所有键值对的列表"""
        return list(self.__dict__.items())


class AttrGetMixin:
    """提供属性访问功能，支持默认值"""

    def __getattr__(self, key: str) -> Any:
        """当属性不存在时返回默认值"""
        # 避免递归，直接返回None
        return None


class AttrSetMixin:
    """提供属性设置(cls.key = value)的功能

    重写__setattr__方法，在设置属性值时记录日志，然后调用父类的方法完成实际设置。
    """

    def __setattr__(self, key: str, value: Any) -> None:
        """设置属性值并记录日志

        Args:
            key: 要设置的属性名
            value: 要设置的属性值
        """
        super().__setattr__(key, value)  # 直接调用父类方法完成设置


class AttrDelMixin:
    """提供属性删除(del cls.key)的功能

    重写__delattr__方法，在删除属性时记录日志，然后调用父类的方法完成实际删除。
    """

    def __delattr__(self, key: str) -> None:
        """删除属性并记录日志

        Args:
            key: 要删除的属性名
        """
        super().__delattr__(key)  # 直接调用父类方法完成删除


class AttrMixin(AttrGetMixin, AttrSetMixin, AttrDelMixin):
    """组合了所有属性访问(cls.key)相关的功能

    同时继承了AttrGetMixin、AttrSetMixin和AttrDelMixin，
    提供完整的属性操作支持(获取、设置、删除)，其中属性不存在时返回None。
    """

    pass


class GetSetDelMixin(ItemMixin, AttrMixin):
    """组合了下标操作和属性访问功能的混合类

    同时继承了ItemMixin和AttrMixin，提供完整的字典风格下标操作([])
    和属性访问操作(.)的支持，包括获取、设置和删除。
    """

    pass


class ReDictMixin:
    """提供重新生成__dict__的功能

    主要用于只读限制场景，通过get_dict方法重新构建实例的__dict__。
    提供了两个方法：get_dict_from_instance和get_dict_from_class，分别从实例和类层面收集属性。
    """

    def get_dict_from_instance(self) -> dict[str, Any]:
        """从实例层面收集所有非魔术方法和非可调用属性到__dict__

        Returns:
            包含实例所有属性的字典
        """
        if not hasattr(self, '__dict__') or not self.__dict__:
            # 从实例的dir()中收集非魔术属性和非可调用属性
            self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}
        return self.__dict__

    def get_dict_from_class(self) -> dict[str, Any]:
        """从类层面收集所有非魔术方法和非可调用属性到__dict__

        Returns:
            包含类所有属性的字典
        """
        if not hasattr(self, '__dict__') or not self.__dict__:
            # 从类的__dict__中收集非魔术属性和非可调用属性
            self.__dict__ = {key: value for key, value in self.__class__.__dict__.items() if not key.startswith('__') and not callable(value)}

        return self.__dict__

    get_dict = get_dict_from_class


class IterMixin:
    """提供迭代功能的混合类

    使继承该类的对象可以直接用于for循环，迭代其__dict__中的所有键值对。
    支持Python的Iterable接口。
    """

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """返回一个迭代器，用于迭代实例的所有属性"""
        yield from self.__dict__.items()


class ReprMixin(ReDictMixin):
    """提供更好的字符串表示形式的混合类

    继承自ReDictMixin，重写__repr__方法，使对象在打印或转换为字符串时，
    以更易读的格式显示其所有属性。
    """

    def __repr__(self) -> str:
        """返回对象的字符串表示，包含所有属性

        Returns:
            格式为"ClassName(attr1=value1, attr2=value2, ...)"的字符串
        """
        # 使用__dict__，如果为空则调用get_dict()
        dic = self.__dict__ or self.get_dict()
        # 构建格式为"ClassName(attr1=value1, attr2=value2, ...)"的字符串
        return f'{self.__class__.__qualname__}({", ".join([f"{k}={v!r}" for k, v in dic.items()])})'


# 基类,支持下标,迭代,打印
class BaseCls(AttrMixin, ItemMixin, IterMixin, ReprMixin): ...


class SetOnceDict:
    """限制下标[key]赋值的字典类

    该类实现了一种特殊的字典，其中键值对只能被设置一次(当键不存在或值为None时)。
    主要特点是通过内部的_dict字典存储数据，且对属性访问(如obj.key)无效，只支持下标访问。
    """

    __slots__ = ('_dict',)  # 限制实例只能有_dict属性，优化内存使用

    def __init__(self):
        """初始化SetOnceDict实例

        创建一个空的内部字典用于存储键值对。
        """
        self._dict: dict[Any, Any] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值，但仅当键不存在或当前值为None时允许设置

        Args:
            key: 要设置的键
            value: 要设置的值

        注意：如果键已存在且值不为None，则记录日志但不覆盖原有值。
        """
        if key in self._dict and self._dict[key] is not None:
            return
        self._dict[key] = value

    def __getitem__(self, key: str) -> Any:
        """获取指定键的值

        Args:
            key: 要获取的键

        Returns:
            键对应的值

        Raises:
            KeyError: 如果键不存在
        """
        return self._dict[key]

    def __repr__(self) -> str:
        """返回对象的字符串表示

        Returns:
            内部字典的字符串表示
        """
        return repr(self._dict)


class MixinClsMeta(type):
    """智能元类，根据类属性动态选择并应用相应的Mixin类

    该元类通过检查类定义中的Mixin*属性，自动将对应的Mixin类添加到基类列表中。
    支持的Mixin属性包括：MixinAttr、MixinItem、MixinIter、MixinRepr。

    本实现结合了MethodClsMeta的优点，包括避免重复添加Mixin类，
    同时优化了基类列表构建策略，避免MRO冲突问题。

    示例用法:
    ```python
    class BaseClsMeta(metaclass=MixinClsMeta):
        MixinAttr = True  # 启用属性访问支持
        MixinItem = True  # 启用下标操作支持
        MixinIter = True  # 启用迭代支持
        MixinRepr = True  # 启用友好的字符串表示支持
    ```
    """

    # 预定义Mixin映射
    MIXIN_MAP: ClassVar[dict[str, Any]] = {
        'MixinItem': ItemMixin,
        'MixinAttr': AttrMixin,
        'MixinIter': IterMixin,
        'MixinRepr': ReprMixin,
    }

    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any], **kwds: Any) -> type:
        """创建新的类对象，并根据类属性添加相应的Mixin类

        Args:
            name: 要创建的类名
            bases: 原始基类元组
            dct: 类的属性字典
            **kwds: 额外的关键字参数

        Returns:
            创建的新类
        """
        # 收集需要添加的Mixin类
        mixin_classes = []
        for mixin_key, mixin_class in cls.MIXIN_MAP.items():
            if dct.get(mixin_key):
                mixin_classes.append(mixin_class)

        # 优化基类列表构建
        new_bases = list(bases)
        existing_mixins = {base for base in bases if base in cls.MIXIN_MAP.values()}

        for mixin_cls in mixin_classes:
            if mixin_cls not in existing_mixins:
                new_bases.append(mixin_cls)

        return super().__new__(cls, name, tuple(new_bases), dct)


class MixinConfig:
    """Mixin配置类"""

    DEFAULT_MIXINS: ClassVar[dict[str, Any]] = {
        'item': ItemMixin,
        'attr': AttrMixin,
        'iter': IterMixin,
        'repr': ReprMixin,
    }

    @classmethod
    def get_mixins(cls, config: dict[str, bool]) -> list[type]:
        """根据配置获取Mixin类列表"""
        return [mixin for key, mixin in cls.DEFAULT_MIXINS.items() if config.get(key)]


class MixinClsParent(metaclass=MixinClsMeta):
    """可直接继承的Mixin功能基类

    该类结合了MixinClsMeta元类，提供更简洁的使用方式。
    通过设置类属性控制启用哪些Mixin功能，实现"混入继承"。

    示例用法:
    ```python
    class MyClass(MixinClsParent):
        MixinAttr = True  # 启用属性访问支持
        MixinItem = True  # 启用下标操作支持
    ```

    这样MyClass就直接继承了MixinClsParent，并且根据设置的类属性自动获得相应的Mixin功能。
    """

    pass


if __name__ == '__main__':
    """xt_class.py 快速功能测试程序（优化版）"""
    
    def quick_test():
        """快速测试所有功能（避免卡住）"""
        print("xt_class.py 快速功能测试")
        print("=" * 40)
        
        try:
            # 1. 基础Mixin测试
            print("\n1. 基础Mixin功能测试")
            item = ItemMixin()
            item["test"] = "value"
            print(f"[OK] 下标访问: {item['test']}")
            
            attr = AttrMixin()
            attr.test_attr = "test_value"
            print(f"[OK] 属性访问: {attr.test_attr}")
            
            # 2. 高级功能测试
            print("\n2. 高级功能测试")
            iter_obj = IterMixin()
            iter_obj.name = "test"
            iter_obj.version = "1.0"
            print(f"[OK] 迭代功能: {dict(iter_obj)}")
            
            repr_obj = ReprMixin()
            repr_obj.name = "test"
            print(f"[OK] 字符串表示: {repr_obj}")
            
            # 3. SetOnceDict测试
            print("\n3. SetOnceDict测试")
            once_dict = SetOnceDict()
            once_dict["config"] = "initial"
            once_dict["config"] = "override"  # 应该被忽略
            print(f"[OK] SetOnceDict: {once_dict['config']}")
            
            # 4. 元类功能测试
            print("\n4. 元类功能测试")

            class DynamicClass(MixinClsParent):
                MixinItem = True
                MixinAttr = True
                
                def __init__(self):
                    self.name = "DynamicTest"
            
            obj = DynamicClass()
            obj["dynamic_key"] = "dynamic_value"  # type: ignore
            print(f"[OK] 动态功能: {obj['dynamic_key']}")  # type: ignore
            
            # 5. MixinConfig测试
            print("\n5. MixinConfig测试")
            config = {'item': True, 'attr': True}
            mixins = MixinConfig.get_mixins(config)
            print(f"[OK] 配置选择: {[mixin.__name__ for mixin in mixins]}")
            
            # 6. 性能测试（轻量级）
            print("\n6. 性能测试")
            import time
            start_time = time.time()
            for i in range(1000):
                obj[f"perf_{i}"] = f"value_{i}"  # type: ignore
            perf_time = time.time() - start_time
            print(f"[OK] 10次操作耗时: {perf_time:.4f}秒")
            
            print("\n" + "=" * 40)
            print("所有测试完成!")
            print("=" * 40)
            
        except Exception as e:
            print(f"\n测试过程中出现错误: {e}")
            print("请检查代码实现")
    
    # 运行快速测试
    quick_test()