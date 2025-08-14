<#!
.SYNOPSIS
  生成版本对比的汇总指标 JSON (summary_metrics.json)。
.DESCRIPTION
  从 git diff / git log 及脚本输出文件生成机器可消费的指标：
    - commits_total / files_changed / lines_added / lines_deleted / modules_impacted
    - apis_breaking (候选数量或语义分类计数)
    - risks_open (来自风险状态 JSON 或启发式扫描)
    - 可选富集：读取 risk_status.json / breaking_api_candidates.json / module_impact.json / metrics_code_enriched.json
.PARAMETER Old 旧版本引用
.PARAMETER New 新版本引用
.PARAMETER Output 输出文件路径 (默认 summary_metrics.json)
.PARAMETER WorktreePath 已存在的 worktree 输出目录
.PARAMETER IncludeRiskScan 启用启发式 Markdown 风险扫描 (若 risk_status.json 未提供)
.PARAMETER BreakingApiCandidates 破坏性 API 候选文本文件（行计数）
.PARAMETER RiskStatusJson 指定 risk_status.json 路径用于精确风险统计 (优先于 IncludeRiskScan)
.PARAMETER BreakingApiJson 指定 breaking_api_candidates.json 或 semantic 分类 JSON，支持字段 candidates / removed / signature_changed 等
.PARAMETER ModuleImpactJson 指定 module_impact.json 以获取模块总数与 top_modules
.PARAMETER CodeMetricsJson 指定 metrics_code_enriched.json (run-code-metrics.ps1 输出) 以嵌入多语言代码统计
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Old,
  [Parameter(Mandatory)][string]$New,
  [string]$Output = 'summary_metrics.json',
  [string]$WorktreePath,
  [switch]$IncludeRiskScan,
  [string]$BreakingApiCandidates,
  [string]$RiskStatusJson,
  [string]$BreakingApiJson,
  [string]$ModuleImpactJson,
  [string]$CodeMetricsJson,
  [Alias('h','help')][switch]$Help
)

set-strictmode -version latest
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }

