"""Simple smoke tests for ico-to-svg CLI logic."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv_cli" / "Scripts"
CLI = VENV / "ico-to-svg.exe"
DATA = ROOT / "data"
ICO = DATA / "test-multi.ico"


def run(cmd):
    print("==>", " ".join(cmd))
    completed = subprocess.run(cmd, capture_output=True, text=True)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)
    completed.check_returncode()


def main():
    if not ICO.exists():
        print("ICO file missing; run generate_ico.py first", file=sys.stderr)
        sys.exit(1)
    run([str(CLI), "info", str(ICO), "--json"])
    run([str(CLI), "convert", str(ICO), str(DATA / "test-64-raster.svg"), "--size", "64"])
    run(
        [
            str(CLI),
            "convert",
            str(ICO),
            str(DATA / "test-64-vector.svg"),
            "--size",
            "64",
            "--mode",
            "vector",
            "--alpha-threshold",
            "16",
        ]
    )
    print("Smoke tests passed.")


if __name__ == "__main__":
    main()
