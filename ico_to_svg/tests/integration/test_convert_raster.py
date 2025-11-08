"""Integration tests for raster conversion mode."""

from pathlib import Path

import pytest

from ico_to_svg import convert_ico_to_svg


class TestRasterConversion:
    """Integration tests for raster conversion mode."""

    def test_convert_with_size_selection(self, multi_size_ico: Path, tmp_path: Path) -> None:
        """Test raster conversion with size selection."""
        output = tmp_path / "out-32.svg"
        convert_ico_to_svg(str(multi_size_ico), str(output), mode="raster", size="32")
        assert output.exists()
        content = output.read_text()
        assert "data:image/png;base64," in content
        assert "width='32'" in content or 'width="32"' in content

    def test_convert_with_background(self, multi_size_ico: Path, tmp_path: Path) -> None:
        """Test raster conversion with background color."""
        output = tmp_path / "out-bg.svg"
        convert_ico_to_svg(str(multi_size_ico), str(output), mode="raster", background="#ffffff")
        assert output.exists()
        content = output.read_text()
        assert "data:image/png;base64," in content

    @pytest.mark.parametrize("size", ["16", "32", "64", "128"])
    def test_all_available_sizes(self, multi_size_ico: Path, tmp_path: Path, size: str) -> None:
        """Test conversion at all available sizes."""
        output = tmp_path / f"out-{size}.svg"
        convert_ico_to_svg(str(multi_size_ico), str(output), size=size)
        assert output.exists()

    def test_convert_without_size_uses_largest(self, multi_size_ico: Path, tmp_path: Path) -> None:
        """Test that omitting size uses largest available."""
        output = tmp_path / "out-default.svg"
        convert_ico_to_svg(str(multi_size_ico), str(output), mode="raster")
        assert output.exists()
        content = output.read_text()
        # Should use 128x128 (largest)
        assert "128" in content

    def test_convert_single_size_ico(self, single_size_ico: Path, tmp_path: Path) -> None:
        """Test conversion of single-size ICO."""
        output = tmp_path / "out-single.svg"
        convert_ico_to_svg(str(single_size_ico), str(output), mode="raster")
        assert output.exists()
        content = output.read_text()
        assert "data:image/png;base64," in content

    def test_convert_with_pathlib_paths(self, multi_size_ico: Path, tmp_path: Path) -> None:
        """Test conversion with pathlib.Path objects."""
        output = tmp_path / "out-path.svg"
        convert_ico_to_svg(multi_size_ico, output, mode="raster", size="32")
        assert output.exists()

    def test_transparent_background_explicit(self, multi_size_ico: Path, tmp_path: Path) -> None:
        """Test explicit transparent background."""
        output = tmp_path / "out-transparent.svg"
        convert_ico_to_svg(
            str(multi_size_ico),
            str(output),
            mode="raster",
            background="transparent",
        )
        assert output.exists()
