# Analysis Workflow Detailed Guide | 分析工作流详细指南

> 🌍 **Language Version | 语言版本**: [中文版本](README.md) | [Back to Main](../README.md)

## 📋 Table of Contents

- [Overview](#overview)
- [Workflow Features](#workflow-features)
- [Usage Methods](#usage-methods)
- [Analysis Dimensions](#analysis-dimensions)
- [Environment Setup](#environment-setup)
- [Analysis Process](#analysis-process)
- [Template Usage](#template-usage)
- [Tool Usage](#tool-usage)
- [Best Practices](#best-practices)
- [Directory Structure](#directory-structure)

## Overview

The Analysis Workflow is a systematic code analysis solution based on GitHub Copilot, designed for code quality assessment, technical debt identification, and performance optimization. It provides multi-dimensional analysis methods to ensure systematic and accurate code analysis.

### Core Templates

- **Main Template**: `analysis_system/analysis_workflow_template.md`
- **Supporting Files**: All templates and tools in the `analysis_system/` directory
- **Case Studies**: Actual cases in the `analysis_system/case-studies/` directory

## Workflow Features

### 🎯 Multi-dimensional Analysis Methods

- **Code Structure Analysis**: Module dependencies, coupling analysis, cohesion analysis
- **Code Quality Assessment**: Complexity, readability, maintainability evaluation
- **Performance Analysis**: Algorithm complexity, resource usage, performance hotspot identification
- **Security Assessment**: Potential security risks and best practice checks
- **Technical Debt Identification**: Code smells, duplicate code, outdated pattern identification

### 🤖 AI Collaboration Optimization

- **Copilot Integration**: Optimized for GitHub Copilot Agent mode
- **Natural Language Interaction**: Describe analysis requirements in natural language, AI automatically parses
- **Intelligent Suggestions**: AI provides optimization suggestions and refactoring plans based on analysis results

### 📊 Automated Tool Support

- **Code Metrics Collector**: Automatically extract code quality metrics
- **Dependency Analyzer**: Generate module dependency graphs
- **Performance Profiler**: Identify performance bottlenecks and hotspots
- **Report Generator**: Automatically generate structured analysis reports

## Usage Methods

### Step 1: Initialize Analysis Environment

```powershell
# Enter analysis system directory
cd analysis_system

# Copy workflow template
Copy-Item analysis_workflow_template.md "analysis_workflow_$(Get-Date -Format 'yyyyMMdd').md"
```

### Step 2: Configure Analysis Parameters

Edit the workflow document and configure the following analysis parameters:

- Project path and scope
- Analysis dimension selection
- Success criteria definition
- Output format requirements

### Step 3: Execute Automated Analysis

```powershell
# Run code metrics collection
python tools/code-metrics-collector.py --project-path "C:/path/to/project"

# Generate analysis report
./tools/generate-analysis-report.ps1 -ProjectPath "C:/path/to/project"
```

### Step 4: In-depth Analysis and Reporting

Use templates for in-depth analysis:

- Use `templates/analysis-report-template.md` to generate analysis reports
- Use `templates/performance-analysis-template.md` for performance analysis
- Use `templates/refactor-plan-template.md` to develop refactoring plans

## Analysis Dimensions

### 1. Code Structure Analysis

- **Module Dependencies**: Analyze dependency complexity between modules
- **Coupling Assessment**: Evaluate coupling degree between components
- **Cohesion Analysis**: Analyze functional cohesion within modules

### 2. Code Quality Assessment

- **Complexity Metrics**: Cyclomatic complexity, cognitive complexity analysis
- **Readability Assessment**: Naming conventions, comment quality, code style
- **Maintainability Metrics**: Code duplication, function length, class size

### 3. Performance Analysis

- **Algorithm Complexity**: Time complexity and space complexity analysis
- **Resource Usage**: Memory usage, IO operations, CPU intensity
- **Performance Hotspots**: Identify performance bottlenecks and optimization points

### 4. Security Assessment

- **Security Vulnerability Scanning**: Common security issue identification
- **Best Practice Checks**: Compliance with secure coding standards
- **Dependency Security**: Third-party library security assessment

### 5. Technical Debt Identification

- **Code Smells**: Long methods, large classes, duplicate code, etc.
- **Outdated Patterns**: Deprecated programming patterns and practices
- **Technical Debt Quantification**: Repair cost estimation and priority ranking

## Environment Setup

### Python Environment Requirements

```bash
# Install dependencies
pip install ast
pip install os
pip install pathlib
pip install argparse
```

### PowerShell Environment Requirements

```powershell
# Ensure PowerShell execution policy allows script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Analysis Process

### Phase 1: Project Understanding

1. **Project Overview**: Understand project background, technology stack, business logic
2. **Requirements Analysis**: Clarify analysis goals and success criteria
3. **Scope Definition**: Determine the scope and depth of code analysis

### Phase 2: Automated Analysis

1. **Metrics Collection**: Run automated tools to collect basic metrics
2. **Structure Analysis**: Analyze code structure and dependencies
3. **Quality Assessment**: Evaluate code quality metrics

### Phase 3: In-depth Analysis

1. **Manual Review**: Combine automated results with manual review
2. **Problem Identification**: Identify key issues and improvement opportunities
3. **Solution Development**: Develop specific optimization and refactoring solutions

### Phase 4: Report Generation

1. **Result Summary**: Organize analysis results and key findings
2. **Report Writing**: Generate structured analysis reports
3. **Recommendation Provision**: Provide actionable improvement suggestions and implementation plans

## Template Usage

### Analysis Report Templates

- **analysis-report-template.md**: Standard analysis report template
- **performance-analysis-template.md**: Performance analysis specific template
- **code-review-template.md**: Code review template

### Planning Templates

- **refactor-plan-template.md**: Refactoring plan template
- **analysis-implementation-template.md**: Analysis implementation plan template

### Summary Templates

- **summary-template.md**: Project analysis summary template

## Tool Usage

### Code Metrics Collector

```bash
python tools/code-metrics-collector.py --project-path "/path/to/project" --output-format json
```

### Analysis Report Generator

```powershell
./tools/generate-analysis-report.ps1 -ProjectPath "/path/to/project" -ReportType "comprehensive"
```

### Detailed Tool Documentation

Refer to `tools/analysis-tools-README.md` for detailed tool usage instructions.

## Best Practices

### Pre-analysis Preparation

1. **Clear Objectives**: Clearly define analysis goals and expected outputs
2. **Scope Definition**: Reasonably define analysis scope, avoid being too broad
3. **Tool Preparation**: Ensure all necessary tools and environments are ready

### Analysis Process

1. **Progressive Approach**: Start with overview analysis, gradually deepen into details
2. **Data-driven**: Base analysis on objective data, avoid subjective assumptions
3. **Continuous Validation**: Regularly validate accuracy and effectiveness of analysis results

### Result Application

1. **Priority Ranking**: Rank issues based on impact level and repair difficulty
2. **Gradual Improvement**: Develop phased improvement plans
3. **Effect Tracking**: Track actual effects of improvement measures

## Directory Structure

The Analysis Workflow uses a "General-Specific-General" directory organization structure:

```text
analysis_system/
├── README.md                      # This document - workflow overview and usage guide
├── README_en.md                   # English version documentation
├── analysis_workflow_template.md  # Workflow template - reusable analysis process template
├── templates/                     # Standardized templates
│   ├── analysis-implementation-template.md # Implementation template
│   ├── analysis-report-template.md    # Analysis report template
│   ├── code-review-template.md        # Code review template
│   ├── performance-analysis-template.md # Performance analysis template
│   ├── refactor-plan-template.md      # Refactoring plan template
│   └── summary-template.md            # Project summary template
├── tools/                         # Auxiliary tools
│   ├── generate-analysis-report.ps1   # Automated analysis report generation tool
│   ├── code-metrics-collector.py      # Code metrics collection tool
│   └── analysis-tools-README.md       # Tool usage instructions
├── tasks/                         # Analysis round archive directory
│   ├── README.md                  # Archive directory documentation
│   └── [Task ID]/                 # Specific analysis task directory
│       ├── master_plan/           # Overall planning and summary reports
│       ├── [Round Directory]/     # Round-specific analysis directories
│       │   ├── summary/           # Core output documents for this round
│       │   ├── reports/           # Various detailed analysis reports
│       │   ├── metrics/           # Code metrics and quantitative data
│       │   └── analysis/          # Detailed analysis process and intermediate results
│       └── archive/               # Archived workflow documents for completed tasks
└── case-studies/                  # Case studies
    ├── README.md                  # Case study documentation
    └── [Case Name]/               # Specific case directories
```

### Task Directory Organization

Each analysis task is organized according to the following structure:

- **master_plan/**: Contains overall analysis planning and final summary reports
- **[Round Directory]/**: Organized by analysis rounds, such as "1_Initial_Quality_Assessment/", "2_Deep_Architecture_Analysis/", etc.
  - **summary/**: Contains core outputs and summary documents for this round
  - **reports/**: Contains various detailed analysis reports
  - **metrics/**: Contains code metrics and quantitative assessment data
  - **analysis/**: Contains detailed analysis processes and intermediate results
- **archive/**: Contains completed workflow documents and historical records

## Application Scenarios

### Project Types

- **Signal Processing Systems**: Complex algorithm and data processing flow analysis
- **GUI Applications**: Code quality assessment for Qt/PySide interface applications
- **Multi-module Python Projects**: Modular architecture analysis for large projects
- **Scientific Computing Projects**: Optimization analysis for performance-critical algorithms

### Analysis Timing

- **Project Early Stage**: Establish baseline and quality standards
- **Development Process**: Continuously monitor code quality trends
- **Pre-release**: Comprehensive quality assessment and risk identification
- **Refactoring Planning**: Data-driven refactoring decision support

## Common Questions

### Q: How to choose appropriate analysis dimensions?

A: Choose based on project characteristics and analysis goals:

- New projects focus on code structure and quality
- Mature projects focus on performance and technical debt
- Refactoring projects focus on architecture and dependencies

### Q: How accurate are the automated tools?

A: Automated tools provide basic data and metrics, need to be combined with manual analysis:

- Quantitative metrics as analysis foundation
- Manual review to validate tool results
- Combine with business logic for in-depth analysis

### Q: How to use analysis reports?

A: Analysis reports are decision support tools:

- Identify key issues and risk points
- Develop optimization and refactoring plans
- Track effects of improvement measures

---

**Get Started**: Check out `analysis_workflow_template.md` to begin your first project analysis.

**Get Support**: For questions, refer to `tools/analysis-tools-README.md` or check actual cases in `case-studies/`.

---

**Last Updated**: July 29, 2025  
**Version**: v2.4.0  
**Maintainer**: Copilot Workflow System Team
