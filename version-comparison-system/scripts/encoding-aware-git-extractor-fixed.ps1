# Encoding-aware Git Information Extractor v2.0
# This script extracts git information with intelligent multi-encoding detection
# Supports: UTF-8, GBK, GB2312, Big5, ISO-8859-1
# Specifically designed for mixed-encoding git repositories

param(
    [Parameter(Mandatory=$true)]
    [string]$OldVersion,
    
    [Parameter(Mandatory=$true)]
    [string]$NewVersion,
    
    [Parameter(Mandatory=$true)]
    [string]$OutputDir
)

# Function to intelligently convert various encodings to UTF-8
function Convert-EncodingToUtf8 {
    param(
        [string]$inputText
    )
    
    if ([string]::IsNullOrEmpty($inputText)) {
        return ""
    }
    
    try {
        # Check for common garbled patterns and attempt conversion
        $encodingsToTry = @(
            @{ Name = "UTF-8"; Pattern = "^[\x00-\x7F]*$|[\u4e00-\u9fff]" },  # ASCII or valid Chinese
            @{ Name = "GBK"; Pattern = "[\u00C0-\u00FF]{2,}|锟斤拷" },         # GBK garbled patterns
            @{ Name = "GB2312"; Pattern = "[\u00A1-\u00FE]{2,}" },            # GB2312 patterns
            @{ Name = "Big5"; Pattern = "[\u00A1-\u00FE][\u00A1-\u00FE]" },   # Big5 patterns
            @{ Name = "ISO-8859-1"; Pattern = "[\u00C0-\u00FF]" }             # Latin-1 extended
        )
        
        # First check if it's already clean UTF-8
        if ($inputText -match "^[\x00-\x7F\u4e00-\u9fff\u0100-\u017F\u0400-\u04FF]*$") {
            return $inputText
        }
        
        # Try each encoding conversion
        foreach ($encoding in $encodingsToTry) {
            if ($inputText -match $encoding.Pattern) {
                try {
                    $sourceEncoding = [System.Text.Encoding]::GetEncoding($encoding.Name)
                    $bytes = $sourceEncoding.GetBytes($inputText)
                    $converted = [System.Text.Encoding]::UTF8.GetString($bytes)
                    
                    # Verify the conversion improved the text
                    if ($converted -ne $inputText -and $converted.Length -gt 0) {
                        Write-Verbose "Converted using $($encoding.Name): $inputText -> $converted"
                        return $converted
                    }
                }
                catch {
                    # Continue to next encoding if this one fails
                    continue
                }
            }
        }
        
        # If no conversion worked, try byte-level detection
        $textBytes = [System.Text.Encoding]::Default.GetBytes($inputText)
        
        # Attempt GBK conversion for Chinese systems
        try {
            $gbkEncoding = [System.Text.Encoding]::GetEncoding("GBK")
            $gbkResult = $gbkEncoding.GetString($textBytes)
            if ($gbkResult -match "[\u4e00-\u9fff]") {
                return $gbkResult
            }
        }
        catch { }
        
        # Return original if no conversion succeeded
        return $inputText
    }
    catch {
        return $inputText
    }
}

# Ensure output directory exists
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Host "Starting encoding-aware git information extraction..." -ForegroundColor Green
Write-Host "Old Version: $OldVersion" -ForegroundColor Yellow
Write-Host "New Version: $NewVersion" -ForegroundColor Yellow
Write-Host "Output Directory: $OutputDir" -ForegroundColor Yellow

# Step 1: Extract commit overview with encoding conversion
Write-Host "`n[1/6] Extracting commit overview..." -ForegroundColor Cyan

$commitOutput = git log --oneline "$OldVersion..$NewVersion" --encoding=UTF-8 2>&1
$commitList = @()
$suspiciousFiles = @()

foreach ($line in $commitOutput) {
    if ($line -and $line.ToString().Trim()) {
        $convertedLine = Convert-EncodingToUtf8 -inputText $line.ToString()
        $commitList += $convertedLine
        
        # Check for suspicious encoding patterns (expanded detection)
        if ($line.ToString() -match 'ï¿½|锟斤拷|\?\?\?|�{2,}' -or 
            $line.ToString() -match '[\x80-\xFF]{2,}') {
            $suspiciousFiles += "Commit: $line"
        }
    }
}

# Save commits overview
$commitsFile = Join-Path $OutputDir "commits_overview.txt"
$commitHeader = @"
# Commits Overview: $OldVersion to $NewVersion
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Total commits: $($commitList.Count)

"@

$commitHeader | Out-File -FilePath $commitsFile -Encoding UTF8
$commitList | Out-File -FilePath $commitsFile -Encoding UTF8 -Append

Write-Host "   Commits extracted: $($commitList.Count)" -ForegroundColor Green

# Step 2: Extract file statistics
Write-Host "`n[2/6] Extracting file statistics..." -ForegroundColor Cyan

$statsOutput = git diff --stat "$OldVersion..$NewVersion" 2>&1
$statsFile = Join-Path $OutputDir "files_stat.txt"

$statsHeader = @"
# File Statistics: $OldVersion to $NewVersion
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

"@

$statsHeader | Out-File -FilePath $statsFile -Encoding UTF8

foreach ($line in $statsOutput) {
    if ($line -and $line.ToString().Trim()) {
        $convertedLine = Convert-EncodingToUtf8 -inputText $line.ToString()
        $convertedLine | Out-File -FilePath $statsFile -Encoding UTF8 -Append
    }
}

Write-Host "   File statistics extracted" -ForegroundColor Green

# Step 3: Extract changed files list
Write-Host "`n[3/6] Extracting changed files list..." -ForegroundColor Cyan

