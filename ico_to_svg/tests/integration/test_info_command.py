"""Integration tests for info command."""

import json
from pathlib import Path

from ico_to_svg.cli import main


class TestInfoCommand:
    """Integration tests for the info subcommand."""

    def test_info_text_output(self, multi_size_ico: Path, capsys) -> None:
        """Test info command with text output."""
        main(["info", str(multi_size_ico)])
        captured = capsys.readouterr()
        assert "Available sizes:" in captured.out
        assert "16x16" in captured.out
        assert "32x32" in captured.out
        assert "64x64" in captured.out
        assert "128x128" in captured.out

    def test_info_json_output(self, multi_size_ico: Path, capsys) -> None:
        """Test info command with JSON output."""
        main(["info", str(multi_size_ico), "--json"])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert len(data) >= 4
        # Check expected sizes are present
        widths = {item["width"] for item in data}
        assert 16 in widths
        assert 32 in widths
        assert 64 in widths
        assert 128 in widths

    def test_info_with_size_filter(self, multi_size_ico: Path, capsys) -> None:
        """Test info command with size filter."""
        main(["info", str(multi_size_ico), "--size", "32"])
        captured = capsys.readouterr()
        assert "32x32" in captured.out

    def test_info_json_with_size_filter(
        self, multi_size_ico: Path, capsys
    ) -> None:
        """Test info command with JSON and size filter."""
        main(["info", str(multi_size_ico), "--json", "--size", "64"])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data) == 1
        assert data[0]["width"] == 64
        assert data[0]["height"] == 64

    def test_info_single_size_ico(self, single_size_ico: Path, capsys) -> None:
        """Test info on single-size ICO."""
        main(["info", str(single_size_ico)])
        captured = capsys.readouterr()
        assert "48x48" in captured.out
