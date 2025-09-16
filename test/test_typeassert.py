from xjlib.xt_class import typeassert

# 测试基本类型检查
@typeassert(name=str, age=int)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 测试联合类型
@typeassert(name=str, score=(int, float))
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

# 测试允许None值
@typeassert(name=str, address={'type': str, 'allow_none': True})
class Contact:
    def __init__(self, name, address=None):
        self.name = name
        self.address = address

# 运行测试
if __name__ == '__main__':
    # 正常情况
    try:
        p = Person("Alice", 30)
        print(f"✅ 基本类型检查通过: {p.name}, {p.age}")
    except TypeError as e:
        print(f"❌ 基本类型检查失败: {e}")
    
    # 类型错误情况
    try:
        p = Person(123, "thirty")
        print("❌ 类型错误未被捕获")
    except TypeError as e:
        print(f"✅ 类型错误被正确捕获: {e}")
    
    # 联合类型正常情况
    try:
        s1 = Student("Bob", 85)
        s2 = Student("Charlie", 89.5)
        print(f"✅ 联合类型检查通过: {s1.name}={s1.score}, {s2.name}={s2.score}")
    except TypeError as e:
        print(f"❌ 联合类型检查失败: {e}")
    
    # 允许None值正常情况
    try:
        c1 = Contact("Dave", "123 Main St")
        c2 = Contact("Eve")
        print(f"✅ None值处理通过: {c1.name}={c1.address}, {c2.name}={c2.address}")
    except TypeError as e:
        print(f"❌ None值处理失败: {e}")
    
    # 不允许None值的情况
    try:
        p = Person(None, 30)
        print("❌ None值未被正确阻止")
    except TypeError as e:
        print(f"✅ None值被正确阻止: {e}")

    print("\n所有测试完成!")