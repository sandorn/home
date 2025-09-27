# !/usr/bin/env python3
"""
==============================================================
Description  : 文件操作工具库，提供文件读写、路径处理、大小计算等功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-01-15 11:57:50
FilePath     : /CODE/xjlib/xt_utils/files.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import os
import winreg
from typing import Any

from xt_wraps import LogCls

log = LogCls()


class FileSize:
    """文件大小计算和格式化工具类

    提供文件大小的多单位表示和自动格式化功能，支持字节、KB、MB、GB、TB等单位。
    优化内存使用，通过__slots__限制实例属性。

    示例用法：
    >>> size = FileSize('example.txt')
    >>> log(size)  # 自动选择合适的单位显示
    >>> log(size.bytes)  # 获取字节数
    >>> log(size.mb)  # 获取MB数
    """

    __slots__ = ('_bytes',)  # 优化内存使用

    def __init__(self, file_path: str | os.PathLike):
        """
        初始化FileSize实例

        Args:
            file_path: 文件路径

        Raises:
            FileNotFoundError: 当文件不存在时
            IsADirectoryError: 当路径指向目录时
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'文件不存在: {file_path}')
        if os.path.isdir(file_path):
            raise IsADirectoryError(f'路径指向的是目录，不是文件: {file_path}')
        self._bytes = os.path.getsize(file_path)

    @property
    def bytes(self) -> int:
        """获取文件的字节大小"""
        return self._bytes

    @property
    def kb(self) -> float:
        """获取文件的KB大小"""
        return self._bytes / 1024

    @property
    def mb(self) -> float:
        """获取文件的MB大小"""
        return self._bytes / (1024**2)

    @property
    def gb(self) -> float:
        """获取文件的GB大小"""
        return self._bytes / (1024**3)

    @property
    def tb(self) -> float:
        """获取文件的TB大小"""
        return self._bytes / (1024**4)

    def __str__(self) -> str:
        """自动选择最合适的单位返回文件大小的字符串表示"""
        if self._bytes >= 1024**4:
            return f'{self.tb:.2f} TB'
        if self._bytes >= 1024**3:
            return f'{self.gb:.2f} GB'
        if self._bytes >= 1024**2:
            return f'{self.mb:.2f} MB'
        if self._bytes >= 1024:
            return f'{self.kb:.2f} KB'
        return f'{self._bytes} Bytes'

    def __repr__(self) -> str:
        """返回FileSize实例的代码表示"""
        return f'FileSize(bytes={self._bytes})'


class QSSTools:
    """Qt样式表(QSS)文件读取工具类

    提供读取和应用Qt样式表文件的便捷方法，适用于PyQt或PySide应用程序。

    示例用法：
    >>> QSSTools.set('styles.qss', main_window)
    """

    @classmethod
    def set(cls, file_path: str | os.PathLike, obj: Any) -> None:
        """
        读取QSS文件并应用到Qt对象

        Args:
            file_path: QSS文件路径
            obj: Qt对象，需要有setStyleSheet方法

        Raises:
            FileNotFoundError: 当QSS文件不存在时
            AttributeError: 当obj没有setStyleSheet方法时
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'QSS文件不存在: {file_path}')

        with open(file_path, encoding='UTF-8') as f:
            qss_content = f.read()

        if not hasattr(obj, 'setStyleSheet'):
            raise AttributeError(f'对象没有setStyleSheet方法: {type(obj).__name__}')

        obj.setStyleSheet(qss_content)


def get_desktop() -> str:
    """
    获取当前用户的桌面路径

    Returns:
        str: 桌面路径

    Raises:
        OSError: 当无法访问注册表时
    """
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',
        ) as key:
            return winreg.QueryValueEx(key, 'Desktop')[0]
    except OSError as e:
        raise OSError(f'无法获取桌面路径: {e}') from e


def file_to_list(filepath: str | os.PathLike, encoding: str = 'utf-8') -> list[str]:
    """
    读取文件内容并转换为行列表

    Args:
        filepath: 文件路径
        encoding: 文件编码，默认为"utf-8"

    Returns:
        List[str]: 文件内容的行列表

    Raises:
        FileNotFoundError: 当文件不存在时
        IOError: 当读取文件失败时
    """
    try:
        with open(filepath, encoding=encoding) as file_content:
            return list(file_content)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'文件不存在: {filepath}') from e
    except OSError as e:
        raise OSError(f'读取文件失败: {filepath}, 错误: {e}') from e


def save_file(filename: str | os.PathLike, data: Any, br: str = '\n') -> None:
    """
    将数据写入文件，支持多层次的列表或元组迭代

    Args:
        filename: 文件名
        data: 要写入的数据，可以是字符串、列表或元组
        br: 元素结束标志，默认为换行符"\n"

    Raises:
        IOError: 当写入文件失败时
    """
    # 确保目录存在
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(filename) + br)

            def _write_nested(data_item: Any) -> None:
                """递归写入嵌套的数据结构"""
                if isinstance(data_item, (list, tuple)):
                    for item in data_item:
                        _write_nested(item)
                    file.write(br)  # 在每个列表/元组结束后添加换行
                else:
                    file.write(str(data_item) + br)

            if isinstance(data, (list, tuple)):
                _write_nested(data)
            else:
                file.write(str(data) + br)

        # 输出文件保存信息
        size = f'size: {FileSize(filename)}'
        log(f'[{filename}]保存完成,\tfile {size}。')

    except OSError as e:
        raise OSError(f'写入文件失败: {filename}, 错误: {e}') from e


def read_file(filepath: str | os.PathLike, encoding: str = 'utf-8') -> str:
    """
    读取整个文件内容

    Args:
        filepath: 文件路径
        encoding: 文件编码，默认为"utf-8"

    Returns:
        str: 文件内容

    Raises:
        FileNotFoundError: 当文件不存在时
        IOError: 当读取文件失败时
    """
    try:
        with open(filepath, encoding=encoding) as f:
            return f.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(f'文件不存在: {filepath}') from err
    except OSError as err:
        raise OSError(f'读取文件失败: {filepath}, 错误: {err}') from err


def write_file(filepath: str | os.PathLike, content: str, encoding: str = 'utf-8', append: bool = False) -> None:
    """
    写入内容到文件

    Args:
        filepath: 文件路径
        content: 要写入的内容
        encoding: 文件编码，默认为"utf-8"
        append: 是否以追加模式写入，默认为False

    Raises:
        IOError: 当写入文件失败时
    """
    mode = 'a' if append else 'w'

    # 确保目录存在
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    try:
        with open(filepath, mode, encoding=encoding) as f:
            f.write(content)
    except OSError as e:
        raise OSError(f'写入文件失败: {filepath}, 错误: {e}') from e


def ensure_dir(path: str | os.PathLike) -> None:
    """
    确保目录存在，如果不存在则创建

    Args:
        path: 目录路径

    Raises:
        OSError: 当创建目录失败时
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            raise OSError(f'创建目录失败: {path}, 错误: {e}') from e


