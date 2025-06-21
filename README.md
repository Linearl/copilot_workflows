# Debug Workflow Templates | 调试工作流程模板

A comprehensive debugging workflow template package for systematic problem-solving and code debugging.

> 完整的调试工作流模板包，用于系统化问题解决和代码调试。

## 📋 Table of Contents | 目录

- [Features](#-features--功能特点) 
- [Quick Start](#-quick-start--快速开始)
- [Project Structure](#-project-structure--项目结构)
- [Usage](#-usage--使用方法)
- [Templates](#-templates--模板资源)
- [Documentation](#-documentation--文档说明)
- [Contributing](#-contributing--贡献指南)
- [License](#-license--许可证)

## ✨ Features | 功能特点

- **Systematic Debugging Process** | **系统化调试流程**: 6-step debugging cycle for consistent problem-solving | 6步调试循环，确保问题解决的一致性
- **Template Collection** | **模板集合**: Pre-built templates for documentation and workflow management | 预构建的文档和工作流管理模板
- **Symbol Reference** | **符号参考**: Comprehensive symbol guide for project organization | 全面的项目组织符号指南
- **Human-AI Collaboration** | **人机协作**: Optimized workflow for AI-assisted debugging | 针对AI辅助调试优化的工作流
- **Modular Structure** | **模块化结构**: Organized file system for efficient debugging sessions | 有序的文件系统，提高调试会话效率

## 📁 Project Structure | 项目结构

```
debug-system/
├── workflow_template_v2.md          # Core V2 workflow template | V2核心工作流模板
├── templates/                       # Template collection | 模板集合
│   ├── README-template.md           # Debug session documentation | 调试会话文档模板
│   ├── summary-template.md          # Project summary template | 项目总结模板
│   ├── experience-template.md       # Experience summary template | 经验总结模板
│   ├── INDEX-template.md            # Debug index template | 调试索引模板
│   └── SUMMARY-TEMPLATE-UPDATE.md   # Updated summary template | 更新版总结模板
└── docs/
    └── 常用符号.md                   # Symbol reference guide | 符号参考指南
```

## 🚀 Quick Start | 快速开始

### 1. Clone the Repository | 克隆仓库

```bash
git clone https://github.com/Linearl/copilot_debug_workflow.git
cd copilot_debug_workflow
```

### 2. Create a New Debug Session | 创建新的调试会话

```powershell
# Copy the workflow template for your specific task | 为特定任务复制工作流模板
Copy-Item "debug-system\workflow_template_v2.md" "debug-system\workflow_[task-name]_v2.md"

# Initialize debug environment | 初始化调试环境
mkdir debug; cd debug; $round = 1
mkdir $round\{src,core,archive,deprecated,docs,logs,files}
Copy-Item "..\debug-system\templates\README-template.md" "$round\README.md"
```

## 🔄 Usage | 使用方法

### Workflow Document Usage | 工作流文档使用方法

The core functionality of this package is the **workflow template document** (`workflow_template_v2.md`). Here's how to use it effectively: | 此包的核心功能是**工作流模板文档** (`workflow_template_v2.md`)。以下是有效使用方法：

#### Step 1: Create Task-Specific Document | 步骤1：创建任务专用文档

```powershell
# Copy the template for your specific debugging task | 为特定调试任务复制模板
Copy-Item "debug-system\workflow_template_v2.md" "debug-system\workflow_[task-name]_v2.md"
```

**Example** | **示例**:
- `workflow_高DPI缩放问题_v2.md` (High DPI scaling issue)
- `workflow_数据库连接错误_v2.md` (Database connection error)
- `workflow_API响应超时_v2.md` (API timeout issue)

#### Step 2: Initialize Debug Environment | 步骤2：初始化调试环境

```powershell
# Create structured debug directory | 创建结构化调试目录
mkdir debug; cd debug; $round = 1
mkdir $round\{src,core,archive,deprecated,docs,logs,files}
Copy-Item "..\debug-system\templates\README-template.md" "$round\README.md"
```

#### Step 3: Follow the 7-Step Standard Process | 步骤3：遵循7步标准流程

The workflow template guides you through: | 工作流模板将引导您完成：

1. **Problem Description** | **问题描述**: Clearly describe the issue using structured format | 使用结构化格式清晰描述问题
2. **AI Analysis** | **AI分析**: Let AI parse and format the problem information | 让AI解析并格式化问题信息
3. **User Confirmation** | **用户确认**: Review and confirm AI's understanding | 检查并确认AI的理解
4. **Document Creation** | **文档创建**: Auto-generate task-specific workflow document | 自动生成任务专用工作流文档
5. **Environment Setup** | **环境设置**: Initialize organized debug workspace | 初始化有组织的调试工作空间
6. **Debug Iteration** | **调试迭代**: Execute structured debugging cycles | 执行结构化调试循环
7. **Documentation** | **文档记录**: Record results and organize files | 记录结果并整理文件

#### Step 4: Use the Debug Iteration Cycle | 步骤4：使用调试迭代循环

Within each debug session, follow the 6-step cycle: | 在每个调试会话中，遵循6步循环：

- 📋 **Plan** | **计划**: Define objectives | 确定目标
- 🔍 **Analyze** | **分析**: Investigate root causes | 调查根本原因  
- 💡 **Design** | **设计**: Create solution approach | 创建解决方案
- ⚙️ **Implement** | **实施**: Execute and test changes | 执行并测试更改
- ✅ **Verify** | **验证**: Confirm results | 确认结果
- 📊 **Document** | **记录**: Update documentation | 更新文档

### File Organization System | 文件组织系统

| Symbol | Directory | File Type | Storage Rule | 目录说明 | 文件类型 | 存储规则 |
|--------|-----------|-----------|--------------|----------|----------|----------|
| 🔴 | core/ | Core solutions | 5-10 key files | 核心解决方案 | 核心方案 | 5-10个关键文件 |
| 📚 | archive/ | Important milestones | Staged results | 重要里程碑 | 阶段性成果 | 重要调试历程 |
| 🗑️ | deprecated/ | Obsolete/replaced | Discarded files | 废弃/替换 | 废弃文件 | 无效或被替代文件 |
| 📝 | docs/ | Analysis documents | Documentation | 分析文档 | 说明文档 | 分析和说明文档 |
| 📋 | logs/ | Test logs | Runtime records | 测试日志 | 运行记录 | 测试和运行日志 |
| 🗂️ | files/ | Other files | Supporting files | 其他文件 | 支持文件 | 辅助和支持文件 |
| 🐍 | src/ | Working directory | Code and scripts during debugging | 工作目录 | 调试代码 | 调试过程中的代码和脚本 |

## 📚 Templates | 模板资源

The `debug-system/templates/` directory contains: | `debug-system/templates/` 目录包含：

- **README-template.md**: Standard template for debugging session documentation | 调试会话文档的标准模板
- **summary-template.md**: Project summary template for comprehensive reporting | 项目总结模板，用于全面报告
- **experience-template.md**: Experience summary template for lessons learned | 经验总结模板，用于记录经验教训
- **INDEX-template.md**: Debug index template for session organization | 调试索引模板，用于会话组织
- **SUMMARY-TEMPLATE-UPDATE.md**: Updated version of summary template | 总结模板的更新版本

## 📖 Documentation | 文档说明

### Symbol Reference | 符号参考

For detailed symbol reference, see `debug-system/docs/常用符号.md` which includes: | 详细的符号参考请查看 `debug-system/docs/常用符号.md`，包含：

- 🎯 Core symbol table: Common symbols and domain-specific symbols | 核心符号表：通用符号和主要功能域常用符号
- 📊 Complete symbol table: Comprehensive index of all project symbols | 完整符号表：项目中所有符号的全面索引
- 🎨 Usage guide: Best practices and usage standards | 使用指南：优秀案例和使用规范
- 📋 Workflow template symbol usage guide | 工作流模板符号使用指南
- 📑 Symbol quick reference | 符号速查表

## 🤝 Contributing | 贡献指南

We welcome contributions! Please feel free to submit issues and pull requests. | 我们欢迎贡献！请随时提交问题和拉取请求。

1. Fork the repository | 分叉仓库
2. Create your feature branch (`git checkout -b feature/amazing-feature`) | 创建功能分支
3. Commit your changes (`git commit -m 'Add some amazing feature'`) | 提交更改
4. Push to the branch (`git push origin feature/amazing-feature`) | 推送到分支
5. Open a Pull Request | 打开拉取请求

## 📄 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. | 此项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

**Created** | **创建时间**: June 21, 2025 | 2025年6月21日  
**Version** | **版本**: v2.0  
**Use Cases** | **适用场景**: Technical project debugging, problem troubleshooting, system optimization | 技术项目调试、问题排查、系统优化
