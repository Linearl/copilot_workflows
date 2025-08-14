<#!
.SYNOPSIS
  校验版本对比分析产出之间的一致性 (alignment 检查)。
.DESCRIPTION
  对以下对象进行交叉校验并输出 alignment_report.json / alignment_report.md：
    - summary_metrics.json 与实际 git diff / git log 统计值 (commits/files/lines)
    - summary_metrics.json.enrichment.* 引用的 source 文件是否存在
    - metrics_summary.json / metrics_files.csv (可选存在时) 与 summary 核心计数关系
    - id_validation.json 中的 ID 与 version_comparison_report / update_log_draft 中引用情况
    - 关键字段缺失 / 数值不一致 / 文件缺失 列出详细 mismatch 明细
.PARAMETER AnalysisDir 分析任务根目录 (含 worktree_outputs)
.PARAMETER SummaryPath 指定 summary_metrics.json 路径 (默认 AnalysisDir/worktree_outputs/summary_metrics.json)
.PARAMETER MetricsSummaryPath 指定 metrics_summary.json 路径
.PARAMETER IdValidationPath 指定 id_validation.json 路径
.PARAMETER VersionReportPath 指定 version_comparison_report.md (若存在)
.PARAMETER UpdateLogDraftPath 指定 update_log_draft.md (若存在)
.PARAMETER OutputDir 输出目录 (默认 AnalysisDir/worktree_outputs)
.PARAMETER FailOnMismatch 若存在 mismatch 时以非零退出码结束
.EXAMPLE
  ./alignment-checker.ps1 -AnalysisDir analysis/1_xxx
