"""Unit tests for ICO parsing functions."""

from pathlib import Path

import pytest
from PIL import Image

from ico_to_svg.ico_parser import load_ico_frames, open_ico_at_size, parse_size_arg


class TestParseSizeArg:
    """Test size argument parsing."""

    @pytest.mark.parametrize(
        "size_str,expected",
        [
            ("256", (256, 256)),
            ("32", (32, 32)),
            ("1", (1, 1)),
            ("1024", (1024, 1024)),
            ("32x64", (32, 64)),
            ("16X32", (16, 32)),  # Case insensitive
            ("128x128", (128, 128)),
        ],
    )
    def test_valid_size_formats(self, size_str: str, expected: tuple[int, int]) -> None:
        """Test valid size string parsing."""
        assert parse_size_arg(size_str) == expected

    @pytest.mark.parametrize(
        "invalid_size",
        [
            "0",  # Zero dimension
            "-32",  # Negative
            "32x0",  # Zero height
            "32x-16",  # Negative height
            "32x64x128",  # Too many dimensions
            "abc",  # Non-numeric
            "32xabc",  # Invalid height
            "",  # Empty
        ],
    )
    def test_invalid_size_formats(self, invalid_size: str) -> None:
        """Test that invalid formats raise ValueError."""
        with pytest.raises(ValueError):
            parse_size_arg(invalid_size)


class TestLoadIcoFrames:
    """Test ICO frame enumeration."""

    def test_load_multi_size_ico(self, multi_size_ico: Path) -> None:
        """Test loading multi-size ICO returns all sizes."""
        sizes = load_ico_frames(multi_size_ico)
        assert len(sizes) >= 4  # At least 16, 32, 64, 128
        assert (16, 16) in sizes
        assert (32, 32) in sizes
        assert (64, 64) in sizes
        assert (128, 128) in sizes

    def test_load_single_size_ico(self, single_size_ico: Path) -> None:
        """Test loading single-size ICO."""
        sizes = load_ico_frames(single_size_ico)
        assert len(sizes) >= 1
        assert (48, 48) in sizes

    def test_nonexistent_file_raises_error(self, tmp_path: Path) -> None:
        """Test that missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_ico_frames(tmp_path / "nonexistent.ico")

    def test_invalid_file_raises_error(self, tmp_path: Path) -> None:
        """Test that non-ICO file raises appropriate error."""
        invalid = tmp_path / "invalid.ico"
        invalid.write_text("not an ico file")
        with pytest.raises(Exception):  # PIL raises various exceptions
            load_ico_frames(invalid)


class TestOpenIcoAtSize:
    """Test opening ICO at specific size."""

    def test_open_at_exact_size(self, multi_size_ico: Path) -> None:
        """Test opening at exact available size."""
        img = open_ico_at_size(multi_size_ico, (32, 32))
        assert img.size == (32, 32)
        assert img.mode == "RGBA"

    def test_open_at_largest_size(self, multi_size_ico: Path) -> None:
        """Test opening at largest size."""
        img = open_ico_at_size(multi_size_ico, (128, 128))
        assert img.size == (128, 128)
        assert img.mode == "RGBA"

    def test_open_returns_rgba_mode(self, single_size_ico: Path) -> None:
        """Test that output is always RGBA mode."""
        img = open_ico_at_size(single_size_ico, (48, 48))
        assert img.mode == "RGBA"

    def test_open_non_square_size(self, non_square_ico: Path) -> None:
        """Test opening non-square ICO."""
        img = open_ico_at_size(non_square_ico, (32, 64))
        assert img.size == (32, 64)
        assert img.mode == "RGBA"
