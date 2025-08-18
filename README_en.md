# Copilot Workflow System

> 🌍 **Language Versions**: [English](README_en.md) | [中文](README.md)

A comprehensive workflow system based on GitHub Copilot for systematic debugging, file organization, code analysis, refactoring, and version comparison.

## 🎯 Core Philosophy

> **"Process as Tool, Tool as Leverage"**

*"New tools are not extensions of old methods, but declarations of new possibilities."* — Kevin Kelly

The essence of tools is **"reusable leverage"**, while processes are **"industrialized packaging of tools"**. As Kevin Kelly observed, *"The greatest invention of the past 200 years was not any specific tool, but the scientific method itself—a process that reliably produces innovation."*

This system embodies this philosophy by transforming debugging, file organization, and code analysis from ad-hoc activities into **systematic, replicable processes** that serve as powerful leverage tools for AI-assisted development.

**💡 Extend and Customize**: You can leverage these existing workflows as templates to develop your own specialized workflows with Copilot's assistance, then iteratively optimize them through practice.

## 🚀 Why Use Workflows

### 🎯 Enhanced Focus and Context Management

Workflows have been extensively tested and optimized to help AI models maintain focus on objectives and automatically preserve context during complex task execution. This structured approach prevents AI from losing track of the original goals while navigating through multi-step processes.

### 💰 Optimized Request Efficiency

Using workflows can significantly reduce the number of interactions with Copilot, enabling single requests to accomplish more comprehensive work. This efficiency translates directly into cost savings by reducing the consumption of premium request quotas.

### 🔄 Systematic Reproducibility

Workflows ensure consistent results across different sessions and users, transforming ad-hoc problem-solving into reliable, repeatable processes that can be refined and improved over time.

## 🎯 Core Workflows

The system provides six primary workflows designed for AI-assisted development:

### 1. Debug Workflow

**Template**: `debug-system/debug_workflow_template.md`
**Description**: Systematic debugging process with 6-step debugging cycle for consistent problem-solving.

**Features**:
- Structured problem-solving approach
- Reproducible debugging methods
- Comprehensive documentation system
- Human verification checkpoints

### 2. File Organization Workflow

**Template**: `file-organize-system/file_organize_workflow_template.md`
**Description**: Comprehensive file organization system with three major organization approaches and systematic cleanup processes.

**Features**:
- Priority-driven organization
- Type-based classification
- Timeline-oriented sorting
- Systematic cleanup processes
- Symbol-based file management

### 3. Analysis Workflow

**Template**: `analysis_system/analysis_workflow_template.md`
**Description**: Comprehensive code analysis and quality assessment system using multi-dimensional analysis methods for technical debt identification, performance optimization, and refactoring guidance.

**Features**:
- Multi-dimensional code analysis
- Automated tools and metrics collection
- Systematic report generation
- Template-driven processes

### 4. Refactor Workflow

**Template**: `refactor_system/refactor_workflow_template.md`
**Description**: Systematic refactoring workflow based on code analysis results, featuring three-tier planning management and dual-loop execution mechanisms.

**Features**:
- Three-tier planning system (Overall → Phase → Implementation)
- P0-P3 priority-driven phase management
- Dual-loop control (Phase-level + Modification-point-level)
- Visual flowchart guidance
- Risk control and rollback mechanisms

### 5. Version Comparison Workflow

**Template**: `version-comparison-system/version-comparison-workflow-template.md`
**Description**: Structured workflow for multi-version differential analysis, supporting Git worktree isolation, modular phase analysis, and version report generation.

**Features**:
- Three-stage layered analysis (Overview → Module → Documentation)
- Bottom-up module ordering (tools → logic → algorithm)
- Git diff statistics and commit classification
- Workflow template-driven recording and reporting
- Update log supplementation and upgrade guidance output

### 6. Workflow Builder

**Template**: `workflow-builder-system/workflow_builder_template.md`
**Description**: Intelligent workflow construction system based on IPD Integrated Product Development methodology, guiding new workflow design through AI.

