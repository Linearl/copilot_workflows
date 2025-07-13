# 分析报告生成工具

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,
    
    [string]$OutputDir = "reports",
    [string]$ToolsPath = "tools",
    [switch]$SkipMetrics,
    [switch]$SkipComplexity,
    [switch]$SkipSecurity,
    [switch]$Verbose
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 日志函数
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    
    # 可选：写入日志文件
    $logFile = Join-Path $OutputDir "analysis.log"
    Add-Content -Path $logFile -Value $logMessage -ErrorAction SilentlyContinue
}

# 创建输出目录
function Initialize-OutputDirectory {
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
        Write-Log "创建输出目录: $OutputDir"
    }
}

# 验证项目路径
function Test-ProjectPath {
    if (-not (Test-Path $ProjectPath)) {
        Write-Error "项目路径不存在: $ProjectPath"
        exit 1
    }
    
    $pythonFiles = Get-ChildItem -Path $ProjectPath -Filter "*.py" -Recurse
    if ($pythonFiles.Count -eq 0) {
        Write-Warning "项目路径下未找到Python文件: $ProjectPath"
    }
    
    Write-Log "项目路径验证通过: $ProjectPath"
    Write-Log "发现 $($pythonFiles.Count) 个Python文件"
}

# 收集基础代码指标
function Invoke-MetricsCollection {
    if ($SkipMetrics) {
        Write-Log "跳过基础指标收集"
        return
    }
    
    Write-Log "开始收集基础代码指标..."
    
    $metricsScript = Join-Path $ToolsPath "code-metrics-collector.py"
    $outputFile = Join-Path $OutputDir "basic-metrics.json"
    
    if (Test-Path $metricsScript) {
        try {
            & python $metricsScript --project-path $ProjectPath --output $outputFile
            Write-Log "基础指标收集完成: $outputFile"
        }
        catch {
            Write-Warning "基础指标收集失败: $($_.Exception.Message)"
        }
    }
    else {
        Write-Warning "指标收集脚本不存在: $metricsScript"
    }
}

# 代码复杂度分析
function Invoke-ComplexityAnalysis {
    if ($SkipComplexity) {
        Write-Log "跳过复杂度分析"
        return
    }
    
    Write-Log "开始代码复杂度分析..."
    
    # 使用radon进行复杂度分析
    $outputFile = Join-Path $OutputDir "complexity-report.json"
    
    try {
        # 检查radon是否安装
        $radonCheck = & python -c "import radon; print('OK')" 2>$null
        if ($radonCheck -eq "OK") {
            & radon cc $ProjectPath -j > $outputFile
            Write-Log "复杂度分析完成: $outputFile"
        }
        else {
            Write-Warning "radon未安装，跳过复杂度分析。安装命令: pip install radon"
        }
    }
    catch {
        Write-Warning "复杂度分析失败: $($_.Exception.Message)"
    }
}

# 安全检查
function Invoke-SecurityScan {
    if ($SkipSecurity) {
        Write-Log "跳过安全检查"
        return
    }
    
    Write-Log "开始安全漏洞扫描..."
    
    $outputFile = Join-Path $OutputDir "security-report.json"
    
    try {
        # 检查bandit是否安装
        $banditCheck = & python -c "import bandit; print('OK')" 2>$null
        if ($banditCheck -eq "OK") {
            & bandit -r $ProjectPath -f json -o $outputFile
            Write-Log "安全扫描完成: $outputFile"
        }
        else {
            Write-Warning "bandit未安装，跳过安全检查。安装命令: pip install bandit"
        }
    }
    catch {
        Write-Warning "安全扫描失败: $($_.Exception.Message)"
    }
}

# 生成项目结构
function Export-ProjectStructure {
    Write-Log "导出项目结构..."
    
    $outputFile = Join-Path $OutputDir "project-structure.txt"
    
    try {
        # 使用tree命令（如果可用）
        if (Get-Command tree -ErrorAction SilentlyContinue) {
            & tree /f $ProjectPath > $outputFile
        }
        else {
            # 使用PowerShell递归列出文件
            Get-ChildItem -Path $ProjectPath -Recurse | 
                Select-Object FullName, @{Name="RelativePath";Expression={$_.FullName.Replace($ProjectPath, "")}} |
                Format-Table -AutoSize |
                Out-String > $outputFile
        }
        
        Write-Log "项目结构导出完成: $outputFile"
    }
    catch {
        Write-Warning "项目结构导出失败: $($_.Exception.Message)"
    }
}

# 代码风格检查
function Invoke-StyleCheck {
    Write-Log "开始代码风格检查..."
    
    $outputFile = Join-Path $OutputDir "style-report.txt"
    
    try {
        # 检查flake8是否安装
        $flake8Check = & python -c "import flake8; print('OK')" 2>$null
        if ($flake8Check -eq "OK") {
            & flake8 $ProjectPath --output-file=$outputFile --statistics
            Write-Log "代码风格检查完成: $outputFile"
        }
        else {
            Write-Warning "flake8未安装，跳过代码风格检查。安装命令: pip install flake8"
        }
    }
    catch {
        Write-Warning "代码风格检查失败: $($_.Exception.Message)"
    }
}

