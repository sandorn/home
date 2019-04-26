﻿# 检索需要升级的库，逐个升级

import os
import subprocess
import time  # 引入time模块

mypath = os.path.split(os.path.realpath(__file__))[0] + "/"


def PIP_list_备份():
    print("PIP_list_备份:\n检查已经安装库:")
    # pip显示需要更新的python列表
    com_list = 'pip list '
    print("执行命令并返回结果")
    p = subprocess.Popen(
        com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 取命令返回结果，结果是一个二进制字符串，包含了我们上面执行pip list -o后展现的所有内容
    out = p.communicate()[0]
    print("二进制转utf-8字符串")
    out = str(out, 'utf-8')

    print("切出待升级的包名, 并存入列表")
    need_back = []
    for i in out.splitlines()[2:]:
        临时字符 = i.split(' ')[0]
        print("----------备份{} -----------".format(临时字符))
        need_back.append(临时字符)

    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = mypath + 'PIP-list-%s.txt' % (ticks)
    print(filename)
    print("写库名到备份文件")
    file = open(filename, 'w')
    sep = '\n'
    file.write(str(sep.join(need_back)))
    file.close()
    print("{}个库已全部备份完毕！".format(len(need_back)))


def CONDA_list_备份():
    print("CONDA_list_备份:\n检查已经安装库:")
    com_list = 'conda list '
    print("执行命令并返回结果")
    p = subprocess.Popen(
        com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 取命令返回结果，结果是一个二进制字符串，包含了我们上面执行conda list后展现的所有内容
    out = p.communicate()[0]
    print("二进制转utf-8字符串")
    out = str(out, 'utf-8')

    print("切出待升级的包名, 并存入列表")
    need_back = []
    for i in out.splitlines()[4:]:
        临时字符 = i.split(' ')[0]
        print("----------备份{} -----------".format(临时字符))
        need_back.append(临时字符)

    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = mypath + 'CONDA-list-%s.txt' % (ticks)
    print(filename)
    print("写库名到备份文件")
    file = open(filename, 'w')
    sep = '\n'
    file.write(str(sep.join(need_back)))
    file.close()
    print("{}个库已全部备份完毕！".format(len(need_back)))


def PIP_freeze备份():
    print("PIP_freeze备份:")
    '''pip批量导出包含环境中所有组件的requirements.txt文件
    pip freeze > requirements.txt
    pip批量安装requirements.txt文件中包含的组件依赖
    pip install -r requirements.txt
    conda批量导出包含环境中所有组件的requirements.txt文件
    conda list -e > requirements.txt
    pip批量安装requirements.txt文件中包含的组件依赖
    conda install --yes --file requirements.txt'''
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = mypath + 'PIP-requirements-%s.txt' % (ticks)
    subprocess.call("pip freeze > " + filename, shell=True)
    print("PIP_freeze备份完成！")


def CONDA_list_e备份():
    print("CONDA_list_e备份开始:")
    ticks = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = mypath + 'CONDA-requirements-%s.txt' % (ticks)
    subprocess.call("conda list -e > " + filename, shell=True)
    print("CONDA_list_e备份完成！")


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
    NO = input("PIP_list_备份(0);\n\
CONDA_list_备份(1);\n\
PIP_freeze备份(2);\n\
CONDA_list_e备份(3);\n\
执行所有备份(9);\n\
please input:")

    for case in switch(NO):
        if case('0'):
            PIP_list_备份()
            break
        if case('1'):
            CONDA_list_备份()
            break
        if case('2'):
            PIP_freeze备份()
            break
        if case('3'):
            CONDA_list_e备份()
            break
        if case('9'):
            PIP_list_备份()
            CONDA_list_备份()
            PIP_freeze备份()
            CONDA_list_e备份()
            break
