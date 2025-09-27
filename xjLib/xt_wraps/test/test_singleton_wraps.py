# !/usr/bin/env python3
"""测试singleton_wraps装饰器功能 - 验证不同单例实现方式的正确性

本测试模块验证单例模式的多种实现方式：
- SingletonMeta: 元类实现的单例
- SingletonMixin: 混入类实现的单例  
- SingletonWraps: 装饰器实现的单例
"""
from __future__ import annotations

from xt_wraps.singleton import SingletonMeta, SingletonMixin, SingletonWraps


# 1. 元类单例测试
class MetaSingleton(metaclass=SingletonMeta):
    """1.1 元类实现的单例类"""

    def __init__(self, value: str) -> None:
        self.value = value


# 2. 混入类单例测试
class MixinSingleton(SingletonMixin):
    """2.1 混入类实现的单例类"""

    def __init__(self, value: str) -> None:
        self.value = value


# 3. 装饰器单例测试
@SingletonWraps
class DecoratorSingleton:
    """3.1 装饰器实现的单例类"""

    def __init__(self, value: str) -> None:
        self.value = value


# 4. 基本功能测试
def test_basic_singleton() -> None:
    """1. 基本单例功能测试"""
    # 1.1 元类单例基本功能
    meta1 = MetaSingleton('第一个')
    meta2 = MetaSingleton('第二个')
    assert meta1 is meta2, '元类单例实例不唯一'
    assert meta1.value == '第一个', '元类单例值不正确'

    # 1.2 混入类单例基本功能
    mixin1 = MixinSingleton('第一个')
    mixin2 = MixinSingleton('第二个')
    assert mixin1 is mixin2, '混入类单例实例不唯一'
    assert mixin1.value == '第二个', '混入类单例值不正确'

    # 1.3 装饰器单例基本功能
    decorator1 = DecoratorSingleton('第一个')
    decorator2 = DecoratorSingleton('第二个')
    assert decorator1 is decorator2, '装饰器单例实例不唯一'
    assert decorator1.value == '第一个', '装饰器单例值不正确'


# 5. 实例重置测试
def test_reset_instance() -> None:
    """2. 实例重置功能测试"""
    # 2.1 元类单例重置
    meta_old = MetaSingleton('旧值')
    MetaSingleton.reset_instance()
    meta_new = MetaSingleton('新值')
    assert meta_old is not meta_new, '元类单例重置失败'
    assert meta_new.value == '新值', '元类单例重置后值不正确'

    # 2.2 混入类单例重置
    mixin_old = MixinSingleton('旧值')
    MixinSingleton.reset_instance()
    mixin_new = MixinSingleton('新值')
    assert mixin_old is not mixin_new, '混入类单例重置失败'
    assert mixin_new.value == '新值', '混入类单例重置后值不正确'

    # 2.3 装饰器单例重置
    decorator_old = DecoratorSingleton('旧值')
    DecoratorSingleton.reset_instance()
    decorator_new = DecoratorSingleton('新值')
    assert decorator_old is not decorator_new, '装饰器单例重置失败'
    assert decorator_new.value == '新值', '装饰器单例重置后值不正确'


# 6. 重新初始化测试
def test_reinit() -> None:
    """3. 重新初始化功能测试"""
    decorator_old = DecoratorSingleton('旧值')
    decorator_new = DecoratorSingleton('新值', reinit=True)
    assert decorator_old is not decorator_new, '重新初始化失败'
    assert decorator_new.value == '新值', '重新初始化后值不正确'


# 7. 获取实例测试
def test_get_instance() -> None:
    """4. 获取实例功能测试"""
    # 4.1 获取现有实例
    existing_instance = DecoratorSingleton.get_instance()
    assert existing_instance is not None, '获取现有实例失败'
    assert existing_instance.value == '新值', '获取的实例值不正确'

    # 4.2 清空实例后再测试
    DecoratorSingleton.reset_instance()
    no_instance = DecoratorSingleton.get_instance()
    assert no_instance is None, '重置后实例未清空'


# 8. 多线程安全测试模拟
def test_thread_safety() -> None:
    """5. 多线程安全测试（模拟）"""
    # 重置实例
    DecoratorSingleton.reset_instance()

    # 模拟多线程创建实例
    instances = []
    for i in range(3):
        instances.append(DecoratorSingleton(f'线程{i}'))

    # 验证所有实例是否相同
    for i in range(1, len(instances)):
        assert instances[0] is instances[i], f'线程{i}创建的实例不一致'


# 9. 实例存在性检查测试
def test_has_instance() -> None:
    """6. 实例存在性检查测试"""
    # 6.1 测试实例存在
    DecoratorSingleton('测试值')
    assert DecoratorSingleton.has_instance(), '实例存在性检查失败'

    # 6.2 测试实例不存在
    DecoratorSingleton.reset_instance()
    assert not DecoratorSingleton.has_instance(), '实例不存在检查失败'


# 10. 主测试函数
def run_all_tests() -> None:
    """主测试函数 - 按序号组织所有测试用例"""
    
    test_basic_singleton()
    
    test_reset_instance()
    
    test_reinit()
    
    test_get_instance()
    
    test_thread_safety()
    
    test_has_instance()
    

# 运行主测试函数
if __name__ == '__main__':
    run_all_tests()