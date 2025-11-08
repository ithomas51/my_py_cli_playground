# Windows Installation Guide

## Installation from Built Package

### Method 1: Install from wheel (Recommended for local use)

```powershell
# Navigate to the ico_to_svg directory
cd c:\Users\ithom\PythonProjects\my_py_cli_playground\ico_to_svg

# Install the wheel directly using pip
pip install dist\ico_to_svg-0.1.0-py3-none-any.whl

# Or install with user flag (no admin required)
pip install --user dist\ico_to_svg-0.1.0-py3-none-any.whl
```

### Method 2: Install with pipx (Recommended for CLI tools)

```powershell
# Install pipx if not already installed
pip install --user pipx
python -m pipx ensurepath

# Install ico-to-svg in isolated environment
pipx install dist\ico_to_svg-0.1.0-py3-none-any.whl
```

### Method 3: Install in development mode (for testing)

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install in editable mode
pip install -e .
```

## Verify Installation

After installation, verify the tool works:

```powershell
# Check version
ico-to-svg --version

# View help
ico-to-svg --help

# Test conversion (if you have an .ico file)
ico-to-svg convert test.ico test.svg

# Get info about an ICO file
ico-to-svg info test.ico --json
```

## Using the Tool

### Basic Conversion

```powershell
# Convert to raster SVG (default)
ico-to-svg convert icon.ico icon.svg

# Convert to vector SVG
ico-to-svg convert icon.ico icon.svg --mode vector

# Convert specific size
ico-to-svg convert icon.ico icon_32.svg --size 32

# Convert with white background
ico-to-svg convert icon.ico icon.svg --background "#ffffff"
```

### Get Icon Information

```powershell
# List available sizes
ico-to-svg info icon.ico

# Get sizes as JSON
ico-to-svg info icon.ico --json
```

## Uninstallation

```powershell
# If installed with pip
pip uninstall ico-to-svg

# If installed with pipx
pipx uninstall ico-to-svg
```

## Troubleshooting

### Command not found

If `ico-to-svg` command is not recognized:

1. **Check if Scripts directory is in PATH**:
   ```powershell
   $env:Path -split ';' | Select-String Scripts
   ```

2. **Add to PATH temporarily**:
   ```powershell
   $env:Path += ";C:\Users\YourUsername\AppData\Local\Programs\Python\Python3XX\Scripts"
   ```

3. **Use full path**:
   ```powershell
   C:\Users\YourUsername\AppData\Local\Programs\Python\Python3XX\Scripts\ico-to-svg.exe
   ```

### Import errors

If you get import errors, ensure dependencies are installed:

```powershell
pip install Pillow>=10.0.0 svgwrite>=1.4.3
```

## Building from Source

If you need to rebuild the package:

```powershell
# Install build tools
pip install build

# Build the package
python -m build

# This creates:
# - dist/ico_to_svg-0.1.0-py3-none-any.whl
# - dist/ico_to_svg-0.1.0.tar.gz
```

## Development Setup

For contributing or modifying the code:

```powershell
# Clone or navigate to the repository
cd c:\Users\ithom\PythonProjects\my_py_cli_playground\ico_to_svg

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install with dev dependencies
pip install -e ".[dev,test]"

# Run tests
pytest tests/ -v

# Run linting
ruff check src/ tests/

# Run type checking
mypy src/
```
