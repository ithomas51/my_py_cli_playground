"""Pytest fixtures and configuration for ico-to-svg tests."""

from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def multi_size_ico(tmp_path: Path) -> Path:
    """Generate multi-size ICO with 16, 32, 64, 128 px frames.

    Parameters
    ----------
    tmp_path : Path
        Pytest temporary directory.

    Returns
    -------
    Path
        Path to generated ICO file.
    """
    ico_path = tmp_path / "multi.ico"
    base = Image.new("RGBA", (256, 256), (255, 0, 0, 255))
    # Draw simple pattern for visual identification
    for i in range(256):
        base.putpixel((i, i), (0, 128, 255, 255))
        base.putpixel((i, 255 - i), (0, 128, 255, 255))
    base.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (64, 64), (128, 128)])
    return ico_path


@pytest.fixture
def single_size_ico(tmp_path: Path) -> Path:
    """Generate a single-size 48x48 ICO.

    Parameters
    ----------
    tmp_path : Path
        Pytest temporary directory.

    Returns
    -------
    Path
        Path to generated ICO file.
    """
    ico_path = tmp_path / "single.ico"
    img = Image.new("RGBA", (48, 48), (0, 200, 0, 255))
    # Draw border
    for x in range(48):
        img.putpixel((x, 0), (255, 255, 255, 255))
        img.putpixel((x, 47), (255, 255, 255, 255))
    for y in range(48):
        img.putpixel((0, y), (255, 255, 255, 255))
        img.putpixel((47, y), (255, 255, 255, 255))
    img.save(ico_path, format="ICO")
    return ico_path


@pytest.fixture
def non_square_ico(tmp_path: Path) -> Path:
    """Generate a non-square 32x64 ICO.

    Parameters
    ----------
    tmp_path : Path
        Pytest temporary directory.

    Returns
    -------
    Path
        Path to generated ICO file.
    """
    ico_path = tmp_path / "non_square.ico"
    img = Image.new("RGBA", (32, 64), (128, 0, 128, 255))
    img.save(ico_path, format="ICO")
    return ico_path


@pytest.fixture
def output_svg(tmp_path: Path) -> Path:
    """Temporary output SVG path.

    Parameters
    ----------
    tmp_path : Path
        Pytest temporary directory.

    Returns
    -------
    Path
        Path for output SVG file.
    """
    return tmp_path / "output.svg"
