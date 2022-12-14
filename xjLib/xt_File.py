# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
LastEditTime : 2022-12-03 18:18:08
FilePath     : /xjLib/xt_File.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os


class filesize:

    def __init__(self, filePath):
        self.Bytes = os.path.getsize(filePath)
        self.KB = self.Bytes / 1024
        self.MB = self.KB / 1024

    def __str__(self):
        if self.MB > 10:
            res = f'{self.MB:.2f} MB'
        elif self.KB > 10:
            res = f'{self.KB:.2f} KB'
        else:
            res = f'{self.Bytes} Bytes'
        return res


class qsstools:

    def __init__(self):
        pass

    """定义一个读取样式的工具类"""

    @classmethod
    def set(cls, file_path, obj):
        with open(file_path, 'r', encoding='UTF-8') as f:
            obj.setStyleSheet(f.read())


import winreg


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    if path := winreg.QueryValueEx(key, "Desktop")[0]: return path


def file_to_List(filepath):
    res_list = []
    with open(filepath, 'r') as file_to_read:
        while content := file_to_read.readline():
            res_list.append(content)
    return res_list


def savefile(_filename, _list_texts, br=''):
    """
    函数说明:将多层次的list 或 tupl写入文件,迭代多层
    br为元素结束标志,可以用'\t'  '\n'  等
    """
    if not isinstance(_list_texts, (list, tuple)): return

    with open(_filename, 'w', encoding='utf-8') as file:

        def each(data):
            for value in data:
                if isinstance(value, (list, tuple)):
                    each(value)
                else:
                    file.write(str(value) + br)

            # # 最后一个元素已处理完毕,添加换行
            file.write('\n')

        file.write(_filename + '\n')
        each(_list_texts)

    size = f"size: {filesize(_filename)}"

    print(f'[{_filename}]保存完成,\tfile {size}。')


def filedialog(_dir='c:/'):
    import win32ui

    _dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    _dlg.SetOFNInitialDir(_dir)  # 设置打开文件对话框中的初始显示目录
    _dlg.DoModal()
    filename = _dlg.GetPathName()  # 获取选择的文件名称
    return filename


if __name__ == "__main__":
    print(get_desktop())
    print(os.getenv('TMP'))
    nums = [4, 9, 16, 25, 36, 49]

    def f(x):
        print('调用次数')
        return x**0.5

    print([n for i in nums if (n := f(i)) >= 5])
