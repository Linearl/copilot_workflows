# Debug Workflow Templates

A comprehensive debugging workflow template package for systematic problem-solving and code debugging.

## � Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Templates](#-templates)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **Systematic Debugging Process**: 6-step debugging cycle for consistent problem-solving
- **Template Collection**: Pre-built templates for documentation and workflow management
- **Symbol Reference**: Comprehensive symbol guide for project organization
- **Human-AI Collaboration**: Optimized workflow for AI-assisted debugging
- **Modular Structure**: Organized file system for efficient debugging sessions

## � Project Structure

```
debug-system/
├── workflow_template_v2.md          # Core V2 workflow template
├── templates/                       # Template collection
│   ├── README-template.md           # Debug session documentation
│   ├── summary-template.md          # Project summary template
│   ├── experience-template.md       # Experience summary template
│   ├── INDEX-template.md            # Debug index template
│   └── SUMMARY-TEMPLATE-UPDATE.md   # Updated summary template
└── docs/
    └── 常用符号.md                   # Symbol reference guide
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Linearl/copilot_debug_workflow.git
cd copilot_debug_workflow
```

### 2. Create a New Debug Session

```powershell
# Copy the workflow template for your specific task
Copy-Item "debug-system\workflow_template_v2.md" "debug-system\workflow_[task-name]_v2.md"

# Initialize debug environment
mkdir debug; cd debug; $round = 1
mkdir $round\{src,core,archive,deprecated,docs,logs,files}
Copy-Item "..\debug-system\templates\README-template.md" "$round\README.md"
```

## 🔄 Usage

### The 6-Step Debug Cycle

| Step | Symbol | Phase | Core Task |
|------|--------|-------|-----------|
| 1 | 📋 | Planning | Define objectives and create plan |
| 2 | 🔍 | Analysis | Problem analysis and root cause identification |
| 3 | 💡 | Solution | Design approach and strategy selection |
| 4 | ⚙️ | Implementation | Code modification and testing |
| 5 | ✅ | Verification | Result validation and status confirmation |
| 6 | 📊 | Documentation | Update docs and organize files |

### File Organization System

| Symbol | Directory | File Type | Storage Rule |
|--------|-----------|-----------|--------------|
| 🔴 | core/ | Core solutions | 5-10 key files |
| 📚 | archive/ | Important milestones | Staged results |
| 🗑️ | deprecated/ | Obsolete/replaced | Discarded files |
| 📝 | docs/ | Analysis documents | Documentation |
| 📋 | logs/ | Test logs | Runtime records |
| 🗂️ | files/ | Other files | Supporting files |
| 🐍 | src/ | Working directory | Code and scripts during debugging |

## � Templates

The `debug-system/templates/` directory contains:

- **README-template.md**: Standard template for debugging session documentation
- **summary-template.md**: Project summary template for comprehensive reporting
- **experience-template.md**: Experience summary template for lessons learned
- **INDEX-template.md**: Debug index template for session organization
- **SUMMARY-TEMPLATE-UPDATE.md**: Updated version of summary template

## 📖 Documentation

### Core Debugging Principles

#### Minimal Working Set Debugging
- **Principle**: Create minimal isolated test environment
- **Application**: Isolate specific issues in complex systems
- **Process**: Simplify environment → Simplify data → Precise monitoring → Problem reproduction

#### Human-AI Collaboration Mode
- **AI Responsibility**: Analysis, suggestions, code generation
- **Human Responsibility**: Test execution, result confirmation, decision making
- **Collaboration Key**: Timely feedback on test results, clear description of phenomena

### Symbol Reference

For detailed symbol reference, see `debug-system/docs/常用符号.md` which includes:
- 🎯 Core symbol table: Common symbols and domain-specific symbols
- 📊 Complete symbol table: Comprehensive index of all project symbols
- 🎨 Usage guide: Best practices and usage standards
- 📋 Workflow template symbol usage guide
- 📑 Symbol quick reference

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Created**: June 21, 2025  
**Version**: v2.0  
**Use Cases**: Technical project debugging, problem troubleshooting, system optimization
