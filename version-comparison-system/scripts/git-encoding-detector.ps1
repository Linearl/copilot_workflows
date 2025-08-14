# Git Encoding Detector and Fixer v1.0
# Automatically detects git commit message encoding and provides correct commands

param(
    [Parameter(Mandatory=$true)]
    [string]$OldVersion,
    
    [Parameter(Mandatory=$true)]
    [string]$NewVersion,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = ".",
    
    [Parameter(Mandatory=$false)]
    [switch]$TestMode = $false
)

# Function to detect terminal encoding
function Get-TerminalEncoding {
    try {
        $currentEncoding = [Console]::OutputEncoding
        Write-Host "[INFO] Terminal encoding: $($currentEncoding.EncodingName)" -ForegroundColor Green
        return $currentEncoding
    } catch {
        Write-Host "[WARNING] Could not detect terminal encoding, using UTF-8" -ForegroundColor Yellow
        return [System.Text.Encoding]::UTF8
    }
}

# Function to extract commits with proper encoding
function Get-EncodingAwareCommits {
    param(
        [string]$FromTag,
        [string]$ToTag,
        [string]$OutputFile
    )
    
    Write-Host "[INFO] Extracting commits from $FromTag to $ToTag..." -ForegroundColor Cyan
    
    try {
        # Get commit list
        $commits = & git log --oneline --reverse "$FromTag..$ToTag"
        Write-Host "[SUCCESS] Found commits" -ForegroundColor Green
        
        if ($TestMode) {
            Write-Host "[TEST MODE] Would process commits" -ForegroundColor Magenta
            Write-Host "Sample commits:"
            $commits | Select-Object -First 5 | Write-Host
            return
        }
        
        # Save results
        $output = @"
# Git Commits with Encoding Information
# Generated: $(Get-Date)
# Range: $FromTag to $ToTag

$($commits -join "`n")
"@
        
        $output | Out-File -FilePath $OutputFile -Encoding UTF8
        Write-Host "[SUCCESS] Commits saved to: $OutputFile" -ForegroundColor Green
        
    } catch {
        Write-Host "[FAILED] Error extracting commits: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

# Function to validate git repository
function Test-GitRepository {
    try {
        $gitStatus = & git status 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Not in a git repository"
        }
        Write-Host "[SUCCESS] Git repository detected" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[FAILED] Git repository validation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to validate git tags
function Test-GitTags {
    param(
        [string]$OldVersion,
        [string]$NewVersion
    )
    
    try {
        # Check if tags exist
        $oldExists = & git tag -l $OldVersion
        $newExists = & git tag -l $NewVersion
        
        if (-not $oldExists) {
            throw "Tag $OldVersion not found"
        }
        
        if (-not $newExists) {
            throw "Tag $NewVersion not found"
        }
        
        Write-Host "[SUCCESS] Both tags validated: $OldVersion, $NewVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[FAILED] Tag validation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "=== Git Encoding Detector v1.0 ===" -ForegroundColor Cyan
Write-Host "[INFO] Processing version range: $OldVersion to $NewVersion" -ForegroundColor White

# Set UTF-8 encoding for PowerShell output
Write-Host "[INFO] Setting PowerShell output encoding to UTF-8..." -ForegroundColor Yellow
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "[INFO] Created output directory: $OutputDir" -ForegroundColor Green
}

# Validate environment
Write-Host "`n[STEP 1] Validating environment..." -ForegroundColor Yellow

if (-not (Test-GitRepository)) {
    exit 1
}

if (-not (Test-GitTags -OldVersion $OldVersion -NewVersion $NewVersion)) {
    exit 1
}

# Detect terminal encoding
Write-Host "`n[STEP 2] Detecting terminal encoding..." -ForegroundColor Yellow
$terminalEncoding = Get-TerminalEncoding

# Extract commits with encoding awareness
Write-Host "`n[STEP 3] Extracting commits..." -ForegroundColor Yellow
$commitsFile = Join-Path $OutputDir "commits_with_encoding.md"
Get-EncodingAwareCommits -FromTag $OldVersion -ToTag $NewVersion -OutputFile $commitsFile

Write-Host "`n=== Analysis Complete ===" -ForegroundColor Cyan
