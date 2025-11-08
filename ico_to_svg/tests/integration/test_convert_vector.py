"""Integration tests for vector conversion mode."""

from pathlib import Path

import pytest

from ico_to_svg import convert_ico_to_svg


class TestVectorConversion:
    """Integration tests for vector conversion mode."""

    def test_convert_vector_mode(self, multi_size_ico: Path, tmp_path: Path) -> None:
        """Test basic vector conversion."""
        output = tmp_path / "out-vec.svg"
        convert_ico_to_svg(
            str(multi_size_ico), str(output), mode="vector", size="32"
        )
        assert output.exists()
        content = output.read_text()
        assert "<path" in content
        assert "data:image/png;base64," not in content  # Should be vector, not raster

    @pytest.mark.parametrize("threshold", [8, 16, 32, 64, 128])
    def test_alpha_thresholds(
        self, multi_size_ico: Path, tmp_path: Path, threshold: int
    ) -> None:
        """Test vector conversion with various alpha thresholds."""
        output = tmp_path / f"out-vec-{threshold}.svg"
        convert_ico_to_svg(
            str(multi_size_ico),
            str(output),
            mode="vector",
            alpha_threshold=threshold,
            size="16",  # Smaller size for faster test
        )
        assert output.exists()

    def test_vector_with_background(
        self, multi_size_ico: Path, tmp_path: Path
    ) -> None:
        """Test vector conversion with background color."""
        output = tmp_path / "out-vec-bg.svg"
        convert_ico_to_svg(
            str(multi_size_ico),
            str(output),
            mode="vector",
            background="#ffffff",
            size="32",
        )
        assert output.exists()
        content = output.read_text()
        assert "<rect" in content  # Background rectangle
        assert "#ffffff" in content

    def test_vector_default_alpha_threshold(
        self, single_size_ico: Path, tmp_path: Path
    ) -> None:
        """Test that default alpha threshold is 16."""
        output = tmp_path / "out-vec-default.svg"
        convert_ico_to_svg(
            str(single_size_ico), str(output), mode="vector"
        )  # No explicit threshold
        assert output.exists()
        content = output.read_text()
        assert "<path" in content

    def test_vector_with_size_selection(
        self, multi_size_ico: Path, tmp_path: Path
    ) -> None:
        """Test vector conversion with size selection."""
        output = tmp_path / "out-vec-size.svg"
        convert_ico_to_svg(
            str(multi_size_ico), str(output), mode="vector", size="64"
        )
        assert output.exists()
        content = output.read_text()
        assert 'viewBox="0 0 64 64"' in content