**Features**:

- **AI-guided requirement clarification**: Complete requirement collection in 3-5 rounds of dialogue
- **IPD 6-stage gate control**: Concept → Analysis → Conceptual Design → Detailed Design → Development & Build → Quality Verification
- **24 design pattern library**: Reusable design patterns extracted from existing workflows
- **Plugin-based verification system**: Assessment of completeness, usability, maintainability, documentation quality, and extensibility
- **Three complexity options**: Lightweight/Standard/Professional levels for different skill levels


## 📁 Project Structure

```text
copilot_workflows/
├── debug-system/                        # Debug workflow supporting files
│   ├── debug_workflow_template.md       # Debug workflow template
│   ├── README.md                        # Debug system documentation (Chinese)
│   ├── README_en.md                     # Debug system documentation (English)
│   ├── templates/                       # Debug template collection
│   ├── docs/                           # Symbol reference guides
│   └── buglist/                        # Bug tracking and resolution archive
├── file-organize-system/                # File organization workflow supporting files
│   ├── file_organize_workflow_template.md # File organization workflow template
│   ├── README.md                        # File organization documentation (Chinese)
│   ├── README_en.md                     # File organization documentation (English)
│   ├── templates/                       # Organization template collection
│   ├── docs/                           # Operation guides and best practices
│   ├── tools/                          # Organization tools and utilities
│   ├── organize/                       # Organization task working directory
│   └── version.md                      # Version history
├── analysis_system/                     # Code analysis workflow supporting files
│   ├── analysis_workflow_template.md    # Analysis workflow template
│   ├── README.md                        # Analysis system documentation (Chinese)
│   ├── README_en.md                     # Analysis system documentation (English)
│   ├── templates/                       # Analysis template collection
│   ├── tools/                          # Analysis tools and utilities
│   ├── tasks/                          # Analysis task archive directory
│   ├── docs/                           # Analysis documentation
│   └── case-studies/                   # Analysis case studies
├── refactor_system/                     # Refactor workflow supporting files
│   ├── refactor_workflow_template.md    # Refactor workflow template
│   ├── README.md                        # Refactor system documentation (Chinese)
│   ├── README_en.md                     # Refactor system documentation (English)
│   ├── templates/                       # Refactor template collection
│   ├── tools/                          # Refactor tools and utilities
│   ├── docs/                           # Refactor documentation
│   └── case-studies/                   # Refactor case studies
├── version-comparison-system/           # Version comparison workflow supporting files
│   ├── version-comparison-workflow-template.md
│   ├── README.md                        # Version comparison documentation (Chinese)
│   ├── README_en.md                     # Version comparison documentation (English)
│   ├── templates/                       # Version comparison template collection
│   ├── analysis/                        # Version analysis working directory
│   └── scripts/                        # Version comparison tools
├── workflow-builder-system/             # Workflow builder supporting files
│   ├── workflow_builder_template.md     # Workflow builder template
│   ├── README.md                        # Workflow builder documentation (Chinese)
│   ├── README_en.md                     # Workflow builder documentation (English)
│   ├── config.yaml                      # System configuration file
│   ├── templates/                       # Builder template collection
│   ├── tools/                          # Building tools and utilities
│   ├── docs/                           # Builder documentation and design patterns
│   ├── builds/                         # Generated workflow output directory
│   ├── develop/                        # Development workspace
│   └── logs/                           # Build logs and history
├── .copilot-instructions.md             # Copilot AI collaboration instructions
├── git-commit-workflow.md               # Git commit workflow specification
├── README.md                            # Main documentation (Chinese)
├── README_en.md                         # English documentation
├── update_log.md                        # Version update log
└── LICENSE                              # MIT License
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Linearl/copilot_workflows.git
cd copilot_workflows
```

### 2. Enable Copilot Agent Mode

Configure your VS Code Copilot to use agent mode for optimal workflow support.

### 3. Choose Your Approach

You can use workflows in two ways:

## ⚡ Option A: Manual Workflow

