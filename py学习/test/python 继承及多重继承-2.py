# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-03 15:02:59
@LastEditors: Even.Sand
@LastEditTime: 2019-06-03 15:11:37
'''
# 1.多继承：子类有多个父类


class Human:
    def __init__(self, sex):
        self.sex = sex

    def p(self):
        print("这是Human的方法")


class Person:
    def __init__(self, name):
        self.name = name

    def p(self):
        print("这是Person的方法")

    def person(self):
        print("这是我person特有的方法")


class Teacher(Person):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age


class Student(Human, Person):
    def __init__(self, name, sex, grade):
        # super().__init__(name) #注意：对于多继承来说，使用super只会调用第一个父类的属性方法
        # super().__init__(sex)  #要想调用特定父类的构造器只能使用父类名.__init__方式。如下：

        Human.__init__(self, sex)
        Person.__init__(self, name)
        self.grade = grade


class Son(Human, Teacher):
    def __init__(self, sex, name, age, fan):
        Human.__init__(self, sex)
        Teacher.__init__(self, name, age)
        self.fan = fan


# ------创建对象 -------------
stu = Student("tom", "male", 88)
print(stu.name, stu.sex, stu.grade)
stu.p()  # 虽然父类Human和Person都有同名P()方法 ，但是调用的是括号里的第一个父类Human的方法

son1 = Son("jerry", "female", 18, "打球")
son1.person()  # 可以调用父类的父类的方法。
son1.p()  # 子类调用众多父类中同名的方法，按继承的顺序查找。
'''
=====================================================================================
tom male 88
这是Human的方法
这是我person特有的方法
这是Human的方法
'''
'''
# !总结:1.需要注意圆括号中继承父类的顺序,若是父类中有相同的方法名,而在子类使用时未指定,python从左至右搜索 即方法在子类中未找到时,从左到右查找父类中是否包含方法。
# !2.支持多层父类继承,子类会继承父类所有的属性和方法,包括父类的父类的所有属性和方法。
---------------------
作者：牛大财有大才
来源：CSDN
原文：https://blog.csdn.net/qq_26442553/article/details/81775449
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
