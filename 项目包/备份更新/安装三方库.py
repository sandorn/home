# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-03-15 20:31:22
FilePath     : /CODE/项目包/备份更新/安装三方库.py
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
    return dlg.GetPathName()


def 执行安装(filename):
    list1 = []
    with open(filename, "r") as file:
        list1 = file.readlines()

    for i in range(len(list1)):
        list1[i] = list1[i].rstrip("\n")

    print(f"{len(list1)}个库开始安装：")
    for n, nu in enumerate(list1, start=1):
        com_ins = f"pip3 install -U {nu}"
        print(f"正在安装第{n}个库{nu},\n执行命令：{com_ins}，请耐心等待.......")
        subprocess.call(com_ins)
        #, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print(f"----------{com_ins} 执行结束-----------\n")

    print(f"{len(list1)}个库已全部安装完毕！")


def 执行删除(filename):
    list1 = []
    with open(filename, "r") as file:
        list1 = file.readlines()

    print(f"{len(list1)}个库开始删除：")

    com_ins = f"D:/Python3/python.exe -m pip uninstall -r  {filename} -y"
    subprocess.call(com_ins)

    print(f"{len(list1)}个库已全部删除完毕！")


if __name__ == "__main__":
    filename = "D:/CODE/项目包/备份更新/PIP-list-20230315232108.txt"
    # 执行删除(filename)
    执行安装(filename)
