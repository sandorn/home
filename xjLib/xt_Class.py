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

from typing import Any

from xt_wraps import LogCls

log = LogCls()


def log_in_main(instr: str) -> None:
    """仅在主模块运行时记录日志

    Args:
        instr: 要记录的日志信息
    """
    if __name__ == '__main__':
        log(instr)


class ItemGetMixin:
    """提供下标访问（[key]）获取属性值的功能

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
        log_in_main(f'ItemGetMixin: {key}')
        # 注意：原代码中有通过getattr获取的注释，现在直接使用__dict__
        return self.__dict__.get(key, None)


class ItemSetMixin:
    """提供下标访问（[key]）设置属性值的功能

    通过__setitem__方法，允许对象使用字典风格的下标访问方式设置属性值。
    直接在实例的__dict__中设置键值对。
    """

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值

        Args:
            key: 要设置的属性名
            value: 要设置的属性值
        """
        log_in_main(f'ItemSetMixin: {key}, {value}')
        self.__dict__[key] = value


class ItemDelMixin:
    """提供下标访问（[key]）删除属性的功能

    通过__delitem__方法，允许对象使用字典风格的下标访问方式删除属性。
    直接从实例的__dict__中删除指定的键值对。
    """

    def __delitem__(self, key: str) -> None:
        """删除指定键的值

        Args:
            key: 要删除的属性名
        """
        log_in_main(f'ItemDelMixin: {key}')
        self.__dict__.pop(key)


class ItemMixin(ItemGetMixin, ItemSetMixin, ItemDelMixin):
    """组合了所有下标访问（[key]）相关的功能

    同时继承了ItemGetMixin、ItemSetMixin和ItemDelMixin，
    提供完整的字典风格下标操作支持（获取、设置、删除）。
    """

    pass


class ItemMixinS:
    """使用内部字典实现下标访问（[key]）的混合类

    与ItemMixin不同，该类使用内部的_data字典来存储所有键值对，
    而不是直接操作实例的__dict__。同时提供了keys()、values()和items()方法，
    更接近Python字典的接口。
    """

    def __init__(self) -> None:
        """初始化内部数据字典"""
        # 初始化一个空字典来存储键值对
        self._data = {}

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值到内部字典

        Args:
            key: 要设置的键
            value: 要设置的值
        """
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        """从内部字典获取指定键的值

        Args:
            key: 要获取的键

        Returns:
            对应的值，如果键不存在则返回None
        """
        return self._data.get(key)

    def __delitem__(self, key: str) -> None:
        """从内部字典删除指定键

        Args:
            key: 要删除的键
        """
        if key in self._data:
            del self._data[key]

    def keys(self) -> list[str]:
        """返回所有键的列表

        Returns:
            包含所有键的列表
        """
        return list(self._data.keys())

    def values(self) -> list[Any]:
        """返回所有值的列表

        Returns:
            包含所有值的列表
        """
        return list(self._data.values())

    def items(self) -> list[tuple[str, Any]]:
        """返回所有键值对的列表

        Returns:
            包含所有键值对的列表，每个元素为(key, value)元组
        """
        return list(self._data.items())


class AttrGetMixin:
    """提供属性访问（cls.key）的功能，当属性不存在时返回None

    重写__getattr__方法，当常规属性访问失败时（即属性不存在），
    不会抛出AttributeError异常，而是返回None。
    """

    def __getattr__(self, key: str) -> Any:
        """当属性不存在时返回None

        Args:
            key: 要获取的属性名

        Returns:
            属性值，如果不存在则返回None
        """
        log_in_main(f'AttrGetMixin: {key}')
        return None


class AttrSetMixin:
    """提供属性设置（cls.key = value）的功能

    重写__setattr__方法，在设置属性值时记录日志，然后调用父类的方法完成实际设置。
    """

    def __setattr__(self, key: str, value: Any) -> None:
        """设置属性值并记录日志

        Args:
            key: 要设置的属性名
            value: 要设置的属性值
        """
        log_in_main(f'AttrSetMixin: {key}, {value}')
        super().__setattr__(key, value)  # 直接调用父类方法完成设置


class AttrDelMixin:
    """提供属性删除（del cls.key）的功能

    重写__delattr__方法，在删除属性时记录日志，然后调用父类的方法完成实际删除。
    """

    def __delattr__(self, key: str) -> None:
        """删除属性并记录日志

        Args:
            key: 要删除的属性名
        """
        log_in_main(f'AttrDelMixin: {key}')
        super().__delattr__(key)  # 直接调用父类方法完成删除


class AttrMixin(AttrGetMixin, AttrSetMixin, AttrDelMixin):
    """组合了所有属性访问（cls.key）相关的功能

    同时继承了AttrGetMixin、AttrSetMixin和AttrDelMixin，
    提供完整的属性操作支持（获取、设置、删除），其中属性不存在时返回None。
    """

    pass


class GetSetDelMixin(ItemMixin, AttrMixin):
    """组合了下标操作和属性访问功能的混合类

    同时继承了ItemMixin和AttrMixin，提供完整的字典风格下标操作（[]）
    和属性访问操作（.）的支持，包括获取、设置和删除。
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
        if not hasattr(self, '__dict__') or len(self.__dict__) == 0:
            # 从实例的dir()中收集非魔术属性和非可调用属性
            self.__dict__ = {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}
        return self.__dict__

    def get_dict_from_class(self) -> dict[str, Any]:
        """从类层面收集所有非魔术方法和非可调用属性到__dict__

        Returns:
            包含类所有属性的字典
        """
        log_in_main('ReDictMixin: get_dict')
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

    def __iter__(self) -> Any:
        """返回一个迭代器，用于迭代实例的所有属性

        Yields:
            包含(键, 值)的元组
        """
        log_in_main('IterMixin:')
        # 迭代实例的__dict__中的所有键值对
        yield from self.__dict__.items()
        # 注意：原代码中有使用get_dict()的注释，但当前实现直接使用__dict__


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
        log_in_main('ReprMixin:')
        # 使用__dict__，如果为空则调用get_dict()
        dic = self.__dict__ or self.get_dict()
        # 构建格式为"ClassName(attr1=value1, attr2=value2, ...)"的字符串
        return f'{self.__class__.__qualname__}({", ".join([f"{k}={v!r}" for k, v in dic.items()])})'


