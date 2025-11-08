"""Core conversion API orchestrating ICO parsing and SVG generation."""

from pathlib import Path

from .ico_parser import load_ico_frames, open_ico_at_size, parse_size_arg, select_size
from .svg_writer import vectorize, write_svg_raster, write_svg_vector


def convert_ico_to_svg(
    input_path: Path | str,
    output_path: Path | str,
    mode: str = "raster",
    alpha_threshold: int = 16,
    background: str | None = "transparent",
    size: str | None = None,
) -> None:
    """Convert an ICO file to SVG.

    Parameters
    ----------
    input_path : Path or str
        Input ICO file path.
    output_path : Path or str
        Output SVG file path.
    mode : {"raster", "vector"}, optional
        Conversion mode. "raster" embeds a base64 PNG; "vector"
        generates rectangle paths per color run. Default is "raster".
    alpha_threshold : int, optional
        Minimum alpha (0-255) to treat pixel as opaque in vector mode.
        Default is 16.
    background : str or None, optional
        CSS color for background, or "transparent". Default is "transparent".
    size : str or None, optional
        Desired size like "256" or "256x256". If None, uses largest available.

    Raises
    ------
    FileNotFoundError
        If input_path does not exist.
    ValueError
        If size format is invalid or ICO has no frames.

    Examples
    --------
    >>> convert_ico_to_svg("icon.ico", "icon.svg")
    >>> convert_ico_to_svg("icon.ico", "icon_32.svg", size="32")
    >>> convert_ico_to_svg("icon.ico", "icon_vec.svg", mode="vector", alpha_threshold=16)
    """
    sizes = load_ico_frames(input_path)
    desired = parse_size_arg(size) if size else None
    selected = select_size(sizes, desired)
    img = open_ico_at_size(input_path, selected)

    if mode == "raster":
        write_svg_raster(img, output_path, background)
    else:
        color_runs, w, h = vectorize(img, alpha_threshold)
        write_svg_vector(color_runs, w, h, output_path, background)


__all__ = ["convert_ico_to_svg"]
