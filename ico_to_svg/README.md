# ico-to-svg [gist - ](https://gist.github.com/ithomas51/c4dbcc2b02a0bf3c12725efc8a400aaf)

Convert Windows `.ico` files to `.svg` via either:

* Raster embed: base64 PNG inside `<image>` (safe for any complexity)
* Naive vector: per-row run-length rectangles (best for flat / pixel-art icons)

## Features
* Multi-size ICO support with size selection rule (exact → nearest larger → largest)
* Subcommands: `convert` and `info`
* Vector mode with adjustable `--alpha-threshold` (default 16)
* Optional background compositing (e.g. `--background "#ffffff"` or `transparent`)
* JSON output for size introspection (`info --json`)
* **Standalone Windows executable** - No Python installation required!

## Installation

### Option 1: Standalone Windows Executable (Recommended)

Download the pre-built executable from [Releases](https://github.com/ithomas51/my_py_cli_playground/releases) - **no Python installation required!**

```powershell
# Quick install (requires Administrator)
New-Item -Path "C:\Program Files\ico-to-svg" -ItemType Directory -Force
Copy-Item ico-to-svg.exe "C:\Program Files\ico-to-svg\"

# Add to PATH
$oldPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
[Environment]::SetEnvironmentVariable('Path', "$oldPath;C:\Program Files\ico-to-svg", 'Machine')

# Verify (restart terminal first)
ico-to-svg --version
```

See [INSTALL_WINDOWS_EXE.md](INSTALL_WINDOWS_EXE.md) for detailed installation instructions, PowerShell install script, and troubleshooting.

### Option 2: Python Package (pipx)
```powershell
pipx install .
# Or from a Git repo:
pipx install git+https://github.com/your/repo.git
```

### Dev Install (Editable)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e .
```

## CLI Usage
```powershell
ico-to-svg convert icon.ico icon.svg                # raster (default)
ico-to-svg convert icon.ico icon.svg --mode vector  # naive vector
ico-to-svg convert icon.ico icon.svg --mode vector --alpha-threshold 32
ico-to-svg convert icon.ico icon.svg --background "#ffffff"  # white background
ico-to-svg convert icon.ico icon.svg --size 256     # choose 256x256 if present
ico-to-svg info icon.ico                            # list sizes
ico-to-svg info icon.ico --json                     # JSON sizes
```

Alias:
```powershell
ico2svg convert icon.ico icon.svg
```

### Size Selection
You may pass `--size 256` or `--size 256x256`. Selection order:
1. Exact match
2. Nearest larger (preferring square, then smallest area)
3. Largest available

### Vector Mode Notes
* Outputs one path element per contiguous horizontal color run.
* Complex, anti-aliased icons produce large SVGs.
* Use raster mode for detailed or gradient-heavy icons.

## Programmatic API
```python
from ico_to_svg import convert_ico_to_svg
convert_ico_to_svg("icon.ico", "icon.svg", mode="vector", alpha_threshold=16, size="256")
```

## Deprecation Notice
Legacy script invocation (`python ico_to_svg.py ...`) is deprecated; use `ico-to-svg`. Shim will be removed after two minor releases.

## Building

### Build Python Wheel
```powershell
pip install build
py -m build
```

### Build Windows Executable
```powershell
pip install pyinstaller
pyinstaller ico_to_svg.spec
Copy-Item dist\ico-to-svg.exe dist\ico2svg.exe
```

See [BUILD_EXE.md](BUILD_EXE.md) for detailed build instructions.

## Private (NO LICENSE FILE INCLUDED)