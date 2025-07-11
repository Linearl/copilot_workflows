# Copilot Workflow System | Copilot工作流系统

> 🌍 **Language Versions | 语言版本**: [English](README_en.md) | [中文](README_ch.md)

A comprehensive workflow system based on GitHub Copilot for systematic debugging and file organization.

> 基于GitHub Copilot的全面工作流系统，用于系统化调试和文件整理。

## 🎯 Core Philosophy | 核心理念

> **"Process as Tool, Tool as Leverage"** | **"流程即工具，工具即杠杆"**

*"New tools are not extensions of old methods, but declarations of new possibilities."* — Kevin Kelly

> *"新工具不是旧方法的延伸，而是新可能性的宣言。"* ——凯文·凯利

The essence of tools is **"reusable leverage"**, while processes are **"industrialized packaging of tools"**. As Kevin Kelly observed, *"The greatest invention of the past 200 years was not any specific tool, but the scientific method itself—a process that reliably produces innovation."*

> 工具的本质是「可复用的杠杆」**，而流程是**「工具的工业化封装」。正如凯文·凯利所言，*"过去200年来最伟大的发明并非具体的工具，而是科学方法本身——这种可靠地产生创新的流程"*。

This system embodies this philosophy by transforming debugging and file organization from ad-hoc activities into **systematic, replicable processes** that serve as powerful leverage tools for AI-assisted development.

> 本系统体现了这一理念，将调试和文件整理从临时性活动转化为**系统化、可复制的流程**，成为AI辅助开发的强大杠杆工具。

**💡 Extend and Customize** | **💡 扩展与定制**: You can leverage these existing workflows as templates to develop your own specialized workflows with Copilot's assistance, then iteratively optimize them through practice.

> **💡 扩展与定制**: 您可以利用这些现有工作流作为模板，借助Copilot的帮助开发自己的专门工作流，然后在实践中逐步调优。

## 🚀 Why Use Workflows | 使用工作流的优势

### 🎯 Enhanced Focus and Context Management | 增强专注力与上下文管理

Workflows have been extensively tested and optimized to help AI models maintain focus on objectives and automatically preserve context during complex task execution. This structured approach prevents AI from losing track of the original goals while navigating through multi-step processes.

> 工作流经过充分的测试和调优，可以让AI模型在完成复杂工作的过程中，专注目标并自动维护上下文。这种结构化方法防止AI在多步骤过程中偏离原始目标。

### 💰 Optimized Request Efficiency | 优化请求效率

Using workflows can significantly reduce the number of interactions with Copilot, enabling single requests to accomplish more comprehensive work. This efficiency translates directly into cost savings by reducing the consumption of premium request quotas.

> 使用工作流可以有效减少和Copilot的交互次数，让单次请求可以完成更多工作，进而节约高级请求次数，带来直接的成本效益。

### 🔄 Systematic Reproducibility | 系统化可重现性

Workflows ensure consistent results across different sessions and users, transforming ad-hoc problem-solving into reliable, repeatable processes that can be refined and improved over time.

> 工作流确保在不同会话和用户间获得一致的结果，将临时性问题解决转化为可靠、可重复的流程，并能够随时间不断完善和改进。

## 🎯 Core Workflows | 核心工作流

This system provides two main workflows designed for AI-assisted development:

> 本系统提供两个主要工作流，专为AI辅助开发设计：

### 1. Debug Workflow | 调试工作流

**Template**: `debug-system/debug_workflow_template.md`**Description**: Systematic debugging process with 6-step debugging cycle for consistent problem-solving.

> **模板**: `debug-system/debug_workflow_template.md`
> **说明**: 系统化调试流程，采用6步调试循环确保问题解决的一致性。

**Documentation**: [Debug Workflow Guide (中文)](README_debug_ch.md) | [Debug Workflow Guide (English)](README_debug_en.md)

### 2. File Organization Workflow | 文件整理工作流

**Template**: `file-organize-system/file_organize_workflow_template.md`**Description**: Comprehensive file organization system with three major organization approaches and systematic cleanup procedures.

> **模板**: `file-organize-system/file_organize_workflow_template.md`
> **说明**: 全面的文件整理系统，包含三大整理方式和系统化清理流程。

