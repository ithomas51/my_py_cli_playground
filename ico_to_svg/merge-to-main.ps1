#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Automated git workflow for merging feature branch into main with PR creation.

.DESCRIPTION
    This script automates the process of:
    1. Checking current branch (protecting main)
    2. Creating new branch if on main
    3. Staging all changes
    4. Creating commit
    5. Pushing to remote
    6. Creating GitHub pull request
    7. Merging PR with squash
    8. Cleaning up branch

.PARAMETER BranchName
    Name for the new branch if current branch is main. Default: "feature/windows-exe-distribution"

.PARAMETER CommitMessage
    Commit message. Default: "feat: Add Windows standalone executable distribution"

.EXAMPLE
    .\merge-to-main.ps1
    # Uses current branch (cli/ico-to-svg) and default commit message

.EXAMPLE
    .\merge-to-main.ps1 -BranchName "cli/ico-to-svg"
    # Explicitly specify branch name (useful if on main)

.EXAMPLE
    .\merge-to-main.ps1 -BranchName "feature/my-feature" -CommitMessage "feat: My feature"
    # Custom branch and commit message
#>

param(
    [string]$BranchName = "cli/ico-to-svg",
    [string]$CommitMessage = "feat: Add Windows standalone executable distribution

- Implement PyInstaller build system with optimized spec file
- Create standalone ico-to-svg.exe and ico2svg.exe (14.46 MB each)
- Fix __main__.py imports for executable compatibility
- Add 21 integration tests for executable functionality (all passing)
- Implement GitHub Actions workflow for automated exe builds
- Create comprehensive documentation (BUILD_EXE.md, INSTALL_WINDOWS_EXE.md)
- Update README with executable installation instructions
- Add .gitignore rules for build artifacts

Size: 14.46 MB | Startup: ~600ms | Tests: 21/21 passing"
)

# Colors for output
$ErrorColor = "Red"
$WarningColor = "Yellow"
$SuccessColor = "Green"
$InfoColor = "Cyan"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor $InfoColor
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $SuccessColor
}

function Write-Failure {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor $ErrorColor
}

function Write-Info {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor Gray
}

# Change to script directory (project root)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
Write-Info "Working directory: $(Get-Location)"

# Check if git is available
Write-Step "Checking prerequisites"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Failure "Git is not installed or not in PATH"
    exit 1
}
Write-Success "Git found: $(git --version)"

# Check if gh CLI is available
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Failure "GitHub CLI (gh) is not installed. Install from: https://cli.github.com/"
    Write-Info "Required for creating pull requests"
    exit 1
}
Write-Success "GitHub CLI found: $(gh --version | Select-Object -First 1)"

# Get current branch
Write-Step "Checking current branch"
$CurrentBranch = git branch --show-current
Write-Info "Current branch: $CurrentBranch"

# Check if on main branch
if ($CurrentBranch -eq "main" -or $CurrentBranch -eq "master") {
    Write-Warning "Currently on protected branch: $CurrentBranch"
    Write-Info "Creating new branch: $BranchName"
    
    # Create and checkout new branch
    git checkout -b $BranchName
    if ($LASTEXITCODE -ne 0) {
        Write-Failure "Failed to create new branch"
        exit 1
    }
    
    $CurrentBranch = $BranchName
    Write-Success "Created and switched to branch: $CurrentBranch"
} else {
    Write-Success "Safe to proceed on branch: $CurrentBranch"
}

# Check for changes
Write-Step "Checking for changes"
$Status = git status --porcelain
if (-not $Status) {
    Write-Warning "No changes to commit"
    $Response = Read-Host "Continue anyway? (y/N)"
    if ($Response -ne "y" -and $Response -ne "Y") {
        Write-Info "Aborted by user"
        exit 0
    }
} else {
    $ChangeCount = ($Status | Measure-Object).Count
    Write-Success "Found $ChangeCount file(s) with changes"
    Write-Info "Changes:"
    git status --short | ForEach-Object { Write-Info "  $_" }
}

# Stage all changes
Write-Step "Staging all changes"
git add -A
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to stage changes"
    exit 1
}
Write-Success "All changes staged"

# Show what will be committed
Write-Info "Staged files:"
git diff --cached --name-status | ForEach-Object { Write-Info "  $_" }

# Commit changes
Write-Step "Creating commit"
git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to create commit"
    exit 1
}
Write-Success "Commit created"

# Push to remote
Write-Step "Pushing to remote"
Write-Info "Pushing branch: $CurrentBranch"
git push -u origin $CurrentBranch
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to push to remote"
    exit 1
}
Write-Success "Pushed to origin/$CurrentBranch"

# Create pull request
Write-Step "Creating pull request"
$PRTitle = $CommitMessage.Split("`n")[0]  # First line as title
$PRBody = $CommitMessage.Split("`n", 2)[1].Trim()  # Rest as body

Write-Info "Title: $PRTitle"
Write-Info "Creating PR to merge $CurrentBranch → main"

$PR = gh pr create --title $PRTitle --body $PRBody --base main --head $CurrentBranch 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to create pull request"
    Write-Info "Error: $PR"
    Write-Warning "You may need to authenticate: gh auth login"
    exit 1
}

# Extract PR number from output
$PRNumber = $PR | Select-String -Pattern '#(\d+)' | ForEach-Object { $_.Matches.Groups[1].Value }
Write-Success "Pull request created: PR #${PRNumber}"
Write-Info "URL: $PR"

# Wait a moment for PR to be created on GitHub
Start-Sleep -Seconds 2

# Merge pull request with squash
Write-Step "Merging pull request (squash)"
Write-Info "PR #${PRNumber} will be squash merged into main"

gh pr merge $PRNumber --squash --delete-branch
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to merge pull request"
    Write-Warning "PR #${PRNumber} remains open. You can merge it manually on GitHub."
    exit 1
}

Write-Success "Pull request merged and branch deleted on remote"

# Switch back to main and pull
Write-Step "Updating local main branch"
git checkout main
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to checkout main"
    exit 1
}

git pull origin main
if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to pull latest main"
    exit 1
}
Write-Success "Local main branch updated"

# Delete local feature branch
Write-Step "Cleaning up local branch"
git branch -d $CurrentBranch
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Failed to delete local branch (may already be deleted)"
} else {
    Write-Success "Local branch deleted: $CurrentBranch"
}

# Summary
Write-Host "`n" -NoNewline
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    WORKFLOW COMPLETED                          ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Success "Branch: $CurrentBranch"
Write-Success "PR #${PRNumber}: Merged into main (squash)"
Write-Success "Local repository: Up to date with main"
Write-Host ""
Write-Info "Next steps:"
Write-Info "  1. Verify changes on GitHub"
Write-Info "  2. Tag release: git tag v0.1.0 && git push --tags"
Write-Info "  3. GitHub Actions will build Windows executables"
Write-Host ""
