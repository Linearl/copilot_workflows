# Debug Workflow Templates

A comprehensive debugging workflow template package for systematic problem-solving and code debugging.

## 📋 Table of Contents

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

## 📁 Project Structure

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

### Workflow Document Usage

The core functionality of this package is the **workflow template document** (`workflow_template_v2.md`). Here's how to use it effectively:

#### Step 1: Copy Project to Your Workspace

```bash
# Clone or copy the project to your local workspace
git clone https://github.com/Linearl/copilot_debug_workflow.git
# Or copy the debug-system folder to your existing project
```

#### Step 2: Open Workflow Document in VS Code

```powershell
# Open the workflow template in VS Code
code debug-system/workflow_template_v2.md
```

#### Step 3: Enable Copilot Agent Mode

1. **Enable Agent Mode**: Use `@workspace` or agent commands in VS Code
2. **Start Debugging Session**: Follow the guidance in the workflow document

#### Step 4: Describe Your Problem and Start Debugging

Simply describe your problem in natural language - the workflow will handle the parsing and formatting automatically:

1. **Problem Description**: Describe your issue naturally, the agent will parse it
2. **AI Analysis**: Let the agent parse and understand your problem
3. **User Confirmation**: Review and confirm the agent's understanding
4. **Document Creation**: Agent creates task-specific workflow document
5. **Environment Setup**: Initialize organized debug workspace
6. **Debug Iteration**: Execute structured debugging cycles
7. **Documentation**: Record results and organize files

### 🤖 Agent Configuration Recommendations

#### Model and Settings

- **Preferred Model**: Use Claude 4.0 for best results
- **Enable Thinking Mode**: Turn on agent thinking mode for better analysis
- **Terminal Access**: Configure and enable terminal usage permissions

#### Budget and Control

- **Request Budget**: Set agent call budget to 10-20 requests per session
- **Budget Warning**: Too many requests may cause the agent to drift off-topic
- **Active Monitoring**: Monitor agent progress and intervene when necessary

#### Best Practices

⚠️ **Important**: If you notice the agent drifting off-topic or have new ideas, **pause immediately** and provide additional instructions.

- **Stay Engaged**: Actively review agent's analysis and suggestions
- **Provide Feedback**: Give clear feedback on agent's direction
- **Course Correction**: Don't hesitate to redirect when agent goes off-track

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

## 📚 Templates

The `debug-system/templates/` directory contains:

- **README-template.md**: Standard template for debugging session documentation
- **summary-template.md**: Project summary template for comprehensive reporting
- **experience-template.md**: Experience summary template for lessons learned
- **INDEX-template.md**: Debug index template for session organization
- **SUMMARY-TEMPLATE-UPDATE.md**: Updated version of summary template

## 📖 Documentation

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