$changedFilesOutput = git diff --name-only "$OldVersion..$NewVersion" 2>&1
$changedFiles = @()
$emptyFiles = @()

foreach ($line in $changedFilesOutput) {
    if ($line -and $line.ToString().Trim()) {
        $convertedLine = Convert-EncodingToUtf8 -inputText $line.ToString()
        $changedFiles += $convertedLine
        
        # Check if file exists and is empty
        $fullPath = Join-Path (Get-Location) $convertedLine
        if (Test-Path $fullPath) {
            $fileSize = (Get-Item $fullPath).Length
            if ($fileSize -eq 0) {
                $emptyFiles += $convertedLine
            }
        }
    }
}

# Save changed files
$changedFilesFile = Join-Path $OutputDir "changed_files.txt"
$changedFilesHeader = @"
# Changed Files: $OldVersion to $NewVersion
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Total files: $($changedFiles.Count)

"@

$changedFilesHeader | Out-File -FilePath $changedFilesFile -Encoding UTF8
$changedFiles | Out-File -FilePath $changedFilesFile -Encoding UTF8 -Append

Write-Host "   Changed files extracted: $($changedFiles.Count)" -ForegroundColor Green

# Step 4: Discover algorithm modules
Write-Host "`n[4/6] Discovering algorithm modules..." -ForegroundColor Cyan

$algorithmPattern = "^algorithm/"
$modules = $changedFiles | Where-Object { $_ -match $algorithmPattern } | ForEach-Object {
    $parts = $_ -split "/"
    if ($parts.Length -gt 1) {
        $parts[1]
    }
} | Sort-Object | Get-Unique

# Save discovered modules
$modulesFile = Join-Path $OutputDir "discovered_modules.txt"
$modulesHeader = @"
# Discovered Algorithm Modules: $OldVersion to $NewVersion
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Total modules: $($modules.Count)

"@

$modulesHeader | Out-File -FilePath $modulesFile -Encoding UTF8
$modules | Out-File -FilePath $modulesFile -Encoding UTF8 -Append

Write-Host "   Algorithm modules discovered: $($modules.Count)" -ForegroundColor Green

# Step 5: Generate module-specific statistics
Write-Host "`n[5/6] Generating module statistics..." -ForegroundColor Cyan

foreach ($module in $modules) {
    $moduleFiles = $changedFiles | Where-Object { $_ -match "^algorithm/$module/" }
    $moduleStatsFile = Join-Path $OutputDir "${module}_changes_stat.txt"
    
    $moduleHeader = @"
# Module Statistics: algorithm/$module
# Version Range: $OldVersion to $NewVersion
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Files changed: $($moduleFiles.Count)

"@

    $moduleHeader | Out-File -FilePath $moduleStatsFile -Encoding UTF8
    $moduleFiles | Out-File -FilePath $moduleStatsFile -Encoding UTF8 -Append
    
    Write-Host "     Module '$module': $($moduleFiles.Count) files" -ForegroundColor Gray
}

# Step 6: Generate summary report
Write-Host "`n[6/6] Generating summary report..." -ForegroundColor Cyan

$summaryFile = Join-Path $OutputDir "extraction_summary.txt"
$summaryContent = @"
# Git Information Extraction Summary v2.0
# Version Range: $OldVersion to $NewVersion
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# Encoding Support: UTF-8, GBK, GB2312, Big5, ISO-8859-1

## Extraction Results

- Commit Records: $(if ($commitList) { $commitList.Count } else { 0 }) items
- Changed Files: $(if ($changedFiles) { $changedFiles.Count } else { 0 }) files
- Discovered Modules: $(if ($modules) { $modules.Count } else { 0 }) modules
- Empty Files: $(if ($emptyFiles) { $emptyFiles.Count } else { 0 }) files
- Encoding Issues: $(if ($suspiciousFiles) { $suspiciousFiles.Count } else { 0 }) files

## Output Files

- commits_overview.txt - Commit records overview
- files_stat.txt - File change statistics  
- changed_files.txt - Changed files list
- discovered_modules.txt - Auto-discovered modules
- *_changes_stat.txt - Per-module change statistics

$(if ($emptyFiles -or $suspiciousFiles) {
@"

## WARNING: Issues Detected

$(if ($emptyFiles) {
@"
Empty Files Detected:
$($emptyFiles | ForEach-Object { "- $_" } | Out-String)
"@
})

$(if ($suspiciousFiles) {
@"
Encoding Issues Detected:
$($suspiciousFiles | ForEach-Object { "- $_" } | Out-String)
"@
})

Please review these files manually before proceeding with analysis.
"@
} else {
@"

## Status: Clean Extraction
No empty files or encoding issues detected.
Ready for analysis phase.
"@
})

## Algorithm Modules Discovered

$(if ($modules) {
$modules | ForEach-Object { "- algorithm/$_" } | Out-String
} else {
"No algorithm modules found in the changes."
})

## Next Steps

1. Review the extraction summary above
2. Check for any warnings or issues
3. Proceed to detailed analysis phase if clean
4. Manually inspect suspicious files if any warnings exist

"@

$summaryContent | Out-File -FilePath $summaryFile -Encoding UTF8

Write-Host "`nExtraction completed successfully!" -ForegroundColor Green
Write-Host "Summary report: $summaryFile" -ForegroundColor Yellow
Write-Host "Output directory: $OutputDir" -ForegroundColor Yellow

if ($emptyFiles -or $suspiciousFiles) {
    Write-Host "`nWARNING: Issues detected - please review the summary report" -ForegroundColor Red
} else {
    Write-Host "`nStatus: Clean extraction - ready for analysis" -ForegroundColor Green
}
