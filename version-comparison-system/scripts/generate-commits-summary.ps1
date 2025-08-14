<#!
.SYNOPSIS
  生成 commits_summary.txt (Conventional Commits 分组汇总)。
.DESCRIPTION
  按给定版本区间 (Old..New) 提取提交，基于 Conventional Commits 前缀分类并输出：
    - 每类数量
    - 示例若干条（可控数量）
    - 未匹配类型归入 other
.PARAMETER Old 旧版本引用 (tag/branch/commit)
.PARAMETER New 新版本引用 (tag/branch/commit)
.PARAMETER Output 输出文件路径 (默认 commits_summary.txt)
.PARAMETER SamplesPerType 每个类型示例条数 (默认 5)
.PARAMETER Types 要识别的类型顺序 (默认 feat,fix,refactor,perf,docs,style,test,chore,build,ci)
.EXAMPLE
  ./generate-commits-summary.ps1 -Old v1.0.0 -New v1.1.0 -SamplesPerType 3
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Old,
  [Parameter(Mandatory)][string]$New,
  [string]$Output = 'commits_summary.txt',
  [int]$SamplesPerType = 5,
  [string[]]$Types = @('feat','fix','refactor','perf','docs','style','test','chore','build','ci'),
  [Alias('h','help')][switch]$Help
)

set-strictmode -version latest
$ErrorActionPreference = 'Stop'
if($Help){
  @'
generate-commits-summary.ps1 - 输出 Conventional Commits 分类摘要
用法:
  ./generate-commits-summary.ps1 -Old <旧> -New <新> [-SamplesPerType N] [-Types feat,fix,...]
示例:
  ./generate-commits-summary.ps1 -Old v1.0.0 -New v1.1.0 -SamplesPerType 3
输出:
  commits_summary.txt 含每类计数与示例
'@ | Write-Host; return }

if(-not (Test-Path .git)) { throw '需在 Git 仓库根目录运行。' }

$range = "$Old..$New"
$raw = git log --pretty=format:'%h|%ad|%s' --date=short $range
if(-not $raw){ Write-Warning "区间无提交: $range"; return }

$groups = @{}
foreach($t in $Types){ $groups[$t] = @() }
$groups['other'] = @()

$regex = '^(?<type>' + ($Types -join '|') + ')(\(.+?\))?:\s'
foreach($line in $raw){
  $parts = $line -split '\|',3
  if($parts.Count -lt 3){ continue }
  $hash,$date,$subject = $parts
  $m = [regex]::Match($subject,$regex)
  $type = if($m.Success){ $m.Groups['type'].Value } else { 'other' }
  $groups[$type] += [pscustomobject]@{ hash=$hash; date=$date; subject=$subject }
}

$total = ($raw | Measure-Object).Count
$outLines = @()
$outLines += "# Commits Summary ($Old -> $New)"
$outLines += "总提交数: $total"
$outLines += "生成时间: " + (Get-Date).ToString('s')
$outLines += ""

foreach($t in $Types + 'other'){
  $list = $groups[$t]
  if(-not $list -or $list.Count -eq 0){ continue }
  $outLines += "## $t ($($list.Count))"
  $outLines += ($list | Select-Object -First $SamplesPerType | ForEach-Object { "${_ .hash} - ${_ .subject} (${_ .date})" })
  if($list.Count -gt $SamplesPerType){ $outLines += "... (${($list.Count - $SamplesPerType)} more)" }
  $outLines += ""
}

$outLines | Out-File -Encoding UTF8 $Output
Write-Host "生成: $Output" -ForegroundColor Green