if($Help){
  @'
generate-summary-metrics.ps1 - 汇总版本区间核心指标
用法:
  ./generate-summary-metrics.ps1 -Old <旧> -New <新> [-Output <file>] \
    [-RiskStatusJson rs.json] [-BreakingApiJson ba.json] [-ModuleImpactJson mi.json] \
    [-CodeMetricsJson metrics_code_enriched.json] [-BreakingApiCandidates txt] [-IncludeRiskScan]
关键字段:
  commits_total / files_changed / lines_added / lines_deleted / modules_impacted / apis_breaking / risks_open
富集 (enrichment):
  risk_status_source / breaking_api_source / module_impact_source / code_metrics_source / top_modules / breaking_removed 等
示例:
  ./generate-summary-metrics.ps1 -Old v1.0.0 -New v1.1.0 -RiskStatusJson worktree_outputs/risk_status.json -BreakingApiJson worktree_outputs/breaking_api_candidates.json -ModuleImpactJson worktree_outputs/module_impact.json -CodeMetricsJson worktree_outputs/metrics_code_enriched.json
'@ | Write-Host; return }

# 基础数据收集
$commitsTotal = (git log --oneline "$Old..$New" | Measure-Object).Count
$filesChanged = (git diff --name-only "$Old..$New" | Measure-Object).Count

# 行级统计
$added = 0; $deleted = 0
$null = git diff --numstat "$Old..$New" | ForEach-Object {
  $p = $_ -split "\t"; if($p.Length -ge 3){
    if($p[0] -match '^[0-9]+$'){ $added += [int]$p[0] }
    if($p[1] -match '^[0-9]+$'){ $deleted += [int]$p[1] }
  }
}

# 模块影响 (基础)
$modulesImpacted = (git diff --name-only "$Old..$New" | ForEach-Object { ($_ -split '/')[0] } | Where-Object { $_ -match '^[A-Za-z_]' } | Sort-Object -Unique | Measure-Object).Count

# 破坏性 API (初始)
$apisBreaking = 0
if($BreakingApiCandidates -and (Test-Path $BreakingApiCandidates)){
  $apisBreaking = (Get-Content $BreakingApiCandidates | Where-Object { $_ -match '\S' } | Measure-Object).Count
}

$riskOpenHeuristic = 0
if($IncludeRiskScan){
  $mdFiles = Get-ChildItem -Recurse -Include *.md -ErrorAction SilentlyContinue
  foreach($f in $mdFiles){
    $content = Get-Content $f.FullName -Raw
    $rxMatches = [regex]::Matches($content,'RSK-[0-9A-Za-z_-]+.*?OPEN')
    $riskOpenHeuristic += $rxMatches.Count
  }
}

$enrichment = [ordered]@{}

# 富集：风险状态 JSON
$risksOpen = 0
if($RiskStatusJson -and (Test-Path $RiskStatusJson)){
  try {
    $riskJson = Get-Content $RiskStatusJson -Raw | ConvertFrom-Json
    if($riskJson -is [System.Collections.IEnumerable]){
      $risksOpen = ($riskJson | Where-Object { $_.status -eq 'OPEN' }).Count
      $enrichment.risk_status_source = $RiskStatusJson
    } elseif($riskJson.items){
      $risksOpen = ($riskJson.items | Where-Object { $_.status -eq 'OPEN' }).Count
      $enrichment.risk_status_source = $RiskStatusJson
    }
    $enrichment.risks_total = if($riskJson.items){ ($riskJson.items | Measure-Object).Count } elseif($riskJson){ ($riskJson | Measure-Object).Count } else { 0 }
  } catch { Warn "解析 RiskStatusJson 失败: $_" }
}
if(-not $risksOpen){ $risksOpen = $riskOpenHeuristic }

# 富集：breaking api JSON
if($BreakingApiJson -and (Test-Path $BreakingApiJson)){
  try {
    $bJson = Get-Content $BreakingApiJson -Raw | ConvertFrom-Json
    $enrichment.breaking_api_source = $BreakingApiJson
    if($bJson.candidates){ $apisBreaking = ($bJson.candidates | Measure-Object).Count }
    foreach($k in 'removed','signature_changed','visibility_changed','deprecated_added'){
      if($bJson.PSObject.Properties.Name -contains $k){
        $countVal = ($bJson.$k | Measure-Object).Count
        $enrichment["breaking_$k"] = $countVal
      }
    }
  } catch { Warn "解析 BreakingApiJson 失败: $_" }
}

# 富集：module impact JSON
if($ModuleImpactJson -and (Test-Path $ModuleImpactJson)){
  try {
    $mJson = Get-Content $ModuleImpactJson -Raw | ConvertFrom-Json
    if($mJson){
      $enrichment.module_impact_source = $ModuleImpactJson
      $enrichment.modules_listed = ($mJson | Measure-Object).Count
      $enrichment.top_modules = ($mJson | Sort-Object count -Descending | Select-Object -First 5 | ForEach-Object { $_.module })
      $modulesImpacted = $enrichment.modules_listed
    }
  } catch { Warn "解析 ModuleImpactJson 失败: $_" }
}

# 富集：代码度量 JSON (run-code-metrics 输出)
if($CodeMetricsJson -and (Test-Path $CodeMetricsJson)){
  try {
    $cJson = Get-Content $CodeMetricsJson -Raw | ConvertFrom-Json
    if($cJson){
      $enrichment.code_metrics_source = $CodeMetricsJson
      if($cJson.totals){ $enrichment.code_metrics_totals = $cJson.totals }
      if($cJson.languages){ $enrichment.code_metrics_languages = ($cJson.languages | Select-Object name code files blank comment) }
      if($cJson.confidence){ $enrichment.code_metrics_confidence = $cJson.confidence }
      if($cJson.warnings){ $enrichment.code_metrics_warnings = $cJson.warnings }
    }
  } catch { Warn "解析 CodeMetricsJson 失败: $_" }
}

$result = [ordered]@{
  schema_version = 2
  range = "$Old->$New"
  commits_total = $commitsTotal
  files_changed = $filesChanged
  lines_added = $added
  lines_deleted = $deleted
  modules_impacted = $modulesImpacted
  apis_breaking = $apisBreaking
  risks_open = $risksOpen
  generated_at = (Get-Date).ToString('s')
}
if($enrichment.Count -gt 0){ $result.enrichment = $enrichment }

$result | ConvertTo-Json -Depth 8 | Out-File -Encoding UTF8 $Output
Info "生成指标文件: $Output"
