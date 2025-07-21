# Copilot 工作流系统 - AI 协作指令

> **项目**: 基于GitHub Copilot的全面工作流系统，专为系统化调试、文件整理和代码分析设计

## 📋 核心工作流

### 专业工作流系统

#### 🔍 调试工作流 - `debug-system/`

- **用途**: 系统性问题诊断和修复
- **模板**: `debug_workflow_template.md`
- **特点**: 6步调试循环，人工确认机制，结构化问题解决

#### 📁 文件整理工作流 - `file-organize-system/`

- **用途**: 项目文件系统化整理和清理
- **模板**: `file_organize_workflow_template.md`
- **特点**: 三大整理方式（优先级、类型、时间线导向）

#### 📊 分析工作流 - `analysis_system/`

- **用途**: 代码质量分析、性能评估、架构分析
- **模板**: `analysis_workflow_template.md`
- **特点**: 总-分-总结构，可量化分析，支持多轮深入

## 🔄 自动触发条件

### 调试工作流触发

**关键词**: debugging, error fixing, troubleshooting, bug resolution, code issues, 调试, 错误修复, 故障排除

**自动建议**: "我注意到您在进行调试工作。是否需要我启动系统化调试工作流？我可以创建结构化的调试会话文档来帮助组织故障排除过程。"

### 文件整理工作流触发

**关键词**: file organization, cleanup, directory restructure, file management, project organization, 文件整理, 清理, 目录重构

**自动建议**: "我看到您需要文件整理协助。是否需要我启动文件整理工作流？我可以帮助您使用优先级导向、类型导向或时间线导向的方式系统地整理文件。"

### 分析工作流触发

**关键词**: code analysis, code quality, performance optimization, technical debt, refactoring, architecture review, 代码分析, 质量评估

**自动建议**: "我看到您需要代码分析协助。是否需要我启动分析工作流？我可以帮助您系统地分析代码质量，识别技术债务，并提供优化建议。"

## 📁 工作流模板路径

- **调试模板**: `debug-system/debug_workflow_template.md`
- **整理模板**: `file-organize-system/file_organize_workflow_template.md`
- **分析模板**: `analysis_system/analysis_workflow_template.md`

## 🚨 强制性要求

### 文件编辑流程

- 编辑前必须使用 `read_file` 查看文件当前状态
- 使用 `replace_string_in_file` 时必须包含 3-5 行上下文确保唯一性
- 避免重复现有代码，使用 `...existing code...` 注释表示

### Git提交工作流程

- 严格遵循 `git-commit-workflow.md` 规范
- ❌ 禁止在逐文件审查前执行 `git add .`
- ❌ 禁止未 `git diff` 审查就提交
- ✅ 用户主导：仅在用户明确要求时提交
- ✅ 使用Conventional Commits格式：`feat:`, `fix:`, `docs:`, `refactor:`

### 工作流选择原则

**复杂问题诊断** → 使用 `debug-system/`
**代码质量分析** → 使用 `analysis_system/`
**文件整理清理** → 使用 `file-organize-system/`

### 终端环境

- **PowerShell**: 使用分号 `;` 连接命令，不要使用 `&&`
- 当执行终端命令时，在结尾额外增加一个换行符

## 💡 协作原则

- **优先遵循**本文件的工作流规范和模板约定
- **保持一致性**确保生成的文档符合项目的格式标准
- **模板优先**优先使用项目现有模板而非临时创建
- **结构化解决方案**对于复杂任务，主动建议使用标准化工作流程

### 命名约定

- 工作流文档: `*_workflow_*.md`
- 模板文件: `*-template.md`
- 指南文档: `README_*.md`

### 符号分类系统

- 🔴 核心文件/解决方案
- 📚 归档/重要里程碑
- 🗑️ 废弃/过时文件
- 📝 文档/分析说明
- 📋 日志/记录文件
- 🗂️ 其他支持文件

### 版本控制协作

**Git工作流约定**:

- 提交信息使用约定式提交格式
- 功能更新使用 `feat:` 前缀
- 文档更新使用 `docs:` 前缀
- 修复使用 `fix:` 前缀
- 重构使用 `refactor:` 前缀

当您为这个项目工作时，请遵循以上约定和模式，确保输出内容的一致性和专业性。优先使用项目的标准化工作流和模板系统，保持文档的结构化和可维护性。
