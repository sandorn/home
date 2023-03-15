# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-03-15 20:29:40
FilePath     : /CODE/项目包/备份更新/检查更新.py
Github       : https://github.com/sandorn/home
==============================================================
'''
# 检索需要升级的库,逐个升级
import subprocess


def PIP更新():
    print("PIP-outdated更新:")
    # pip显示需要更新的python列表
    p = subprocess.Popen(
        'pip3 list --outdated',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding='utf-8',
        errors='ignore',
    )

    # 取命令返回结果,包含了我们上面执行pip list -o后展现的所有内容

    out = p.communicate()[0]

    print("切出待升级的包名, 并存入列表........")
    need_update = [i.split(' ')[0] for i in out.splitlines()[2:]]
    s = len(need_update)
    print(f"需要升级的库有:{s}个")

    for n, nu in enumerate(need_update, start=1):
        #  --upgrade-strategy only-if-needed 会升级到最新的兼容版本
        # com_update = f'pip3 install --upgrade-strategy only-if-needed {nu}'
        com_update = f'pip3 install -U {nu}'
        print(f"正在更新第{n}/{s}个库[{nu}],\n执行:{com_update},请等待...")
        subprocess.call(com_update)
        print("----------{com} 执行结束-----------\n".format(com=com_update))

    print(f"{s}个库已全部更新完毕！")


if __name__ == '__main__':

    PIP更新()
