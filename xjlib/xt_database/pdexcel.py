#!/usr/bin/env python3
"""
==============================================================
Description  : Excel操作工具 - 基于pandas的Excel文件读写功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-07-26 10:09:40
LastEditTime : 2024-09-06 11:00:00
FilePath     : /CODE/xjlib/xt_database/pdexcel.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- ExcelUtil类:封装了pandas库的Excel操作功能
- 支持Excel文件的创建、读取、修改和合并
- 支持多种数据格式转换和列名映射
- 支持多工作表数据处理

主要特性:
- 支持上下文管理器,自动处理资源关闭
- 提供灵活的API,支持多种数据读写方式
- 包含错误处理和类型检查,提高代码健壮性
- 集成日志系统,便于调试和问题追踪
==============================================================
"""
from __future__ import annotations

import os
from typing import IO

import numpy as np
import pandas
from pydantic import BaseModel, Field
from xt_wraps.log import LogCls

# 初始化日志实例
logger = LogCls()


class ColumnMapping(BaseModel):
    """列名映射 - 定义Excel列名与别名的对应关系"""

    column_name: str = Field(description='原始列名')
    column_alias: str = Field(description='显示列名')


class SheetMapping(BaseModel):
    """工作表映射 - 定义文件与工作表名称的对应关系"""

    file_name: str = Field(description='文件名')
    sheet_name: str = Field(description='工作表名称')


class DataCollect(BaseModel):
    """多工作表数据集合 - 封装单个工作表的完整数据和配置"""

    data_list: list[dict] = Field(description='数据列表')
    col_mappings: list[ColumnMapping] = Field(description='列名映射列表')
    sheet_name: str = Field(description='工作表名称')


