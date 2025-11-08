#!/usr/bin/env python3
"""Deprecated entry point.

Use the installed console script `ico-to-svg` (or alias `ico2svg`).
This shim will be removed after two minor releases.
"""
from warnings import warn

from ico_to_svg.cli import main

if __name__ == "__main__":
    warn(
        "Direct invocation of ico_to_svg.py is deprecated; use the `ico-to-svg` command.",
        DeprecationWarning,
        stacklevel=2,
    )
    main()