def get_file_extension(filepath: str | os.PathLike) -> str:
    """
    获取文件的扩展名

    Args:
        filepath: 文件路径

    Returns:
        str: 文件扩展名（不含点号）
    """
    return os.path.splitext(filepath)[1][1:].lower()


def get_file_name(filepath: str | os.PathLike, with_extension: bool = True) -> str:
    """
    获取文件名

    Args:
        filepath: 文件路径
        with_extension: 是否包含扩展名，默认为True

    Returns:
        str: 文件名
    """
    if with_extension:
        return os.path.basename(filepath)
    return os.path.splitext(os.path.basename(filepath))[0]


if __name__ == '__main__':
    """测试文件操作工具的功能"""

    # 测试基本功能
    log('=== 文件路径测试 ===')
    log(f'桌面路径: {get_desktop()}')

    # 测试FileSize类
    # 注意：这里需要确保有一个存在的文件用于测试
    current_file = __file__
    log(f'\n=== FileSize测试 (文件: {current_file}) ===')
    try:
        size = FileSize(current_file)
        log(f'文件大小 (Bytes): {size.bytes}')
        log(f'文件大小 (KB): {size.kb:.2f}')
        log(f'文件大小 (MB): {size.mb:.2f}')
        log(f'自动格式化: {size}')
    except (FileNotFoundError, IsADirectoryError) as e:
        log(f'FileSize测试失败: {e}')

    # 测试文件读写功能示例
    test_data = [4, [9, 99, 999, 9999], 16, 25, 36, 49]
    test_file = os.path.join(os.environ.get('TEMP', '.'), 'test_file.txt')
    log(f'\n=== 文件写入测试 (文件: {test_file}) ===')
    try:
        save_file(test_file, test_data)

        # 读取并显示内容
        content = read_file(test_file)
        log(f'写入的文件内容:\n{content}')

        # 测试file_to_list函数
        lines = file_to_list(test_file)
        log(f'按行读取的内容: {lines}')

        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
            log(f'测试文件已删除: {test_file}')
    except (OSError, FileNotFoundError) as e:
        log(f'文件操作测试失败: {e}')

    # 测试路径操作函数
    test_path = 'example/dir/file.txt'
    log(f'\n=== 路径操作测试 (路径: {test_path}) ===')
    log(f'文件扩展名: {get_file_extension(test_path)}')
    log(f'文件名(带扩展名): {get_file_name(test_path)}')
    log(f'文件名(不带扩展名): {get_file_name(test_path, with_extension=False)}')