### 3A. Direct Template Usage

Open the appropriate workflow template in VS Code:

```bash
# For debugging tasks
code debug-system/debug_workflow_template.md

# For file organization tasks
code file-organize-system/file_organize_workflow_template.md

# For code analysis tasks
code analysis_system/analysis_workflow_template.md

# For refactor tasks
code refactor_system/refactor_workflow_template.md

# For version comparison tasks
code version-comparison-system/version-comparison-workflow-template.md

# For building new workflows
code workflow-builder-system/workflow_builder_template.md
```

> **📝 Note**: These are template files. The actual workflow documents will be automatically generated when you start the workflow process.

### 4A. Natural Language Interaction

Simply describe your problem or task in natural language - the workflow will handle the parsing and formatting automatically.

## ⚡ Option B: Auto-Trigger Workflow

### 3B. Configure Auto-Trigger

#### Step 1: Create Instructions File

Create a `.github/copilot-instructions.md` file in your project to enable automatic workflow triggering:

#### Step 2: Configure VS Code Settings

Add the following configuration to your VS Code `settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {"file": ".github/copilot-instructions.md"}
  ]
}
```

#### Step 3: Instructions File Content

```markdown
# Copilot Workflow Instructions

## Auto-Trigger Conditions

### For Debug Workflow
When user mentions: debugging, error fixing, troubleshooting, bug resolution, code issues
Automatically suggest: "I notice you're working on debugging. Would you like me to start the systematic debug workflow? I can create a structured debugging session document to help organize the troubleshooting process."

### For File Organization Workflow
When user mentions: file organization, cleanup, directory restructure, file management, project organization
Automatically suggest: "I see you need file organization assistance. Would you like me to start the file organization workflow? I can help you systematically organize files using priority-based, type-based, or timeline-based approaches."

### For Analysis Workflow
When user mentions: code analysis, code quality, performance optimization, technical debt, refactoring, architecture review
Automatically suggest: "I see you need code analysis assistance. Would you like me to start the analysis workflow? I can help you systematically analyze code quality, identify technical debt, and provide optimization recommendations."

### For Refactor Workflow
When user mentions: code refactoring, system refactoring, architecture improvement, code restructuring, refactor plan
Automatically suggest: "I see you need code refactoring assistance. Would you like me to start the refactor workflow? I can help you develop systematic refactoring plans based on analysis results and safely execute refactoring tasks."

### For Version Comparison Workflow
When user mentions: version comparison, diff analysis, change tracking, version control, git diff
Automatically suggest: "I see you need version comparison assistance. Would you like me to start the version comparison workflow? I can help you systematically analyze differences between code versions, track changes, and generate comprehensive reports."

### For Workflow Builder
When user mentions: workflow design, workflow building, custom workflow, workflow development, workflow creation
Automatically suggest: "I see you need workflow building assistance. Would you like me to start the workflow builder? I can help you design and create custom workflows using IPD methodology and our 24 design pattern library."

## Workflow Templates
- Debug Template: `debug-system/debug_workflow_template.md`
- File Organization Template: `file-organize-system/file_organize_workflow_template.md`
- Analysis Template: `analysis_system/analysis_workflow_template.md`
- Refactor Template: `refactor_system/refactor_workflow_template.md`
- Version Comparison Template: `version-comparison-system/version-comparison-workflow-template.md`
- Workflow Builder Template: `workflow-builder-system/workflow_builder_template.md`
```

### 4B. Natural Language Interaction

Once configured, simply mention your needs in conversation - AI will automatically suggest the appropriate workflow:

**Example triggers**:

- "I need to debug this error..." → Debug workflow suggestion
- "I want to organize these files..." → File organization workflow suggestion
- "I need to analyze this code quality..." → Analysis workflow suggestion
- "I need to refactor this project..." → Refactor workflow suggestion
- "I want to compare these versions..." → Version comparison workflow suggestion
- "I want to create a custom workflow..." → Workflow builder suggestion

## 📋 Workflow Execution Details

