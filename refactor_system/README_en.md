# 🔧 Refactor Workflow System

> **Version**: v2.4.0 | **Updated**: July 29, 2025 | **Language**: [中文](README.md) | [English](README_en.md)

A systematic refactor workflow based on code analysis results, providing visual process guidance and three-tier plan management system for module-level refactoring.

## 🎯 System Overview

### Core Philosophy

The Refactor Workflow System aims to transform module-level code refactoring from ad-hoc activities into a **systematic, controllable engineering process**. Through a three-tier planning system and dual-loop mechanism, it ensures predictability and high-quality delivery of module-level refactoring work.

### Design Principles

- **🔄 Dual-Loop Control**: Stage-level outer loop + modification-point-level inner loop
- **📋 Three-Tier Planning**: Overall Plan → Stage Plan → Implementation Plan
- **🎯 Priority-Driven**: P0/P1/P2/P3 priority stage management
- **🤝 Manual Confirmation**: User confirmation required at critical checkpoints
- **📊 Visual Process**: Mermaid flowcharts guide execution

## 🚀 Core Features

### 📊 Visual Workflow

- **Stage 1**: Refactor planning flowchart
- **Stage 2**: Dual-loop execution process
- **Stage 3**: Validation and summary flowchart
- **Three-Tier Planning System Diagram**: Complete planning hierarchy relationship

### 🎯 Three-Tier Planning System

| Level | Template File | Description |
|-------|---------------|-------------|
| **Level 1** | `level1-overall-plan-template.md` | Overall refactor plan, P0-P3 priority division |
| **Level 2** | `level2-phase-detailed-plan-template.md` | Stage detailed plan, specific modification point list |
| **Level 3** | `level3-implementation-plan-template.md` | Function-level implementation plan, code examples and tests |

### 🔄 Dual-Loop Mechanism

#### Outer Loop (Stage Level)

- Select execution stage (P0/P1/P2/P3)
- Develop stage detailed plan
- User confirmation checkpoints
- Stage validation and Git commit

#### Inner Loop (Modification Point Level)

- Develop specific implementation plan
- Code implementation and quality verification
- Immediate testing and fixes
- Modification point completion confirmation

## 📁 Directory Structure

```text
refactor_system/
├── refactor_workflow_template.md       # Refactor workflow template
├── README.md                          # System documentation (Chinese)
├── README_en.md                       # System documentation (English)
├── templates/                         # Template file collection
│   ├── level1-overall-plan-template.md          # Level1 overall plan template
│   ├── level2-phase-detailed-plan-template.md   # Level2 stage detailed plan template
│   ├── level3-implementation-plan-template.md   # Level3 implementation plan template
│   ├── delivery-template.md                     # Delivery document template
│   ├── INDEX-template.md                        # Refactor index template
│   ├── module-comparison-analysis-template.md   # Module comparison analysis template
│   └── refactor-lessons-learned-template.md     # Refactor lessons learned template
├── tasks/                             # Refactor task archive directory
│   └── [Task Number]/                 # Specific refactor task directory
│       ├── refactor_workflow_[TaskName].md  # Task-specific workflow document
│       ├── plans/                     # Planning documents directory
│       ├── implementation/            # Implementation records directory
│       └── delivery/                  # Delivery documents directory
└── tools/                             # Refactor tools collection
    └── refactor-tools-README.md      # Tool usage documentation
```

## 🔧 Template Resources

### 📋 Core Planning Templates

- **level1-overall-plan-template.md**: Overall refactor plan template
  - Overall architecture vision and risk assessment
  - P0/P1/P2/P3 priority stage division
  - Resource allocation and time planning

- **level2-phase-detailed-plan-template.md**: Stage detailed plan template
  - Specific modification point list (P0.1/P0.2/P0.3)
  - User confirmation checkpoint setup
  - Plan change version control

- **level3-implementation-plan-template.md**: Implementation plan template
  - Function-level modification solutions
  - Code examples and test cases
  - Contains only approved modification content

### 📊 Supporting Document Templates

- **delivery-template.md**: Delivery document template
- **INDEX-template.md**: Refactor index template
- **module-comparison-analysis-template.md**: Module comparison analysis template
- **refactor-lessons-learned-template.md**: Refactor lessons learned template

## 🚀 Usage

### Prerequisites

1. **Complete Code Analysis**: Use `analysis_system` to complete project analysis
2. **Prepare Analysis Results**: Ensure complete analysis reports and refactor recommendations
3. **Define Refactor Goals**: Define expected improvement effects and constraints

