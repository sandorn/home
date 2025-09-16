# !/usr/bin/env python
"""
==============================================================
Description  : 增强型枚举工具类库，提供更丰富的枚举功能和类型支持
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-07-26 10:20:03
LastEditTime : 2024-07-26 10:20:05
FilePath     : /CODE/xjLib/xt_enum.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

from enum import Enum
from typing import Any, TypeVar

T = TypeVar('T')


class BaseEnum(Enum):
    """增强型枚举基类，提供更丰富的枚举功能支持

    扩展了Python标准库的Enum类，添加了描述信息存储、成员查询等功能。
    支持通过code和msg属性分别访问枚举的值和描述信息。

    示例用法：
    >>> class StatusEnum(BaseEnum):
    ...     SUCCESS = (200, '操作成功')
    ...     ERROR = (500, '操作失败')
    >>> StatusEnum.SUCCESS.code  # 200
    >>> StatusEnum.SUCCESS.msg  # '操作成功'
    """

    def __new__(cls, value: Any, desc: str | None = None) -> BaseEnum:
        """
        构造枚举成员实例

        Args:
            value: 枚举成员的值
            desc: 枚举成员的描述信息，默认None

        Returns:
            构造的枚举成员实例
        """
        if issubclass(cls, int):
            obj = int.__new__(cls, value)
        elif issubclass(cls, str):
            obj = str.__new__(cls, value)
        else:
            obj = object.__new__(cls)
        obj._value_ = value
        obj.desc = desc
        return obj

    def __str__(self) -> str:
        """返回枚举的字符串表示"""
        return f'{self.name}: {self.value}({self.desc})'

    def __repr__(self) -> str:
        """返回枚举的代码表示"""
        return f'{self.__class__.__name__}.{self.name}({self.value!r}, {self.desc!r})'

    @property
    def code(self) -> Any:
        """获取枚举的值，与value属性相同"""
        return self.value

    @property
    def msg(self) -> str | None:
        """获取枚举的描述信息"""
        return self.desc

    @classmethod
    def get_members(cls, exclude_members: list[BaseEnum] | None = None, only_value: bool = False) -> list[BaseEnum] | list[Any]:
        """
        获取枚举的所有成员

        Args:
            exclude_members: 需要排除的枚举成员列表，默认为None
            only_value: 是否只返回成员的值，默认False

        Returns:
            如果only_value为True，则返回枚举成员值列表；否则返回枚举成员列表
        """
        members = list(cls)
        if exclude_members:
            # 排除指定的枚举成员
            members = [member for member in members if member not in exclude_members]

        if only_value:
            # 只返回成员的值
            members = [member.value for member in members]

        return members

    @classmethod
    def get_values(cls, exclude_members: list[BaseEnum] | None = None) -> list[Any]:
        """
        获取枚举的所有成员值

        Args:
            exclude_members: 需要排除的枚举成员列表，默认为None

        Returns:
            枚举成员值列表
        """
        return cls.get_members(exclude_members=exclude_members, only_value=True)

    @classmethod
    def get_names(cls) -> list[str]:
        """
        获取枚举的所有成员名称

        Returns:
            枚举成员名称列表
        """
        return list(cls._member_names_)

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        检查枚举是否包含指定的值

        Args:
            value: 要检查的值

        Returns:
            如果枚举包含该值则返回True，否则返回False
        """
        return value in cls.get_values()

    @classmethod
    def has_name(cls, name: str) -> bool:
        """
        检查枚举是否包含指定的名称

        Args:
            name: 要检查的名称

        Returns:
            如果枚举包含该名称则返回True，否则返回False
        """
        return name in cls.get_names()

    @classmethod
    def from_value(cls, value: Any) -> BaseEnum | None:
        """
        根据值获取枚举成员

        Args:
            value: 枚举成员的值

        Returns:
            如果找到匹配的枚举成员则返回，否则返回None
        """
        for member in cls:
            if member.value == value:
                return member
        return None


class StrEnum(str, BaseEnum):
    """字符串类型枚举基类，继承自Python内置str和BaseEnum

    结合了字符串的特性和增强型枚举的功能，适合需要字符串操作的枚举场景。
    枚举值会被自动转换为字符串类型。

    示例用法：
    >>> class ColorEnum(StrEnum):
    ...     RED = ('red', '红色')
    ...     GREEN = ('green', '绿色')
    >>> ColorEnum.RED.upper()  # 'RED'，支持字符串方法
    >>> ColorEnum.RED.msg  # '红色'
    """

    pass


class IntEnum(int, BaseEnum):
    """整型枚举基类，继承自Python内置int和BaseEnum

    结合了整数的特性和增强型枚举的功能，适合需要数值计算的枚举场景。
    枚举值会被自动转换为整数类型。

    示例用法：
    >>> class PriorityEnum(IntEnum):
    ...     LOW = (1, '低优先级')
    ...     MEDIUM = (2, '中优先级')
    ...     HIGH = (3, '高优先级')
    >>> PriorityEnum.HIGH + 1  # 4，支持整数运算
    >>> PriorityEnum.HIGH.msg  # '高优先级'
    """

    pass


if __name__ == '__main__':
    """测试枚举功能"""

    class BaseErrCodeEnum(StrEnum):
        """
        错误码枚举示例

        错误码格式: 模块前缀-具体错误编号
        - 000-通用基础错误码前缀
        - 100-待定
        - 200-通用业务错误码前缀
            - 201-用户模块
            - 202-订单模块
        - 300-待定
        - 400-通用请求错误
        - 500-通用系统错误码前缀
        """

        OK = ('000-0000', '操作成功')
        FAILED = ('000-0001', '操作失败')
        PARAM_ERROR = ('400-0001', '参数错误')
        SYSTEM_ERROR = ('500-0001', '系统错误')

    # 测试枚举基本功能
    print('=== 基本功能测试 ===')
    print(f'所有枚举成员: {BaseErrCodeEnum.get_members()}')
    print(f'所有枚举值: {BaseErrCodeEnum.get_values()}')
    print(f'所有枚举名称: {BaseErrCodeEnum.get_names()}')
    print(f'OK枚举: {BaseErrCodeEnum.OK}')
    print(f'OK枚举值: {BaseErrCodeEnum.OK.value}')
    print(f'OK枚举代码: {BaseErrCodeEnum.OK.code}')
    print(f'OK枚举描述: {BaseErrCodeEnum.OK.msg}')
    print(f'OK枚举名称: {BaseErrCodeEnum.OK.name}')

    # 测试StrEnum特性
    print('\n=== StrEnum特性测试 ===')
    print(f'OK枚举大写转换: {BaseErrCodeEnum.OK.upper()}')
    print(f"OK枚举包含'-': {'-' in BaseErrCodeEnum.OK}")

    # 测试扩展功能
    print('\n=== 扩展功能测试 ===')
    print(f"是否包含值'000-0000': {BaseErrCodeEnum.has_value('000-0000')}")
    print(f"是否包含名称'NOT_EXIST': {BaseErrCodeEnum.has_name('NOT_EXIST')}")
    print(f'通过值获取枚举: {BaseErrCodeEnum.from_value("000-0001")}')

    # 测试排除功能
    exclude_list = [BaseErrCodeEnum.OK]
    print(f'\n排除OK后的成员: {BaseErrCodeEnum.get_members(exclude_members=exclude_list)}')
    print(f'排除OK后的值: {BaseErrCodeEnum.get_values(exclude_members=exclude_list)}')
