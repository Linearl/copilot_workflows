<#!
.SYNOPSIS
  清理版本对比分析创建的 worktree 及其输出文件。
.DESCRIPTION
  - 根据 setup snapshot 或参数指定路径进行安全清理
  - 可选择仅移除 worktree，保留分析输出
  - 校验清理条件(可通过 -Force 跳过)
.PARAMETER Path
  setup_worktree.ps1 使用时指定的输出根目录（包含 worktree_OLD / worktree_NEW 等）
.PARAMETER Snapshot
  指定 snapshot JSON 文件路径（覆盖默认 Path 推断）
.PARAMETER KeepOutputs
  保留差异输出文件（commits_overview.txt 等）
.PARAMETER Force
  跳过条件校验直接清理
.EXAMPLE
  ./cleanup_worktree.ps1 -Path analysis/worktree_v1.0.0_v1.1.0
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Path,
  [string]$Snapshot,
  [switch]$KeepOutputs,
  [switch]$Force,
  [Alias('h','help')][switch]$Help
)

set-strictmode -version latest
$ErrorActionPreference = 'Stop'

if($Help){
  @'
cleanup_worktree.ps1 - 清理由 setup_worktree.ps1 创建的 worktree 及输出
用法:
  ./cleanup_worktree.ps1 -Path <输出根目录> [-Snapshot <snapshot.json>] [-KeepOutputs] [-Force]
参数:
  -Path          setup_worktree 输出根目录
  -Snapshot      指定快照 JSON (默认 <Path>/worktree_setup_snapshot.json)
  -KeepOutputs   仅移除 worktree, 保留差异输出文件
  -Force         跳过交互确认与缺失文件警告
  -Help|-h       显示帮助
示例:
  ./cleanup_worktree.ps1 -Path analysis/wt_v1.0.0_v1.1.0 -KeepOutputs
'@ | Write-Host; return }

function Write-Step($m){ Write-Host "[STEP] $m" -ForegroundColor Cyan }
function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Write-Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[ERR ] $m" -ForegroundColor Red }

$Path = $Path.TrimEnd('/','\\')
if(-not (Test-Path $Path)){ throw "路径不存在: $Path" }

# 尝试读取 snapshot
if(-not $Snapshot){ $Snapshot = Join-Path $Path 'worktree_setup_snapshot.json' }
if(Test-Path $Snapshot){
  Write-Step "读取快照: $Snapshot"
  $snap = Get-Content $Snapshot -Raw | ConvertFrom-Json
  $oldWt = $snap.worktrees.old
  $newWt = $snap.worktrees.new
}else{
  Write-Warn "未找到快照，尝试推断 worktree 路径"
  $oldWt = Get-ChildItem -Directory $Path | Where-Object Name -like 'worktree_*' | Select-Object -First 1 | Select-Object -ExpandProperty FullName
  $newWt = Get-ChildItem -Directory $Path | Where-Object Name -like 'worktree_*' | Select-Object -Last 1 | Select-Object -ExpandProperty FullName
}

Write-Info "旧版本 worktree: $oldWt"
Write-Info "新版本 worktree: $newWt"

if(-not $Force){
  Write-Step "校验清理条件 (若无需校验可使用 -Force)"
  $required = @('commits_overview.txt','files_stat.txt','changed_files.txt')
  foreach($f in $required){
    $p = Join-Path $Path $f
    if(-not (Test-Path $p)){ Write-Warn "缺少输出文件: $f" }
  }
  $confirm = Read-Host '确认清理? (yes/no)'
  if($confirm -ne 'yes'){ Write-Host '已取消'; return }
}

function Remove-Worktree($wt){
  if(-not $wt -or -not (Test-Path $wt)){ Write-Warn "跳过不存在的 worktree: $wt"; return }
  Write-Info "移除 worktree: $wt"
  git worktree remove --force $wt 2>$null | Out-Null
}

Write-Step "移除 worktree"
Remove-Worktree $oldWt
Remove-Worktree $newWt

if(-not $KeepOutputs){
  Write-Step "清理输出文件"
  Get-ChildItem -Path $Path -File -Force | ForEach-Object { Remove-Item $_.FullName -Force }
}

Write-Step "完成"
