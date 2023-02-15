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

    def __str__(self):
        if self.Bytes > 1024 * 1024:
            return f'{self.Bytes / 1024 / 1024:.2f} MB'
        elif self.Bytes > 1024:
            return f'{self.Bytes / 1024:.2f} KB'
        else:
            return f'{self.Bytes} B'


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
    return winreg.QueryValueEx(key, "Desktop")[0]


def file_to_List(filepath):
    with open(filepath, 'r') as file_to_read:
        # 1:while content := file_to_read.readline():
        #     res_list.append(content)
        # 2:return [content for content in file_to_read]
        return list(file_to_read)


def savefile(_filename, _str_list, br=''):
    """
    函数说明:将多层次的list 或 tupl写入文件,迭代多层
    br为元素结束标志,可以用'\t'  '\n'  等
    """
    # 类型检查
    assert isinstance(_str_list, (list, tuple)), '参数类型错误'

    with open(_filename, 'w', encoding='utf-8') as _file:
        # 内部函数
        def _each(data):
            for item in data:
                if isinstance(item, (list, tuple)):
                    _each(item)
                else:
                    _file.write(str(item) + br)

            # 最后一个元素已处理完毕,添加换行符
            _file.write('\n')

        _file.write(_filename + '\n')
        _each(_str_list)

    size = f"size: {filesize(_filename)}"
    print(f'[{_filename}]保存完成,\tfile {size}。')


import win32ui


def filedialog(_dir='C:/'):
    '''依据封装win32ui库,实现打开文件对话框,并返回文件路径名'''
    arg = f'defaultDir={_dir or "C:/"}'
    _dlg = win32ui.CreateFileDialog(1, arg)  # 1表示打开文件对话框
    # _dlg.SetOFNInitialDir(_dir)  # 设置打开文件对话框中的初始显示目录
    _dlg.DoModal()
    return _dlg.GetPathName()


if __name__ == "__main__":
    # print(get_desktop())
    # print(os.getenv('TMP'))
    # nums = [4, 9, 16, 25, 36, 49]

    # def f(x):
    #     print('调用次数')
    #     return x**0.5

    # print([n for i in nums if (n := f(i)) >= 5])
    print(filedialog())
