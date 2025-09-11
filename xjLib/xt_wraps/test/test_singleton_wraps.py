# !/usr/bin/env python
"""
测试singleton_wraps装饰器功能 - 验证不同单例实现方式的正确性

开发工具: VS Code
作者: Trae AI
FilePath: d:/CODE/xjLib/xt_wraps/test/test_singleton_wraps.py
LastEditTime: 2025-09-06 09:35:00
"""
from __future__ import annotations

from xt_wraps.singleton import SingletonMeta, SingletonMixin, SingletonWraps


# 1. 元类单例测试
class MetaSingleton(metaclass=SingletonMeta):
    """1.1 元类实现的单例类"""

    def __init__(self, value):
        self.value = value
        print(f'元类单例创建，值: {value}')


# 2. 混入类单例测试
class MixinSingleton(SingletonMixin):
    """2.1 混入类实现的单例类"""

    def __init__(self, value):
        self.value = value
        print(f'混入类单例创建，值: {value}')


# 3. 装饰器单例测试
@SingletonWraps
class DecoratorSingleton:
    """3.1 装饰器实现的单例类"""

    def __init__(self, value):
        self.value = value
        print(f'装饰器单例创建，值: {value}')


# 4. 基本功能测试
async def test_basic_singleton():
    """1. 基本单例功能测试"""
    print('\n1. 基本单例功能测试:')

    # 1.1 元类单例基本功能
    print('\n1.1 元类单例基本功能:')
    m1 = MetaSingleton('第一个')
    m2 = MetaSingleton('第二个')
    print(f'是同一个实例吗? {m1 is m2}, 当前值: {m1.value}')
    print(f'存在实例吗? {MetaSingleton.has_instance()}')

    # 1.2 混入类单例基本功能
    print('\n1.2 混入类单例基本功能:')
    mx1 = MixinSingleton('第一个')
    mx2 = MixinSingleton('第二个')
    print(f'是同一个实例吗? {mx1 is mx2}, 当前值: {mx1.value}')
    print(f'存在实例吗? {MixinSingleton.has_instance()}')

    # 1.3 装饰器单例基本功能
    print('\n1.3 装饰器单例基本功能:')
    d1 = DecoratorSingleton('第一个')
    d2 = DecoratorSingleton('第二个')
    print(f'是同一个实例吗? {d1 is d2}, 当前值: {d1.value}')
    print(f'存在实例吗? {DecoratorSingleton.has_instance()}')


# 5. 实例重置测试
async def test_reset_instance():
    """2. 实例重置功能测试"""
    print('\n2. 实例重置功能测试:')

    # 2.1 元类单例重置
    print('\n2.1 元类单例重置:')
    MetaSingleton.reset_instance()
    print(f'重置实例后，存在实例吗? {MetaSingleton.has_instance()}')
    m3 = MetaSingleton('第三个')
    print(f'重置后 - 是同一个实例吗? {MetaSingleton.has_instance()}, 当前值: {m3.value}')

    # 2.2 混入类单例重置
    print('\n2.2 混入类单例重置:')
    MixinSingleton.reset_instance()
    print(f'重置实例后，存在实例吗? {MixinSingleton.has_instance()}')
    mx3 = MixinSingleton('第三个')
    print(f'重置后 - 是同一个实例吗? {MixinSingleton.has_instance()}, 当前值: {mx3.value}')

    # 2.3 装饰器单例重置
    print('\n2.3 装饰器单例重置:')
    DecoratorSingleton.reset_instance()
    print(f'重置实例后，存在实例吗? {DecoratorSingleton.has_instance()}')
    d3 = DecoratorSingleton('第三个')
    print(f'重置后 - 是同一个实例吗? {DecoratorSingleton.has_instance()}, 当前值: {d3.value}')


# 6. 重新初始化测试
async def test_reinit():
    """3. 重新初始化功能测试"""
    print('\n3. 重新初始化功能测试:')
    d4 = DecoratorSingleton('第四个', reinit=True)
    print(f'重新初始化后 - 是同一个实例吗? {d4 is DecoratorSingleton.get_instance()}, 当前值: {d4.value}')


# 7. 获取实例测试
async def test_get_instance():
    """4. 获取实例功能测试"""
    print('\n4. 获取实例功能测试:')
    existing_instance = DecoratorSingleton.get_instance()
    if existing_instance:
        print(f'获取到现有实例，值: {existing_instance.value}')
    else:
        print('没有现有实例')

    # 清空实例后再测试
    DecoratorSingleton.reset_instance()
    no_instance = DecoratorSingleton.get_instance()
    if no_instance:
        print(f'清空实例后,获取到现有实例，值: {no_instance.value}')
    else:
        print('清空实例后,没有现有实例')


# 8. 多线程安全测试模拟
async def test_thread_safety():
    """5. 多线程安全测试（模拟）"""
    print('\n5. 多线程安全测试（模拟）:')
    # 重置实例
    DecoratorSingleton.reset_instance()

    # 模拟多线程创建实例
    instances = []
    for i in range(3):
        instances.append(DecoratorSingleton(f'线程{i}'))

    # 验证所有实例是否相同
    is_same = True
    for i in range(1, len(instances)):
        if instances[0] is not instances[i]:
            is_same = False
            break

    print(f'模拟多线程创建，所有实例是否相同? {is_same}')
    print(f'最终实例值: {instances[0].value}')


# 9. 主测试函数
async def run_all_tests():
    """主测试函数 - 按序号组织所有测试用例"""
    print('====== 开始测试 singleton_wraps 装饰器 ======')

    await test_basic_singleton()
    await test_reset_instance()
    await test_reinit()
    await test_get_instance()
    await test_thread_safety()

    print('\n====== 测试完成 ======')


# 运行主测试函数
if __name__ == '__main__':
    import asyncio

    asyncio.run(run_all_tests())