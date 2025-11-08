"""Command-line interface for ico-to-svg."""

import argparse
import json
import sys

from .core import convert_ico_to_svg
from .ico_parser import load_ico_frames, parse_size_arg, select_size


def main(argv: list[str] | None = None) -> None:
    """Entry point for ico-to-svg CLI.

    Parameters
    ----------
    argv : List[str] or None, optional
        Command-line arguments. If None, uses sys.argv[1:].

    Notes
    -----
    Supports legacy invocation without subcommand by auto-prepending "convert"
    when first argument is not a subcommand or option flag.

    Examples
    --------
    >>> main(["convert", "icon.ico", "icon.svg"])
    >>> main(["icon.ico", "icon.svg", "--size", "32"])  # Legacy
    >>> main(["info", "icon.ico", "--json"])
    """
    # Accept legacy invocation without subcommand by auto-prepending "convert"
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] not in {"convert", "info"} and not argv[0].startswith("-"):
        argv = ["convert", *argv]

    parser = argparse.ArgumentParser(
        prog="ico-to-svg", description="Convert ICO to SVG (raster embed or naive vector)"
    )
    parser.add_argument("--version", action="version", version="ico-to-svg 0.1.0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # convert subcommand
    p_conv = sub.add_parser("convert", help="Convert an ICO to SVG")
    p_conv.add_argument("input", help="Input .ico file")
    p_conv.add_argument("output", help="Output .svg file")
    p_conv.add_argument(
        "--mode",
        choices=["raster", "vector"],
        default="raster",
        help="Conversion mode (default: raster)",
    )
    p_conv.add_argument(
        "--alpha-threshold",
        type=int,
        default=16,
        help="Vector mode: minimum alpha to treat pixel as solid (default: 16)",
    )
    p_conv.add_argument(
        "--background",
        default="transparent",
        help='Background color (CSS color) or "transparent" (default: transparent)',
    )
    p_conv.add_argument("--size", help="Desired icon size (e.g., 256 or 256x256)")

    # info subcommand
    p_info = sub.add_parser("info", help="List available sizes in an ICO")
    p_info.add_argument("input", help="Input .ico file")
    p_info.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    p_info.add_argument("--size", help="Filter by size (e.g., 256 or 256x256)")

    args = parser.parse_args(argv)

    if args.cmd == "convert":
        convert_ico_to_svg(
            input_path=args.input,
            output_path=args.output,
            mode=args.mode,
            alpha_threshold=args.alpha_threshold,
            background=args.background,
            size=args.size,
        )
        print(f"Wrote {args.output} ({args.mode} mode)")
        return

    # info subcommand
    sizes = load_ico_frames(args.input)
    if args.size:
        desired = parse_size_arg(args.size)
        selected = select_size(sizes, desired)
        sizes = [selected]

    if args.json:
        out = [
            {"width": int(w), "height": int(h)}
            for (w, h) in sorted(sizes, key=lambda s: (s[0] * s[1], s[0], s[1]))
        ]
        print(json.dumps(out, ensure_ascii=False))
    else:
        if not sizes:
            print("No sizes found")
        else:
            print("Available sizes:")
            for w, h in sorted(sizes, key=lambda s: (s[0] * s[1], s[0], s[1])):
                print(f" - {w}x{h}")
