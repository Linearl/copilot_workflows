# 分析工具使用说明

## 🛠️ 工具概览

本目录包含项目代码分析所需的自动化工具，用于收集代码质量指标、生成分析报告等。

## 📁 工具列表

### 1. code-metrics-collector.py
**用途**: 收集Python项目的基础代码指标

**功能**:
- 统计代码行数、函数数、类数
- 计算代码复杂度
- 分析import依赖
- 生成JSON格式的指标报告

**使用方法**:
```bash
python code-metrics-collector.py --project-path /path/to/project --output metrics.json
```

**参数说明**:
- `--project-path`: 项目根目录路径（必需）
- `--output`: 输出文件路径（可选，默认为metrics.json）

**输出示例**:
```json
{
  "project_path": "/path/to/project",
  "python_files": 25,
  "code_lines": 1500,
  "total_functions": 120,
  "total_classes": 30,
  "avg_file_length": 60.0,
  "complexity_distribution": {
    "low": 20,
    "medium": 4,
    "high": 1,
    "very_high": 0
  }
}
```

### 2. generate-analysis-report.ps1
**用途**: 自动化分析报告生成工具

**功能**:
- 集成多种分析工具
- 生成综合分析报告
- 自动创建报告目录结构
- 支持多种分析类型的开关控制

**使用方法**:
```powershell
./generate-analysis-report.ps1 -ProjectPath "C:\path\to\project"
```

**参数说明**:
- `-ProjectPath`: 项目路径（必需）
- `-OutputDir`: 输出目录（可选，默认为reports）
- `-ToolsPath`: 工具目录（可选，默认为tools）
- `-SkipMetrics`: 跳过基础指标收集
- `-SkipComplexity`: 跳过复杂度分析
- `-SkipSecurity`: 跳过安全检查
- `-Verbose`: 详细输出

**生成的文件**:
- `analysis-report.md`: 综合分析报告
- `basic-metrics.json`: 基础代码指标
- `complexity-report.json`: 复杂度分析结果
- `security-report.json`: 安全检查结果
- `style-report.txt`: 代码风格检查
- `project-structure.txt`: 项目结构
- `dependencies.txt`: 依赖关系分析

## 🔧 环境准备

### Python依赖

分析工具需要以下Python包：

```bash
# 基础依赖（必需）
pip install ast

# 代码复杂度分析（推荐）
pip install radon

# 安全检查（推荐）
pip install bandit

# 代码风格检查（推荐）
pip install flake8

# 测试覆盖率（可选）
pip install coverage pytest-cov
```

### 系统要求

- **Python**: 3.7+
- **PowerShell**: 5.1+ (Windows) 或 PowerShell Core 6+ (跨平台)
- **操作系统**: Windows/Linux/macOS

## 📋 使用流程

### 1. 快速开始

```powershell
# 进入分析系统目录
cd workflow/analysis_system

# 执行完整分析
./tools/generate-analysis-report.ps1 -ProjectPath "."

# 查看报告
# 报告将保存在 reports/ 目录下
```

### 2. 自定义分析

```powershell
# 只收集基础指标
./tools/generate-analysis-report.ps1 -ProjectPath "." -SkipComplexity -SkipSecurity

# 指定输出目录
./tools/generate-analysis-report.ps1 -ProjectPath "." -OutputDir "custom-reports"

# 详细输出模式
./tools/generate-analysis-report.ps1 -ProjectPath "." -Verbose
```

### 3. 单独使用工具

```bash
# 只收集代码指标
python tools/code-metrics-collector.py --project-path . --output my-metrics.json

# 只进行复杂度分析
radon cc . -j > complexity.json

# 只进行安全检查
bandit -r . -f json -o security.json
```

## 📊 输出解读

### 基础指标说明

| 指标 | 说明 | 建议范围 |
|------|------|----------|
| 代码行数 | 有效代码行数（不含注释和空行） | - |
| 函数数量 | 项目中定义的函数总数 | - |
| 类数量 | 项目中定义的类总数 | - |
| 平均文件长度 | 每个文件的平均代码行数 | < 300行 |
| 最大文件长度 | 最长文件的代码行数 | < 500行 |

### 复杂度等级

| 等级 | 复杂度值 | 含义 | 建议 |
|------|----------|------|------|
| 低 (Low) | 1-5 | 简单，易理解 | 保持 |
| 中 (Medium) | 6-10 | 中等复杂 | 可接受 |
| 高 (High) | 11-20 | 较复杂 | 考虑重构 |
| 极高 (Very High) | >20 | 非常复杂 | 建议重构 |

### 安全风险等级

| 等级 | 说明 | 处理建议 |
|------|------|----------|
| 高危 | 严重安全漏洞 | 立即修复 |
| 中危 | 潜在安全风险 | 计划修复 |
| 低危 | 轻微安全问题 | 可选修复 |

## 🔍 故障排除

### 常见问题

#### 1. Python包未安装
**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**: 安装相应的Python包
```bash
pip install radon bandit flake8
```

#### 2. 编码问题
**错误**: `UnicodeDecodeError`

**解决**: 工具已自动处理常见编码问题，如仍出现问题，请检查文件编码

#### 3. 权限问题
**错误**: `Access denied` 或类似权限错误

**解决**: 确保对项目目录和输出目录有读写权限

#### 4. PowerShell执行策略
**错误**: `execution of scripts is disabled`

**解决**: 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 调试技巧

1. **使用-Verbose参数**: 获得详细的执行日志
2. **检查日志文件**: 查看 `reports/analysis.log`
3. **单独执行工具**: 逐个运行分析工具定位问题
4. **检查路径**: 确保所有路径使用绝对路径或正确的相对路径

## 🚀 扩展开发

### 添加新的分析工具

1. **创建分析脚本**: 在tools目录下创建新的分析脚本
2. **更新PowerShell脚本**: 在generate-analysis-report.ps1中添加新的分析函数
3. **更新文档**: 在本文档中添加新工具的说明

### 自定义指标收集

可以修改 `code-metrics-collector.py` 中的 `ASTVisitor` 类来收集自定义的代码指标。

### 报告模板定制

可以修改 `generate-analysis-report.ps1` 中的 `New-AnalysisReport` 函数来自定义报告格式。

## 📞 技术支持

如果在使用过程中遇到问题：

1. 查看本文档的故障排除部分
2. 检查工具的输出日志
3. 参考templates目录下的模板文件
4. 查看case-studies目录下的使用案例

---

**最后更新**: 2025年7月11日  
**工具版本**: v1.0  
**兼容性**: Python 3.7+, PowerShell 5.1+
