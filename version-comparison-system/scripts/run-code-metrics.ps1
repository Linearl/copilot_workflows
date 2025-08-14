<#!
.SYNOPSIS
  聚合 Python/C/C++ 代码度量 (行/注释/空行/函数计数) 并输出统一 JSON。
.DESCRIPTION
  调用外部工具 (scc + universal-ctags) 收集代码统计, 合并为 metrics_code_enriched.json:
    - 语言维度: 代码行(code)/注释(comment)/空行(blank)/文件数(files)/函数数(functions)
    - 汇总 totals
    - sources 使用情况 + confidence 评估
  若某工具缺失则降级 (写入 warnings)。
  仅聚焦语言: Python / C / C++ (可通过 -Languages 调整)。
.PARAMETER Root 扫描根目录 (默认当前目录)
.PARAMETER OutputDir 输出目录 (默认当前目录)
.PARAMETER CtagsCmd ctags 可执行 (默认自动查找 "ctags")
.PARAMETER SccCmd scc 可执行 (默认自动查找 "scc")
.PARAMETER Languages 目标语言列表 (默认 Python,C,C++)
.PARAMETER IncludeHeaders 是否统计 .h/.hpp 头文件函数 (默认 开启)
.PARAMETER MaxFilesCtags ctags 解析最大文件数 (0=不限制)
.EXAMPLE
  ./run-code-metrics.ps1 -Root . -OutputDir analysis/worktree_outputs
.EXAMPLE
  ./run-code-metrics.ps1 -Root src -Languages Python,C -SccCmd scc.exe -CtagsCmd ctags.exe
