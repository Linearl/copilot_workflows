<#!
.SYNOPSIS
  校验分析与报告 Markdown 中的 ID 规范、唯一性与引用完整性。
.DESCRIPTION
  扫描指定根目录下所有 .md 文件，提取符合 (RSK|DISC|MOD|API|CMP)-[A-Z0-9]{2,} 模式的 ID：
    1. 统计各 ID 出现次数 (引用完整性参考)
    2. 统计各前缀分布 (风险/发现/模块/API/比较项)
    3. 识别大小写变体 (标准化为大写输出)
    4. 输出 JSON + Markdown 汇总 (便于后续报告引用)
  说明：当前无法精准区分“定义 vs 引用”，因此提供出现次数，人工判断是否缺少说明/首次定义。
.PARAMETER Root 扫描根目录 (默认当前目录)
.PARAMETER OutputDir 输出目录 (默认当前目录)
.PARAMETER Prefixes 允许的 ID 前缀集合
.PARAMETER FailOnDuplicate 若开启：当存在仅出现 1 次的关键 ID（潜在缺少引用）或非法 ID 时返回非零退出码
.PARAMETER ExcludeDirs 排除的目录名
.EXAMPLE
  ./validate-ids.ps1 -Root . -OutputDir analysis/任务/worktree_outputs
.EXAMPLE
  ./validate-ids.ps1 -Root version-comparison-system -FailOnDuplicate
