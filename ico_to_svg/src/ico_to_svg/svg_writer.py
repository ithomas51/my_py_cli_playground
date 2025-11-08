"""SVG generation for raster and vector modes."""

import base64
import io
from dataclasses import dataclass
from pathlib import Path

import svgwrite
from PIL import Image


@dataclass
class Run:
    """Horizontal run of pixels with same color.

    Attributes
    ----------
    y : int
        Row index (0-based).
    x1 : int
        Starting column (inclusive).
    x2 : int
        Ending column (inclusive).
    """

    y: int
    x1: int
    x2: int  # inclusive end


def vectorize(
    image: Image.Image, alpha_threshold: int
) -> tuple[dict[tuple[int, int, int, int], list[Run]], int, int]:
    """Vectorize an image into horizontal runs grouped by color.

    Parameters
    ----------
    image : Image.Image
        PIL Image in RGBA mode.
    alpha_threshold : int
        Minimum alpha value (0-255) to consider pixel opaque.

    Returns
    -------
    color_runs : Dict[Tuple[int, int, int, int], List[Run]]
        Dictionary mapping (R, G, B, 255) tuples to lists of Run objects.
    width : int
        Image width.
    height : int
        Image height.

    Notes
    -----
    Pixels with alpha below threshold are treated as transparent (skipped).
    All opaque pixels are normalized to alpha=255.

    Examples
    --------
    >>> img = Image.new("RGBA", (4, 2), (255, 0, 0, 255))
    >>> color_runs, w, h = vectorize(img, 128)
    >>> w, h
    (4, 2)
    >>> len(color_runs)
    1
    """
    w, h = image.size
    pixels = image.load()
    if pixels is None:
        raise ValueError("Failed to load image pixels")

    color_runs: dict[tuple[int, int, int, int], list[Run]] = {}
    for y in range(h):
        x = 0
        while x < w:
            pixel = pixels[x, y]
            if not isinstance(pixel, tuple) or len(pixel) < 4:
                x += 1
                continue
            r, g, b, a = int(pixel[0]), int(pixel[1]), int(pixel[2]), int(pixel[3])
            if a < alpha_threshold:
                x += 1
                continue
            color = (r, g, b, 255)
            x_start = x
            x += 1
            while x < w:
                pixel2 = pixels[x, y]
                if not isinstance(pixel2, tuple) or len(pixel2) < 4:
                    break
                r2, g2, b2, a2 = int(pixel2[0]), int(pixel2[1]), int(pixel2[2]), int(pixel2[3])
                if a2 < alpha_threshold or (r2, g2, b2) != (r, g, b):
                    break
                x += 1
            x_end = x - 1
            color_runs.setdefault(color, []).append(Run(y, x_start, x_end))
    return color_runs, w, h


def runs_to_path_d(runs: list[Run]) -> str:
    """Convert runs into SVG path data string.

    Parameters
    ----------
    runs : List[Run]
        List of horizontal runs.

    Returns
    -------
    str
        SVG path data string with rectangle commands for each run.

    Notes
    -----
    Each run becomes a rectangle: M x,y H x2 V y+1 H x Z

    Examples
    --------
    >>> runs = [Run(0, 0, 3), Run(1, 0, 3)]
    >>> runs_to_path_d(runs)
    'M0,0H4V1H0Z M0,1H4V2H0Z'
    """
    parts = []
    for run in runs:
        x1 = run.x1
        x2 = run.x2 + 1  # exclusive for H command
        y = run.y
        parts.append(f"M{x1},{y}H{x2}V{y + 1}H{x1}Z")
    return " ".join(parts)


def write_svg_vector(
    color_runs: dict[tuple[int, int, int, int], list[Run]],
    width: int,
    height: int,
    output: Path | str,
    background: str | None = None,
) -> None:
    """Write vectorized SVG with rectangle paths.

    Parameters
    ----------
    color_runs : Dict[Tuple[int, int, int, int], List[Run]]
        Color-keyed runs from vectorize().
    width : int
        Canvas width.
    height : int
        Canvas height.
    output : Path or str
        Output SVG file path.
    background : str or None, optional
        CSS color for background, or "transparent".

    Notes
    -----
    Creates one path element per color, each containing all runs of that color.

    Examples
    --------
    >>> runs = {(255, 0, 0, 255): [Run(0, 0, 3)]}
    >>> write_svg_vector(runs, 4, 1, "out.svg")
    """
    dwg = svgwrite.Drawing(
        str(output), size=(f"{width}px", f"{height}px"), viewBox=f"0 0 {width} {height}"
    )
    if background and background != "transparent":
        dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=background))
    for (r, g, b, _a), runs in color_runs.items():
        fill = f"#{r:02x}{g:02x}{b:02x}"
        d = runs_to_path_d(runs)
        dwg.add(dwg.path(d=d, fill=fill, stroke="none"))
    dwg.save()


def write_svg_raster(image: Image.Image, output: Path | str, background: str | None = None) -> None:
    """Write raster SVG with base64-embedded PNG.

    Parameters
    ----------
    image : Image.Image
        PIL Image in RGBA mode.
    output : Path or str
        Output SVG file path.
    background : str or None, optional
        CSS color for background compositing, or "transparent".

    Notes
    -----
    If background is specified (and not "transparent"), composites the image
    over a solid background before embedding.

    Examples
    --------
    >>> img = Image.new("RGBA", (16, 16), (255, 0, 0, 255))
    >>> write_svg_raster(img, "out.svg")
    >>> write_svg_raster(img, "out_bg.svg", background="#ffffff")
    """
    if background and background != "transparent":
        bg = Image.new("RGBA", image.size, background)
        bg.alpha_composite(image)
        image = bg.convert("RGBA")
    else:
        image = image.convert("RGBA")
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    w, h = image.size
    svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>
  <image href='data:image/png;base64,{b64}' x='0' y='0' width='{w}' height='{h}' />
</svg>
"""
    with open(str(output), "w", encoding="utf-8") as f:
        f.write(svg)
