"""ico-to-svg: Convert Windows ICO files to SVG."""

__all__ = ["convert_ico_to_svg", "load_ico_frames", "main"]

from .cli import main
from .core import convert_ico_to_svg
from .ico_parser import load_ico_frames

__version__ = "0.1.0"
