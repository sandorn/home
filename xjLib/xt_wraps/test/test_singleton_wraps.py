from xt_wraps.singleton import SingletonMeta, SingletonMixin, SingletonWraps


def test_singleton_implementations():
    """测试三种单例实现方式"""

    # 测试元类实现
    class MetaSingleton(metaclass=SingletonMeta):
    # class MetaSingleton0():
        def __init__(self, value):
            self.value = value
            print(f"元类单例创建，值: {value}")
    # MetaSingleton = singleton(MetaSingleton0)
    print("=== 1.测试元类单例 ===")
    m1 = MetaSingleton("第一个")
    m2 = MetaSingleton("第二个")
    print(f"是同一个实例吗? {m1 is m2}, 当前值: {m1.value}")
    print(f"存在实例吗? {MetaSingleton.has_instance()}")

    MetaSingleton.reset_instance()
    print("重置实例后，存在实例吗?", MetaSingleton.has_instance())

    m3 = MetaSingleton("第三个")
    print(f"重置后 - 是同一个实例吗? {m1 is m3}, 当前值: {m3.value}")

    # 测试混入类实现
    class MixinSingleton(SingletonMixin):
        def __init__(self, value):
            self.value = value
            print(f"混入类单例创建，值: {value}")

    print("\n=== 2.测试混入类单例 ===")
    mx1 = MixinSingleton("第一个")
    mx2 = MixinSingleton("第二个")
    print(f"是同一个实例吗? {mx1 is mx2}, 当前值: {mx1.value}")
    print(f"存在实例吗? {MixinSingleton.has_instance()}")

    MixinSingleton.reset_instance()
    print("重置实例后，存在实例吗?", MixinSingleton.has_instance())

    mx3 = MixinSingleton("第三个")
    print(f"重置后 - 是同一个实例吗? {mx1 is mx3}, 当前值: {mx3.value}")

    # 测试装饰器实现
    @SingletonWraps
    class DecoratorSingleton:
        def __init__(self, value):
            self.value = value
            print(f"装饰器单例创建，值: {value}")

    print("\n=== 3.测试装饰器单例 ===")
    d1 = DecoratorSingleton("第一个")
    d2 = DecoratorSingleton("第二个")
    print(f"是同一个实例吗? {d1 is d2}, 当前值: {d1.value}")
    print(f"存在实例吗? {DecoratorSingleton.has_instance()}")

    DecoratorSingleton.reset_instance()
    print("重置实例后，存在实例吗?", DecoratorSingleton.has_instance())

    d3 = DecoratorSingleton("第三个")
    print(f"重置后 - 是同一个实例吗? {d1 is d3}, 当前值: {d3.value}")

    # 测试重新初始化功能
    print("\n=== 4.测试重新初始化功能 ===")
    d4 = DecoratorSingleton("第四个", reinit=True)
    print(f"重新初始化后 - 是同一个实例吗? {d3 is d4}, 当前值: {d4.value}")

    # 测试获取实例功能（不创建新实例）
    print("\n=== 5.测试获取实例功能 ===")
    existing_instance = DecoratorSingleton.get_instance()
    if existing_instance:
        print(f"获取到现有实例，值: {existing_instance.value}")
    else:
        print("没有现有实例")

    # 清空实例后再测试
    DecoratorSingleton.reset_instance()
    no_instance = DecoratorSingleton.get_instance()
    if no_instance:
        print(f"清空实例后,获取到现有实例，值: {no_instance.value}")
    else:
        print("清空实例后,没有现有实例")


test_singleton_implementations()