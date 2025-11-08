"""ICO file parsing and size selection logic."""

from pathlib import Path
from typing import List, Tuple

from PIL import Image


def parse_size_arg(size_str: str) -> Tuple[int, int]:
    """Parse size argument like '256' or '256x256'.

    Parameters
    ----------
    size_str : str
        Size specification as integer or WxH format.

    Returns
    -------
    Tuple[int, int]
        Width and height as tuple.

    Raises
    ------
    ValueError
        If format is invalid or dimensions are non-positive.

    Examples
    --------
    >>> parse_size_arg("256")
    (256, 256)
    >>> parse_size_arg("32x64")
    (32, 64)
    """
    if "x" in size_str.lower():
        parts = size_str.lower().split("x")
        if len(parts) != 2:
            raise ValueError("--size must be like 256 or 256x256")
        w = int(parts[0])
        h = int(parts[1])
    else:
        w = h = int(size_str)
    if w <= 0 or h <= 0:
        raise ValueError("--size dimensions must be positive")
    return w, h


def load_ico_frames(path: Path | str) -> List[Tuple[int, int]]:
    """Load available frame sizes from an ICO file.

    Parameters
    ----------
    path : Path or str
        Path to the ICO file.

    Returns
    -------
    List[Tuple[int, int]]
        List of unique (width, height) tuples available in the ICO.

    Raises
    ------
    FileNotFoundError
        If the ICO file does not exist.
    ValueError
        If the file is not a valid ICO.

    Notes
    -----
    Uses PIL's im.info['sizes'] when available, otherwise iterates
    through frames to determine sizes.

    Examples
    --------
    >>> load_ico_frames("icon.ico")
    [(16, 16), (32, 32), (64, 64), (128, 128)]
    """
    im = Image.open(str(path))
    sizes = im.info.get("sizes")
    if sizes:
        return list({(int(w), int(h)) for (w, h) in sizes})
    # Fallback: iterate frames if available
    frames = []
    n = getattr(im, "n_frames", 1)
    for i in range(n):
        if n > 1:
            im.seek(i)
        frames.append((im.width, im.height))
    # Unique them
    return list({(int(w), int(h)) for (w, h) in frames})


def select_size(
    available: List[Tuple[int, int]], desired: Tuple[int, int] | None
) -> Tuple[int, int]:
    """Select ICO frame size using priority rules.

    Selection priority:
    1. Exact match
    2. Nearest larger size (prefer square, then smallest area)
    3. Largest available

    Parameters
    ----------
    available : List[Tuple[int, int]]
        Available (width, height) sizes in the ICO.
    desired : Tuple[int, int] or None
        Desired (width, height), or None for largest.

    Returns
    -------
    Tuple[int, int]
        Selected (width, height).

    Raises
    ------
    ValueError
        If no sizes are available.

    Examples
    --------
    >>> select_size([(16, 16), (32, 32), (64, 64)], (32, 32))
    (32, 32)
    >>> select_size([(16, 16), (64, 64)], (40, 40))
    (64, 64)
    >>> select_size([(16, 16), (32, 32)], None)
    (32, 32)
    """
    if not available:
        raise ValueError("No sizes available in ICO")

    # Largest by area default
    largest = max(available, key=lambda s: (s[0] * s[1], s[0], s[1]))
    if not desired:
        return largest

    dw, dh = desired
    # Exact match
    if (dw, dh) in available:
        return (dw, dh)

    # Nearest larger candidates (both dimensions >= requested)
    larger = [(w, h) for (w, h) in available if w >= dw and h >= dh]
    if larger:
        # Prefer square (min |w-h|), then lowest area, then smallest width
        return min(larger, key=lambda s: (abs(s[0] - s[1]), s[0] * s[1], s[0], s[1]))

    # Else largest
    return largest


def open_ico_at_size(path: Path | str, size: Tuple[int, int]) -> Image.Image:
    """Open an ICO file at a specific size.

    Parameters
    ----------
    path : Path or str
        Path to the ICO file.
    size : Tuple[int, int]
        Desired (width, height) to load.

    Returns
    -------
    Image.Image
        PIL Image in RGBA mode at the requested size.

    Notes
    -----
    Pillow may select the closest available size if exact match doesn't exist.
    Always returns RGBA mode for consistent processing.

    Examples
    --------
    >>> img = open_ico_at_size("icon.ico", (32, 32))
    >>> img.size
    (32, 32)
    >>> img.mode
    'RGBA'
    """
    try:
        im = Image.open(str(path), sizes=[size])
        return im.convert("RGBA")
    except Exception:
        im = Image.open(str(path))
        return im.convert("RGBA")
