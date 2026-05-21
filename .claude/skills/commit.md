---
title: commit
description: 一键代码检查 + Git 提交（neat → typecheck → git add/commit）
---

Run code quality checks and commit changes in one step:

1. Format and fix code with `ruff`
2. Run type checking with `basedpyright`
3. Stage all changes and commit

```powershell
ruff format .
ruff check --fix --unsafe-fixes .
basedpyright .
git add .
git commit
```
