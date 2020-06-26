# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-05 11:48:40
#FilePath     : /xjLib/xt_File.py
#LastEditTime : 2020-06-25 17:26:43
#Github       : https://github.com/sandorn/home
#==============================================================
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


def file_to_List(filepath):
    res_list = []
    with open(filepath, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            res_list.append(line)
    return res_list


def savefile(_filename, _list_texts, br=''):
    '''
    函数说明:将多层次的list 或 tupl写入文件,迭代多层
    br为元素结束标志，可以用'\t'  '\n'  等
    '''
    if not isinstance(_list_texts, (list, tuple)):
        return

    with open(_filename, 'w', encoding='utf-8') as file:
        file.write(_filename + '\n')

        def each(data):
            for index, value in enumerate(data):
                if isinstance(value, (list, tuple)):
                    each(value)
                else:
                    file.write(str(value) + br)

            # # 最后一个元素已处理完毕，添加换行
            file.write('\n')

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
