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
@LastEditors: Even.Sand
@LastEditTime: 2020-02-29 17:15:27
'''

# 检索需要升级的库，逐个升级
import subprocess


def PIP更新1():
    print("PIP更新1：")
    # pip显示需要更新的python列表
    com_list_o = 'pip3 list --outdated'

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
        com_update = 'pip3 install --upgrade {py}'.format(py=nu)
        print("正在更新第{}/{}个库[{}]，\n执行：{}，请等待...".format(
            n, s, nu, com_update))
        subprocess.call(com_update)
        n += 1
        print("----------{com} 执行结束-----------\n".format(com=com_update))

    print("{}个库已全部更新完毕！".format(s))


def PIP更新2():
    print("PIP更新2：")
    subprocess.call(
        'pip3 install pip3-review', shell=True, stdout=subprocess.PIPE)
    subprocess.call(
        'pip-review --local --interactive --auto',
        shell=True,
        stdout=subprocess.PIPE)
    print('结束')


def CONDA更新():
    print("CONDA更新：")
    # # subprocess.call("conda update -n base -c defaults conda ", shell=True)
    subprocess.call("conda update --all ", shell=True)
    subprocess.call("conda upgrade --all ", shell=True)
    subprocess.call("conda clean -a ", shell=True)


if __name__ == '__main__':
    expression = True
    while expression:
        NO = input('''PIP更新1(1)\nPIP更新2(2)\nCONDA更新(3)\n不更新退出(0)\n输入选项:''')
        if NO == '1':
            PIP更新1()
        elif NO == '2':
            PIP更新2()
        elif NO == '3':
            CONDA更新()
        elif NO == '0':
            print('退出更新')
            expression = False
        else:
            print('输入选项错误，请重新输入')