#>
[CmdletBinding()] param(
  [Parameter(Mandatory)][string]$AnalysisDir,
  [string]$SummaryPath,
  [string]$MetricsSummaryPath,
  [string]$IdValidationPath,
  [string]$VersionReportPath,
  [string]$UpdateLogDraftPath,
  [string]$OutputDir,
  [switch]$FailOnMismatch,
  [Alias('h','help')][switch]$Help
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
if($Help){ @'
alignment-checker.ps1 - 分析产出一致性校验
必需: -AnalysisDir <目录>
可选: -SummaryPath -MetricsSummaryPath -IdValidationPath -VersionReportPath -UpdateLogDraftPath -OutputDir -FailOnMismatch
输出: alignment_report.json / alignment_report.md
检查: commits/files/lines 数值; enrichment 源文件存在; ID 引用覆盖; 缺失与差异。
'@|Write-Host;return }

# 解析默认路径
if(-not $OutputDir){ $OutputDir = Join-Path $AnalysisDir 'worktree_outputs' }
if(-not (Test-Path $OutputDir)){ New-Item -ItemType Directory -Path $OutputDir | Out-Null }
if(-not $SummaryPath){ $SummaryPath = Join-Path $OutputDir 'summary_metrics.json' }
if(-not $MetricsSummaryPath){ $MetricsSummaryPath = Join-Path $OutputDir 'metrics_summary.json' }
if(-not $IdValidationPath){ $IdValidationPath = Join-Path $OutputDir 'id_validation.json' }
if(-not $VersionReportPath){ $VersionReportPath = Join-Path $AnalysisDir 'summary' 'version_comparison_report.md' }
if(-not $UpdateLogDraftPath){ $UpdateLogDraftPath = Join-Path $AnalysisDir 'summary' 'update_log_draft.md' }

$mismatches=@(); $notes=@(); $missing=@();

# 读取 summary
$summary = $null
if(Test-Path $SummaryPath){
  try { $summary = Get-Content $SummaryPath -Raw | ConvertFrom-Json } catch { $mismatches += 'summary_metrics_json_parse_error' }
} else { $missing += 'summary_metrics.json' }

# 真实 git 统计（基于 summary.range）
$realStats = $null
if($summary -and $summary.range -match '^(?<o>[^>]+)->(?<n>.+)$'){
  $o=$Matches['o']; $n=$Matches['n']
  $realCommits = (git log --oneline "$o..$n" | Measure-Object).Count
  $realFiles   = (git diff --name-only "$o..$n" | Measure-Object).Count
  $added=0; $deleted=0
  git diff --numstat "$o..$n" | ForEach-Object { $p=$_ -split "\t"; if($p.Length -ge 3){ if($p[0] -match '^[0-9]+$'){ $added+=[int]$p[0] }; if($p[1] -match '^[0-9]+$'){ $deleted+=[int]$p[1] } } }
  $realStats=[pscustomobject]@{commits_total=$realCommits; files_changed=$realFiles; lines_added=$added; lines_deleted=$deleted}
  if($summary.commits_total -ne $realCommits){ $mismatches += 'commits_total_mismatch' }
  if($summary.files_changed -ne $realFiles){ $mismatches += 'files_changed_mismatch' }
  if($summary.lines_added -ne $added){ $mismatches += 'lines_added_mismatch' }
  if($summary.lines_deleted -ne $deleted){ $mismatches += 'lines_deleted_mismatch' }
}

# enrichment source 文件存在性
if($summary -and $summary.enrichment){
  foreach($sk in $summary.enrichment.PSObject.Properties.Name){
    if($sk -match '_source$'){
      $sp = $summary.enrichment.$sk
      if($sp -and -not (Test-Path $sp)){ $mismatches += "missing_source_file:$sp" }
    }
  }
}

# metrics_summary.json 存在时检查文件总数一致性（允许不一致只记录）
if(Test-Path $MetricsSummaryPath){
  try { $metricsSummary = Get-Content $MetricsSummaryPath -Raw | ConvertFrom-Json } catch { $mismatches += 'metrics_summary_json_parse_error' }
  if($metricsSummary){
    if($metricsSummary.totals.files -and $summary -and $metricsSummary.totals.files -lt  $summary.files_changed){ $notes += 'metrics_files_subset_of_changed_files' }
  }
}

# ID 校验覆盖
$idMap = @{}
if(Test-Path $IdValidationPath){
  try { $idJson = Get-Content $IdValidationPath -Raw | ConvertFrom-Json } catch { $mismatches += 'id_validation_json_parse_error' }
  if($idJson){
    foreach($item in $idJson.ids){ $idMap[$item.id] = $item }
  }
}
# 收集文档文本
$docText=''
if(Test-Path $VersionReportPath){ $docText += (Get-Content $VersionReportPath -Raw) + "`n" }
if(Test-Path $UpdateLogDraftPath){ $docText += (Get-Content $UpdateLogDraftPath -Raw) + "`n" }
if($docText -and $idMap.Count -gt 0){
  foreach($id in $idMap.Keys){
    $cnt = ([regex]::Matches($docText,[regex]::Escape($id))).Count
    if($cnt -eq 0){ $mismatches += "id_unreferenced:$id" }
  }
}

$summaryCore = $null
if($summary){ $summaryCore = [ordered]@{ commits_total=$summary.commits_total; files_changed=$summary.files_changed; lines_added=$summary.lines_added; lines_deleted=$summary.lines_deleted } }

# 构造 inputsOrdered 改为增量方式避免解析问题
$inputsOrdered = [ordered]@{}
$inputsOrdered.analysis_dir = $AnalysisDir
$inputsOrdered.summary_path = $SummaryPath
$inputsOrdered.metrics_summary_path = $MetricsSummaryPath
$inputsOrdered.id_validation_path = $IdValidationPath
$inputsOrdered.version_report_path = $VersionReportPath
$inputsOrdered.update_log_draft_path = $UpdateLogDraftPath

$report = [ordered]@{}
$report.schema_version = 1
$report.generated_at = (Get-Date).ToString('s')
$report.inputs = $inputsOrdered
$report.real_stats = $realStats
$report.summary_core = $summaryCore
$report.mismatches = $mismatches
$report.missing = $missing
$report.notes = $notes
$report.pass = ($mismatches.Count -eq 0 -and $missing.Count -eq 0)

$jsonOut = Join-Path $OutputDir 'alignment_report.json'
$mdOut   = Join-Path $OutputDir 'alignment_report.md'

$mdLines = @()
$mdLines += '# Alignment Report'
$mdLines += "生成时间: $($report.generated_at)"
$mdLines += ''
$mdLines += '## Core'
$mdLines += "- pass: $($report.pass)"
$mdLines += ''
$mdLines += '### Mismatches'
if($mismatches.Count){ foreach($m in $mismatches){ $mdLines += "- $m" } } else { $mdLines += '- (none)' }
$mdLines += ''
$mdLines += '### Missing'
if($missing.Count){ foreach($m in $missing){ $mdLines += "- $m" } } else { $mdLines += '- (none)' }
$mdLines += ''
$mdLines += '### Notes'
if($notes.Count){ foreach($m in $notes){ $mdLines += "- $m" } } else { $mdLines += '- (none)' }

$report | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $jsonOut
$mdLines | Out-File -Encoding UTF8 $mdOut
Info "已生成: $jsonOut, $mdOut"
if($FailOnMismatch -and -not $report.pass){ exit 2 }