# 依赖关系分析
function Invoke-DependencyAnalysis {
    Write-Log "开始依赖关系分析..."
    
    $outputFile = Join-Path $OutputDir "dependencies.txt"
    
    try {
        # 查找requirements文件
        $requirementsFiles = @("requirements.txt", "requirements-dev.txt", "Pipfile", "pyproject.toml")
        $foundRequirements = @()
        
        foreach ($reqFile in $requirementsFiles) {
            $fullPath = Join-Path $ProjectPath $reqFile
            if (Test-Path $fullPath) {
                $foundRequirements += $fullPath
            }
        }
        
        if ($foundRequirements.Count -gt 0) {
            "=== 发现的依赖文件 ===" | Out-File $outputFile
            foreach ($file in $foundRequirements) {
                "文件: $file" | Out-File $outputFile -Append
                Get-Content $file | Out-File $outputFile -Append
                "---" | Out-File $outputFile -Append
            }
        }
        else {
            "未发现标准的依赖文件" | Out-File $outputFile
        }
        
        # 分析import语句
        "=== Python导入分析 ===" | Out-File $outputFile -Append
        $pythonFiles = Get-ChildItem -Path $ProjectPath -Filter "*.py" -Recurse
        $imports = @()
        
        foreach ($file in $pythonFiles) {
            $content = Get-Content $file.FullName
            $fileImports = $content | Select-String "^(import |from \w+)" | ForEach-Object { $_.Line.Trim() }
            $imports += $fileImports
        }
        
        $uniqueImports = $imports | Sort-Object -Unique
        $uniqueImports | Out-File $outputFile -Append
        
        Write-Log "依赖关系分析完成: $outputFile"
    }
    catch {
        Write-Warning "依赖关系分析失败: $($_.Exception.Message)"
    }
}

# 生成综合报告
function New-AnalysisReport {
    Write-Log "生成综合分析报告..."
    
    $reportFile = Join-Path $OutputDir "analysis-report.md"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # 报告头部
    $reportContent = @"
# 代码分析报告

**项目路径**: $ProjectPath
**分析时间**: $timestamp
**生成工具**: Analysis System v1.0

## 分析概要

"@
    
    # 读取基础指标
    $metricsFile = Join-Path $OutputDir "basic-metrics.json"
    if (Test-Path $metricsFile) {
        try {
            $metrics = Get-Content $metricsFile | ConvertFrom-Json
            $reportContent += @"

### 基础代码指标

- **Python文件数**: $($metrics.python_files)
- **代码行数**: $($metrics.code_lines)
- **函数数量**: $($metrics.total_functions)
- **类数量**: $($metrics.total_classes)
- **平均文件长度**: $([math]::Round($metrics.avg_file_length, 1)) 行

"@
        }
        catch {
            Write-Warning "读取基础指标失败: $($_.Exception.Message)"
        }
    }
    
    # 添加文件列表
    $reportContent += @"

## 生成的分析文件

"@
    
    $reportFiles = Get-ChildItem -Path $OutputDir -File
    foreach ($file in $reportFiles) {
        if ($file.Name -ne "analysis-report.md") {
            $reportContent += "- [$($file.Name)]($($file.Name))`n"
        }
    }
    
    $reportContent += @"

## 使用说明

1. 查看 `basic-metrics.json` 了解项目基础指标
2. 查看 `complexity-report.json` 了解代码复杂度分布
3. 查看 `security-report.json` 了解潜在安全问题
4. 查看 `style-report.txt` 了解代码风格问题
5. 查看 `project-structure.txt` 了解项目文件结构

## 下一步建议

根据分析结果，建议关注以下方面：

1. **代码质量**: 关注高复杂度的函数和类
2. **安全性**: 修复发现的安全漏洞
3. **代码风格**: 统一代码风格，提高可读性
4. **架构设计**: 分析模块依赖关系，优化架构

---
*报告生成时间: $timestamp*
"@
    
    $reportContent | Out-File $reportFile -Encoding UTF8
    Write-Log "综合报告生成完成: $reportFile"
}

# 主执行流程
function Main {
    Write-Log "=== 开始项目代码分析 ==="
    Write-Log "项目路径: $ProjectPath"
    Write-Log "输出目录: $OutputDir"
    
    try {
        # 初始化
        Initialize-OutputDirectory
        Test-ProjectPath
        
        # 执行各种分析
        Export-ProjectStructure
        Invoke-MetricsCollection
        Invoke-ComplexityAnalysis
        Invoke-StyleCheck
        Invoke-SecurityScan
        Invoke-DependencyAnalysis
        
        # 生成综合报告
        New-AnalysisReport
        
        Write-Log "=== 项目代码分析完成 ==="
        Write-Log "查看报告: $(Join-Path $OutputDir "analysis-report.md")"
        
        # 打开报告（可选）
        if ($env:OS -eq "Windows_NT") {
            $reportPath = Join-Path $OutputDir "analysis-report.md"
            if (Test-Path $reportPath) {
                Write-Log "正在打开分析报告..."
                Start-Process $reportPath
            }
        }
    }
    catch {
        Write-Error "分析过程中发生错误: $($_.Exception.Message)"
        exit 1
    }
}

# 执行主流程
Main
