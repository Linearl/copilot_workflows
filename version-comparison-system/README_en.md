# Version Comparison Workflow System

> 🌍 A version difference analysis workflow solution architected on top of the debug-system foundations

## 📋 Table of Contents

- [Overview](#overview)
- [Workflow Characteristics](#workflow-characteristics)
- [How to Use](#how-to-use)
- [3-Stage Analysis Flow](#3-stage-analysis-flow)
- [Environment Setup](#environment-setup)
- [Template Usage](#template-usage)
- [Best Practices](#best-practices)
- [Version & Maintenance](#version--maintenance)

## Overview

The Version Comparison Workflow is a structured version analysis system powered by GitHub Copilot, designed specifically for large-scale version diff analysis with AI assistance. It provides a disciplined methodology that ensures completeness and accuracy while effectively managing AI context limitations.

### Core Templates

- Primary Template: `version-comparison-system/version-comparison-workflow-template.md`
- Supporting Assets: All templates and tools under `version-comparison-system/`

## Workflow Characteristics

### 🎯 Phased Analysis Process

- 3 analysis stages: Overview → Deep Module Diff → Documentation Changes
- Bottom-up module order: tools → logic → algorithm
- Periodic consolidation: Summarize every 2–5 minutes or every 5–10 files

### 🤖 AI Collaboration Optimization

- Context management rhythm optimized for AI token limits
- Safe working area using Git worktree inside the project
- Template-driven recording and reporting

### 📊 Version Diff Specialization

- Deep Git integration for change extraction
- Layered modular analysis by architectural tiers
- Multi-dimensional outputs: version report, update log supplements, upgrade guidance

## How to Use

### Step 1: Initialize Analysis Environment

```powershell
# Enter the version comparison workflow directory
cd workflow/version-comparison-system

# Create analysis directory if absent
mkdir analysis -ErrorAction SilentlyContinue
```

### Step 2: Copy Workflow Template

```powershell
# Copy template for a specific version comparison task
Copy-Item "version-comparison-workflow-template.md" "version-comparison-V1.86-to-V1.87.md"
```

### Step 3: Launch in VS Code

```powershell
# Open task-specific workflow document
code version-comparison-V1.86-to-V1.87.md

# Ensure Copilot Agent mode is enabled
# Start session with @workspace command
```

### Step 4: Describe Comparison Objective & Begin

1. Requirement Example: "Analyze changes from V1.86 to V1.87 focusing on algorithm module to enrich update log"
2. AI Parsing: Copilot derives an analysis plan
3. User Confirmation: Validate AI interpretation
4. Execute: Follow the 3-stage analysis flow

## 3-Stage Analysis Flow

### Stage 1: 📊 Global Change Overview

- Commit classification (feat / fix / refactor / etc.)
- File change statistics and hotspots
- Module impact prioritization

### Stage 2: 🔧 Core Module Deep Diff

- tools layer: utilities and shared libraries
- logic layer: business logic & configuration management
- algorithm layer: core algorithms and analytical capabilities
- config governance: configuration file & process changes

### Stage 3: 📝 Documentation Change Analysis

- Structural changes: added / modified / removed docs
- Content inspection for key docs
- Lightweight capture (no exhaustive commentary)

## Environment Setup

### Directory Structure

```text
version-comparison-system/
├── version-comparison-workflow-template.md     # Main workflow template
├── templates/                                  # Template collection
│   ├── mgmt-analysis-index.md                  # Analysis index template
│   ├── analysis-stage-record.md                # Stage record template
│   ├── report-module-analysis.md               # Module analysis template
│   ├── report-version-summary.md               # Version summary template
│   └── worktree-setup.md                       # Worktree setup template
└── analysis/                                   # Analysis workspace
    ├── workflow_archive/                       # Archived workflow docs
    └── 1_version_diff_task/                    # Task-specific folder
        ├── INDEX.md                            # Navigation index
        ├── worktree_V1.86/                     # Previous version worktree
        ├── stage_1_overview/                   # Stage 1 outputs
        ├── stage_2_modules/                    # Stage 2 outputs
        ├── stage_3_docs/                       # Stage 3 outputs
        └── summary/                            # Consolidated reports
```

### Git Worktree Integration

The system uses Git worktree to create safe version contexts:

```powershell
# Auto-created worktree example
git worktree add analysis/1_V1.86-to-V1.87/worktree_V1.86 V1.86

# Cleanup after analysis (requires user confirmation)
git worktree remove analysis/1_V1.86-to-V1.87/worktree_V1.86
```

Benefits:

- In-project visibility for AI agents
- Full Git history preserved
- Primary workspace remains untouched
- All Git operations supported

## Template Usage

### Core Template Purposes

#### mgmt-analysis-index.md

Creates the navigation and tracking hub:

- Task metadata & status
- Progress tracking
- Key findings snapshot
- File navigation links

#### analysis-stage-record.md

Captures detailed execution per stage:

- Stage task checklist
- Findings log
- Execution trace
- Periodic summaries

#### report-version-summary.md

Generates final comparison deliverable:

- High-impact change overview
- Module-level details
- Compatibility considerations
- Upgrade guidance

## Best Practices

### Analysis Strategy

#### Bottom-Up Layering

- Principle: Understand foundational shifts before higher-level impacts
- Order: tools → logic → algorithm → config
- Benefit: Complete dependency impact chain awareness

#### Periodic Summarization

- Time cadence: every 2–5 minutes
- File cadence: every 5–10 reviewed files
- Depth cadence: after each module completes

#### Modular Documentation

- Stage isolation for clarity
- Per-module dedicated docs
- Unified final synthesis

### Quality Assurance

#### Analysis Completeness

- All planned modules reviewed
- Significant changes validated
- Compatibility impact assessed

#### Documentation Quality

- Consistent template usage
- Objective, evidence-based descriptions
- Concrete code references where relevant

#### Collaboration Efficiency

- Timely recording of findings
- Regular directional confirmations
- Stable execution cadence

### Workspace Management

#### Safety Principles

- Do not remove worktree immediately post-analysis
- Await user validation of deliverables
- Explicit permission before cleanup

#### Archival Discipline

- Copy workflow doc to task folder
- Update index completion states
- Move finalized documents to archive

## FAQ

### Q: How to handle massive version gaps?

**A**: Use staged decomposition plus frequent summarization to partition the change surface into manageable analytical units.

### Q: How to avoid missing critical changes?

**A**: Enforce bottom-up order, use templated recording, and continuously reconcile against the planned module checklist.

### Q: How to ensure objectivity?

**A**: Favor functional impact, avoid speculative interpretations, ground assertions in concrete diffs and commit metadata.

### Q: How to manage multiple concurrent diff tasks?

**A**: Create isolated task folders, maintain an index per task, and archive completed workflows under `workflow_archive`.

## Version & Maintenance

- Chinese Documentation: `version-comparison-system/README.md`
- Integrated Release: Introduced with project version v2.5.0
- Roadmap:
  - Add diff visualization scripts (planned)
  - Multi-hop sequential version comparison (planned)
  - Automated change classification tooling (planned)

---

**Last Updated**: 2025-08-13  
**System Integration Version**: v2.5.0  
**Design Foundation**: debug-system ≥ v2.3.4

**v1.0.0 Core Features**:

- Built on mature debug-system architecture
- Optimized for structured version comparison
- Safe workspace management via Git worktree
- Standardized analysis & reporting templates
