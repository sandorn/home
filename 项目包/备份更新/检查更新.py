# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-06-06 16:25:50
FilePath     : /CODE/项目包/备份更新/检查更新.py
Github       : https://github.com/sandorn/home
==============================================================
'''
# 检索需要升级的库,逐个升级
import subprocess


def update_outdated_libraries():
    print("正在检查需要更新的库...")

    try:
        # 运行pip list命令并捕获输出
        result = subprocess.run(['pip3', 'list', '--outdated'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        # 解析输出并获取需要更新的库列表
        outdated_libraries = [line.split()[0] for line in result.stdout.splitlines()[2:]]
        total_libraries = len(outdated_libraries)

        if total_libraries > 0:
            print(f"共有{total_libraries}个库需要更新：")

            for i, library in enumerate(outdated_libraries, start=1):
                print(f"正在更新库 {i}/{total_libraries}: {library}...")
                subprocess.run(['pip3', 'install', '-U', library])
                print(f"库 {library} 更新完成。\n")

            print(f"所有{total_libraries}个库已更新完毕！")
        else:
            print("没有需要更新的库。")

    except subprocess.CalledProcessError as e:
        print(f"错误：{e.stderr}")


if __name__ == "__main__":
    update_outdated_libraries()
