# 文件整理完整性验证脚本
# 用于验证文件整理过程的完整性和正确性

param(
    [Parameter(Mandatory=$true)]
    [string]$OriginalPath,
    
    [string]$OrganizedPath,
    
    [string]$BackupPath,
    
    [switch]$SkipEmptyCheck,
    
    [string]$ReportPath
)

function Test-DirectoryEmpty {
    param(
        [string]$Path,
        [string]$ExcludePath = $null
    )
    
    Write-Host "🔍 检查目录是否清空: $Path"
    
    $items = Get-ChildItem $Path -Recurse -Force
    
    # 排除已整理目录
    if ($ExcludePath) {
        $excludeRelative = [System.IO.Path]::GetRelativePath($Path, $ExcludePath)
        $items = $items | Where-Object { 
            $relative = [System.IO.Path]::GetRelativePath($Path, $_.FullName)
            -not $relative.StartsWith($excludeRelative)
        }
    }
    
    if ($items.Count -gt 0) {
        Write-Host "⚠️ 发现 $($items.Count) 个未处理的项目:" -ForegroundColor Yellow
        $items | ForEach-Object { Write-Host "  - $($_.FullName)" -ForegroundColor Yellow }
        return $false
    } else {
        Write-Host "✅ 目录已完全清空" -ForegroundColor Green
        return $true
    }
}

function Test-FileIntegrity {
    param(
        [string]$BeforePath,
        [string]$AfterPath
    )
    
    Write-Host "🔍 验证文件完整性..."
    
    $beforeFiles = Get-ChildItem $BeforePath -Recurse -File | Select-Object Name, Length, @{Name="RelativePath";Expression={[System.IO.Path]::GetRelativePath($BeforePath, $_.FullName)}}
    $afterFiles = Get-ChildItem $AfterPath -Recurse -File | Select-Object Name, Length, @{Name="RelativePath";Expression={[System.IO.Path]::GetRelativePath($AfterPath, $_.FullName)}}
    
    $beforeCount = $beforeFiles.Count
    $afterCount = $afterFiles.Count
    
    Write-Host "原始文件数: $beforeCount"
    Write-Host "整理后文件数: $afterCount"
    
    if ($beforeCount -eq $afterCount) {
        Write-Host "✅ 文件数量匹配" -ForegroundColor Green
        return $true
    } else {
        Write-Host "⚠️ 文件数量不匹配!" -ForegroundColor Yellow
        return $false
    }
}

function Test-Classification {
    param(
        [string]$OrganizedPath
    )
    
    Write-Host "🔍 验证文件分类..."
    
    # 定义分类规则
    $classificationRules = @{
        "01_学术教育资料" = @(".pdf", ".docx", ".doc", ".pptx", ".ppt")
        "02_政策法规文档" = @(".pdf", ".docx", ".doc")
        "03_商业投资资料" = @(".pdf", ".xlsx", ".xls", ".docx")
        "04_软件工具" = @(".exe", ".msi", ".zip", ".7z", ".rar")
        "05_办公文档" = @(".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt")
        "06_媒体文件" = @(".mp4", ".avi", ".mkv", ".jpg", ".png", ".gif")
        "07_数据分析" = @(".csv", ".xlsx", ".xls", ".json", ".xml")
        "99_待确认" = @()  # 任何类型都可以
    }
    
    $misclassified = @()
    $categories = Get-ChildItem $OrganizedPath -Directory
    
    foreach ($category in $categories) {
        $categoryName = $category.Name
        $expectedExtensions = $classificationRules[$categoryName]
        
        if ($expectedExtensions -and $expectedExtensions.Count -gt 0) {
            $files = Get-ChildItem $category.FullName -Recurse -File
            foreach ($file in $files) {
                $extension = $file.Extension.ToLower()
                if ($extension -notin $expectedExtensions) {
                    $misclassified += @{
                        File = $file.FullName
                        Category = $categoryName
                        Extension = $extension
                        Expected = $expectedExtensions -join ", "
                    }
                }
            }
        }
    }
    
    if ($misclassified.Count -gt 0) {
        Write-Host "⚠️ 发现 $($misclassified.Count) 个可能分类错误的文件:" -ForegroundColor Yellow
        $misclassified | ForEach-Object {
            Write-Host "  - $($_.File) (类型$($_.Extension), 期望$($_.Expected))" -ForegroundColor Yellow
        }
        return $false
    } else {
        Write-Host "✅ 文件分类验证通过" -ForegroundColor Green
        return $true
    }
}

function New-ValidationReport {
    param(
        [hashtable]$Results,
        [string]$ReportPath
    )
    
    $report = @{
        ValidationTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Results = $Results
        Summary = @{
            TotalChecks = $Results.Count
            PassedChecks = ($Results.Values | Where-Object { $_ -eq $true }).Count
            FailedChecks = ($Results.Values | Where-Object { $_ -eq $false }).Count
        }
    }
    
    if ($ReportPath) {
        $report | ConvertTo-Json -Depth 3 | Out-File $ReportPath -Encoding UTF8
        Write-Host "📄 验证报告已保存到: $ReportPath"
    }
    
    return $report
}

function Show-ValidationSummary {
    param([hashtable]$Results)
    
    Write-Host "`n" + "="*50
    Write-Host "📊 验证结果摘要" -ForegroundColor Cyan
    Write-Host "="*50
    
    $passed = 0
    $failed = 0
    
    foreach ($check in $Results.GetEnumerator()) {
        $status = if ($check.Value) { "✅ 通过" } else { "❌ 失败" }
        $color = if ($check.Value) { "Green" } else { "Red" }
        Write-Host "$($check.Key): $status" -ForegroundColor $color
        
        if ($check.Value) { $passed++ } else { $failed++ }
    }
    
    Write-Host "`n总计: $($Results.Count) 项检查"
    Write-Host "通过: $passed 项" -ForegroundColor Green
    Write-Host "失败: $failed 项" -ForegroundColor Red
    
    if ($failed -eq 0) {
        Write-Host "`n🎉 所有验证项目都通过了！整理工作完成得很好。" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️ 发现 $failed 个问题，请检查并修复。" -ForegroundColor Yellow
    }
    
    Write-Host "="*50
}

# 主程序
Write-Host "🔍 开始文件整理完整性验证..." -ForegroundColor Cyan
Write-Host "原始目录: $OriginalPath"
if ($OrganizedPath) { Write-Host "整理后目录: $OrganizedPath" }
if ($BackupPath) { Write-Host "备份目录: $BackupPath" }
Write-Host "-" * 50

$results = @{}

# 检查原目录是否清空
if (-not $SkipEmptyCheck) {
    $results["原目录清空检查"] = Test-DirectoryEmpty -Path $OriginalPath -ExcludePath $OrganizedPath
}

# 检查文件完整性
if ($BackupPath -and $OrganizedPath) {
    $results["文件完整性检查"] = Test-FileIntegrity -BeforePath $BackupPath -AfterPath $OrganizedPath
}

# 检查分类正确性
if ($OrganizedPath) {
    $results["文件分类检查"] = Test-Classification -OrganizedPath $OrganizedPath
}

# 生成报告
$report = New-ValidationReport -Results $results -ReportPath $ReportPath

# 显示摘要
Show-ValidationSummary -Results $results

# 返回总体结果
$overallSuccess = ($results.Values | Where-Object { $_ -eq $false }).Count -eq 0
exit $(if ($overallSuccess) { 0 } else { 1 })