**Documentation**: [File Organization Guide (中文)](README_file_organize_ch.md) | [File Organization Guide (English)](README_file_organize_en.md)

## 📋 Table of Contents | 目录

- [Features](#-features--功能特点)
- [Quick Start](#-quick-start--快速开始)
- [Project Structure](#-project-structure--项目结构)
- [Agent Configuration](#-agent-configuration-recommendations--agent配置建议)
- [File Organization System](#-file-organization-system--文件组织系统)
- [Templates](#-templates--模板资源)
- [Documentation](#-documentation--文档说明)
- [Contributing](#-contributing--贡献指南)
- [License](#-license--许可证)

## ✨ Features | 功能特点

### Debug Workflow Features | 调试工作流功能

- **Systematic Debugging Process** | **系统化调试流程**: 6-step debugging cycle for consistent problem-solving | 6步调试循环，确保问题解决的一致性
- **Official Documentation Verification** | **官方文档验证法**: New core methodology using fetch_webpage tool to verify API usage | 新增核心方法论，使用fetch_webpage工具验证API用法
- **Human-AI Collaboration** | **人机协作**: Optimized workflow for AI-assisted debugging | 针对AI辅助调试优化的工作流
- **Template Collection** | **模板集合**: Pre-built templates for documentation and workflow management | 预构建的文档和工作流管理模板

### File Organization Features | 文件整理工作流功能

- **Three Organization Approaches** | **三大整理方式**: Priority-based, Type-based, and Timeline-based organization | 优先级导向、类型导向、时间线导向整理
- **Systematic Cleanup Process** | **系统化清理流程**: Comprehensive file cleanup and archiving procedures | 全面的文件清理和归档流程
- **Symbol-Based Classification** | **符号分类系统**: Comprehensive symbol guide for project organization | 全面的项目组织符号指南

### Shared Features | 共享功能

- **Modular Structure** | **模块化结构**: Organized file system for efficient workflow sessions | 有序的文件系统，提高工作流会话效率
- **Multi-language Support** | **多语言支持**: Comprehensive Chinese and English documentation | 全面的中英文文档支持

## 📁 Project Structure | 项目结构

```
copilot_debug_workflow/
├── debug-system/                        # Debug workflow supporting files | 调试工作流支持文件
│   ├── debug_workflow_template.md       # Debug workflow template | 调试工作流模板
│   ├── templates/                       # Debug template collection | 调试模板集合
│   │   ├── README-template.md           # Debug session documentation | 调试会话文档模板
│   │   ├── summary-template.md          # Project summary template | 项目总结模板
│   │   ├── experience-template.md       # Experience summary template | 经验总结模板
│   │   ├── INDEX-template.md            # Debug index template | 调试索引模板
│   │   ├── bug-list-template.md         # Bug list template | Bug清单模板
│   │   └── bug-report-template.md       # Bug report template | Bug报告模板
│   ├── buglist/                         # Bug management directory | Bug管理目录
│   │   ├── to_fix/                      # Bugs to be fixed | 待修复Bug
│   │   └── fixed/                       # Fixed bugs | 已修复Bug
│   ├── debug/                           # Debug working directory | 调试工作目录
│   │   └── workflow_archive/            # Archived workflow documents | 工作流文档存档
│   └── docs/
│       └── 常用符号.md                   # Symbol reference guide | 符号参考指南
├── file-organize-system/                # File organization workflow supporting files | 文件整理工作流支持文件
│   ├── file_organize_workflow_template.md # File organization workflow template | 文件整理工作流模板
│   ├── templates/                       # File organization template collection | 文件整理模板集合
│   │   ├── analysis-template.md         # Analysis template | 分析模板
│   │   ├── directory-templates.md       # Directory structure templates | 目录结构模板
│   │   ├── plan-template.md             # Planning template | 计划模板
│   │   └── summary-report-template.md   # Summary report template | 总结报告模板
│   ├── tools/                           # Organization tools and utilities | 整理工具和实用程序
│   ├── organize/                        # Organization task working directory | 整理任务工作目录
│   └── version.md                       # Version history | 版本历史
├── README_debug_ch.md                   # Debug workflow Chinese guide | 调试工作流中文指南
├── README_debug_en.md                   # Debug workflow English guide | 调试工作流英文指南
├── README_file_organize_ch.md           # File organization Chinese guide | 文件整理工作流中文指南
├── README_file_organize_en.md           # File organization English guide | 文件整理工作流英文指南
└── LICENSE                              # License file | 许可证文件
```

## 🚀 Quick Start | 快速开始

### 1. Clone the Repository | 克隆仓库

```bash
git clone https://github.com/Linearl/copilot_debug_workflow.git
cd copilot_debug_workflow
```

### 2. Enable Copilot Agent Mode | 启用Copilot Agent模式

1. **Enable Agent Mode** | **启用Agent模式**: Use `@workspace` or agent commands in VS Code | 在VS Code中使用 `@workspace`或agent命令
2. **Start Workflow Session** | **开始工作流会话**: Follow the guidance in the workflow document | 按照工作流文档中的指引进行

## 🔀 Choose Your Workflow Approach | 选择工作流方式

After completing steps 1-2, you have two options to proceed: | 完成步骤1-2后，您有两种方式继续：

---

## 📋 Option A: Manual Workflow | 方式A：手动工作流

### 3A. Open Workflow Template in VS Code | 在VS Code中打开工作流模板

```powershell
# For debugging tasks | 调试任务
code debug-system/debug_workflow_template.md

# For file organization tasks | 文件整理任务  
code file-organize-system/file_organize_workflow_template.md
```

> **📝 Note** | **说明**: These are template files. The actual workflow documents will be automatically generated when you start the workflow process. | 这些是模板文件。实际的工作流文档会在开始工作流程时自动生成。

### 4A. Describe Your Task and Start Working | 描述任务并开始工作

Simply describe your problem or organization task in natural language - the workflow will handle the parsing and formatting automatically: | 只需用自然语言描述你的问题或整理任务 - 工作流会自动处理解析和格式化：

---

## ⚡ Option B: Auto-Trigger Workflow | 方式B：自动触发工作流

### 3B. Configure Auto-Trigger | 配置自动触发

Create a `.copilot-instructions.md` file in your project root to enable automatic workflow triggering: | 在项目根目录创建 `.copilot-instructions.md`文件来启用自动工作流触发：

```markdown
# Copilot Workflow Instructions

## Auto-Trigger Conditions | 自动触发条件

### For Debug Workflow | 调试工作流触发
When user mentions: debugging, error fixing, troubleshooting, bug resolution, code issues
Automatically suggest: "I notice you're working on debugging. Would you like me to start the systematic debug workflow? I can create a structured debugging session document to help organize the troubleshooting process."

### For File Organization Workflow | 文件整理工作流触发  
When user mentions: file organization, cleanup, directory restructure, file management, project organization
Automatically suggest: "I see you need file organization assistance. Would you like me to start the file organization workflow? I can help you systematically organize files using priority-based, type-based, or timeline-based approaches."

## Workflow Templates | 工作流模板
- Debug Template: `debug-system/debug_workflow_template.md`
- File Organization Template: `file-organize-system/file_organize_workflow_template.md`
```

### 4B. Natural Language Interaction | 自然语言交互

Once configured, simply mention your needs in conversation - AI will automatically suggest the appropriate workflow: | 配置完成后，只需在对话中提及您的需求 - AI会自动建议合适的工作流：

**Example triggers** | **触发示例**:

- "I need to debug this error..." → Debug workflow suggestion
- "I want to organize these files..." → File organization workflow suggestion

---

## 📋 Workflow Execution Details | 工作流执行详情

### For Debug Workflow | 调试工作流流程

> **📄 Working Document** | **工作文档**: Created in `debug-system/debug_workflow_[task-name].md` | 在 `debug-system/debug_workflow_[任务名].md` 中创建

1. **Problem Description** | **问题描述**: Describe your debugging issue naturally | 自然地描述你的调试问题
2. **AI Analysis** | **AI分析**: Let the agent parse and understand your problem | 让agent解析并理解你的问题
3. **User Confirmation** | **用户确认**: Review and confirm the agent's understanding | 检查并确认agent的理解
4. **Document Creation** | **文档创建**: Agent creates task-specific workflow document | Agent创建任务专用工作流文档
5. **Environment Setup** | **环境设置**: Initialize organized debug workspace | 初始化有组织的调试工作空间
6. **Debug Iteration** | **调试迭代**: Execute structured debugging cycles | 执行结构化调试循环
7. **Documentation** | **文档记录**: Record results and organize files | 记录结果并整理文件

### For File Organization Workflow | 文件整理工作流流程

> **📄 Working Document** | **工作文档**: Created in `organize/[task-name]/file_organize_workflow_[task-name].md` | 在 `organize/[任务名]/file_organize_workflow_[任务名].md` 中创建

1. **Task Analysis** | **任务分析**: Analyze the scope and requirements of file organization | 分析文件整理的范围和需求
2. **Approach Selection** | **方法选择**: Choose from three organization approaches | 从三种整理方式中选择
3. **Environment Setup** | **环境设置**: Initialize organized workspace structure | 初始化有组织的工作空间结构
4. **Systematic Organization** | **系统化整理**: Execute the chosen organization approach | 执行选定的整理方法
5. **Cleanup and Archiving** | **清理和归档**: Remove redundant files and archive important ones | 清理多余文件并归档重要文件
6. **Documentation** | **文档记录**: Document the organization process and results | 记录整理过程和结果

## 🤖 Agent Configuration Recommendations | Agent配置建议

### Model and Settings | 模型和设置

- **Preferred Model** | **推荐模型**: Use Claude 4.0 for best results | 使用Claude 4.0以获得最佳效果
- **Enable Thinking Mode** | **启用思考模式**: Turn on agent thinking mode for better analysis | 开启agent思考模式以获得更好的分析
- **Terminal Access** | **终端访问权限**: Configure and enable terminal usage permissions | 配置并启用终端使用权限

### Budget and Control | 预算和控制

- **Request Budget** | **请求预算**: Set agent call budget to 10-20 requests per session | 将每次会话的agent调用预算设置为10-20次
- **Budget Warning** | **预算警告**: Too many requests may cause the agent to drift off-topic | 过多的请求可能导致agent偏离主题
- **Active Monitoring** | **主动监控**: Monitor agent progress and intervene when necessary | 监控agent进度，必要时进行干预

### Best Practices | 最佳实践

⚠️ **Important** | **重要提示**: If you notice the agent drifting off-topic or have new ideas, **pause immediately** and provide additional instructions. | 如果发现agent跑偏或有新的思路，请**立即暂停**并补充新指令。

- **Stay Engaged** | **保持参与**: Actively review agent's analysis and suggestions | 积极审查agent的分析和建议
- **Provide Feedback** | **提供反馈**: Give clear feedback on agent's direction | 就agent的方向给出明确反馈
- **Course Correction** | **纠正方向**: Don't hesitate to redirect when agent goes off-track | 当agent偏离轨道时不要犹豫进行重定向

## 📊 File Organization System | 文件组织系统

### Debug Workflow Organization | 调试工作流组织

| Symbol | Directory   | File Type            | Storage Rule                      | 目录说明     | 文件类型   | 存储规则               |
| ------ | ----------- | -------------------- | --------------------------------- | ------------ | ---------- | ---------------------- |
| 🔴     | core/       | Core solutions       | 5-10 key files                    | 核心解决方案 | 核心方案   | 5-10个关键文件         |
| 📚     | archive/    | Important milestones | Staged results                    | 重要里程碑   | 阶段性成果 | 重要调试历程           |
| 🗑️   | deprecated/ | Obsolete/replaced    | Discarded files                   | 废弃/替换    | 废弃文件   | 无效或被替代文件       |
| 📝     | docs/       | Analysis documents   | Documentation                     | 分析文档     | 说明文档   | 分析和说明文档         |
| 📋     | logs/       | Test logs            | Runtime records                   | 测试日志     | 运行记录   | 测试和运行日志         |
| 🗂️   | files/      | Other files          | Supporting files                  | 其他文件     | 支持文件   | 辅助和支持文件         |
| 🐍     | src/        | Working directory    | Code and scripts during debugging | 工作目录     | 调试代码   | 调试过程中的代码和脚本 |

### File Organization Workflow System | 文件整理工作流系统

| Symbol | Directory   | Organization Type | Storage Rule                   | 目录说明   | 整理类型           | 存储规则         |
| ------ | ----------- | ----------------- | ------------------------------ | ---------- | ------------------ | ---------------- |
| ⭐     | priority/   | Priority-based    | High/Medium/Low priority files | 优先级导向 | 高/中/低优先级文件 | 按重要性分类     |
| 📁     | type/       | Type-based        | By file type and format        | 类型导向   | 按文件类型和格式   | 按格式分类       |
| 📅     | timeline/   | Timeline-based    | By creation/modification time  | 时间线导向 | 按创建/修改时间    | 按时间分类       |
| 🔴     | core/       | Core files        | Essential project files        | 核心文件   | 项目核心文件       | 5-10个关键文件   |
| 📚     | archive/    | Archive           | Historical versions            | 归档       | 历史版本           | 重要历史文件     |
| 🗑️   | deprecated/ | Deprecated        | Obsolete files                 | 废弃       | 过时文件           | 无效或被替代文件 |

## 📚 Templates | 模板资源

### Debug System Templates | 调试系统模板

The `debug-system/templates/` directory contains: | `debug-system/templates/` 目录包含：

- **README-template.md**: Standard template for debugging session documentation | 调试会话文档的标准模板
- **summary-template.md**: Project summary template for comprehensive reporting | 项目总结模板，用于全面报告
- **experience-template.md**: Experience summary template for lessons learned | 经验总结模板，用于记录经验教训
- **INDEX-template.md**: Debug index template for session organization | 调试索引模板，用于会话组织

### File Organization System Templates | 文件整理系统模板

The `file-organize-system/templates/` directory contains: | `file-organize-system/templates/` 目录包含：

- **analysis-template.md**: Template for file analysis and assessment | 文件分析和评估模板
- **directory-templates.md**: Directory structure templates for different organization approaches | 不同整理方法的目录结构模板
- **plan-template.md**: Planning template for organization tasks | 整理任务计划模板
- **summary-report-template.md**: Comprehensive summary report template | 综合总结报告模板

## 📖 Documentation | 文档说明

### Main Documentation | 主要文档

- **Debug Workflow Documentation** | **调试工作流文档**:

  - [中文说明](README_debug_ch.md): 详细的调试工作流中文说明
  - [English Guide](README_debug_en.md): Comprehensive debug workflow English guide
- **File Organization Documentation** | **文件整理工作流文档**:

  - [中文说明](README_file_organize_ch.md): 详细的文件整理工作流中文说明
  - [English Guide](README_file_organize_en.md): Comprehensive file organization English guide

### Symbol Reference | 符号参考

For detailed symbol reference, see `debug-system/docs/常用符号.md` which includes: | 详细的符号参考请查看 `debug-system/docs/常用符号.md`，包含：

- 🎯 Core symbol table: Common symbols and domain-specific symbols | 核心符号表：通用符号和主要功能域常用符号
- 📊 Complete symbol table: Comprehensive index of all project symbols | 完整符号表：项目中所有符号的全面索引
- 🎨 Usage guide: Best practices and usage standards | 使用指南：优秀案例和使用规范
- 📋 Workflow template symbol usage guide | 工作流模板符号使用指南
- 📑 Symbol quick reference | 符号速查表

### Version History | 版本历史

For detailed version history and change logs, see `file-organize-system/version.md` which includes: | 详细的版本历史和变更日志请查看 `file-organize-system/version.md`，包含：

- 📝 Version tracking: Complete history of template and system changes | 版本跟踪：模板和系统变更的完整历史
- 🔄 Refactoring notes: Documentation of major structural changes | 重构说明：主要结构变更的文档记录
- 🎯 Feature updates: New functionality and improvement records | 功能更新：新功能和改进记录

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
**Last Updated** | **最后更新**: July 10, 2025 | 2025年7月10日
**Version** | **版本**: v2.2
**Use Cases** | **适用场景**: Technical project debugging, problem troubleshooting, system optimization, file organization, project cleanup | 技术项目调试、问题排查、系统优化、文件整理、项目清理

**v2.2 Updates** | **v2.2 更新内容**:

- Added Official Documentation Verification Method to debug workflow | 调试工作流新增官方文档验证法
- Enhanced API usage verification with fetch_webpage tool | 增强API使用验证功能，使用fetch_webpage工具
- Updated all README documentation | 更新所有README文档
