# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-07-26 10:20:03
LastEditTime : 2024-07-26 10:20:05
FilePath     : /CODE/xjLib/xt_enum.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from enum import Enum
from typing import Optional


class BaseEnum(Enum):
    """枚举基类"""

    def __new__(cls, value, desc=None):
        """
        构造枚举成员实例
        Args:
            value: 枚举成员的值
            desc: 枚举成员的描述信息，默认None
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

    @classmethod
    def get_members(
        cls, exclude_enums: Optional[list] = None, only_value: bool = False
    ) -> list:
        """
        获取枚举的所有成员
        Args:
            exclude_enums: 排除的枚举类列表
            only_value: 是否只需要成员的值，默认False

        Returns: 枚举成员列表 or 枚举成员值列表

        """
        members = list(cls)
        if exclude_enums:
            # 排除指定枚举
            members = [member for member in members if member not in exclude_enums]

        if only_value:
            # 只需要成员的值
            members = [member.value for member in members]

        return members

    @classmethod
    def get_values(cls, exclude_enums: Optional[list] = None):
        return cls.get_members(exclude_enums=exclude_enums, only_value=True)

    @classmethod
    def get_names(cls):
        return list(cls._member_names_)


class StrEnum(str, BaseEnum):
    """字符串枚举"""

    ...


class IntEnum(int, BaseEnum):
    """整型枚举"""

    ...


class BaseErrCodeEnum(StrEnum):
    """
    错误码前缀
     - 000-通用基础错误码前缀
     - 100-待定
     - 200-通用业务错误码前缀
        - 201-用户模块
        - 202-订单模块
     - 300-待定
     - 400-通用请求错误
     - 500-通用系统错误码前缀
    """

    OK = ("000-0000", "SUCCESS")
    FAILED = ("000-0001", "FAILED")

    @property
    def code(self):
        return self.value

    @property
    def msg(self):
        return self.desc


if __name__ == "__main__":
    print(BaseErrCodeEnum.get_members())
    print(BaseErrCodeEnum.get_values())
    print(BaseErrCodeEnum.get_names())
    print(BaseErrCodeEnum.OK)
    print(BaseErrCodeEnum.OK._value_)
    print(BaseErrCodeEnum.OK.code)
    print(BaseErrCodeEnum.OK.msg)
    print(BaseErrCodeEnum.OK.value)
    print(BaseErrCodeEnum.OK.desc)
    print(BaseErrCodeEnum.OK.name)
