# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-26 16:35:54
FilePath     : /CODE/py学习/test/停车场.py
Github       : https://github.com/sandorn/home
==============================================================
"""


class Example:
    __slots__ = ['attribute']  # 只允许 'attribute' 这一个属性

    def __init__(self) -> None:
        pass

    def age(self):
        return 18


# 使用 __slots__ 的好处是它能限制实例属性，减少内存消耗
# 下面的例子演示了如何使用 __slots__

example = Example()
example.attribute = 'some value'

# 尝试添加不在 __slots__ 列表中的属性会抛出 AttributeError
# example.another_attribute = 'another value'  # 这会抛出错误

print(example.age(), example.attribute)  # 输出: some value
