# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-03 23:26:06
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-11 01:30:32
'''

# 检索需要升级的库，逐个升级
import subprocess


def PIP更新1():
    print("PIP更新1：\n检查更新情况:")
    # pip显示需要更新的python列表
    com_list_o = 'pip list --outdated'

    # 执行命令并返回结果
    p = subprocess.Popen(
        com_list_o,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    # 取命令返回结果，结果是一个二进制字符串，包含了我们上面执行pip list -o后展现的所有内容
    out = p.communicate()[0]

    print("二进制转utf-8字符串....")
    out = str(out, 'utf-8')

    print("切出待升级的包名, 并存入列表........")
    need_update = []
    for i in out.splitlines()[2:]:
        need_update.append(i.split(' ')[0])
    s = len(need_update)
    print("需要升级的库有:{}个".format(s))

    # 执行升级命令，每次取一个包进行升级，pip只支持一个包一个包的升级
    n = 1
    for nu in need_update:
        com_update = 'pip install -U {py}'.format(py=nu)
        print("正在更新第{}/{}个库[{}]，\n执行：{}，请等待...".format(
            n, s, nu, com_update))
        subprocess.call(com_update)
        n += 1
        print("----------{com} 执行结束-----------\n".format(com=com_update))

    print("{}个库已全部更新完毕！".format(s))


def PIP更新2():

    from pip._internal.utils.misc import get_installed_distributions
    # 如果版本是9.0.1，下面get_installed_distributions后无括号
    # 如果版本是10.0.1，下面get_installed_distributions后有括号
    print("PIP更新2：\n检查更新情况:")
    n = 1
    s = len(get_installed_distributions())
    for dist in get_installed_distributions():
        subprocess.call("pip install -U " + dist.project_name, shell=True)
        # conda upgrade --all：更新所有包
        print("正在更新第{}/{}个库[{}]，请等待.......".format(n, s, dist.project_name))
        n += 1
    print("{}个库已全部更新完毕！".format(s))
    # 逐个更新，速度较慢


def PIP更新3():
    print("PIP更新3：\n检查更新情况:")
    subprocess.call(
        'pip install pip-review', shell=True, stdout=subprocess.PIPE)
    subprocess.call(
        'pip -review --local --interactive --auto',
        shell=True,
        stdout=subprocess.PIPE)
    print('结束')


def CONDA更新():
    print("CONDA更新：\n检查更新情况:")
    # # subprocess.call("conda update -n base -c defaults conda ", shell=True)
    subprocess.call("conda update --all ", shell=True)
    subprocess.call("conda upgrade --all ", shell=True)
    subprocess.call("conda clean -a ", shell=True)


class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


if __name__ == '__main__':
    NO = input("CONDA更新(0)\n\
PIP更新1(1)\n\
PIP更新2(2)\n\
PIP更新3(3)\n\
不更新退出(9)\n\
please input:")

    for case in switch(NO):
        if case('0'):
            CONDA更新()
            exit
        if case('1'):
            PIP更新1()
            exit
        if case('2'):
            PIP更新2()
            exit
        if case('3'):
            PIP更新3()
            exit
        if case('9'):
            exit
