# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
LastEditTime : 2022-12-05 01:20:29
FilePath     : /项目包/备份更新/检查更新.py
Github       : https://github.com/sandorn/home
==============================================================
'''

# 检索需要升级的库，逐个升级
import subprocess


def PIP更新1():
    print("PIP-outdated更新：")
    # pip显示需要更新的python列表
    com_list_o = 'pip3 list --outdated'

    # 执行命令并返回结果
    p = subprocess.Popen(com_list_o, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        print("正在更新第{}/{}个库[{}]，\n执行：{}，请等待...".format(n, s, nu, com_update))
        subprocess.call(com_update)
        n += 1
        print("----------{com} 执行结束-----------\n".format(com=com_update))

    print("{}个库已全部更新完毕！".format(s))


if __name__ == '__main__':

    PIP更新1()
