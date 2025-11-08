"""Unit tests for ICO size selection algorithm."""

import pytest

from ico_to_svg.ico_parser import select_size


class TestSizeSelection:
    """Test size selection algorithm: exact → nearest larger → largest."""

    @pytest.mark.parametrize(
        "available,desired,expected",
        [
            # Exact match
            ([(16, 16), (32, 32), (64, 64)], (32, 32), (32, 32)),
            ([(16, 16), (48, 48), (128, 128)], (48, 48), (48, 48)),
            # Nearest larger (prefer square)
            ([(16, 16), (48, 48), (64, 64)], (40, 40), (48, 48)),
            # Nearest larger (prefer smallest area when multiple larger)
            ([(32, 32), (64, 64), (128, 128)], (50, 50), (64, 64)),
            # Fallback to largest when no larger available
            ([(16, 16), (32, 32)], (64, 64), (32, 32)),
            ([(16, 16), (32, 32), (48, 48)], (100, 100), (48, 48)),
            # Non-square: prefer square on tie
            ([(32, 16), (32, 32)], (24, 24), (32, 32)),
            # Multiple candidates: prefer lower area
            ([(40, 40), (50, 30), (60, 60)], (35, 35), (40, 40)),
            # No desired size: return largest
            ([(16, 16), (32, 32), (64, 64)], None, (64, 64)),
            ([(48, 48), (16, 16), (128, 128), (32, 32)], None, (128, 128)),
        ],
    )
    def test_size_selection_rules(
        self,
        available: list[tuple[int, int]],
        desired: tuple[int, int] | None,
        expected: tuple[int, int],
    ) -> None:
        """Test size selection priority rules."""
        result = select_size(available, desired)
        assert result == expected

    def test_no_sizes_raises_error(self) -> None:
        """Test that empty size list raises ValueError."""
        with pytest.raises(ValueError, match="No sizes available"):
            select_size([], (32, 32))

    def test_single_size_always_selected(self) -> None:
        """Test that single available size is always chosen."""
        assert select_size([(128, 128)], None) == (128, 128)
        assert select_size([(128, 128)], (16, 16)) == (128, 128)
        assert select_size([(128, 128)], (256, 256)) == (128, 128)

    def test_non_square_sizes(self) -> None:
        """Test selection with non-square sizes."""
        # Prefer square when available
        assert select_size([(32, 64), (64, 64)], (50, 50)) == (64, 64)
        # Choose non-square if only option
        assert select_size([(32, 64)], (40, 40)) == (32, 64)
        # Nearest larger with mixed aspect ratios
        assert select_size([(16, 32), (32, 32), (64, 32)], (24, 24)) == (32, 32)
