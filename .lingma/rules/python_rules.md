---
trigger: always_on
alwaysApply: true
---
# Python 编码规范

## 1. 基础规范

### 1.1 代码质量与合规性
- 必须通过 `ruff check --fix --unsafe-fixes` 验证
- 遵循 PEP 8 规范，行长度限制为 200 字符
- 文件头必须包含 `# !/usr/bin/env python3`
- 移除冗余代码和死代码，避免过度工程化
- 采用模块化设计，功能分离清晰

## 2. 命名与结构

### 2.1 命名约定
- **语义化命名**：使用 `user_count` 而非缩写 `uc`
- **临时变量**：使用 `tmp_` 前缀（如 `tmp_result`）
- **布尔变量**：使用 `is_`、`has_`、`can_` 前缀
- **常量**：全大写加下划线（如 `MAX_RETRIES`）

### 2.2 结构要求
- **单一职责**：函数/类职责单一明确
- **嵌套限制**：嵌套深度不超过 3 层
- **导入规范**：使用绝对路径导入，禁止相对导入
- **模块组织**：相关功能组织在同一模块中

## 3. 类型提示与文档

### 3.1 类型注解要求
- 所有函数参数和返回值必须标注类型（包括 `None`）
- 使用现代类型语法：
  - `list[int]`、`dict[str, Any]`、`tuple[int, str]`（替代旧式泛型）
  - `str | None`（替代 `Optional[str]`）
- 禁止使用：`List`, `Dict`, `Tuple`, `Optional`, `Union`
- 尽量不使用泛型 如 `TypeVar`, `Generic`等
- 遵循 PEP 695 类型参数规则

### 3.2 文档风格
- 使用 Google 风格文档字符串
- 参考模板：`D:/CODE/xjlib/template.py`
- 文档应包含：函数描述、参数说明、返回值说明、异常说明（如有）、使用示例

## 4. 逻辑优化

### 4.1 条件处理
- 优先使用卫语句（Guard Clauses）提前返回，避免深层嵌套
  ```python
  # 推荐
  if not user:
      return None
  # 处理正常逻辑
  ```

### 4.2 分支优化
- 复杂分支使用 `match-case`（Python 3.10+）
- 使用字典调度替代复杂的 if-elif 链
  ```python
  handlers = {
      'create': handle_create,
      'update': handle_update,
      'delete': handle_delete
  }
  handler = handlers.get(action, handle_default)
  handler()
  ```

## 5. 日志与异常处理

### 5.1 日志规范
- 统一使用 `from xt_log import mylog`
- 合理使用日志级别：


### 5.2 异常处理
- 捕获特定异常，禁止使用裸 `except:`
- 记录详细上下文信息（函数名、参数值等）
- 适当情况下重新抛出异常
- 数据库操作必须有事务处理和异常回滚机制
- 确保资源正确释放

## 6. 开发环境与工具

### 6.1 环境要求
- Python 版本：3.13
- Ruff 版本：0.13.1
- 操作系统：Windows

### 6.2 自动化检查
- 配置 Ruff 预提交钩子
- 集成 CI/CD 自动化代码质量检查
- 编辑器配置支持规则检查

## 7. 代码示例

### 7.1 符合规范的示例
- 见：`D:/CODE/xjlib/template.py`

## 8. 代码提交前检查清单

- [ ] 通过 `ruff check --fix --unsafe-fixes`
- [ ] 类型注解完整且使用现代语法
- [ ] 命名语义化且符合规范
- [ ] 日志记录适当且统一
- [ ] 异常处理完善
- [ ] 文档字符串符合Google风格
- [ ] 符合单一职责原则
- [ ] 嵌套深度不超过3层

## 9. 更新记录

| 版本 | 日期 | 修改内容 | 修改人 |
|------|------|----------|--------|
| 1.0  | 2025-9-23 | 初始版本 | 系统 |

---

**注意**：本规范自发布之日起生效，所有新代码必须遵循此规范，现有代码应逐步重构以符合规范要求。