# CODE — 个人代码仓库

## 项目概览

个人代码仓库，托管于 Gitee，作为动态更新的代码网盘使用。包含多个独立子项目/模块。

## 目录结构

| 目录       | 用途                                                     |
| ---------- | -------------------------------------------------------- |
| `项目包/`  | Python 并发编程示例（线程池、进程池、异步等）            |
| `AHK/`     | AutoHotkey 脚本（鼠标点击器等）                          |
| `configs/` | 开发环境配置文件（git、ruff、uv、pyproject 等）          |
| `VBS/`     | VBScript 脚本（Excel/Word 自动化、VBA 脚本库）           |
| `xjlib/`   | 自定义 Python 工具库（数据库、HTTP、线程、日志、ORM 等） |
| `.cursor/` | Cursor 编辑器配置（skills、rules 等）                    |

## 关键约定

- Python 包管理使用 `uv`，配置文件在 `configs/`
- 代码格式化使用 `ruff`，配置见 `configs/ruff.toml`
- 类型检查使用 `basedpyright`
- 自定义库 `xjlib/` 通过 `configs/xjlib.pth` 注册到 Python 路径
- VBScript 脚本在 `VBS/` 目录下，VBA 脚本在 `VBS/VBA脚本/`
- 项目根 `pyproject.toml` 为 uv 项目配置（含依赖声明）

## Agent Skills（`.cursor/skills/`）

| Skill        | 触发词                                              | 用途                           |
| ------------ | --------------------------------------------------- | ------------------------------ |
| `neat-freak` | `/neat`, `/sync`, `同步一下`, `整理文档`, `收尾` 等 | 会话结束后文档与记忆洁癖级同步 |
| `commit`     | `/commit`                                           | 规范化 git commit 消息         |
| `forch`      | `/forch`                                            | 代码审查与重构                 |
| `help`       | `/help`                                             | 技能帮助                       |
| `lint`       | `/lint`                                             | 代码检查                       |
| `test`       | `/test`                                             | 测试                           |
| `typecheck`  | `/typecheck`                                        | 类型检查                       |

## 开发命令

```powershell
# 代码质量检查
ruff check --fix --unsafe-fixes .
ruff format .

# 类型检查
basedpyright .

# 一键检查
ruff check --fix --unsafe-fixes .; ruff format --check .; basedpyright .
```

## 深入文档

- `configs/help/` — 开发流程、符号链接、打包上传等帮助文档
- `configs/rules/` — 项目标准、模板、设置脚本
- `xjlib/xt_pyqt/README.md` — PyQt 工具库说明
- `.cursor/skills/neat-freak/references/` — neat-freak 参考资料（变更影响矩阵、Agent 路径速查）
