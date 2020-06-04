# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-03 17:06:56
@LastEditors: Even.Sand
@LastEditTime: 2020-04-03 17:06:58
'''


import hashlib
from contextlib import contextmanager
# contextlib
'''
任何对象，只要正确实现了上下文管理，就可以用于with语句。
实现上下文管理是通过__enter__和__exit__这两个方法实现的，
也可以通过@contextmanager和closing函数实现
'''
print('用contextlib实现在函数调用前后打印log的功能：')
print('（1）contextlib: with...as...语句')


class Call(object):
    def __init__(self, func):
        self.__func = func

    def __enter__(self):
        print('Call %s()' % self.__func.__name__)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('%s() End' % self.__func.__name__)

    def doProcess(self):
        self.__func()


def testFunc():
    print('I am testFunc, I am doing something...')


'''
执行顺序：
1，执行Call里面的__enter__函数
2，然后执行with语句里面的c.doProcess()
3，再执行Call里面的__exit__函数
结果：
	Call testFunc()
	I am testFunc, I am doing something...
	testFunc() End
'''
with Call(testFunc) as c:
    c.doProcess()

# 用@contextmanager实现和上面一样的功能，在函数调用前后打印log
print('（2）contextlib: with...as...语句，用@contextmanager实现')
from contextlib import contextmanager


class Call2(object):  # 不用实现__enter__和__exit__函数了
    def __init__(self, func):
        self.__func = func

    def doProcess(self):
        self.__func()


@contextmanager
def callWraper(func):
    print('Call %s()' % func.__name__)
    c = Call2(func)
    yield c
    print('%s() End' % func.__name__)


'''
执行流程：
1, with语句先执行callWraper函数里面yield之前的语句
2，yield调用会执行with语句内部的所有语句c.doProcess()
3，最后执行yield之后的语句
'''
with callWraper(testFunc) as c:
    c.doProcess()

# 实现用with语句可以在用户执行操作前连接数据库，在执行完操作后关闭数据库的功能

# 由字符串获取md5摘要信息串


def md5DigestGet(str):
    str += '!@#$%^'  # 为了使简单的字符串不被黑客破解，将字符串添油加醋
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()


class myDb(object):
    def __init__(self, users):
        self.__linkFlag = False  # 连接标志
        self.__usersLoginDigests = {}  # 保存用户名和密码的摘要信息
        for name, passward in users.items():
            md5Digest = md5DigestGet(name + passward)
            self.__usersLoginDigests[name] = md5Digest

    def getDbInfo(self):
        return self.__usersLoginDigests

    def loginCheck(self, name, passward):
        if md5DigestGet(name + passward) == self.getDbInfo()[name]:
            print('%s Login success' % name)
        else:
            print('%s Login fail' % name)

    def linkDb(self):
        self.__linkFlag = True
        return self.loginCheck

    def unlinkDb(self):
        self.__linkFlag = False


def linkDb(db):  # 连接到数据库
    print('Trying to link to db...')
    checkFunc = db.linkDb()
    print('Link db success..')
    return checkFunc


def unlinkDb(db):
    print('Trying to unlink db...')
    db.unlinkDb()
    print('unLink db success..')


@contextmanager
def userLoginCheck(db, name, passward):
    checkFunc = linkDb(db)
    yield checkFunc
    unlinkDb(db)
