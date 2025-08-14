<#!
.SYNOPSIS
  从两个版本差异中提取潜在破坏性 API 变更候选 (函数/方法/类签名)。
.DESCRIPTION
  基于 git diff (统一补丁) 解析 +/- 行，匹配可能的函数/方法/类声明；尝试配对同名旧/新行标记为 MOD，否则为 ADD/DEL。
  结果输出：
    - breaking_api_candidates.txt  (Markdown 表)
    - breaking_api_candidates.json (结构化)
  注意：这是启发式扫描，仅用于候选提炼，需人工复核。
.PARAMETER Old 旧版本引用 (tag/branch/commit)
.PARAMETER New 新版本引用 (tag/branch/commit)
.PARAMETER OutputDir 输出目录 (默认当前目录)
.PARAMETER IncludeExt 需要扫描的扩展（默认常见代码扩展）
.PARAMETER MaxDiffSize 允许的最大 diff 行数（防止超大补丁 OOM），默认 200000 行
.EXAMPLE
  ./extract-breaking-api.ps1 -Old v1.0.0 -New v1.1.0 -OutputDir analysis/worktree_outputs
#>
[CmdletBinding()] param(
  [Parameter(Mandatory)][string]$Old,
  [Parameter(Mandatory)][string]$New,
  [string]$OutputDir = '.',
  [string[]]$IncludeExt = @('.py','.js','.ts','.tsx','.java','.cs','.go','.rb','.php','.cpp','.c','.h'),
  [int]$MaxDiffSize = 200000,
  [Alias('h','help')][switch]$Help
)

set-strictmode -version latest
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERR ] $m" -ForegroundColor Red }

if($Help){
  @'
extract-breaking-api.ps1 - 提取潜在破坏性 API 候选
用法:
  ./extract-breaking-api.ps1 -Old <旧> -New <新> [-OutputDir out] [-IncludeExt .py,.ts] [-MaxDiffSize N]
输出:
  breaking_api_candidates.txt / breaking_api_candidates.json
说明:
  启发式匹配 ADD/DEL/MOD, 需人工复核。
'@ | Write-Host; return }

if(-not (Test-Path .git)){ throw '请在 Git 仓库根目录运行。' }
if(-not (Test-Path $OutputDir)){ New-Item -ItemType Directory -Path $OutputDir | Out-Null }

$range = "$Old..$New"
Info "扫描 diff: $range"
# --unified=0 减少上下文, 仍保留 @@ hunk 行
$diff = git diff --unified=0 $range 2>$null
if(!$diff){ Warn "无差异"; return }
$lines = $diff -split "`n"
if($lines.Count -gt $MaxDiffSize){ throw "Diff 过大: $($lines.Count) 行 > $MaxDiffSize" }

$hunkFile = ''
$patternExt = ($IncludeExt | ForEach-Object { [regex]::Escape($_) }) -join '|'
# 可能的声明模式（粗略）
$declPatterns = @(
  '^(?<indent>\s*)(public|private|protected|internal)?\s*(static\s+)?[A-Za-z0-9_<>,\[\]:\*&]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', # C#/Java/C/C++ 函数
  '^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(',  # Python def
  '^\s*(export\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', # JS/TS function 声明
  '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\([^)]*\)\s*=>', # 箭头函数赋值
  '^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*', # 类定义
  '^func\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(' # Go
)

# 存储结构：name -> @{ old=@(签名集合); new=@(签名集合) }
$index = @{}
$results = @()

function Add-Decl([string]$name,[string]$sig,[string]$file,[string]$side){
  if(-not $index.ContainsKey($name)){
    $index[$name] = @{ old=@(); new=@() }
  }
  $index[$name][$side] += [pscustomobject]@{ file=$file; sig=$sig }
}

foreach($l in $lines){
  if($l -match '^diff --git a/(.+?) b/(.+)$') { continue }
  if($l -match '^\+\+\+ b/(.+)$'){ $pathNew = $Matches[1]; continue }
  if($l -match '^--- a/(.+)$'){ $pathOld = $Matches[1]; continue }
  if($l -match '^@@'){ continue }
  # 统一路径
  if($pathNew){ $hunkFile = $pathNew }
  if([string]::IsNullOrEmpty($hunkFile)){ continue }
  $ext = [IO.Path]::GetExtension($hunkFile)
  if($IncludeExt -notcontains $ext){ continue }
  # 仅解析 +/- 行
  if($l.Length -lt 2){ continue }
  $sideChar = $l[0]
  if($sideChar -ne '+' -and $sideChar -ne '-') { continue }
  $code = $l.Substring(1)
  foreach($pat in $declPatterns){
    if($code -match $pat){
      # 提取 name：最后一个捕获组中近似函数或类名
      $m = [regex]::Match($code,$pat)
      $name = ($m.Groups | Select-Object -Last 1).Value
      if([string]::IsNullOrEmpty($name)){ continue }
      $sig = ($code.Trim())
      $side = if($sideChar -eq '+'){ 'new' } else { 'old' }
      Add-Decl -name $name -sig $sig -file $hunkFile -side $side
      break
    }
  }
}

# 组装结果
foreach($k in $index.Keys){
  $entry = $index[$k]
  $olds = $entry.old
  $news = $entry.new
  if($olds.Count -gt 0 -and $news.Count -gt 0){
    # 可能修改
    $results += [pscustomobject]@{ change='MOD'; name=$k; old_sig=$olds[0].sig; new_sig=$news[0].sig; old_file=$olds[0].file; new_file=$news[0].file }
  } elseif($olds.Count -gt 0){
    $results += [pscustomobject]@{ change='DEL'; name=$k; old_sig=$olds[0].sig; new_sig=$null; old_file=$olds[0].file; new_file=$null }
  } elseif($news.Count -gt 0){
    $results += [pscustomobject]@{ change='ADD'; name=$k; old_sig=$null; new_sig=$news[0].sig; old_file=$null; new_file=$news[0].file }
  }
}

# 过滤明显非 API (例如内部匿名) — 可追加规则
$results = $results | Where-Object { $_.name -match '^[A-Za-z_]' }

# 输出
$txtPath = Join-Path $OutputDir 'breaking_api_candidates.txt'
$jsonPath = Join-Path $OutputDir 'breaking_api_candidates.json'

$md = @()
$md += '| 变更 | 名称 | 旧签名/文件 | 新签名/文件 |'
$md += '|------|------|-------------|-------------|'
foreach($r in $results){
  $oldBlock = if($r.old_sig){ "`"$($r.old_sig)`"<br/>$($r.old_file)" } else { '' }
  $newBlock = if($r.new_sig){ "`"$($r.new_sig)`"<br/>$($r.new_file)" } else { '' }
  $md += "| $($r.change) | $($r.name) | $oldBlock | $newBlock |"
}
$md | Out-File -Encoding UTF8 $txtPath
$results | ConvertTo-Json -Depth 4 | Out-File -Encoding UTF8 $jsonPath

Info "候选数: $($results.Count)"
Info "输出: $txtPath"
Info "输出: $jsonPath"
