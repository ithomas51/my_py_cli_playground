"""Unit tests for SVG generation functions."""

from pathlib import Path

import pytest
from PIL import Image

from ico_to_svg.svg_writer import Run, runs_to_path_d, vectorize, write_svg_raster, write_svg_vector


class TestVectorize:
    """Test image vectorization into color runs."""

    def test_solid_color_image(self) -> None:
        """Test vectorizing a solid color image."""
        img = Image.new("RGBA", (4, 2), (255, 0, 0, 255))
        color_runs, w, h = vectorize(img, alpha_threshold=128)
        assert w == 4
        assert h == 2
        assert len(color_runs) == 1
        assert (255, 0, 0, 255) in color_runs
        # Should have 2 rows, each with 1 run of 4 pixels
        assert len(color_runs[(255, 0, 0, 255)]) == 2

    def test_transparent_pixels_ignored(self) -> None:
        """Test that transparent pixels are skipped."""
        img = Image.new("RGBA", (4, 1), (255, 0, 0, 0))  # Fully transparent
        color_runs, w, h = vectorize(img, alpha_threshold=128)
        assert w == 4
        assert h == 1
        assert len(color_runs) == 0  # No runs for transparent pixels

    def test_alpha_threshold_effect(self) -> None:
        """Test alpha threshold filtering."""
        img = Image.new("RGBA", (2, 1), (255, 0, 0, 100))  # Semi-transparent
        # Threshold 128: should be ignored
        color_runs_high, _, _ = vectorize(img, alpha_threshold=128)
        assert len(color_runs_high) == 0
        # Threshold 50: should be included
        color_runs_low, _, _ = vectorize(img, alpha_threshold=50)
        assert len(color_runs_low) == 1

    def test_multiple_colors(self) -> None:
        """Test vectorizing image with multiple colors."""
        img = Image.new("RGBA", (4, 1))
        img.putpixel((0, 0), (255, 0, 0, 255))
        img.putpixel((1, 0), (255, 0, 0, 255))
        img.putpixel((2, 0), (0, 255, 0, 255))
        img.putpixel((3, 0), (0, 255, 0, 255))
        color_runs, _, _ = vectorize(img, alpha_threshold=128)
        assert len(color_runs) == 2
        assert (255, 0, 0, 255) in color_runs
        assert (0, 255, 0, 255) in color_runs


class TestRunsToPathD:
    """Test SVG path data generation from runs."""

    def test_single_run(self) -> None:
        """Test path data for a single run."""
        runs = [Run(0, 0, 3)]
        path_d = runs_to_path_d(runs)
        assert "M0,0" in path_d
        assert "H4" in path_d  # x2 + 1
        assert "V1" in path_d
        assert "Z" in path_d

    def test_multiple_runs(self) -> None:
        """Test path data for multiple runs."""
        runs = [Run(0, 0, 3), Run(1, 0, 3)]
        path_d = runs_to_path_d(runs)
        assert "M0,0" in path_d
        assert "M0,1" in path_d
        assert path_d.count("Z") == 2

    def test_empty_runs(self) -> None:
        """Test path data for empty run list."""
        path_d = runs_to_path_d([])
        assert path_d == ""


class TestWriteSvgRaster:
    """Test raster SVG writing."""

    def test_write_basic_raster_svg(self, tmp_path: Path) -> None:
        """Test writing basic raster SVG."""
        img = Image.new("RGBA", (16, 16), (255, 0, 0, 255))
        output = tmp_path / "test.svg"
        write_svg_raster(img, output)
        assert output.exists()
        content = output.read_text()
        assert "data:image/png;base64," in content
        assert "width='16'" in content
        assert "height='16'" in content

    def test_write_with_background(self, tmp_path: Path) -> None:
        """Test writing raster SVG with background."""
        img = Image.new("RGBA", (16, 16), (255, 0, 0, 128))  # Semi-transparent
        output = tmp_path / "test_bg.svg"
        write_svg_raster(img, output, background="#ffffff")
        assert output.exists()
        content = output.read_text()
        assert "data:image/png;base64," in content

    def test_write_transparent_background(self, tmp_path: Path) -> None:
        """Test writing with explicit transparent background."""
        img = Image.new("RGBA", (16, 16), (255, 0, 0, 255))
        output = tmp_path / "test_trans.svg"
        write_svg_raster(img, output, background="transparent")
        assert output.exists()


class TestWriteSvgVector:
    """Test vector SVG writing."""

    def test_write_basic_vector_svg(self, tmp_path: Path) -> None:
        """Test writing basic vector SVG."""
        runs = {(255, 0, 0, 255): [Run(0, 0, 15)]}
        output = tmp_path / "test_vec.svg"
        write_svg_vector(runs, 16, 16, output)
        assert output.exists()
        content = output.read_text()
        assert "<svg" in content
        assert "<path" in content
        assert "#ff0000" in content

    def test_write_with_background(self, tmp_path: Path) -> None:
        """Test writing vector SVG with background."""
        runs = {(0, 0, 255, 255): [Run(0, 0, 7)]}
        output = tmp_path / "test_vec_bg.svg"
        write_svg_vector(runs, 8, 8, output, background="#ffffff")
        assert output.exists()
        content = output.read_text()
        assert "<rect" in content  # Background rect
        assert "#ffffff" in content

    def test_write_multiple_colors(self, tmp_path: Path) -> None:
        """Test writing vector SVG with multiple colors."""
        runs = {
            (255, 0, 0, 255): [Run(0, 0, 3)],
            (0, 255, 0, 255): [Run(1, 0, 3)],
        }
        output = tmp_path / "test_multi.svg"
        write_svg_vector(runs, 4, 2, output)
        assert output.exists()
        content = output.read_text()
        assert "#ff0000" in content
        assert "#00ff00" in content
        assert content.count("<path") == 2
