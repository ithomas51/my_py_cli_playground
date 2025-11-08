# Installing ico-to-svg Windows Executable

This guide explains how to install the standalone `ico-to-svg.exe` executable on Windows, making it available globally from any directory without requiring Python installation.

## Prerequisites

- **None!** The executable is completely standalone and requires no Python installation or dependencies.
- Windows 10 or Windows 11 (64-bit)

## Quick Install

### Option 1: Manual Installation (Recommended)

1. **Download the executables** from the [latest release](https://github.com/ithomas51/my_py_cli_playground/releases):
   - `ico-to-svg.exe`
   - `ico2svg.exe` (optional alias)
   - SHA256 checksum files (for verification)

2. **Create installation directory**:
   ```powershell
   New-Item -Path "C:\Program Files\ico-to-svg" -ItemType Directory -Force
   ```

3. **Copy executables**:
   ```powershell
   Copy-Item ico-to-svg.exe "C:\Program Files\ico-to-svg\"
   Copy-Item ico2svg.exe "C:\Program Files\ico-to-svg\"
   ```

4. **Add to PATH** (requires Administrator):
   ```powershell
   # Run PowerShell as Administrator
   $oldPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
   $newPath = "$oldPath;C:\Program Files\ico-to-svg"
   [Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
   ```

5. **Verify installation** (restart terminal first):
   ```powershell
   ico-to-svg --version
   ```

### Option 2: PowerShell Install Script

Save this as `install-ico-to-svg.ps1`:

```powershell
#Requires -RunAsAdministrator

$InstallPath = "C:\Program Files\ico-to-svg"
$Version = "0.1.0"
$BaseUrl = "https://github.com/ithomas51/my_py_cli_playground/releases/download/v$Version"

Write-Host "Installing ico-to-svg v$Version..." -ForegroundColor Cyan

# Create installation directory
New-Item -Path $InstallPath -ItemType Directory -Force | Out-Null

# Download executables
Write-Host "Downloading executables..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$BaseUrl/ico-to-svg.exe" -OutFile "$InstallPath\ico-to-svg.exe"
Invoke-WebRequest -Uri "$BaseUrl/ico2svg.exe" -OutFile "$InstallPath\ico2svg.exe"

# Add to PATH if not already present
$Path = [Environment]::GetEnvironmentVariable('Path', 'Machine')
if ($Path -notlike "*$InstallPath*") {
    Write-Host "Adding to system PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable('Path', "$Path;$InstallPath", 'Machine')
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine')
}

# Verify installation
Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "Location: $InstallPath" -ForegroundColor Gray
& "$InstallPath\ico-to-svg.exe" --version

Write-Host "`nPlease restart your terminal to use 'ico-to-svg' from any location." -ForegroundColor Cyan
```

Run it:
```powershell
# Run PowerShell as Administrator
.\install-ico-to-svg.ps1
```

### Option 3: User-Local Installation (No Admin Required)

If you don't have administrator access:

```powershell
# Install to user directory
$InstallPath = "$env:LOCALAPPDATA\Programs\ico-to-svg"
New-Item -Path $InstallPath -ItemType Directory -Force
Copy-Item ico-to-svg.exe $InstallPath\
Copy-Item ico2svg.exe $InstallPath\

# Add to user PATH
$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$newPath = "$oldPath;$InstallPath"
[Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
```

## Verifying Installation

After installation and restarting your terminal:

```powershell
# Check version
ico-to-svg --version

# View help
ico-to-svg --help

# Test conversion
ico-to-svg convert myicon.ico output.svg
```

## Verifying Download Integrity

Before installing, verify the download using SHA256 checksums:

```powershell
# Calculate hash of downloaded file
Get-FileHash ico-to-svg.exe -Algorithm SHA256

# Compare with published checksum from GitHub release
Get-Content ico-to-svg.exe.sha256
```

The hashes should match exactly.

## Usage Examples

Once installed, use `ico-to-svg` from any directory:

```powershell
# Get info about an ICO file
ico-to-svg info myicon.ico

# Convert to raster SVG (default)
ico-to-svg convert input.ico output.svg

# Convert specific size
ico-to-svg convert input.ico output.svg --size 32

# Convert to vector SVG
ico-to-svg convert input.ico output.svg --mode vector

# With background color
ico-to-svg convert input.ico output.svg --background white

# Get JSON info
ico-to-svg info input.ico --json
```

## Uninstalling

### System-wide installation:
```powershell
# Run as Administrator
Remove-Item "C:\Program Files\ico-to-svg" -Recurse -Force

# Remove from PATH
$oldPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$newPath = $oldPath -replace ';C:\\Program Files\\ico-to-svg', ''
[Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')
```

### User-local installation:
```powershell
Remove-Item "$env:LOCALAPPDATA\Programs\ico-to-svg" -Recurse -Force

# Remove from user PATH
$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$newPath = $oldPath -replace ";$env:LOCALAPPDATA\\Programs\\ico-to-svg", ''
[Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
```

## Troubleshooting

### "ico-to-svg: The term is not recognized..."

After installation:
1. **Restart your terminal** - PATH changes require a new terminal session
2. Verify PATH includes installation directory:
   ```powershell
   $env:Path -split ';' | Select-String 'ico-to-svg'
   ```
3. Run with full path as temporary workaround:
   ```powershell
   C:\"Program Files"\ico-to-svg\ico-to-svg.exe --version
   ```

### Windows Defender SmartScreen Warning

First run may show "Unknown publisher" warning:
1. This is normal for unsigned executables
2. Click "More info" → "Run anyway"
3. Verify download integrity using SHA256 checksums (see above)

### Antivirus False Positive

Some antivirus software may flag PyInstaller executables:
1. Verify SHA256 checksum matches official release
2. Add exception to antivirus software
3. Download from official GitHub releases only

### Startup Delay

First run extracts bundled Python runtime (1-2 seconds):
- Subsequent runs are faster
- This is normal for single-file executables

## Updating

To update to a new version:
1. Download new executables from latest release
2. Replace files in installation directory:
   ```powershell
   Copy-Item ico-to-svg.exe "C:\Program Files\ico-to-svg\" -Force
   Copy-Item ico2svg.exe "C:\Program Files\ico-to-svg\" -Force
   ```
3. Verify:
   ```powershell
   ico-to-svg --version
   ```

## Alternative Installation Methods

### Portable Mode

For USB drive or portable use:
1. Copy `ico-to-svg.exe` to any directory
2. Run with full path (no PATH modification needed)
3. Works on any Windows machine

### Network Share

For organization-wide deployment:
1. Place executables on network share
2. Add network path to PATH on each machine
3. Users can run without local installation

## Next Steps

- See [README.md](README.md) for usage examples
- See [BUILD_EXE.md](BUILD_EXE.md) for building from source
- Report issues on [GitHub Issues](https://github.com/ithomas51/my_py_cli_playground/issues)
