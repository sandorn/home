from xjlib.xt_class import typed_property

# 测试基本类型检查和property使用
class Person:
    # 使用typed_property定义属性
    name = typed_property('name', str)
    age = typed_property('age', int)
    score = typed_property('score', (int, float), allow_none=True)  # 支持联合类型和None值

    def __init__(self, name=None, age=None, score=None):
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if score is not None:
            self.score = score

# 测试与__slots__兼容
class PersonWithSlots:
    __slots__ = ('_name', '_age', '_score')  # 注意这里使用带下划线的名称
    name = typed_property('name', str)
    age = typed_property('age', int)
    score = typed_property('score', (int, float), allow_none=True)

    def __init__(self, name=None, age=None, score=None):
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if score is not None:
            self.score = score

# 运行测试
if __name__ == '__main__':
    print("===== 测试基本类型检查 =====")
    try:
        p = Person("Alice", 30, 89.5)
        print(f"✅ 基本类型检查通过: {p.name}, {p.age}, {p.score}")
    except TypeError as e:
        print(f"❌ 基本类型检查失败: {e}")
    
    # 测试默认值（未设置的属性返回None）
    p2 = Person()
    print(f"✅ 默认值测试: name={p2.name}, age={p2.age}, score={p2.score}")
    
    # 类型错误情况
    try:
        p.name = 123
        print("❌ 类型错误未被捕获")
    except TypeError as e:
        print(f"✅ 类型错误被正确捕获: {e}")
    
    # 联合类型测试
    try:
        p.score = 90
        print(f"✅ 整数类型接受: score={p.score}")
        p.score = 95.5
        print(f"✅ 浮点数类型接受: score={p.score}")
    except TypeError as e:
        print(f"❌ 联合类型测试失败: {e}")
    
    # None值测试
    try:
        p.score = None
        print(f"✅ None值被接受: score={p.score}")
        p.name = None  # 应该失败，因为name不允许None
        print("❌ None值未被正确阻止")
    except TypeError as e:
        print(f"✅ None值被正确阻止: {e}")
    
    # 删除属性测试
    try:
        p.age = 31
        print(f"✅ 设置属性: age={p.age}")
        del p.age
        print(f"✅ 删除属性后: age={p.age}")  # 应该返回None
    except Exception as e:
        print(f"❌ 删除属性测试失败: {e}")
    
    print("\n===== 测试与__slots__兼容 =====")
    try:
        p_slots = PersonWithSlots("Bob", 25, 85)
        print(f"✅ 与__slots__兼容: {p_slots.name}, {p_slots.age}, {p_slots.score}")
        p_slots.score = 90.5
        print(f"✅ __slots__中更新属性: score={p_slots.score}")
    except Exception as e:
        print(f"❌ 与__slots__兼容测试失败: {e}")

    print("\n所有测试完成!")