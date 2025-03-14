# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-01-15 11:57:50
FilePath     : /CODE/xjLib/xt_file.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import winreg


class FileSize:
    def __init__(self, filePath):
        self.bytes = os.path.getsize(filePath)

    @property
    def mb(self):
        return self.bytes / (1024**2)

    @property
    def kb(self):
        return self.bytes / 1024

    def __str__(self):
        if self.mb >= 1.00:
            return f"{self.mb:.2f} MB"
        elif self.kb >= 1.00:
            return f"{self.kb:.2f} KB"
        return f"{self.bytes} Bytes"


class qsstools:
    def __init__(self):
        pass

    """定义一个读取样式的工具类"""

    @classmethod
    def set(cls, file_path, obj):
        with open(file_path, encoding="UTF-8") as f:
            obj.setStyleSheet(f.read())


def get_desktop():
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
    ) as key:
        return winreg.QueryValueEx(key, "Desktop")[0]


def file_to_List(filepath):
    with open(filepath) as file_content:
        return list(file_content)


def savefile(_filename, _str_list, br=""):
    """
    函数说明:将多层次的list 或 tupl写入文件,迭代多层
    br为元素结束标志,可以用'\t'  '\n'  等
    """

    def _each(data):
        for item in data:
            if isinstance(item, (list, tuple)):
                _each(item)
            else:
                _file.write(str(item) + br)

        _file.write("\n")  # 最后一个元素已处理完毕,添加换行符

    with open(_filename, "w", encoding="utf-8") as _file:
        _file.write(_filename + "\n")
        if isinstance(_str_list, (list, tuple)):
            _each(_str_list)
        else:
            _file.write(str(_str_list) + br)

    size = f"size: {FileSize(_filename)}"
    print(f"[{_filename}]保存完成,\tfile {size}。")


if __name__ == "__main__":
    # print(get_desktop())
    # print(os.getenv("TMP"))
    nums = [4, [9, 99, 999, 9999], 16, 25, 36, 49]
    # savefile("c:\\1.txt", str(nums))

    def f(x):
        print("调用次数", x)
        return x**2

    print([n for i in range(50) if (n := f(i)) >= 5])