#>
[CmdletBinding()] param(
  [string]$Root='.',
  [string]$OutputDir='.',
  [string[]]$Prefixes=@('RSK','DISC','MOD','API','CMP'),
  [switch]$FailOnDuplicate,
  [string[]]$ExcludeDirs=@('.git','node_modules','dist','build','out','.vs','.vscode'),
  [Alias('h','help')][switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERR ] $m" -ForegroundColor Red }

if($Help){
  @'
validate-ids.ps1 - 校验 ID 规范/唯一性/引用次数
用法:
  ./validate-ids.ps1 -Root <目录> -OutputDir out [-FailOnDuplicate] [-Prefixes RSK,DISC,MOD,API,CMP]
输出:
  id_validation.json / id_validation.md
策略:
  occurrences=1 的 ID 需人工确认是否缺少引用; invalid_like_ids 列出潜在格式问题。
'@ | Write-Host; return }

if(-not (Test-Path $Root)){ throw "Root 不存在: $Root" }
if(-not (Test-Path $OutputDir)){ New-Item -ItemType Directory -Path $OutputDir | Out-Null }

$prefixAlt = ($Prefixes | ForEach-Object { [regex]::Escape($_) }) -join '|'
$rxId = "\b(($prefixAlt)-[A-Z0-9]{2,})\b"
$rxLoose = "\b(($prefixAlt)-[A-Za-z0-9_-]{1,})\b"  # 捕获潜在格式不完全规范的 ID

$occurrences = @()   # { id, file, line, content }
$invalid = @()       # 非严格匹配但松散匹配到的

$files = Get-ChildItem -Path $Root -Recurse -Filter *.md | Where-Object { $ExcludeDirs -notcontains $_.Directory.Name }
foreach($f in $files){
  $ln = 0
  foreach($line in (Get-Content $f.FullName)){
    $ln++
    $strictMatches = [regex]::Matches($line,$rxId)
    if($strictMatches.Count -gt 0){
      foreach($m in $strictMatches){
        $id = $m.Groups[1].Value.ToUpper()
        $occurrences += [pscustomobject]@{ id=$id; file=$f.FullName; line=$ln; content=($line.Trim()) }
      }
    } else {
      $looseMatches = [regex]::Matches($line,$rxLoose)
      foreach($m in $looseMatches){
        $cand = $m.Groups[1].Value
        if(-not ($cand -cmatch '^[A-Z0-9-]+$')){ $cand = $cand.ToUpper() }
        # 如果松散匹配但不符合严格格式 -> 记录为 invalid
        if(-not ($cand -match $rxId)){
          $invalid += [pscustomobject]@{ candidate=$cand; file=$f.FullName; line=$ln; content=($line.Trim()) }
        }
      }
    }
  }
}

if($occurrences.Count -eq 0){ Warn '未发现任何符合规范的 ID'; }

# 汇总统计
$byId = $occurrences | Group-Object id | ForEach-Object {
  [pscustomobject]@{
    id = $_.Name
    occurrences = $_.Count
    files = ($_.Group.file | Sort-Object -Unique)
    lines = ($_.Group | ForEach-Object { @{ file=$_.file; line=$_.line } })
  }
} | Sort-Object id

$single = $byId | Where-Object occurrences -eq 1
$multi  = $byId | Where-Object occurrences -gt 1

$prefixSummary = $Prefixes | ForEach-Object {
  $p = $_
  $matchedIds = $byId | Where-Object { $_.id -like "$p-*" }
  [pscustomobject]@{
    prefix=$p
    distinct_ids=$matchedIds.Count
    total_occurrences=($matchedIds | Measure-Object occurrences -Sum).Sum
    single_occurrence=($matchedIds | Where-Object occurrences -eq 1).Count
    multi_occurrence=($matchedIds | Where-Object occurrences -gt 1).Count
  }
}

$invalidDistinct = $invalid | Group-Object candidate | ForEach-Object {
  [pscustomobject]@{ id=$_.Name; occurrences=$_.Count; samples=($_.Group | Select-Object -First 2 | ForEach-Object { "$(Split-Path $_.file -Leaf):$($_.line)" }) }
}

# 构建 JSON 结果
$result = [pscustomobject]@{
  scanned_root = (Resolve-Path $Root).Path
  prefixes = $Prefixes
  total_files = $files.Count
  total_ids_distinct = $byId.Count
  total_occurrences = ($byId | Measure-Object occurrences -Sum).Sum
  ids = $byId
  ids_single_occurrence = $single
  ids_multi_occurrence = $multi
  prefix_summary = $prefixSummary
  invalid_like_ids = $invalidDistinct
  generated_at = (Get-Date).ToString('s')
}

$jsonPath = Join-Path $OutputDir 'id_validation.json'
$mdPath = Join-Path $OutputDir 'id_validation.md'

$result | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $jsonPath

# Markdown 汇总
$md = @('# ID 校验报告','',"扫描根目录: $($result.scanned_root)","生成时间: $($result.generated_at)", '', '## 汇总指标', '', '| 指标 | 数值 |','|------|------|',"| 文件数 | $($result.total_files) |", "| 不重复 ID 数 | $($result.total_ids_distinct) |", "| 总引用次数 | $($result.total_occurrences) |", '', '## 按前缀统计','', '| 前缀 | 不重复ID | 引用总数 | 单次出现 | 多次出现 |','|------|----------|----------|-----------|-----------|')
foreach($p in $prefixSummary){ $md += "| $($p.prefix) | $($p.distinct_ids) | $($p.total_occurrences) | $($p.single_occurrence) | $($p.multi_occurrence) |" }

$md += '', '## 单次出现 (需确认是否缺少引用)', '', '| ID | 出现次数 | 文件 |', '|----|----------|------|'
foreach($i in $single){ $md += "| $($i.id) | $($i.occurrences) | $([string]::Join('<br/>',($i.files | ForEach-Object { Split-Path $_ -Leaf }))) |" }

$md += '', '## 多次出现 (正常或被多处引用)', '', '| ID | 次数 | 文件数 |', '|----|------|--------|'
foreach($i in $multi){ $md += "| $($i.id) | $($i.occurrences) | $($i.files.Count) |" }

if($invalidDistinct.Count -gt 0){
  $md += '', '## 可疑 / 非规范 ID (需修正)', '', '| 候选 | 次数 | 示例(文件:行) |','|------|------|----------------|'
  foreach($inv in $invalidDistinct){ $md += "| $($inv.id) | $($inv.occurrences) | $([string]::Join(', ',$inv.samples)) |" }
}

$md | Out-File -Encoding UTF8 $mdPath

Info "输出: $jsonPath"
Info "输出: $mdPath"

if($FailOnDuplicate){
  $hasProblem = $invalidDistinct.Count -gt 0 -or $single.Count -gt 0
  if($hasProblem){
    Err '存在单次出现或非法 ID (FailOnDuplicate 启用)'; exit 1
  }
}
