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
@LastEditTime: 2019-06-03 15:13:10
'''
# 1.多继承子类对父类构造方法的调用


class Human:
    def __init__(self, sex):
        self.sex = sex

    def p(self):
        print("这是Human的方法")

    def str1(self):
        print("this si :" + str(self.sex))


class Person:
    def __init__(self, name):
        self.name = name

    def p(self):
        print("这是Person的方法")

    def person(self):
        print("这是我person特有的方法")

    def str2(self):
        print("this is :" + str(self.name))


class Student(Human, Person):  # 注意子类如果没有构造方法时，按括号内父类的继承顺序去继承父类构造方法，只继承一个
    def prin(self):
        print("student")


# ------创建对象 -------------
# stu1=Studnent("男","tom")报错。
stu = Student("sex")  # 这里继承的是Huma的构造方法。
stu.p()
stu.str1()
# stu.str2()报错，因为即使human和person都是一个参数的构造方法，但是这里继承调用的是第一个Human的构造方法


'''
====================================================================================
这是Human的方法
this sisex
# ! 总结：子类从多个父类派生，而子类又没有自己的构造函数时，
# ! （1）按顺序继承，哪个父类在最前面且它又有自己的构造函数，就继承它的构造函数；
# ! （2）如果最前面第一个父类没有构造函数，则继承第2个的构造函数，第2个没有的话，再往后找，以此类推。
---------------------
作者：牛大财有大才
来源：CSDN
原文：https://blog.csdn.net/qq_26442553/article/details/81775449
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
