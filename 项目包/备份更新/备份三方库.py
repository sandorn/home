# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
LastEditTime : 2022-12-05 01:23:03
FilePath     : /项目包/备份更新/备份三方库.py
Github       : https://github.com/sandorn/home
==============================================================
'''

# 检索需要升级的库，逐个升级

import os
import subprocess
import time  # 引入time模块

mypath = os.path.split(os.path.realpath(__file__))[0] + "\\"


def PIP_list_备份():
    print("PIP_list_备份:")
    # pip显示需要更新的python列表
    com_list = 'pip3 list '
    p = subprocess.Popen(com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    filename.replace('\\', '/')
    subprocess.call("pip3 freeze > " + filename, shell=True)
    print("PIP_freeze备份完成！")


if __name__ == '__main__':
    PIP_list_备份()
    PIP_freeze备份()
