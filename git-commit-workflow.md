# Git 提交工作流规范

## 1. 概述

本规范为标准的Git提交工作流。所有贡献者都必须遵循此流程，以确保代码库的提交历史清晰、可追溯，并且每一次变更都经过了充分的审查。

## 2. 核心原则

- **清晰性**: 提交信息应清晰地说明“做了什么”和“为什么做”。
- **原子性**: 每次提交应只包含一个逻辑上独立的变更单元。
- **可追溯性**: 任何代码变更都应能轻松追溯到其原因和相关讨论。

## 3. 强制性提交流程

在执行任何 `git commit` 操作之前，**必须严格遵循**以下步骤。

### 步骤 1: 检查工作区状态

在开始提交过程前，首先检查当前工作区的状态，了解哪些文件被修改、暂存或未跟踪。

```bash
git status
```

### 步骤 2: 详细审查文件变更

对每一个被修改的文件，使用 `git diff` 命令进行详细审查，以准确了解每一行代码的变更。
注：由ui文件生成的py文件除外（这部分文件名通常以"_window.py"结尾），你应该查看ui文件的变更而不是生成的py文件。

```bash
# 审查所有变更
git diff

# 或审查单个文件的变更
git diff path/to/your/file.py
```

**关键要求**: **禁止**在未完全理解代码变更内容的情况下进行提交。

### 步骤 3: 编写规范的提交信息

我们遵循 **Conventional Commits** 规范来格式化提交信息。这有助于自动化生成更新日志和更好地管理项目历史。

**格式:**

```
<类型>[可选的作用域]: <主题>

[可选的正文]

[可选的页脚]
```

**常用类型:**

- `feat`: 新增功能。
- `fix`: 修复Bug。
- `docs`: 只修改了文档。
- `style`: 代码风格的调整（不影响代码逻辑，如格式化）。
- `refactor`: 代码重构（既不是新增功能，也不是修复Bug）。
- `perf`: 提升性能的修改。
- `test`: 新增或修改测试。
- `chore`: 构建流程、辅助工具等非业务代码的变更。

**示例:**

- **新增功能**: `feat(gui): 添加统计信息面板的刷新按钮`
- **修复Bug**: `fix(encoding): 修复处理GBK编码文件时的解码错误`
- **文档修改**: `docs(workflow): 更新AI手动分类工作流文档`

### 步骤 4: 执行提交

完成以上步骤后，将文件添加到暂存区并执行提交。

```bash
# 添加所有变更的文件
git add .

# 或者添加指定文件
git add path/to/your/file.py

# 执行提交，并使用-m标志提供提交信息
git commit -m "feat(core): 实现新的关键词匹配算法"
```

## 4. 临时变更记录 (可选)

对于复杂的提交，开发者可能会发现在提交前使用一个临时文件来组织思路和记录变更会很有帮助。`commit.md` 文件可用于此目的。

### `commit.md` 使用指南

1. **创建与编辑**: 在提交前，创建一个 `commit.md` 文件，记录下每个文件的变更详情、原因和影响。
2. **辅助审查**: 在 `git commit` 之前，回顾 `commit.md` 的内容，确保没有遗漏任何重要信息。
3. **清理**: `commit.md` **永远不应**被提交到版本库中。它只是一个临时的草稿文件。请确保在 `git add .` 之前，它已被删除或被添加到 `.gitignore` 文件中。

**`commit.md` 模板示例:**

```markdown
# 本次提交变更草稿

## 目标

- 优化文件导入流程，提高处理速度。

## 文件变更

- `workflows/file_import.py`
  - **变更**: 重构了 `process_file` 函数，使用多线程处理IO操作。
  - **原因**: 旧的单线程实现处理大量小文件时速度很慢。
- `gui/panels/import_panel.py`
  - **变更**: 调整了UI，增加了取消导入操作的按钮。
  - **原因**: 为用户提供更灵活的控制。

## 待办

- [x] 编写单元测试覆盖新的多线程逻辑。
- [ ] 更新相关流程文档。
```

## 5. 最佳实践

- **小步快跑**: 尽量保持提交的粒度小，一个提交只做一件事。
- **先拉后推**: 在推送到远程仓库前，先执行 `git pull --rebase`，确保本地分支基于最新的远程分支，避免不必要的合并冲突。
- **代码审查**: 鼓励通过Pull Request (PR) / Merge Request (MR) 的方式进行代码审查，这是保证代码质量的重要环节。

---

*最后更新: 2025-06-28*
*版本: 2.0*
