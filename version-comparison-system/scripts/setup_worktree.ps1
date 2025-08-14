<#!
.SYNOPSIS
  创建版本对比所需的 Git worktree 并生成基础差异数据。
.DESCRIPTION
  - 验证版本标签是否存在
  - 创建分析输出目录
  - 生成提交概览、文件统计、变更文件清单
  - 输出一个 JSON 快照以供后续脚本解析
.PARAMETER Old
  旧版本标签或提交哈希
.PARAMETER New
  新版本标签或提交哈希
.PARAMETER Path
  目标工作区根目录（将创建 <Path>/worktree_<Old> 与 <Path>/worktree_<New> 子目录）
.PARAMETER Force
  若已存在输出文件是否覆盖
.EXAMPLE
  ./setup_worktree.ps1 -Old v1.0.0 -New v1.1.0 -Path analysis/worktree_v1.0.0_v1.1.0
.NOTES
  需在 Git 仓库根目录运行；PowerShell 5.1+/Core 兼容。
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Old,
  [Parameter(Mandatory)][string]$New,
  [Parameter(Mandatory)][string]$Path,
  [switch]$Force,
  [Alias('h','help')][switch]$Help
)

set-strictmode -version latest
$ErrorActionPreference = 'Stop'

if($Help){
  @'
setup_worktree.ps1 - 创建双版本 worktree 并生成基础差异文件
用法:
  ./setup_worktree.ps1 -Old <旧版本> -New <新版本> -Path <输出目录> [-Force]
参数:
  -Old        旧版本引用 (tag/commit)
  -New        新版本引用 (tag/commit)
  -Path       输出及 worktree 根目录
  -Force      已存在输出文件时覆盖
  -Help|-h    显示本帮助
输出文件:
  commits_overview.txt, files_stat.txt, changed_files.txt, module_stats.json, worktree_setup_snapshot.json
示例:
  ./setup_worktree.ps1 -Old v1.0.0 -New v1.1.0 -Path analysis/wt_v1.0.0_v1.1.0
'@ | Write-Host; return }

function Write-Step($msg){ Write-Host "[STEP] $msg" -ForegroundColor Cyan }
function Write-Info($msg){ Write-Host "[INFO] $msg" -ForegroundColor Gray }
function Write-Warn($msg){ Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg){ Write-Host "[ERR ] $msg" -ForegroundColor Red }

# 1. 基础检查
Write-Step "验证 Git 仓库"
if (-not (Test-Path .git)) { throw '当前目录不是 Git 仓库根目录。' }

function Test-GitRef($ref){
  git rev-parse --verify --quiet $ref > $null 2>&1
  return ($LASTEXITCODE -eq 0)
}

foreach($ref in @($Old,$New)){
  if(-not (Test-GitRef $ref)) { throw "版本引用不存在: $ref" }
}

# 2. 规范化路径
$Path = $Path.TrimEnd('/','\\')
$oldWt = Join-Path $Path "worktree_$Old"
$newWt = Join-Path $Path "worktree_$New"

# Windows 文件名中冒号等处理
$oldWt = $oldWt -replace '[:\\]','_'
$newWt = $newWt -replace '[:\\]','_'

# 3. 创建目录
Write-Step "创建分析输出目录: $Path"
New-Item -ItemType Directory -Path $Path -Force | Out-Null

# 4. 创建 worktree（若不存在）
function Add-Worktree($targetPath,$ref){
  if(Test-Path $targetPath){ Write-Warn "已存在: $targetPath (跳过创建)"; return }
  Write-Info "创建 worktree: $targetPath -> $ref"
  git worktree add $targetPath $ref | Out-Null
}

Write-Step "创建 Git worktree"
Add-Worktree -targetPath $oldWt -ref $Old
Add-Worktree -targetPath $newWt -ref $New

# 5. 生成差异数据
Write-Step "生成差异数据 (${Old}..${New})"
$commitsOverview = Join-Path $Path 'commits_overview.txt'
$filesStat        = Join-Path $Path 'files_stat.txt'
$changedFiles     = Join-Path $Path 'changed_files.txt'

if(-not (Test-Path $commitsOverview) -or $Force){ git log --oneline "$Old..$New" | Out-File -Encoding UTF8 $commitsOverview }
if(-not (Test-Path $filesStat) -or $Force){ git diff --stat "$Old..$New" | Out-File -Encoding UTF8 $filesStat }
if(-not (Test-Path $changedFiles) -or $Force){ git diff --name-only "$Old..$New" | Out-File -Encoding UTF8 $changedFiles }

# 6. 自动模块统计
Write-Step "生成模块统计"
$moduleStats = @()
$modules = git diff --name-only "$Old..$New" | ForEach-Object { ($_ -split '/')[0] } | Where-Object { $_ -match '^[A-Za-z_]' } | Sort-Object -Unique
foreach($m in $modules){
  $stat = git diff --numstat "$Old..$New" -- $m/ 2>$null | ForEach-Object {
    $parts = $_ -split "\t"; if($parts.Length -ge 3){ [pscustomobject]@{Add=[int]$parts[0];Del=[int]$parts[1]} }
  } | Measure-Object -Property Add -Sum
  $add = ($stat.Sum | ForEach-Object { $_ })
  $del = (git diff --numstat "$Old..$New" -- $m/ 2>$null | ForEach-Object { ($_ -split "\t")[1] } | ForEach-Object { [int]$_ } | Measure-Object -Sum).Sum
  $moduleStats += [pscustomobject]@{ module=$m; added=$add; deleted=$del }
}
$moduleStatsPath = Join-Path $Path 'module_stats.json'
$moduleStats | ConvertTo-Json -Depth 3 | Out-File -Encoding UTF8 $moduleStatsPath

# 7. 生成 JSON 快照
Write-Step "生成 setup 快照"
$snapshot = [pscustomobject]@{
  schema_version = 1
  old_version = $Old
  new_version = $New
  created_at = (Get-Date).ToString('s')
  worktrees = @{ old=$oldWt; new=$newWt }
  outputs = @{ commits_overview=$commitsOverview; files_stat=$filesStat; changed_files=$changedFiles; module_stats=$moduleStatsPath }
}
$snapshotPath = Join-Path $Path 'worktree_setup_snapshot.json'
$snapshot | ConvertTo-Json -Depth 5 | Out-File -Encoding UTF8 $snapshotPath

Write-Step "完成"
Write-Host "输出目录: $Path" -ForegroundColor Green
Write-Host "旧版本 worktree: $oldWt" -ForegroundColor Green
Write-Host "新版本 worktree: $newWt" -ForegroundColor Green
Write-Host "快照: $snapshotPath" -ForegroundColor Green
