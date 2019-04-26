# ！/usr/bin/env python
# -*-coding:utf-8-*-
"""
@Software:   VSCode
@File    :   安装三方库.py
@Time    :   2019/04/26 12:33:32
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
"""

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


def 执行安装(filename, comm_1="conda"):
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
        print("共有{}个库，正在安装第{}个库{}，\n执行命令：{}，请耐心等待.......".format(
            s, n, nu, com_ins))
        subprocess.Popen(
            com_ins,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        n += 1
        print("----------{com} 执行结束-----------\n".format(com=com_ins))

    print("{}个库已全部安装完毕！".format(s))


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


def freeze安装(filename, comm_1="conda"):
    print(comm_1 + "  freeze安装:")
    '''pip批量导出包含环境中所有组件的requirements.txt文件
    pip freeze > requirements.txt
    pip批量安装requirements.txt文件中包含的组件依赖
    pip install -r requirements.txt
    conda批量导出包含环境中所有组件的requirements.txt文件
    conda list -e > requirements.txt
    pip批量安装requirements.txt文件中包含的组件依赖
    conda install --yes --file requirements.txt'''
    if comm_1 == "conda":
        subprocess.call("conda install --yes --file  " + filename, shell=True)
    else:
        subprocess.call("pip install -r " + filename, shell=True)
    print(comm_1 + "  freeze安装完成！")


if __name__ == "__main__":
    NO = input("PIP_list(0);\n\
CONDA_list(1);\n\
PIP_freeze(2);\n\
CONDA_list_e(3);\n\
取消(9);\n\
please input:")

    for case in switch(NO):
        if case("0"):
            filename = 获取文件路径()
            执行安装(filename, "pip")
            break
        if case("1"):
            filename = 获取文件路径()
            执行安装(filename)
            break
        if case("2"):
            filename = 获取文件路径()
            freeze安装(filename, "pip")
            break
        if case("3"):
            filename = 获取文件路径()
            freeze安装(filename)
            break
        if case("9"):
            break
