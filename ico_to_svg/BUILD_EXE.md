# Building Windows Executable

This guide explains how to build the standalone Windows executable for `ico-to-svg`.

## Prerequisites

- Python 3.10 or later
- Virtual environment with project dependencies installed
- PyInstaller

## Quick Build

```powershell
# 1. Activate your virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Install PyInstaller (if not already installed)
pip install pyinstaller

# 3. Build the executable
pyinstaller ico_to_svg.spec

# 4. Create the alias
Copy-Item dist\ico-to-svg.exe dist\ico2svg.exe
```

## Output

The build process creates:
- `dist/ico-to-svg.exe` (~7-8 MB) - Main executable
- `dist/ico2svg.exe` - Alias (copy of main executable)

## Build Configuration

The build is configured in `ico_to_svg.spec`:

- **Mode**: Single-file executable (`--onefile`)
- **Console**: CLI application (console window enabled)
- **Compression**: UPX compression enabled (if available)
- **Excluded modules**: tkinter, matplotlib, numpy, scipy, pandas, pytest, jupyter (reduces size)
- **Python version**: 3.13+ recommended

## Testing the Executable

```powershell
# Test version
dist\ico-to-svg.exe --version

# Test help
dist\ico-to-svg.exe --help
dist\ico-to-svg.exe convert --help

# Test conversion
dist\ico-to-svg.exe convert input.ico output.svg
dist\ico-to-svg.exe convert input.ico output.svg --mode vector

# Test info
dist\ico-to-svg.exe info input.ico
```

## Running Integration Tests

```powershell
# Run exe-specific tests
pytest tests/exe/ -v

# Run all tests including exe tests
pytest -v
```

## Clean Build

If you need to rebuild from scratch:

```powershell
# Remove build artifacts
Remove-Item -Recurse -Force build, dist

# Rebuild
pyinstaller --clean ico_to_svg.spec
Copy-Item dist\ico-to-svg.exe dist\ico2svg.exe
```

## Troubleshooting

### Import Errors

If the executable fails with import errors:
1. Check that all dependencies are installed in the virtual environment
2. Rebuild with `--clean` flag
3. Check `build/ico_to_svg/warn-ico_to_svg.txt` for warnings

### Large File Size

The executable size is determined by:
- Python interpreter (~5 MB)
- Pillow library and dependencies (~2 MB)
- Other dependencies

To reduce size:
- Ensure excluded modules list in spec file is complete
- Use UPX compression (enabled by default)

### Antivirus False Positives

PyInstaller executables may trigger antivirus warnings. This is common and expected:
- Provide SHA256 checksums (see below)
- Consider code signing for production distribution

## Checksums

Generate SHA256 checksums for distribution:

```powershell
Get-FileHash dist\ico-to-svg.exe -Algorithm SHA256
Get-FileHash dist\ico2svg.exe -Algorithm SHA256
```

## CI/CD

Automated builds are configured in `.github/workflows/build-exe.yml`:
- Builds on: Push to tags (v*) or manual workflow dispatch
- Runs on: Windows runner
- Uploads: Executables and checksums to GitHub Releases

## Distribution

After building, you can:
1. Copy to a location in PATH (see `INSTALL_WINDOWS_EXE.md`)
2. Distribute via GitHub Releases
3. Create an installer (future enhancement)
4. Package for Chocolatey/Scoop/winget (future enhancement)
