<#!
.SYNOPSIS
  比较两个版本（Python / C / C++）代码行数与函数数量差异。
.DESCRIPTION
  支持两种模式：
    1) 直接使用 Git 引用 (Old/New) - 在当前仓库根目录下基于 git show/git ls-tree 读取文件内容（不写入磁盘）。
    2) 使用已存在的 worktree 目录路径（OldPath/NewPath），对物理文件扫描。
  输出：
    - 总体汇总 metrics_summary.json
    - 每文件行数与方法数差异 metrics_files.csv
  语言与方法识别策略（启发式，仅统计 Python / C / C++）：
    - Python: ^\s*(async\s+)?def\s+NAME\(
    - C/C++: 聚合多行函数签名，匹配 <ret+name(args){>
.PARAMETER Old Git 旧版本引用
.PARAMETER New Git 新版本引用
.PARAMETER OldPath 已检出旧版本目录（优先于 Old 引用）
.PARAMETER NewPath 已检出新版本目录（优先于 New 引用）
.PARAMETER IncludeExt 指定需要统计的文件扩展（默认 .py .c .cpp .h .hpp）
.PARAMETER OutputDir 输出目录，默认当前目录
.PARAMETER CsvDelimiter CSV 分隔符，默认逗号
.PARAMETER ApproximateLength 估算函数长度 (启发式) 并给出平均值
.EXAMPLE
  ./compare-code-metrics.ps1 -Old v1.0.0 -New v1.1.0 -OutputDir analysis/worktree_outputs
.EXAMPLE
  ./compare-code-metrics.ps1 -OldPath analysis/worktree_v1.0.0_v1.1.0/worktree_v1.0.0 -NewPath analysis/worktree_v1.0.0_v1.1.0/worktree_v1.1.0
#>
[CmdletBinding()] param(
  [string]$Old,
  [string]$New,
  [string]$OldPath,
  [string]$NewPath,
  [string[]]$IncludeExt = @('.py','.c','.cpp','.h','.hpp'),
  [string]$OutputDir = '.',
  [string]$CsvDelimiter = ',',
  [switch]$ApproximateLength,
  [Alias('h')][switch]$Help
)
set-strictmode -version latest
$ErrorActionPreference = 'Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }

if($Help){
  @'
compare-code-metrics.ps1 - Python/C/C++ 行 & 函数计数 (启发式)
模式:
  1) Git 引用: -Old <ref> -New <ref>
  2) 目录: -OldPath <dir旧> -NewPath <dir新>
选项:
  -ApproximateLength  估算函数长度 (C/C++ 基于大括号匹配; Python 基于缩进块)
示例:
  ./compare-code-metrics.ps1 -Old v1.0.0 -New v1.1.0 -ApproximateLength
输出:
  metrics_files.csv, metrics_summary.json (schema_version=2)
'@ | Write-Host; return }

if(-not (Test-Path $OutputDir)){ New-Item -ItemType Directory -Path $OutputDir | Out-Null }

# ---------------- 文件收集 ----------------
function Get-FilesFromGitTree($ref){
  git ls-tree -r --name-only $ref | Where-Object { $IncludeExt -contains ([IO.Path]::GetExtension($_)) }
}
function Get-FileContentFromGit($ref,$path){
  git show "$ref`:$path" 2>$null
}
function Get-FilesFromDir($dir){
  Get-ChildItem -Path $dir -Recurse -File | Where-Object { $IncludeExt -contains $_.Extension } | ForEach-Object { $_.FullName }
}

# ---------------- 函数计数 ----------------
function Get-FunctionsCountPython($content){
  $rx = '(?m)^\s*(async\s+)?def\s+[A-Za-z_][A-Za-z0-9_]*\s*\('
  return ([regex]::Matches($content,$rx)).Count
}
function Get-FunctionsListCpp($content){
  $results = @()
  $lines = $content -split "`n"
  $buffer = ''
  $paren = 0
  $lineNum = 0
  foreach($raw in $lines){
    $lineNum++
    $line = $raw
    if($line.Trim().StartsWith('//')){ continue }
    $buffer += ($line.Trim() + ' ')
    $open = ([regex]::Matches($line,'\(')).Count
    $close = ([regex]::Matches($line,'\)')).Count
    $paren += ($open - $close)
    $hasBrace = $line -match '{'
    $isEnd = ($paren -le 0) -and $hasBrace
    if($isEnd){
      $candidate = $buffer.Trim()
      if($candidate -notmatch ';\s*$' -and $candidate -notmatch '^(if|for|while|switch)\b'){
        $sigRx = '^[A-Za-z_][\w:\*<>,\s&]*\s+[A-Za-z_][A-Za-z0-9_:<>]*\s*\([^;{}]*\)\s*(const)?\s*\{'
        if($candidate -match $sigRx){ $results += [pscustomobject]@{ sig=$candidate; line=$lineNum } }
      }
      $buffer=''; $paren=0
    }
    if($buffer.Length -gt 4000){ $buffer=''; $paren=0 } # 防御
  }
  return $results
}
function Get-MethodsCount($ext,$content){
  switch($ext){
    '.py' { return Get-FunctionsCountPython $content }
    '.c' { return (Get-FunctionsListCpp $content).Count }
    '.cpp' { return (Get-FunctionsListCpp $content).Count }
    '.h' { return 0 }
    '.hpp' { return 0 }
    default { return 0 }
  }
}

# ---------------- 函数长度估算 ----------------
function Estimate-FunctionLengths($ext,$content){
  if(-not $ApproximateLength){ return @() }
  $result = @()
  $lines = $content -split "`n"
  if($ext -eq '.py'){
    for($i=0;$i -lt $lines.Count;$i++){
      # 修正正则 (原先字符类大小写拼写错误)
      $m = [regex]::Match($lines[$i],"^(?<indent>\s*)(async\s+)?def\s+(?<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(")
      if($m.Success){
        $baseIndent = $m.Groups['indent'].Value.Length
        $start = $i
        $j = $i + 1
        while($j -lt $lines.Count){
          $l = $lines[$j]
          if($l.Trim() -eq ''){ $j++; continue }
          $curIndent = ($l -replace '(\S.*)$','').Length
          if($curIndent -le $baseIndent -and ($l -notmatch '^\s*#')){ break }
          $j++
        }
        $len = ($j - $start)
        if($len -lt 1){ $len = 1 }
        $result += $len
      }
    }
  } elseif($ext -in @('.c','.cpp')){
    $funcs = Get-FunctionsListCpp $content
    $linesArr = $lines
    foreach($f in $funcs){
      $startIdx = [Math]::Max(0,$f.line - 1)
      $braceDepth = 0; $begun=$false
      for($k=$startIdx; $k -lt $linesArr.Count; $k++){
        $line = $linesArr[$k]
        $opens = ([regex]::Matches($line,'\{')).Count
        $closes = ([regex]::Matches($line,'\}')).Count
        if($opens -gt 0){ $braceDepth += $opens; $begun = $true }
        if($closes -gt 0){ $braceDepth -= $closes }
        if($begun -and $braceDepth -le 0){
          $len = ($k - $startIdx + 1)
          if($len -lt 1){ $len = 1 }
          $result += $len
          break
        }
        if(($k - $startIdx) -gt 20000){ break }
      }
    }
  }
  return $result
}

# ---------------- 主流程 ----------------
$mode = if($OldPath -and $NewPath){ 'dir' } elseif($Old -and $New){ 'git' } else { '' }
if(-not $mode){ throw "Must provide (Old,New) OR (OldPath,NewPath)." }

$oldFiles=@{}; $newFiles=@{}
if($mode -eq 'git'){
  foreach($f in (Get-FilesFromGitTree $Old)){ $oldFiles[$f]=$f }
  foreach($f in (Get-FilesFromGitTree $New)){ $newFiles[$f]=$f }
} else {
  $oldBase = (Resolve-Path $OldPath).Path
  $newBase = (Resolve-Path $NewPath).Path
  $oldLen = $oldBase.Length + 1
  $newLen = $newBase.Length + 1
  foreach($p in (Get-FilesFromDir $OldPath)){ $rel = $p.Substring($oldLen); $oldFiles[$rel]=$p }
  foreach($p in (Get-FilesFromDir $NewPath)){ $rel = $p.Substring($newLen); $newFiles[$rel]=$p }
}

$allKeys = ([System.Linq.Enumerable]::ToArray([System.Linq.Enumerable]::Distinct($oldFiles.Keys + $newFiles.Keys)))
$rows=@()
$totalOldLines=0; $totalNewLines=0; $totalOldFuncs=0; $totalNewFuncs=0
$lenOldAgg=@(); $lenNewAgg=@()

foreach($k in $allKeys){
  $oldContent=''; $newContent=''
  $ext = [IO.Path]::GetExtension($k)
  if($oldFiles.ContainsKey($k)){
    if($mode -eq 'git'){ $oldContent = Get-FileContentFromGit $Old $k } else { $oldContent = Get-Content -LiteralPath $oldFiles[$k] -Raw }
  }
  if($newFiles.ContainsKey($k)){
    if($mode -eq 'git'){ $newContent = Get-FileContentFromGit $New $k } else { $newContent = Get-Content -LiteralPath $newFiles[$k] -Raw }
  }
  $oldLines = if($oldContent -ne ''){ ($oldContent -split "`n").Count } else { 0 }
  $newLines = if($newContent -ne ''){ ($newContent -split "`n").Count } else { 0 }
  $oldFuncs = if($oldContent -ne ''){ Get-MethodsCount $ext $oldContent } else { 0 }
  $newFuncs = if($newContent -ne ''){ Get-MethodsCount $ext $newContent } else { 0 }
  if($ApproximateLength){
    if($oldContent -ne ''){ $lenOldAgg += (Estimate-FunctionLengths $ext $oldContent) }
    if($newContent -ne ''){ $lenNewAgg += (Estimate-FunctionLengths $ext $newContent) }
  }
  $totalOldLines += $oldLines; $totalNewLines += $newLines
  $totalOldFuncs += $oldFuncs; $totalNewFuncs += $newFuncs
  $rows += [pscustomobject]@{ file=$k; line_old=$oldLines; line_new=$newLines; line_diff=($newLines-$oldLines); func_old=$oldFuncs; func_new=$newFuncs; func_diff=($newFuncs-$oldFuncs) }
}

$csvPath = Join-Path $OutputDir 'metrics_files.csv'
$rows | Sort-Object file | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $csvPath -Delimiter $CsvDelimiter

$summary = [ordered]@{}
$summary.schema_version = 2
$summary.generated_at = (Get-Date).ToString('s')
$summary.mode = $mode
$summary.extensions_included = $IncludeExt
$summary.totals = [ordered]@{
  files = $allKeys.Count
  lines_old = $totalOldLines
  lines_new = $totalNewLines
  lines_diff = $totalNewLines - $totalOldLines
  funcs_old = $totalOldFuncs
  funcs_new = $totalNewFuncs
  funcs_diff = $totalNewFuncs - $totalOldFuncs
}
$summary.method_count_confidence = 'heuristic'
if($ApproximateLength){
  $avgOld = if($lenOldAgg.Count -gt 0){ [math]::Round(($lenOldAgg | Measure-Object -Average | Select-Object -ExpandProperty Average),2) } else { 0 }
  $avgNew = if($lenNewAgg.Count -gt 0){ [math]::Round(($lenNewAgg | Measure-Object -Average | Select-Object -ExpandProperty Average),2) } else { 0 }
  $summary.avg_function_length_est = [ordered]@{ old=$avgOld; new=$avgNew }
}
$summary.files_added = ($rows | Where-Object { $_.line_old -eq 0 -and $_.line_new -gt 0 } | ForEach-Object { $_.file })
$summary.files_removed = ($rows | Where-Object { $_.line_old -gt 0 -and $_.line_new -eq 0 } | ForEach-Object { $_.file })
$summary.files_modified = ($rows | Where-Object { $_.line_old -gt 0 -and $_.line_new -gt 0 -and $_.line_diff -ne 0 } | ForEach-Object { $_.file })

$jsonPath = Join-Path $OutputDir 'metrics_summary.json'
$summary | ConvertTo-Json -Depth 6 | Out-File -FilePath $jsonPath -Encoding UTF8

Info "Done: $csvPath, $jsonPath"
