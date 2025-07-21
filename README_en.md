# Copilot Workflow System

> 🌍 **Language Versions**: [English](README_en.md) | [中文](README.md)

A comprehensive workflow system based on GitHub Copilot for systematic debugging, file organization, and code analysis.

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

This system provides three main workflows designed for AI-assisted development:

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
**Description**: Comprehensive file organization system with three major organization approaches and systematic cleanup procedures.

**Features**:
- Priority-based organization
- Type-based classification
- Timeline-based sorting
- Systematic cleanup process
- Symbol-based file categorization

### 3. Analysis Workflow

**Template**: `analysis_system/analysis_workflow_template.md`
**Description**: Comprehensive code analysis and quality assessment system with multi-dimensional analysis approaches for technical debt identification, performance optimization, and refactoring guidance.

**Features**:
- Multi-dimensional code analysis
- Automated tools and metrics collection
- Systematic reporting
- Template-driven process

## 📁 Project Structure

```text
copilot_workflows/
├── debug-system/                        # Debug workflow supporting files
│   ├── debug_workflow_template.md       # Debug workflow template
│   ├── templates/                       # Debug template collection
│   ├── docs/                           # Symbol reference guides
│   └── buglist/                        # Bug tracking and resolution archive
├── file-organize-system/                # File organization workflow supporting files
│   ├── file_organize_workflow_template.md # File organization workflow template
│   ├── templates/                       # Organization template collection
│   ├── docs/                           # Operation guides and best practices
│   ├── tools/                          # Organization tools and utilities
│   ├── organize/                       # Organization task working directory
│   └── version.md                      # Version history
├── analysis_system/                    # Code analysis workflow supporting files
│   ├── analysis_workflow_template.md   # Analysis workflow template
│   ├── README.md                       # Analysis system documentation
│   ├── templates/                      # Analysis template collection
│   ├── tools/                          # Analysis tools and utilities
│   ├── tasks/                          # Analysis task archive directory
│   ├── docs/                           # Analysis documentation
│   └── case-studies/                   # Analysis case studies
├── .copilot-instructions.md            # Copilot AI collaboration instructions
├── git-commit-workflow.md              # Git commit workflow specification
├── README.md                           # Main documentation (Chinese)
├── README_en.md                        # English documentation
└── LICENSE                             # MIT License
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
```

> **📝 Note**: These are template files. The actual workflow documents will be automatically generated when you start the workflow process.

### 4A. Natural Language Interaction

Simply describe your problem or organization task in natural language - the workflow will handle the parsing and formatting automatically:

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

## Workflow Templates
- Debug Template: `debug-system/debug_workflow_template.md`
- File Organization Template: `file-organize-system/file_organize_workflow_template.md`
- Analysis Template: `analysis_system/analysis_workflow_template.md`
```

### 4B. Natural Language Interaction

Once configured, simply mention your needs in conversation - AI will automatically suggest the appropriate workflow:

**Example triggers**:

- "I need to debug this error..." → Debug workflow suggestion
- "I want to organize these files..." → File organization workflow suggestion
- "I need to analyze this code quality..." → Analysis workflow suggestion

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

### Shared Features

- **Modular Structure**: Organized file system for efficient workflow sessions
- **Template System**: Standardized templates for consistent documentation and processes

## 📚 Templates

### Debug System Templates

The `debug-system/templates/` directory contains:

- **bug-report-template.md**: Standardized bug reporting template
- **summary-template.md**: Debug session summary template
- **experience-template.md**: Experience and lessons learned template

### File Organization Templates

The `file-organize-system/templates/` directory contains:

- **analysis-template.md**: File analysis and categorization template
- **plan-template.md**: Planning template for organization tasks
- **summary-report-template.md**: Comprehensive summary report template

### Analysis System Templates

The `analysis_system/templates/` directory contains:

- **analysis-implementation-template.md**: Template for analysis implementation planning
- **analysis-report-template.md**: Standardized analysis report template
- **code-review-template.md**: Code review and quality assessment template
- **performance-analysis-template.md**: Performance analysis and optimization template
- **refactor-plan-template.md**: Refactoring planning and strategy template
- **summary-template.md**: Comprehensive project analysis summary template

## 📖 Documentation

### Main Documentation

- **Debug Workflow Documentation**: 
  - [中文说明](debug-system/README.md): Detailed debug workflow Chinese guide
  - [English Guide](debug-system/README_en.md): Comprehensive debug workflow English guide

- **File Organization Documentation**: 
  - [中文说明](file-organize-system/README.md): Detailed file organization workflow Chinese guide (Coming Soon)
  - [English Guide](file-organize-system/README_en.md): Comprehensive file organization English guide (Coming Soon)

- **Analysis Workflow Documentation**: 
  - [中文说明](analysis_system/README.md): Detailed code analysis workflow Chinese guide
  - [English Guide](analysis_system/README_en.md): Comprehensive analysis workflow English guide (Coming Soon)

### Symbol Reference

For detailed symbol usage and file classification guidelines, see:
- [Debug Symbol Guide](debug-system/docs/常用符号.md)
- [File Organization Best Practices](file-organize-system/docs/最佳实践.md)

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Created**: June 21, 2025
**Last Updated**: December 29, 2025
**Version**: v2.3
**Use Cases**: Technical project debugging, problem troubleshooting, system optimization, file organization, project cleanup, code analysis, quality assessment

**v2.3 Updates**:

- Added Analysis Workflow System for comprehensive code analysis
- Enhanced multi-dimensional analysis capabilities with automated tools
- Added systematic reporting and quantitative metrics for code quality assessment
- Updated project structure and documentation to include analysis workflow
