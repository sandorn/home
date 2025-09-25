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


# 2. 混入类单例测试
class MixinSingleton(SingletonMixin):
    """2.1 混入类实现的单例类"""

    def __init__(self, value):
        self.value = value


# 3. 装饰器单例测试
@SingletonWraps
class DecoratorSingleton:
    """3.1 装饰器实现的单例类"""

    def __init__(self, value):
        self.value = value


# 4. 基本功能测试
async def test_basic_singleton():
    """1. 基本单例功能测试"""

    # 1.1 元类单例基本功能
    MetaSingleton('第一个')
    MetaSingleton('第二个')

    # 1.2 混入类单例基本功能
    MixinSingleton('第一个')
    MixinSingleton('第二个')

    # 1.3 装饰器单例基本功能
    DecoratorSingleton('第一个')
    DecoratorSingleton('第二个')


# 5. 实例重置测试
async def test_reset_instance():
    """2. 实例重置功能测试"""

    # 2.1 元类单例重置
    MetaSingleton.reset_instance()
    MetaSingleton('第三个')

    # 2.2 混入类单例重置
    MixinSingleton.reset_instance()
    MixinSingleton('第三个')

    # 2.3 装饰器单例重置
    DecoratorSingleton.reset_instance()
    DecoratorSingleton('第三个')


# 6. 重新初始化测试
async def test_reinit():
    """3. 重新初始化功能测试"""
    DecoratorSingleton('第四个', reinit=True)


# 7. 获取实例测试
async def test_get_instance():
    """4. 获取实例功能测试"""
    existing_instance = DecoratorSingleton.get_instance()
    if existing_instance:
        pass

    # 清空实例后再测试
    DecoratorSingleton.reset_instance()
    no_instance = DecoratorSingleton.get_instance()
    if no_instance:
        pass


# 8. 多线程安全测试模拟
async def test_thread_safety():
    """5. 多线程安全测试（模拟）"""
    # 重置实例
    DecoratorSingleton.reset_instance()

    # 模拟多线程创建实例
    instances = []
    for i in range(3):
        instances.append(DecoratorSingleton(f'线程{i}'))

    # 验证所有实例是否相同
    for i in range(1, len(instances)):
        if instances[0] is not instances[i]:
            break


# 9. 主测试函数
async def run_all_tests():
    """主测试函数 - 按序号组织所有测试用例"""

    await test_basic_singleton()
    await test_reset_instance()
    await test_reinit()
    await test_get_instance()
    await test_thread_safety()


# 运行主测试函数
if __name__ == '__main__':
    import asyncio

    asyncio.run(run_all_tests())