class ExcelUtil:
    """Excel文件操作工具类 - 提供基于pandas的Excel文件读写功能

    该类封装了pandas库的主要Excel操作功能，提供简洁的API接口操作Excel文件
    支持数据转换、列名映射、多工作表处理等功能

    Attributes:
        DEFAULT_SHEET_NAME: 默认工作表名称
    """

    DEFAULT_SHEET_NAME = 'Sheet1'

    @classmethod
    def _to_excel(
        cls,
        data_list: list[dict],
        col_mappings: list[ColumnMapping],
        sheet_name: str,
        writer: pandas.ExcelWriter,
        **kwargs,
    ) -> None:
        """将数据列表写入Excel文件的内部方法

        Args:
            data_list: 数据集列表
            col_mappings: 表头列字段映射
            sheet_name: 工作表名称
            writer: ExcelWriter实例
            **kwargs: 传递给pandas.DataFrame.to_excel的额外参数
        """
        try:
            col_dict = (
                {cm.column_name: cm.column_alias for cm in col_mappings}
                if col_mappings
                else None
            )
            df = pandas.DataFrame(data=data_list)
            if col_dict:
                df.rename(columns=col_dict, inplace=True)
            df.to_excel(writer, sheet_name=sheet_name, index=False, **kwargs)
            logger.info(f'写入工作表[{sheet_name}]数据成功,包含{len(data_list)}行')
        except Exception as e:
            logger.error(f'写入工作表[{sheet_name}]数据失败: {e!s}')
            raise

    @classmethod
    def list_to_excel(
        cls,
        path_or_buffer: str | IO,
        data_list: list[dict],
        col_mappings: list[ColumnMapping],
        sheet_name: str | None = None,
        **kwargs,
    ) -> None:
        """将数据列表转换并写入Excel文件

        Args:
            path_or_buffer: 文件路径或者字节缓冲流
            data_list: 数据集列表
            col_mappings: 表头列字段映射
            sheet_name: 工作表名称，默认为Sheet1
            **kwargs: 传递给pandas.ExcelWriter的额外参数

        Example:
            >>> # 示例用法
            >>> data_list = [{"id": 1, "name": "hui", "age": 18}]
            >>> user_col_mapping = [
            ...         ColumnMapping(column_name='id', column_alias='用户id'),
            ...         ColumnMapping(column_name='name', column_alias='用户名'),
            ...         ColumnMapping(column_name='age', column_alias='年龄'),
            ... ]
            >>> ExcelUtil.list_to_excel('path_to_file.xlsx', data_list, user_col_mapping)
        """
        try:
            sheet_name = sheet_name or cls.DEFAULT_SHEET_NAME
            logger.info(f'开始写入Excel文件: {path_or_buffer}，工作表: {sheet_name}')
            with pandas.ExcelWriter(path_or_buffer) as writer:
                cls._to_excel(data_list, col_mappings, sheet_name, writer, **kwargs)
            logger.info(f'Excel文件[{path_or_buffer}]写入成功')
        except Exception as e:
            logger.error(f'Excel文件[{path_or_buffer}]写入失败: {e!s}')
            raise

    @classmethod
    def multi_list_to_excel(
        cls, path_or_buffer: str | IO, data_collects: list[DataCollect], **kwargs
    ) -> None:
        """将多个数据列表写入同一个Excel文件的不同工作表

        Args:
            path_or_buffer: 文件路径或者字节缓冲流
            data_collects: 数据集列表，每个元素包含一个工作表的数据
            **kwargs: 传递给pandas.ExcelWriter的额外参数
        """
        try:
            logger.info(f'开始写入多工作表Excel文件: {path_or_buffer}，工作表数量: {len(data_collects)}')
            with pandas.ExcelWriter(path_or_buffer) as writer:
                for data_collect in data_collects:
                    cls._to_excel(
                        data_list=data_collect.data_list,
                        col_mappings=data_collect.col_mappings,
                        sheet_name=data_collect.sheet_name,
                        writer=writer,
                        **kwargs,
                    )
            logger.info(f'多工作表Excel文件[{path_or_buffer}]写入成功')
        except Exception as e:
            logger.error(f'多工作表Excel文件[{path_or_buffer}]写入失败: {e!s}')
            raise

    @classmethod
    def read_excel(
        cls,
        path_or_buffer: str | IO,
        sheet_name: str | None = None,
        col_mappings: list[ColumnMapping] | None = None,
        all_col: bool = True,
        header: int = 0,
        nan_replace=None,
        **kwargs,
    ) -> list[dict]:
        """读取Excel表格数据并可选地根据列映射替换列名

        Args:
            path_or_buffer: 文件路径或者缓冲流
            sheet_name: 工作表名称，默认为Sheet1
            col_mappings: 列字段映射，用于重命名列
            all_col: True返回所有列信息，False则只返回col_mapping对应的字段信息
            header: 指定表头所在行，默认为0（第一行）
            nan_replace: NaN值的替换值，默认为None
            **kwargs: 传递给pandas.read_excel的额外参数

        Returns:
            list[dict]: 读取的数据列表，每行数据以字典形式表示
        """
        try:
            sheet_name = sheet_name or cls.DEFAULT_SHEET_NAME
            logger.info(f'开始读取Excel文件: {path_or_buffer}，工作表: {sheet_name}')
            
            # 构建列名映射字典
            col_dict = (
                {cm.column_name: cm.column_alias for cm in col_mappings}
                if col_mappings
                else None
            )
            
            # 确定要读取的列
            use_cols = None
            if not all_col:
                use_cols = list(col_dict) if col_dict else None

            # 读取Excel数据
            df = pandas.read_excel(
                path_or_buffer,
                sheet_name=sheet_name,
                usecols=use_cols,
                header=header,
                **kwargs,
            )
            
            # 替换NaN值
            df.replace(np.NAN, nan_replace)
            
            # 重命名列
            if col_dict:
                df.rename(columns=col_dict, inplace=True)
            
            # 转换为字典列表
            result = df.to_dict('records')
            logger.info(f'Excel文件[{path_or_buffer}]读取成功,包含{len(result)}条记录')
            return result
        except Exception as e:
            logger.error(f'Excel文件[{path_or_buffer}]读取失败: {e!s}')
            raise

    @classmethod
    def merge_excel_files(
        cls,
        input_files: list[str],
        output_file: str,
        sheet_mappings: list[SheetMapping] | None = None,
        **kwargs,
    ) -> None:
        """合并多个Excel文件到一个文件中，每个文件对应一个工作表

        Args:
            input_files: 待合并的Excel文件列表
            output_file: 输出文件路径
            sheet_mappings: 文件工作表映射，默认为文件名
            **kwargs: 传递给pandas.ExcelWriter的额外参数
        """
        try:
            sheet_mappings = sheet_mappings or []
            sheet_dict = {
                sheet_mapping.file_name: sheet_mapping.sheet_name
                for sheet_mapping in sheet_mappings
            }
            
            logger.info(f'开始合并Excel文件，源文件数: {len(input_files)}，输出文件: {output_file}')
            
            with pandas.ExcelWriter(output_file, engine_kwargs=kwargs) as writer:
                for file in input_files:
                    # 检查文件是否存在
                    if not os.path.exists(file):
                        logger.warning(f'文件不存在: {file}，跳过')
                        continue
                    
                    try:
                        df = pandas.read_excel(file)
                        file_name = os.path.basename(file)
                        sheet_name = sheet_dict.get(file_name, file_name)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        logger.info(f'成功合并文件[{file}]到工作表[{sheet_name}]')
                    except Exception as e:
                        logger.error(f'合并文件[{file}]失败: {e!s}')
                        # 继续处理下一个文件
                        continue
            
            logger.info(f'Excel文件合并完成，输出文件: {output_file}')
        except Exception as e:
            logger.error(f'Excel文件合并失败: {e!s}')
            raise
