<#!
.SYNOPSIS
  基于版本差异生成模块影响分析 (module_impact.md)。
.DESCRIPTION
  读取 changed_files 列表（可传入或自动通过 git diff 生成），按指定深度提取“模块键”聚合，输出：
    - module_impact.md  模块影响表（核心）
    - module_impact_auto.txt (可选 EmitAuto) 原始分组粗列
    - module_impact.json (可选 IncludeJSON) 结构化数据
  根目录文件归类为 _root。
.PARAMETER Old 旧版本引用 (如 tag/commit)。若提供则用于 diff 生成 changed_files。
.PARAMETER New 新版本引用。
.PARAMETER StageDir 阶段输出目录 (默认 stage_1_overview)。
.PARAMETER ChangedFilesPath 已存在的 changed_files.txt 路径；若未提供且 Old/New 存在则自动生成。
.PARAMETER Depth 计算模块键使用的路径层级深度 (默认1)。
.PARAMETER StripPrefix 要从文件路径起始处剥离的路径前缀 (支持多值，如 src/ 或 packages/)，剥离后再按 Depth 计算模块键。
.PARAMETER MinFiles 仅输出变更文件数 >= 此值的模块 (默认0 = 不过滤)。
.PARAMETER MaxSamples 表格中每个模块展示的文件样例数 (默认5)。
.PARAMETER EmitAuto 生成 module_impact_auto.txt 粗分组文件。
.PARAMETER IncludeJSON 额外生成 module_impact.json。
.PARAMETER OutputFile 输出 Markdown 文件名 (默认 module_impact.md)。
.EXAMPLE
  ./generate-module-impact.ps1 -Old v1.0.0 -New v1.1.0 -StageDir analysis/1_x/stage_1_overview -EmitAuto -IncludeJSON
.EXAMPLE
  ./generate-module-impact.ps1 -ChangedFilesPath analysis/1_x/stage_1_overview/changed_files.txt -StageDir analysis/1_x/stage_1_overview -StripPrefix src -Depth 2 -MinFiles 2