### Launch Methods

#### Method 1: Natural Language Launch

Describe refactor requirements to Copilot:

```text
"I need to refactor the project based on analysis results to optimize code structure and performance."
```

#### Method 2: Manual Launch

```bash
# Open refactor workflow template
code refactor_system/refactor_workflow_template.md
```

### Execution Flow

1. **📥 Input Collection**: Provide analysis results and refactor requirements
2. **🔧 Environment Initialization**: Create dedicated directories and workspace
3. **📋 Overall Planning**: Create Level1 overall plan
4. **🤝 User Confirmation**: Confirm plans and priorities
5. **🔄 Loop Execution**: Implement refactoring by stages
6. **📊 Validation Summary**: Complete validation and document archiving

## 🎯 Core Features

### 🔄 Controllable Refactor Process

- **Staged Execution**: P0-P3 priority-driven stage management
- **Checkpoint Control**: Manual confirmation mechanism at critical points
- **Version Control**: Version management for plan changes

### 📊 Visual Guidance

- **Flowchart Navigation**: Mermaid charts provide visual guidance
- **Decision Point Identification**: Clear decision logic and branch handling
- **Status Tracking**: Real-time progress and status management

### 🛡️ Risk Control

- **Progressive Implementation**: Small steps, gradual validation
- **Rollback Mechanism**: Independent commits and rollback points for each stage
- **Quality Assurance**: Built-in quality verification and testing requirements

## 📚 Best Practices

### 🎯 Planning

1. **Overall First, Then Specific**: Gradually refine from Level1 to Level3
2. **Priority-Driven**: Strictly follow P0-P3 priority execution
3. **User Participation**: Get user confirmation at critical decision points

### 🔄 Execution Control

1. **Small Batch Implementation**: Handle only a few modification points at a time
2. **Immediate Validation**: Test immediately after each modification point completion
3. **Document Synchronization**: Real-time updates to plans and progress documents

### 📊 Quality Assurance

1. **Code Review**: Conduct code review after each stage completion
2. **Test Coverage**: Ensure all modifications have corresponding tests
3. **Performance Validation**: Critical modifications need performance benchmark comparison

## 🔗 Workflow Integration

### Integration with Analysis Workflow

The refactor workflow receives output from `analysis_system` as input:

- **Analysis Report**: `final_analysis_report.md`
- **Refactor Recommendations**: `improvement_roadmap.md`
- **Technical Metrics**: Quantitative data in `metrics/` directory

### Collaboration with Debug Workflow

When encountering issues during refactoring, launch `debug-system` for diagnosis:

- **Issue Isolation**: Use debug workflow to locate refactor-introduced issues
- **Solutions**: Find fix solutions through debug loops
- **Experience Accumulation**: Integrate resolution experience into refactor process

## 🤝 Human-AI Collaboration

### 🤖 AI Responsibilities

- **Plan Development**: Generate refactor plans based on analysis results
- **Code Implementation**: Execute specific code modifications
- **Document Maintenance**: Automatically update plans and progress documents
- **Quality Checks**: Automated code quality verification

### 👤 User Responsibilities

- **Goal Confirmation**: Confirm refactor goals and priorities
- **Plan Review**: Review and approve plans at all levels
- **Quality Acceptance**: Verify refactor results and performance improvements
- **Decision Making**: Make decisions at critical branch points

## 📈 Success Metrics

### 🎯 Process Metrics

- **Plan Completion Rate**: Proportion of tasks completed as planned
- **Quality Pass Rate**: Code review and test pass rate
- **Time Control**: Deviation between actual time and planned time

### 📊 Result Metrics

- **Code Quality**: Quality metric comparison before and after refactoring
- **Performance Improvement**: Improvement in key performance indicators
- **Technical Debt**: Degree of technical debt reduction

## 🔧 Extension Development

### Custom Templates

You can create refactor templates for specific technology stacks based on existing templates:

```bash
cp templates/level1-overall-plan-template.md templates/level1-react-refactor-template.md
```

### Tool Integration

Add specific refactor tools and scripts in the `tools/` directory:

- Code analysis tools
- Automated testing tools
- Performance benchmark tools

---

**System Version**: v2.4.0
**Created**: July 29, 2025
**Maintenance Team**: Copilot Workflow System Development Team
**Use Cases**: Module-level refactoring, code quality improvement, architecture optimization, technical debt cleanup