.NOTES
  需预先安装: scc (https://github.com/boyter/scc) 与 universal-ctags。
#>
[CmdletBinding()]
param(
  [string]$Root='.',
  [string]$OutputDir='.',
  [string]$CtagsCmd='ctags',
  [string]$SccCmd='scc',
  [string[]]$Languages=@('Python','C','C++'),
  [switch]$IncludeHeaders,
  [int]$MaxFilesCtags=0,
  [Alias('h')][switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERR ] $m" -ForegroundColor Red }

if($Help){
@'
run-code-metrics.ps1 - 组合 scc + ctags 收集 Python/C/C++ 代码度量
用法:
  ./run-code-metrics.ps1 -Root <目录> -OutputDir <输出目录>
可选:
  -Languages Python,C,C++    自定义语言
  -IncludeHeaders             统计头文件内函数
输出:
  metrics_code_enriched.json
依赖:
  scc, universal-ctags (需在 PATH 或指定 -SccCmd/-CtagsCmd)
'@ | Write-Host; return }

if(-not (Test-Path $Root)){ throw "Root 不存在: $Root" }
if(-not (Test-Path $OutputDir)){ New-Item -ItemType Directory -Path $OutputDir | Out-Null }

$ctagsAvailable = $false; $sccAvailable=$false
try { if(Get-Command $CtagsCmd -ErrorAction Stop){ $ctagsAvailable=$true } } catch {}
try { if(Get-Command $SccCmd -ErrorAction Stop){ $sccAvailable=$true } } catch {}

$warnings=@()
if(-not $ctagsAvailable){ $warnings += 'ctags 不可用 (函数计数将缺失)'; Warn $warnings[-1] }
if(-not $sccAvailable){ $warnings += 'scc 不可用 (代码行/注释分布缺失)'; Warn $warnings[-1] }

# 结果容器
$languageStats = @{}
$functionsPerLang = @{}
$totalFunctions = 0

# ---------- scc 收集行统计 ----------
if($sccAvailable){
  Info '运行 scc (JSON)'
  $sccJsonPath = Join-Path $OutputDir 'scc_raw.json'
  & $SccCmd --format json --no-gen $Root 2>$null | Out-File -Encoding UTF8 $sccJsonPath
  $sccRaw = Get-Content $sccJsonPath -Raw | ConvertFrom-Json
  # scc 输出可能是数组: 每个语言对象 + 汇总代码对象 (Total)
  foreach($entry in $sccRaw){
    if($entry.Name){
      $langName = $entry.Name
      if($Languages -contains $langName){
        $languageStats[$langName] = [pscustomobject]@{ language=$langName; code=$entry.Code; comment=$entry.Comment; blank=$entry.Blank; files=$entry.Count; functions=0 }
      }
    }
  }
}

# ---------- ctags 收集函数 ----------
if($ctagsAvailable){
  Info '运行 ctags (JSON 行)' 
  $ctagsOut = Join-Path $OutputDir 'tags_raw.jsonl'
  $langArg = ($Languages -join ',')
  # universal-ctags JSON 每行一个对象
  & $CtagsCmd --languages=$langArg --fields=+n --extras=-F --output-format=json -R $Root 2>$null | Out-File -Encoding UTF8 $ctagsOut
  $lineCount=0
  Get-Content $ctagsOut | ForEach-Object {
    $line = $_.Trim(); if(-not $line){ return }
    if($line -like '!_*'){ return } # header 行
    $lineCount++
    try { $obj = $line | ConvertFrom-Json } catch { return }
    if(-not $obj.kind){ return }
    # 关注 kind=function 或者在 C/C++ 中方法/原型: function/prototype
    $k = $obj.kind
    $lang = $obj.language
    if(-not $lang){ return }
    if($Languages -notcontains $lang){ return }
    $isFunc = $false
    switch($lang){
      'Python' { if($k -eq 'function'){ $isFunc=$true } }
      'C' { if($k -in @('function','prototype')){ $isFunc=$true } }
      'C++' { if($k -in @('function','prototype')){ $isFunc=$true } }
      default { }
    }
    if($isFunc){
      if(-not $functionsPerLang.ContainsKey($lang)){ $functionsPerLang[$lang]=@() }
      $functionsPerLang[$lang] += $obj
    }
    if($MaxFilesCtags -gt 0 -and $lineCount -ge $MaxFilesCtags){ return }
  }
  foreach($lang in $functionsPerLang.Keys){
    $cnt = $functionsPerLang[$lang].Count
    $totalFunctions += $cnt
    if(-not $languageStats.ContainsKey($lang)){
      # 若 scc 未提供该语言条目, 初始化行统计未知
      $languageStats[$lang] = [pscustomobject]@{ language=$lang; code=$null; comment=$null; blank=$null; files=$null; functions=$cnt }
    } else {
      $languageStats[$lang].functions = $cnt
    }
  }
}

# 汇总 totals (防御空集合)
if($languageStats.Count -eq 0){
  $totals = [pscustomobject]@{ code=0; comment=0; blank=0; files=0; functions=$totalFunctions }
} else {
  $sumCodeObj = ($languageStats.Values | Where-Object { $_.code -ne $null })
  $sumCode = if($sumCodeObj){ ($sumCodeObj | Measure-Object -Property code -Sum).Sum } else { 0 }
  $sumCommentObj = ($languageStats.Values | Where-Object { $_.comment -ne $null })
  $sumComment = if($sumCommentObj){ ($sumCommentObj | Measure-Object -Property comment -Sum).Sum } else { 0 }
  $sumBlankObj = ($languageStats.Values | Where-Object { $_.blank -ne $null })
  $sumBlank = if($sumBlankObj){ ($sumBlankObj | Measure-Object -Property blank -Sum).Sum } else { 0 }
  $sumFilesObj = ($languageStats.Values | Where-Object { $_.files -ne $null })
  $sumFiles = if($sumFilesObj){ ($sumFilesObj | Measure-Object -Property files -Sum).Sum } else { 0 }
  $totals = [pscustomobject]@{ code=$sumCode; comment=$sumComment; blank=$sumBlank; files=$sumFiles; functions=$totalFunctions }
}

# 置信度
$confidence = if($ctagsAvailable -and $sccAvailable){ 'ctags+scc' } elseif($ctagsAvailable){ 'ctags-only' } elseif($sccAvailable){ 'scc-only' } else { 'none' }

$result = [pscustomobject]@{
  schema_version = 1
  root = (Resolve-Path $Root).Path
  languages = ($languageStats.Values | Sort-Object language)
  totals = $totals
  sources = @(@{ tool='ctags'; available=$ctagsAvailable }, @{ tool='scc'; available=$sccAvailable })
  confidence = $confidence
  warnings = $warnings
  generated_at = (Get-Date).ToString('s')
}

$outFile = Join-Path $OutputDir 'metrics_code_enriched.json'
$result | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $outFile

Info "输出: $outFile"
if($confidence -eq 'none'){ Warn '未获取到任何度量 (请安装工具)' }
