# CODE — 个人代码仓库

## 项目概览

个人代码仓库，托管于 GitHub/Gitee，作为动态更新的代码网盘使用。包含多个独立子项目/模块。

## 目录结构

| 目录       | 用途                                                     |
| ---------- | -------------------------------------------------------- |
| `项目包/`  | Python 并发编程示例（线程池、进程池、异步等）            |
| `AHK/`     | AutoHotkey 脚本（鼠标点击器等）                          |
| `configs/` | 开发环境配置文件（git、ruff、uv、pyproject 等）          |
| `VBS/`     | VBScript 脚本（Excel/Word 自动化、VBA 脚本库）           |
| `xjlib/`   | 自定义 Python 工具库（数据库、HTTP、线程、日志、ORM 等） |

## 关键约定

- Python 包管理使用 `uv`，配置文件在 `configs/`
- 代码格式化使用 `ruff`，配置见 `configs/ruff.toml`
- 自定义库 `xjlib/` 通过 `configs/xjlib.pth` 注册到 Python 路径
- VBScript 脚本在 `VBS/` 目录下，VBA 脚本在 `VBS/VBA脚本/`

## 深入文档

- `configs/help/` — 开发流程、符号链接、打包上传等帮助文档
- `configs/rules/` — 项目标准、模板、设置脚本
- `xjlib/xt_pyqt/README.md` — PyQt 工具库说明