### For Debug Workflow

> **📄 Working Document**: Created in `debug-system/debug_workflow_[task-name].md`

1. **Problem Description**: Describe your debugging issue naturally
2. **AI Analysis**: Let the agent parse and understand your problem
3. **User Confirmation**: Review and confirm the agent's understanding
4. **Document Creation**: Agent creates task-specific workflow document
5. **Environment Setup**: Initialize organized debug workspace
6. **Debug Iteration**: Execute structured debugging cycles
7. **Documentation**: Record results and organize files

### For File Organization Workflow

> **📄 Working Document**: Created in `file-organize-system/file_organize_workflow_[task-name].md`

1. **Organization Goals**: Define your file organization objectives
2. **Current State Analysis**: Assess existing file structure and issues
3. **User Confirmation**: Confirm organization strategy and priorities
4. **Document Creation**: Create task-specific organization workflow
5. **Environment Setup**: Prepare organization workspace and tools
6. **Organization Execution**: Execute systematic file organization
7. **Documentation**: Document the organization process and results

### For Analysis Workflow

> **📄 Working Document**: Created in `analysis_system/tasks/[task-id]/analysis_workflow_[task-name].md`

1. **Project Analysis**: Understand project structure and analysis requirements
2. **Analysis Planning**: Define analysis scope, dimensions, and success criteria
3. **Environment Setup**: Initialize analysis workspace and tools
4. **Multi-dimensional Analysis**: Execute code structure, quality, performance, and security analysis
5. **Report Generation**: Generate comprehensive analysis reports with metrics and recommendations
6. **Documentation and Archiving**: Document analysis process and archive results

### For Refactor Workflow

> **📄 Working Document**: Created in `refactor_system/refactor_workflow_[task-name].md`

1. **Requirement Analysis**: Determine refactoring scope and objectives
2. **Three-tier Planning**: Create Level1 (Overall) → Level2 (Stage) → Level3 (Implementation) plans
3. **Phased Execution**: Execute by priority stages (P0 → P1 → P2 → P3)
4. **Quality Assurance**: Validate and test each modification point
5. **Documentation Maintenance**: Synchronously update related documentation

### For Version Comparison Workflow

> **📄 Working Document**: Created in `version-comparison-system/version-comparison-workflow_[task-name].md`

1. **Version Selection**: Choose the versions or commits to compare
2. **Git Worktree Setup**: Create isolated worktree for each version
3. **Modular Analysis**: Analyze differences in a staged, modular fashion
4. **Documentation Generation**: Generate comprehensive documentation of changes
5. **Update Log Supplementation**: Automatically update the version history log
6. **Reporting**: Create a structured report of the version comparison findings

### For Workflow Builder

> **📄 Working Document**: Created in `workflow-builder-system/builds/workflow_build_[task-name].md`

1. **Requirement Clarification**: AI-guided 3-5 round dialogue to collect complete requirements
2. **IPD Gate Control**: 6-stage gate process from concept to quality verification
3. **Design Pattern Selection**: Choose from 24 validated design patterns
4. **Workflow Construction**: Build workflow using selected patterns and IPD methodology
5. **Plugin Verification**: Assess completeness, usability, maintainability, documentation quality, and extensibility
6. **Deployment**: Generate final workflow template and documentation

## 🎯 Features

### Debug Workflow Features

- **6-Step Debug Cycle**: Systematic approach to problem resolution
- **Structured Problem Decomposition**: Break complex issues into manageable parts
- **Documentation System**: Comprehensive logging and knowledge capture
- **Human Verification Checkpoints**: Ensure accuracy and user control

### File Organization Features

- **Multiple Organization Strategies**: Priority-based, type-based, and timeline-based approaches
- **Systematic Cleanup Process**: Comprehensive file cleanup and archiving procedures
- **Symbol-Based Classification**: Comprehensive symbol guide for project organization

### Analysis Workflow Features

