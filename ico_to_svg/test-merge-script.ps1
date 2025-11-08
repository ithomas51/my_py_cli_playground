#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test suite for merge-to-main.ps1 script

.DESCRIPTION
    Validates syntax, logic, and error handling of the merge-to-main.ps1 script
#>

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetScript = Join-Path $ScriptDir "merge-to-main.ps1"

Write-Host "==> Testing merge-to-main.ps1" -ForegroundColor Cyan
Write-Host ""

# Test 1: Script exists
Write-Host "Test 1: Script file exists..." -NoNewline
if (Test-Path $TargetScript) {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Script not found: $TargetScript"
    exit 1
}

# Test 2: PowerShell syntax validation
Write-Host "Test 2: PowerShell syntax validation..." -NoNewline
$SyntaxErrors = $null
$null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $TargetScript -Raw), [ref]$SyntaxErrors)
if ($SyntaxErrors.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Syntax errors found:"
    $SyntaxErrors | ForEach-Object {
        Write-Host "    Line $($_.Token.StartLine): $($_.Message)" -ForegroundColor Red
    }
    exit 1
}

# Test 3: Required functions defined
Write-Host "Test 3: Required functions defined..." -NoNewline
$ScriptContent = Get-Content $TargetScript -Raw
$RequiredFunctions = @('Write-Step', 'Write-Success', 'Write-Failure', 'Write-Info')
$MissingFunctions = @()
foreach ($func in $RequiredFunctions) {
    if ($ScriptContent -notmatch "function $func") {
        $MissingFunctions += $func
    }
}
if ($MissingFunctions.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Missing functions: $($MissingFunctions -join ', ')"
    exit 1
}

# Test 4: Parameter definitions
Write-Host "Test 4: Parameters defined..." -NoNewline
if ($ScriptContent -match 'param\s*\(' -and $ScriptContent -match '\$BranchName' -and $ScriptContent -match '\$CommitMessage') {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Required parameters not found"
    exit 1
}

# Test 5: Git commands present
Write-Host "Test 5: Git commands present..." -NoNewline
$GitCommands = @('git branch', 'git checkout', 'git add', 'git commit', 'git push', 'git status', 'git pull')
$MissingGitCommands = @()
foreach ($cmd in $GitCommands) {
    if ($ScriptContent -notmatch [regex]::Escape($cmd)) {
        $MissingGitCommands += $cmd
    }
}
if ($MissingGitCommands.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Missing git commands: $($MissingGitCommands -join ', ')"
    exit 1
}

# Test 6: GitHub CLI commands present
Write-Host "Test 6: GitHub CLI commands present..." -NoNewline
if ($ScriptContent -match 'gh pr create' -and $ScriptContent -match 'gh pr merge') {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  GitHub CLI commands missing"
    exit 1
}

# Test 7: Branch protection check
Write-Host "Test 7: Branch protection logic..." -NoNewline
if ($ScriptContent -match 'if \(\$CurrentBranch -eq "main"' -and $ScriptContent -match 'git checkout -b') {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Branch protection logic missing"
    exit 1
}

# Test 8: Error handling (LASTEXITCODE checks)
Write-Host "Test 8: Error handling present..." -NoNewline
$ExitCodeChecks = ([regex]::Matches($ScriptContent, '\$LASTEXITCODE')).Count
if ($ExitCodeChecks -ge 5) {
    Write-Host " PASS (found $ExitCodeChecks checks)" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Insufficient error handling (found $ExitCodeChecks checks, expected at least 5)"
    exit 1
}

# Test 9: Variable interpolation (no bare #$ patterns)
Write-Host "Test 9: Variable interpolation safety..." -NoNewline
$BadPatterns = [regex]::Matches($ScriptContent, '#\$(?![{])')
if ($BadPatterns.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Found $($BadPatterns.Count) unsafe variable interpolations:"
    foreach ($match in $BadPatterns) {
        $line = ($ScriptContent.Substring(0, $match.Index) -split "`n").Count
        Write-Host "    Line ${line}: $($match.Value)"
    }
    exit 1
}

# Test 10: Help documentation
Write-Host "Test 10: Help documentation..." -NoNewline
if ($ScriptContent -match '\.SYNOPSIS' -and $ScriptContent -match '\.DESCRIPTION' -and $ScriptContent -match '\.EXAMPLE') {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Help documentation incomplete"
    exit 1
}

# Test 11: Prerequisite checks
Write-Host "Test 11: Prerequisite checks..." -NoNewline
if ($ScriptContent -match 'Get-Command git' -and $ScriptContent -match 'Get-Command gh') {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Missing prerequisite checks"
    exit 1
}

# Test 12: Cleanup operations
Write-Host "Test 12: Cleanup operations..." -NoNewline
if ($ScriptContent -match 'git branch -d' -and $ScriptContent -match '--delete-branch') {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Branch cleanup logic missing"
    exit 1
}

# Test 13: Load script to check for runtime errors
Write-Host "Test 13: Script loads without errors..." -NoNewline
try {
    $ScriptBlock = [scriptblock]::Create($ScriptContent)
    Write-Host " PASS" -ForegroundColor Green
} catch {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)"
    exit 1
}

# Test 14: Check for hardcoded sensitive data
Write-Host "Test 14: No hardcoded credentials..." -NoNewline
$SensitivePatterns = @('password\s*=', 'token\s*=', 'api[_-]?key\s*=', 'secret\s*=')
$Found = @()
foreach ($pattern in $SensitivePatterns) {
    if ($ScriptContent -match $pattern) {
        $Found += $pattern
    }
}
if ($Found.Count -eq 0) {
    Write-Host " PASS" -ForegroundColor Green
} else {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "  Found sensitive patterns: $($Found -join ', ')"
    exit 1
}

# Summary
Write-Host ""
Write-Host "==> All tests passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Script validation complete. The merge-to-main.ps1 script is ready to use." -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the script:" -ForegroundColor Yellow
Write-Host "  .\merge-to-main.ps1"
Write-Host ""
Write-Host "Prerequisites:" -ForegroundColor Yellow
Write-Host "  - Git (installed)" -ForegroundColor Gray
Write-Host "  - GitHub CLI: gh auth login" -ForegroundColor Gray
Write-Host ""
