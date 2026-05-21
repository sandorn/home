---
title: help
description: 显示所有可用的 Cursor 技能和规则
---

# Cursor Skills & Rules

## 可用技能（Slash Commands）

| 命令         | 描述                                   |
| ------------ | -------------------------------------- |
| `/forch`      | 使用 ruff 格式化并修复所有 Python 代码 |
| `/lint`      | 运行 ruff 代码检查（不自动修复）       |
| `/typecheck` | 运行 basedpyright 类型检查             |
| `/test`      | 运行 pytest 测试                       |
| `/commit`    | 一键代码检查 + Git 提交                |
| `/help`      | 显示此帮助信息                         |

## 自动规则

| 规则                   | 匹配文件 | 描述                      |
| ---------------------- | -------- | ------------------------- |
| `project-overview.mdc` | `*`      | 项目概览与目录结构说明    |
| `python-style.mdc`     | `*.py`   | Python 编码规范与风格指南 |

## 一键检查命令

```powershell
# PowerShell 5
ruff check --fix --unsafe-fixes .; ruff format --check .; basedpyright .

# PowerShell 7
ruff check --fix --unsafe-fixes . && ruff format --check . && basedpyright .
```