- **Multi-dimensional Analysis**: Code structure, quality, performance, security, and technical debt assessment
- **Automated Tools**: Code metrics collector, dependency analyzer, and report generator
- **Systematic Reporting**: Structured analysis reports with quantitative metrics and actionable insights
- **Template-driven Process**: Standardized templates for consistent analysis across projects

### Refactor Workflow Features

- **Three-tier Planning System**: Strategic Level1 → Tactical Level2 → Operational Level3
- **Dual-loop Execution**: Stage-level outer loop + modification-point-level inner loop
- **Visual Workflow Support**: First workflow with Mermaid diagram integration
- **Priority-driven Management**: P0-P3 priority-based stage execution
- **Risk Control**: Comprehensive rollback mechanisms and quality checkpoints

### Version Comparison Workflow Features

- **Three-stage Layered Analysis**: Overview, module-level, and documentation-level analysis
- **Bottom-up Module Order**: Analyze from tools and logic to algorithms
- **Git Diff Statistics**: Comprehensive statistics and commit classification
- **Template-driven Tracking**: Standardized templates for consistent tracking and reporting
- **Update Log Supplementation**: Automatic updates to version history and upgrade guidance

### Workflow Builder Features

- **AI-guided Requirement Collection**: Complete requirement collection in 3-5 rounds of dialogue
- **IPD 6-stage Gate Control**: Concept → Analysis → Conceptual Design → Detailed Design → Development & Build → Quality Verification
- **24 Design Pattern Library**: Reusable design patterns extracted from existing workflows
- **Plugin-based Verification**: Assessment of completeness, usability, maintainability, documentation quality, and extensibility
- **Three Complexity Options**: Lightweight/Standard/Professional levels for different skill levels

### Shared Features

- **Modular Structure**: Organized file system for efficient workflow sessions
- **Template System**: Standardized templates for consistent documentation and processes

## 📖 Documentation

### Main Documentation

- **Debug Workflow Documentation**:
  - [中文说明](debug-system/README.md): Detailed debug workflow Chinese guide
  - [English Guide](debug-system/README_en.md): Comprehensive debug workflow English guide

- **File Organization Documentation**:
  - [中文说明](file-organize-system/README.md): Detailed file organization workflow Chinese guide
  - [English Guide](file-organize-system/README_en.md): Comprehensive file organization English guide

- **Analysis Workflow Documentation**:
  - [中文说明](analysis_system/README.md): Detailed code analysis workflow Chinese guide
  - [English Guide](analysis_system/README_en.md): Comprehensive analysis workflow English guide

- **Refactor Workflow Documentation**:
  - [中文说明](refactor_system/README.md): Detailed refactor workflow Chinese guide
  - [English Guide](refactor_system/README_en.md): Comprehensive refactor workflow English guide

- **Version Comparison Workflow Documentation**:
  - [中文说明](version-comparison-system/README.md): Detailed version comparison workflow Chinese guide
  - [English Guide](version-comparison-system/README_en.md): Comprehensive version comparison workflow English guide

- **Workflow Builder Documentation**:
  - [中文说明](workflow-builder-system/README.md): Detailed workflow builder Chinese guide
  - [English Guide](workflow-builder-system/README_en.md): Comprehensive workflow builder English guide

### Symbol Reference

For detailed symbol usage and file classification guidelines, see:

- [Debug Symbol Guide](debug-system/docs/常用符号.md)
- [File Organization Best Practices](file-organize-system/docs/最佳实践.md)

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📋 Update Log

For detailed version history and change information, please refer to: [Update Log](update_log.md)

---

**Created**: June 21, 2025
**Last Updated**: August 18, 2025  
**Current Version**: v3.0.0  
**Use Cases**: Technical project debugging, problem troubleshooting, system optimization, file organization, project cleanup, code analysis, quality assessment, code refactoring, architecture improvement, version diff analysis, workflow design

## 🧾 Author's Note

See workflow design intent, boundaries and practical lessons: [作者的话 (中文)](AUTHOR_NOTE.md) | [Author's Note (EN)](AUTHOR_NOTE_en.md)