# 基类,支持下标,迭代,打印
class BaseCls(AttrMixin, ItemMixin, IterMixin, ReprMixin): ...


class SetOnceDict:
    """限制下标[key]赋值的字典类

    该类实现了一种特殊的字典，其中键值对只能被设置一次（当键不存在或值为None时）。
    主要特点是通过内部的_dict字典存储数据，且对属性访问（如obj.key）无效，只支持下标访问。
    """

    __slots__ = ('_dict',)  # 限制实例只能有_dict属性，优化内存使用

    def __init__(self):
        """初始化SetOnceDict实例

        创建一个空的内部字典用于存储键值对。
        """
        log_in_main('SetOnceDict.__init__')
        self._dict: dict[Any, Any] = {}

    def __setitem__(self, key: str, value: Any) -> None:
        """设置指定键的值，但仅当键不存在或当前值为None时允许设置

        Args:
            key: 要设置的键
            value: 要设置的值

        注意：如果键已存在且值不为None，则记录日志但不覆盖原有值。
        """
        log_in_main(f'SetOnceDict.__setitem__: {key}, {value}')
        if key in self._dict and self._dict[key] is not None:
            log_in_main(f"Key:'{key}' already exists: {value}")
        else:
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
        log_in_main(f'SetOnceDict.__getitem__: {key}')
        return self._dict[key]

    def __repr__(self) -> str:
        """返回对象的字符串表示

        Returns:
            内部字典的字符串表示
        """
        log_in_main('SetOnceDict.__repr__')
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

    def __new__(cls, name: str, bases: tuple[type, ...], dct: dict[str, Any], **kwds: dict[str, Any]) -> type:
        """创建新的类对象，并根据类属性添加相应的Mixin类

        Args:
            cls: 元类自身
            name: 要创建的类名
            bases: 原始基类元组
            dct: 类的属性字典
            **kwds: 额外的关键字参数

        Returns:
            创建的新类
        """
        # 收集需要添加的Mixin类
        mixin_classes = []
        if dct.get('MixinItem'):
            mixin_classes.append(ItemMixin)
        if dct.get('MixinAttr'):
            mixin_classes.append(AttrMixin)
        if dct.get('MixinIter'):
            mixin_classes.append(IterMixin)
        if dct.get('MixinRepr'):
            mixin_classes.append(ReprMixin)

        # 创建新的基类列表，包含原始基类和所有Mixin类
        # 确保Mixin类只添加一次，避免重复
        new_bases = list(bases)
        for mixin_cls in mixin_classes:
            if mixin_cls not in new_bases:
                new_bases.append(mixin_cls)

        # 创建并返回新的类对象，注意不传递**kwds，因为Python的type.__new__不支持
        # 但会保留这些参数，以便在自定义元类中使用
        return super().__new__(cls, name, tuple(new_bases), dct)


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

    class TestFullFunctionality:
        """用于全面测试xt_class.py中所有类和函数的功能"""

        @staticmethod
        def test_all_mixins():
            """测试所有Mixin类的功能"""

            # 测试ItemMixin - 下标操作
            class TestItem(ItemMixin):
                def __init__(self):
                    self._data = {}
                    self.name = 'ItemTest'

            print('\n=== 测试ItemMixin - 下标操作 ===')
            item = TestItem()
            item['key1'] = 'value1'  # __setitem__
            print(f"item['key1'] = {item['key1']}")  # __getitem__
            del item['key1']  # __delitem__
            try:
                print(item['key1'])
            except KeyError as e:
                print(f'预期的KeyError: {e}')

            # 测试AttrMixin - 属性访问
            class TestAttr(AttrMixin):
                def __init__(self):
                    self.attr1 = 'value1'

            print('\n=== 测试AttrMixin - 属性访问 ===')
            attr = TestAttr()
            attr.attr2 = 'value2'  # __setattr__
            print(f'attr.attr1 = {attr.attr1}')  # 正常属性
            print(f'attr.attr2 = {attr.attr2}')  # 设置的属性
            print(f'attr.non_existent = {attr.non_existent}')  # 不存在的属性返回None
            del attr.attr1  # __delattr__
            print(f'删除后 attr.attr1 = {attr.attr1}')  # 删除后返回None

            # 测试IterMixin - 迭代功能
            class TestIter(IterMixin):
                def __init__(self):
                    self.attr1 = 'value1'
                    self.attr2 = 'value2'
                    self._private = 'private'

            print('\n=== 测试IterMixin - 迭代功能 ===')
            iter_obj = TestIter()
            print('迭代对象的所有属性:')
            for key, value in iter_obj:
                print(f'  {key}: {value}')

            # 测试ReprMixin - 字符串表示
            class TestRepr(ReprMixin):
                def __init__(self):
                    self.name = 'ReprTest'
                    self.version = '1.0'

            print('\n=== 测试ReprMixin - 字符串表示 ===')
            repr_obj = TestRepr()
            print(f'对象的字符串表示: {repr_obj}')

            # 测试ReDictMixin - 重新生成__dict__
            class TestReDict(ReDictMixin):
                static_attr = 'static_value'

                def __init__(self):
                    pass  # 故意不初始化__dict__

            print('\n=== 测试ReDictMixin - 重新生成__dict__ ===')
            redict_obj = TestReDict()
            print(f'通过get_dict获取类属性: {redict_obj.get_dict()}')
            redict_obj.instance_attr = 'instance_value'
            print(f'通过get_dict_from_instance获取实例属性: {redict_obj.get_dict_from_instance()}')

            # 测试SetOnceDict - 只能设置一次的字典
            print('\n=== 测试SetOnceDict - 只能设置一次的字典 ===')
            once_dict = SetOnceDict()
            once_dict['key1'] = 'value1'
            print(f"设置key1后: once_dict['key1'] = {once_dict['key1']}")
            once_dict['key1'] = 'new_value'  # 尝试覆盖，应该被忽略
            print(f"尝试覆盖后: once_dict['key1'] = {once_dict['key1']}")
            once_dict['key2'] = None
            print(f"设置key2为None后: once_dict['key2'] = {once_dict['key2']}")
            once_dict['key2'] = 'value2'  # 覆盖None值是允许的
            print(f"覆盖None值后: once_dict['key2'] = {once_dict['key2']}")

            # 测试MixinClsMeta - 动态Mixin元类
            print('\n=== 测试MixinClsMeta - 动态Mixin元类 ===')

            class TestMixinCls(metaclass=MixinClsMeta):
                MixinAttr = True
                MixinItem = True
                MixinIter = True
                MixinRepr = True

                def __init__(self):
                    self.name = 'MetaTest'
                    self.version = '1.0'

            meta_obj = TestMixinCls()
            meta_obj['key1'] = 'value1'  # 测试ItemMixin功能
            print(f"meta_obj['key1'] = {meta_obj['key1']}")
            print(f'meta_obj.non_existent = {meta_obj.non_existent}')  # 测试AttrMixin功能
            print(f'迭代meta_obj: {list(meta_obj)}')  # 测试IterMixin功能
            print(f'meta_obj的字符串表示: {meta_obj}')  # 测试ReprMixin功能

            # 测试MixinClsMeta - 动态方法元类
            print('\n=== 测试MixinClsMeta - 动态方法元类 ===')

            class TestMethodCls(metaclass=MixinClsMeta):
                MixinItem = True  # 启用下标操作支持
                MixinAttr = True  # 启用属性访问支持

                def __init__(self):
                    self.name = 'MethodTest'

            method_obj = TestMethodCls()
            method_obj['key1'] = 'value1'  # 测试ItemMixin功能
            print(f"method_obj['key1'] = {method_obj['key1']}")
            print(f'method_obj.non_existent = {method_obj.non_existent}')  # 测试AttrMixin功能

            print('\n=== 所有测试完成 ===')

        @staticmethod
        def run_all_tests():
            """运行所有测试"""
            TestFullFunctionality.test_all_mixins()

    TestFullFunctionality.run_all_tests()
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
