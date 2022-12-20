# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
LastEditTime : 2022-12-19 22:50:48
FilePath     : /项目包/备份更新/安装三方库.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import subprocess


def 获取文件路径():
    import os

    import win32ui
    mypath = os.path.split(os.path.realpath(__file__))[0] + "\\"
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    dlg.SetOFNInitialDir(mypath)  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()  # 获取选择的文件名称
    return filename


def 执行安装(filename, comm_1="pip3"):
    list1 = []
    with open(filename, "r") as file:
        list1 = file.readlines()

    for i in range(0, len(list1)):
        list1[i] = list1[i].rstrip("\n")
        print(list1[i])

    s = len(list1)
    n = 1
    print("{}个库开始安装：".format(s))
    for nu in list1:
        com_ins = comm_1 + " install {py}".format(py=nu)
        print("共有{}个库，正在安装第{}个库{}，\n执行命令：{}，请耐心等待.......".format(s, n, nu, com_ins))
        subprocess.call(com_ins, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        n += 1
        print("----------{com} 执行结束-----------\n".format(com=com_ins))

    print("{}个库已全部安装完毕！".format(s))


if __name__ == "__main__":
    # 执行安装(filename)
    执行安装("D:/CODE/项目包/备份更新/PIP-list-20221113101840.txt")
