<#!
.SYNOPSIS
  汇总所有 Markdown 中的风险 (RSK-) 行，生成风险状态报告。
.DESCRIPTION
  扫描指定目录 (默认当前仓库) 下 .md 文件，匹配包含 RSK-<数字或字母> 的行，解析状态 (OPEN/MITIGATED/CLOSED/ACCEPTED 等)，输出：
    - risk_status.json
    - risk_status.md (Markdown 表)
  状态解析规则：行内首个 [OPEN] / [MITIGATED] / [CLOSED] / [ACCEPTED] / [DEFERRED] / [RETIRED] 标签（不区分大小写），否则状态 = UNKNOWN。
.PARAMETER Root 扫描根目录 (默认 .)
.PARAMETER OutputDir 输出目录 (默认 .)
.PARAMETER IdPattern 自定义 ID 正则 (默认 '^RSK-[A-Z0-9]{2,}')
.PARAMETER ExcludeDirs 要排除的目录名
.EXAMPLE
  ./risk-status-report.ps1 -Root . -OutputDir analysis/outputs
#>
[CmdletBinding()] param(
  [string]$Root='.',
  [string]$OutputDir='.',
  [string]$IdPattern='RSK-[A-Z0-9]{2,}',
  [string[]]$ExcludeDirs=@('.git','node_modules','dist','build','out'),
  [Alias('h','help')][switch]$Help
)
set-strictmode -version latest
$ErrorActionPreference='Stop'
function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Gray }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }

if($Help){
  @'
risk-status-report.ps1 - 汇总风险 ID 状态
用法:
  ./risk-status-report.ps1 -Root <目录> -OutputDir out [-IdPattern 'RSK-[A-Z0-9]{2,}'] [-ExcludeDirs .git,node_modules]
输出:
  risk_status.json / risk_status.md
说明:
  状态解析优先级: CLOSED < MITIGATED < ACCEPTED < DEFERRED < OPEN < RETIRED < UNKNOWN
'@ | Write-Host; return }

if(-not (Test-Path $OutputDir)){ New-Item -ItemType Directory -Path $OutputDir | Out-Null }

$statuses = 'OPEN','MITIGATED','CLOSED','ACCEPTED','DEFERRED','RETIRED'
$rxStatus = '(?i)\[(OPEN|MITIGATED|CLOSED|ACCEPTED|DEFERRED|RETIRED)\]'
$rxId = "(?i)($IdPattern)"
$records = @()

$files = Get-ChildItem -Path $Root -Recurse -Filter *.md | Where-Object { $ExcludeDirs -notcontains $_.Directory.Name }
foreach($f in $files){
  $ln=0
  foreach($line in (Get-Content $f.FullName)){
    $ln++
    if($line -match $rxId){
      $ids = [regex]::Matches($line,$rxId) | ForEach-Object { $_.Groups[1].Value.ToUpper() } | Select-Object -Unique
      $st = 'UNKNOWN'
      $m = [regex]::Match($line,$rxStatus)
      if($m.Success){ $st = $m.Groups[1].Value.ToUpper() }
      foreach($id in $ids){
        $records += [pscustomobject]@{ id=$id; status=$st; file=$f.FullName; line=$ln; content=$line.Trim() }
      }
    }
  }
}

if($records.Count -eq 0){ Warn '未发现任何风险 ID'; }
$grouped = $records | Group-Object id | ForEach-Object {
  $id = $_.Name
  $entries = $_.Group
  # 最新状态优先：按状态优先级 (CLOSED/MITIGATED/ACCEPTED/DEFERRED/OPEN/UNKNOWN) 取最优一个
  $priority = @{ 'CLOSED'=1; 'MITIGATED'=2; 'ACCEPTED'=3; 'DEFERRED'=4; 'OPEN'=5; 'RETIRED'=6; 'UNKNOWN'=7 }
  $final = $entries | Sort-Object { $priority[$_.status] } | Select-Object -First 1
  [pscustomobject]@{ id=$id; status=$final.status; occurrences=$entries.Count; files=($entries.file | Sort-Object -Unique); lines=($entries.line); samples=$entries.content[0] }
} | Sort-Object id

$jsonPath = Join-Path $OutputDir 'risk_status.json'
$mdPath = Join-Path $OutputDir 'risk_status.md'

$grouped | ConvertTo-Json -Depth 6 | Out-File -Encoding UTF8 $jsonPath

$md = @()
$md += '| ID | 状态 | 次数 | 文件计数 | 示例 |'
$md += '|----|------|------|----------|------|'
foreach($g in $grouped){
  $md += "| $($g.id) | $($g.status) | $($g.occurrences) | $((($g.files).Count)) | `"$([regex]::Escape($g.samples.Substring(0,[Math]::Min(80,$g.samples.Length))))`" |"
}
$md | Out-File -Encoding UTF8 $mdPath

Info "风险条目: $($grouped.Count)"
Info "输出: $jsonPath"
Info "输出: $mdPath"