#>
[CmdletBinding()] param(
  [string]$Old,
  [string]$New,
  [string]$StageDir='stage_1_overview',
  [string]$ChangedFilesPath,
  [int]$Depth=1,
  [string[]]$StripPrefix,
  [int]$MinFiles=0,
  [int]$MaxSamples=5,
  [switch]$EmitAuto,
  [switch]$IncludeJSON,
  [string]$OutputFile='module_impact.md',
  [Alias('h','help')][switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERR ] $m" -ForegroundColor Red }

if($Help){
  @'
generate-module-impact.ps1 - 计算模块变更聚合
用法:
  ./generate-module-impact.ps1 -Old <旧> -New <新> [-StageDir dir] [-Depth N] [-StripPrefix src,packages] [-MinFiles 2] [-EmitAuto] [-IncludeJSON]
  或: -ChangedFilesPath changed_files.txt [-Depth N]
输出:
  module_impact.md (+ module_impact_auto.txt / module_impact.json)
说明:
  StripPrefix 可剥离公共前缀; MinFiles 过滤噪声; Depth 控制聚合层级。
'@ | Write-Host; return }

if(-not (Test-Path $StageDir)){ New-Item -ItemType Directory -Path $StageDir -Force | Out-Null }

# 决定 changed_files 来源
if(-not $ChangedFilesPath){
  if($Old -and $New){
    if(-not (Test-Path .git)){ throw '需要在 Git 仓库根目录或其子目录执行 (缺少 .git)。' }
    $ChangedFilesPath = Join-Path $StageDir 'changed_files.txt'
    Info "生成 changed_files.txt: git diff --name-only $Old..$New"
    git diff --name-only "$Old..$New" | Where-Object { $_ } | Set-Content -Encoding UTF8 $ChangedFilesPath
  } else {
    throw '必须提供 ChangedFilesPath 或 (Old 与 New)。'
  }
}
if(-not (Test-Path $ChangedFilesPath)){ throw "找不到 changed files 列表: $ChangedFilesPath" }

$files = Get-Content $ChangedFilesPath | Where-Object { $_ -and -not ($_ -match '^\s*$') }
if($files.Count -eq 0){ Warn 'changed_files 列表为空'; }

# 归一化函数
function Normalize-PathPrefix($path){
  $p = $path.Trim()
  foreach($pre in ($StripPrefix | Sort-Object Length -Descending)){
    if([string]::IsNullOrWhiteSpace($pre)){ continue }
    $pp = $pre.TrimEnd('/','\\') + '/'
    if($p.StartsWith($pp, [System.StringComparison]::OrdinalIgnoreCase)){
      $p = $p.Substring($pp.Length)
      break
    }
  }
  return $p
}

$map = @{}
foreach($f in $files){
  $clean = $f.Trim()
  if($clean -match '^\.?/'){ $clean = $clean -replace '^\./','' }
  $norm = if($StripPrefix){ Normalize-PathPrefix $clean } else { $clean }
  $parts = $norm -split '/'
  if($parts.Count -lt $Depth){
    $key = ($parts -join '/')
  } else {
    $key = ($parts[0..($Depth-1)] -join '/')
  }
  if([string]::IsNullOrWhiteSpace($key)){ $key = '_root' }
  if(-not $map.ContainsKey($key)){ $map[$key] = @() }
  $map[$key] += $clean  # 原始路径保留
}

# 最小文件数过滤
if($MinFiles -gt 0){
  foreach($k in ($map.Keys)){ if($map[$k].Count -lt $MinFiles){ $map.Remove($k) } }
}

if($map.Keys.Count -eq 0){ Warn '未聚合出任何模块键 (可能全部被过滤)。'; }

# 生成 auto 文件 (可选)
if($EmitAuto){
  $autoPath = Join-Path $StageDir 'module_impact_auto.txt'
  $autoLines = @()
  foreach($k in ($map.Keys | Sort-Object { $map[$_].Count } -Descending)){
    $autoLines += "### $k (files=$($map[$k].Count))"
    foreach($fp in $map[$k]){ $autoLines += "- $fp" }
    $autoLines += ''
  }
  $autoLines | Out-File -Encoding UTF8 $autoPath
  Info "输出: $autoPath"
}

# 生成 Markdown 核心文件
$outPath = Join-Path $StageDir $OutputFile
$md = @('# 模块影响分析','',"> 由脚本 generate-module-impact.ps1 自动生成，可在下方补充分析。",'',"参数: Depth=$Depth  ChangedFiles=$(Split-Path -Leaf $ChangedFilesPath) StripPrefix=[${StripPrefix -join ','}] MinFiles=$MinFiles",'',"| 模块 | 变更文件数 | 示例 (最多"+$MaxSamples+") |","|------|------------|----------------|")
foreach($k in ($map.Keys | Sort-Object { $map[$_].Count } -Descending)){
  $all = $map[$k]
  $samples = $all | Select-Object -First $MaxSamples
  $md += "| $k | $($all.Count) | `\"$([string]::Join(', ',$samples))`\" |"
}
$md += '','## 待补充','- 优先级: 按变更文件数 + 风险 (后续 RSK) + 破坏性 API 交叉判定','- 每模块补充: 行为影响 / 风险 (RSK-) / 破坏性 API / 依赖影响 / 升级注意',''
$md | Out-File -Encoding UTF8 $outPath
Info "输出: $outPath"

if($IncludeJSON){
  $jsonObj = @()
  foreach($k in $map.Keys){
    $jsonObj += [pscustomobject]@{ module=$k; files=$map[$k]; count=$map[$k].Count; depth=$Depth; strip_prefix=$StripPrefix; min_files=$MinFiles }
  }
  $jsonPath = Join-Path $StageDir 'module_impact.json'
  $jsonObj | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $jsonPath
  Info "输出: $jsonPath"
}
