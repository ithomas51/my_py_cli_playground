"""Integration tests for the compiled Windows executable.

These tests verify that the PyInstaller-built ico-to-svg.exe works correctly
as a standalone executable without requiring Python or virtual environment.
"""

import json
import subprocess
from pathlib import Path

import pytest


# Path to the compiled executable
EXE_PATH = Path(__file__).parent.parent.parent / "dist" / "ico-to-svg.exe"
ALIAS_PATH = Path(__file__).parent.parent.parent / "dist" / "ico2svg.exe"


@pytest.mark.skipif(not EXE_PATH.exists(), reason="Executable not built yet")
class TestExeBasicCommands:
    """Test basic CLI commands work in the executable."""

    def test_exe_exists(self):
        """Verify the executable file exists."""
        assert EXE_PATH.exists(), f"Executable not found at {EXE_PATH}"
        assert EXE_PATH.stat().st_size > 0, "Executable is empty"

    def test_alias_exists(self):
        """Verify the alias executable exists."""
        assert ALIAS_PATH.exists(), f"Alias executable not found at {ALIAS_PATH}"

    def test_exe_version(self):
        """Test --version flag returns version string."""
        result = subprocess.run(
            [str(EXE_PATH), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Version command failed: {result.stderr}"
        assert "0.1.0" in result.stdout, f"Expected version in output: {result.stdout}"

    def test_exe_help(self):
        """Test --help flag shows usage information."""
        result = subprocess.run(
            [str(EXE_PATH), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Help command failed: {result.stderr}"
        assert "convert" in result.stdout, "Missing 'convert' subcommand in help"
        assert "info" in result.stdout, "Missing 'info' subcommand in help"

    def test_convert_help(self):
        """Test convert subcommand help."""
        result = subprocess.run(
            [str(EXE_PATH), "convert", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Convert help failed: {result.stderr}"
        assert "--mode" in result.stdout, "Missing --mode option"
        assert "raster" in result.stdout, "Missing raster mode"
        assert "vector" in result.stdout, "Missing vector mode"

    def test_info_help(self):
        """Test info subcommand help."""
        result = subprocess.run(
            [str(EXE_PATH), "info", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Info help failed: {result.stderr}"
        assert "--json" in result.stdout, "Missing --json option"


@pytest.mark.skipif(not EXE_PATH.exists(), reason="Executable not built yet")
class TestExeInfoCommand:
    """Test the info subcommand with various ICO files."""

    def test_info_single_size(self, single_size_ico):
        """Test info command with single-size ICO."""
        result = subprocess.run(
            [str(EXE_PATH), "info", str(single_size_ico)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Info command failed: {result.stderr}"
        assert "Available sizes:" in result.stdout
        assert "256x256" in result.stdout

    def test_info_multi_size(self, multi_size_ico):
        """Test info command with multi-size ICO."""
        result = subprocess.run(
            [str(EXE_PATH), "info", str(multi_size_ico)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Info command failed: {result.stderr}"
        assert "Available sizes:" in result.stdout

    def test_info_json_output(self, multi_size_ico):
        """Test info command with --json flag."""
        result = subprocess.run(
            [str(EXE_PATH), "info", str(multi_size_ico), "--json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Info JSON failed: {result.stderr}"

        # Verify valid JSON
        try:
            data = json.loads(result.stdout)
            assert isinstance(data, list), "JSON output should be a list"
            assert len(data) > 0, "JSON output should contain sizes"
            for item in data:
                assert "width" in item
                assert "height" in item
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON output: {e}\n{result.stdout}")

    def test_info_nonexistent_file(self, tmp_path):
        """Test info command with nonexistent file."""
        nonexistent = tmp_path / "does_not_exist.ico"
        result = subprocess.run(
            [str(EXE_PATH), "info", str(nonexistent)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0, "Should fail on nonexistent file"


@pytest.mark.skipif(not EXE_PATH.exists(), reason="Executable not built yet")
class TestExeConvertRaster:
    """Test raster mode conversion."""

    def test_convert_raster_default(self, single_size_ico, tmp_path):
        """Test basic raster conversion (default mode)."""
        output = tmp_path / "output.svg"
        result = subprocess.run(
            [str(EXE_PATH), "convert", str(single_size_ico), str(output)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"
        assert output.stat().st_size > 0, "Output SVG is empty"

        # Verify it's a valid SVG with embedded image
        content = output.read_text()
        assert '<?xml version' in content
        assert '<svg' in content
        assert 'data:image/png;base64,' in content

    def test_convert_raster_explicit(self, single_size_ico, tmp_path):
        """Test raster conversion with explicit --mode raster."""
        output = tmp_path / "output_raster.svg"
        result = subprocess.run(
            [str(EXE_PATH), "convert", str(single_size_ico), str(output), "--mode", "raster"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"

    def test_convert_raster_specific_size(self, multi_size_ico, tmp_path):
        """Test raster conversion with --size option."""
        output = tmp_path / "output_32.svg"
        result = subprocess.run(
            [str(EXE_PATH), "convert", str(multi_size_ico), str(output), "--size", "32"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"

        # Verify dimensions
        content = output.read_text()
        assert 'width="32"' in content or "width='32'" in content

    def test_convert_raster_with_background(self, single_size_ico, tmp_path):
        """Test raster conversion with background color."""
        output = tmp_path / "output_bg.svg"
        result = subprocess.run(
            [
                str(EXE_PATH),
                "convert",
                str(single_size_ico),
                str(output),
                "--background",
                "white",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"


@pytest.mark.skipif(not EXE_PATH.exists(), reason="Executable not built yet")
class TestExeConvertVector:
    """Test vector mode conversion."""

    def test_convert_vector_mode(self, single_size_ico, tmp_path):
        """Test vector mode conversion."""
        output = tmp_path / "output_vector.svg"
        result = subprocess.run(
            [str(EXE_PATH), "convert", str(single_size_ico), str(output), "--mode", "vector"],
            capture_output=True,
            text=True,
            timeout=30,  # Vector mode can be slower
        )
        assert result.returncode == 0, f"Vector convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"

        # Verify it's a valid SVG with paths (not embedded image)
        content = output.read_text()
        assert '<?xml version' in content
        assert '<svg' in content
        assert '<path' in content, "Vector SVG should contain path elements"
        assert 'data:image/png;base64,' not in content, "Vector SVG should not embed images"

    def test_convert_vector_alpha_threshold(self, single_size_ico, tmp_path):
        """Test vector conversion with custom alpha threshold."""
        output = tmp_path / "output_alpha.svg"
        result = subprocess.run(
            [
                str(EXE_PATH),
                "convert",
                str(single_size_ico),
                str(output),
                "--mode",
                "vector",
                "--alpha-threshold",
                "128",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"Convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"


@pytest.mark.skipif(not ALIAS_PATH.exists(), reason="Alias executable not built yet")
class TestExeAlias:
    """Test the ico2svg alias executable."""

    def test_alias_version(self):
        """Test alias executable version command."""
        result = subprocess.run(
            [str(ALIAS_PATH), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Alias version failed: {result.stderr}"
        assert "0.1.0" in result.stdout

    def test_alias_convert(self, single_size_ico, tmp_path):
        """Test conversion using alias executable."""
        output = tmp_path / "output_alias.svg"
        result = subprocess.run(
            [str(ALIAS_PATH), "convert", str(single_size_ico), str(output)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Alias convert failed: {result.stderr}"
        assert output.exists(), "Output SVG not created"


@pytest.mark.skipif(not EXE_PATH.exists(), reason="Executable not built yet")
class TestExeStability:
    """Test executable stability and edge cases."""

    def test_multiple_conversions(self, single_size_ico, tmp_path):
        """Test running multiple conversions in sequence."""
        for i in range(5):
            output = tmp_path / f"output_{i}.svg"
            result = subprocess.run(
                [str(EXE_PATH), "convert", str(single_size_ico), str(output)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            assert result.returncode == 0, f"Conversion {i} failed: {result.stderr}"
            assert output.exists(), f"Output {i} not created"

    def test_invalid_input_file(self, tmp_path):
        """Test handling of invalid input file."""
        invalid = tmp_path / "not_an_ico.txt"
        invalid.write_text("This is not an ICO file")
        output = tmp_path / "output.svg"

        result = subprocess.run(
            [str(EXE_PATH), "convert", str(invalid), str(output)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0, "Should fail on invalid input"

    def test_missing_required_args(self):
        """Test handling of missing required arguments."""
        result = subprocess.run(
            [str(EXE_PATH), "convert"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0, "Should fail with missing arguments"
