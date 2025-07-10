# Debug Workflow Detailed Guide | 调试工作流详细指南

> 🌍 **Language Version | 语言版本**: [中文版本](README_debug_ch.md) | [Back to Main](README.md)

## 📋 Table of Contents

- [Overview](#overview)
- [Workflow Features](#workflow-features)
- [Usage Guide](#usage-guide)
- [6-Step Debugging Cycle](#6-step-debugging-cycle)
- [Environment Setup](#environment-setup)
- [Template Usage](#template-usage)
- [Symbol System](#symbol-system)
- [Best Practices](#best-practices)
- [FAQ](#faq)

## Overview

The Debug Workflow is a systematic debugging solution based on GitHub Copilot, specifically designed for AI-assisted development. It provides a structured problem-solving approach that ensures consistency and efficiency in the debugging process.

### Core Template
- **Main Template**: `debug-system/debug_workflow_template.md`
- **Supporting Files**: All templates and tools in the `debug-system/` directory

## Workflow Features

### 🎯 Systematic Debugging Process
- **6-Step Debugging Cycle**: Problem Identification → Analysis → Hypothesis → Verification → Fix → Summary
- **Structured Documentation**: Complete documentation record for each debugging session
- **Version Management**: Version control and history tracking for multi-round debugging

### 🤖 AI Collaboration Optimization
- **Copilot Integration**: Optimized specifically for GitHub Copilot Agent mode
- **Natural Language Interaction**: Describe problems in natural language, AI parses automatically
- **Intelligent Suggestions**: AI provides debugging suggestions based on context

### 📊 File Organization System
- **Symbol Classification**: Intuitive file classification using emoji symbols
- **Hierarchical Storage**: Multi-level file management with core/archive/deprecated layers
- **Quick Navigation**: Clear directory structure and indexing system

## Usage Guide

### Step 1: Initialize Debug Environment

```powershell
# Create debug directory
mkdir debug
cd debug

# Create workflow archive directory
mkdir workflow_archive -ErrorAction SilentlyContinue

# Set round variable
$round = 1

# Create standard directory structure
mkdir $round\{src,core,archive,deprecated,docs,logs,files}

# Copy README template
Copy-Item "..\debug-system\templates\README-template.md" "$round\README.md"

# Initialize Bug management system
mkdir ..\buglist -ErrorAction SilentlyContinue
Copy-Item "..\debug-system\templates\bug-list-template.md" "..\buglist\bug_list.md" -ErrorAction SilentlyContinue
```

### Step 2: Copy Workflow Template

```powershell
# Copy template for specific task to debug-system directory
Copy-Item "debug-system/debug_workflow_template.md" "debug-system/debug_workflow_[task-name].md"
```

### Step 3: Launch in VS Code

```powershell
# Open workflow document
code debug_workflow_[task-name].md

# Ensure Copilot Agent mode is enabled
# Use @workspace commands to start session
```

### Step 4: Configure Auto-Trigger (Optional)

You can create a `.copilot-instructions.md` file in your project root to enable automatic workflow triggering:

```markdown
# Copilot Debug Workflow Instructions

## Auto-Trigger Conditions
When user mentions: debugging, error fixing, troubleshooting, bug resolution, code issues
Automatically suggest: "I notice you're working on debugging. Would you like me to start the systematic debug workflow? I can create a structured debugging session document to help organize the troubleshooting process."

## Workflow Templates
- Debug Template: `debug-system/debug_workflow_template.md`
```

**Choose Your Approach**:
- **Automatic Trigger**: Configure `.copilot-instructions.md` for seamless workflow activation
- **Manual Trigger**: Open workflow template documents manually

### Step 5: Describe Problem and Start Debugging

1. **Problem Description**: Describe your problem in detail using natural language
2. **AI Analysis**: Copilot will analyze the problem and propose a debugging plan
3. **Confirm Understanding**: Verify that AI's understanding of the problem is correct
4. **Start Debugging**: Execute according to the 6-step debugging cycle

## 6-Step Debugging Cycle

### 1. 🔍 Problem Identification
- Clearly define the problem phenomenon
- Collect error information and logs
- Determine the scope of impact

### 2. 📊 Analysis
- Analyze the root cause of the problem
- Check related code and configuration
- Review system environment and dependencies

### 3. 💡 Hypothesis Formation
- Propose possible causes based on analysis
- Develop verification plan
- Set priorities

### 4. 🧪 Verification
- Design and execute tests
- Collect verification data
- Record test results

### 5. 🔧 Fix Implementation
- Implement solution
- Perform regression testing
- Verify fix effectiveness

### 6. 📝 Summary and Documentation
- Record the resolution process
- Update documentation
- Summarize lessons learned

## Environment Setup

### Directory Structure Explanation

```
debug-system/
├── debug_workflow_template.md          # Debug workflow template
├── templates/                         # Template collection
│   ├── README-template.md             # Debug session documentation template
│   ├── summary-template.md            # Project summary template
│   ├── experience-template.md         # Experience summary template
│   ├── INDEX-template.md              # Debug index template
│   ├── bug-list-template.md           # Bug list template
│   └── bug-report-template.md         # Bug report template
├── buglist/                           # Bug management directory
│   ├── bug_list.md                    # Bug record and statistics
│   ├── to_fix/                        # Bug documentation to be fixed
│   └── fixed/                         # Fixed bug documentation
└── debug/                             # Debug working directory
    ├── workflow_archive/              # Workflow document archive
    └── 1/                             # First debugging round
        ├── src/         🐍            # Working code directory
        ├── core/        🔴            # Core solutions (5-10 key files)
        ├── archive/     📚            # Important milestone files
        ├── deprecated/  🗑️            # Deprecated files
        ├── docs/        📝            # Analysis documents
        ├── logs/        📋            # Test logs
        ├── files/       🗂️            # Other supporting files
        └── README.md                  # Debug session documentation
```

### Symbol System

| Symbol | Directory | Purpose | Storage Rule |
|--------|-----------|---------|--------------|
| 🐍 | src/ | Current working code | All code files during debugging |
| 🔴 | core/ | Core solutions | Keep maximum 5-10 key files |
| 📚 | archive/ | Important milestones | Staged results and important versions |
| 🗑️ | deprecated/ | Deprecated files | Invalid or replaced files |
| 📝 | docs/ | Analysis documents | Problem analysis and solution documentation |
| 📋 | logs/ | Test logs | Log records during debugging |
| 🗂️ | files/ | Supporting files | Other auxiliary files |

## Template Usage

### README Template (README-template.md)
Used to record detailed information for each debugging session, including:
- Problem description
- Debugging process
- Solution
- Lessons learned

### Summary Template (summary-template.md)
Used for project-level summary reports, including:
- Overall problem overview
- Solution summary
- Performance impact analysis
- Future recommendations

### Experience Template (experience-template.md)
Used to record lessons learned during debugging:
- Successful debugging methods
- Encountered pitfalls
- Best practices
- Tool recommendations

## Best Practices

### Copilot Configuration Recommendations

#### Model Selection
- **Recommended Model**: Claude 4.0
- **Alternative Models**: GPT-4 or other advanced models
- **Avoid**: Basic models (may affect debugging quality)

#### Session Settings
- **Budget Control**: 10-20 requests per session
- **Thinking Mode**: Enable AI thinking mode
- **Terminal Access**: Ensure terminal access permissions

### Debugging Strategies

#### Problem Description
- **Specific and Detailed**: Provide specific error information and reproduction steps
- **Environment Information**: Include system environment, version information, etc.
- **Expected Results**: Clearly state the expected correct behavior

#### Verification Methods
- **Prioritize Official Documentation Verification**: Use fetch_webpage tool to obtain official examples and verify correct API usage
- **Small Step Verification**: Break complex problems into small verification steps
- **Regression Testing**: Perform comprehensive testing after each modification
- **Documentation**: Detailed record of each verification step and result

### File Management

#### Version Control
- **Regular Archiving**: Move important staged results to archive directory
- **Clean Deprecated**: Timely clean expired files in deprecated directory
- **Core Simplification**: Keep core directory file count within 5-10

#### Document Synchronization
- **Real-time Updates**: Update README documentation in real-time during debugging
- **Cross-references**: Add reference links to related files in documentation
- **Summary**: Summarize at the end of each debugging round

### 🧠 Core Debugging Methodologies

#### Official Documentation Verification Method ⭐ (New)

- **Core Principle**: Verify correct API usage through official documentation to avoid debugging based on incorrect assumptions
- **Tool Support**: Use fetch_webpage tool to retrieve official documentation and example code
- **Applicable Scenarios**: Third-party library usage errors, API call failures, version compatibility issues
- **Implementation Steps**:
  1. Identify relevant technology stack and library official documentation
  2. Use tools to obtain official examples and best practices
  3. Compare differences between current code and official examples
  4. Correct code implementation based on official standards
- **Core Value**: Ensure solutions comply with official standards, improving code quality and stability

#### Environment Pre-check Method

- **Principle**: Confirm environment and dependencies meet operational requirements before execution
- **Applicable**: Environment-sensitive and dependency-complex systems
- **Steps**: Environment check → Dependency verification → Permission confirmation → Resource assessment

#### Structured Logging

- **Principle**: Establish detailed execution traces and state recording mechanisms
- **Applicable**: Scenarios with difficult problem reproduction and insufficient debugging information
- **Steps**: Key point recording → Exception detail capture → Performance metric monitoring → State snapshot preservation

## FAQ

### Q: What to do if AI drifts off-topic during debugging?
**A**: Immediately pause and re-describe the problem. If budget is running out, consider starting a new session.

### Q: How to manage too many files during debugging?
**A**: Strictly follow the symbol system for classification, regularly clean the deprecated directory, and move important files to core or archive.

### Q: How to record complex debugging processes?
**A**: Use hierarchical document structure, create separate document files for each major step, and maintain an index in the main README.

### Q: How to manage multi-round debugging?
**A**: Create independent numbered directories for each debugging round (1/, 2/, 3/, etc.), and maintain a round index in the root README.

### Q: How to share debugging results with the team?
**A**: Use summary template to create project-level summaries, organize key files in the core directory, and write clear documentation.

---

**Last Updated**: July 10, 2025  
**Version**: v2.2  
**Maintainer**: Copilot Workflow System Team

**v2.2 Updates**:
- Added core debugging methodology: Official Documentation Verification Method
- Updated best practices to emphasize the importance of official documentation verification
- Synchronized with debug_workflow_template.md
