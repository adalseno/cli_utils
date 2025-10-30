"""Tests for Nerd Font detection utility."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from cli_utils.utils.nerd_font_check import check_nerd_fonts, get_nerd_fonts_list


class TestCheckNerdFonts:
    """Test the check_nerd_fonts function."""

    def test_check_nerd_fonts_returns_int(self):
        """Test that check_nerd_fonts returns an integer."""
        result = check_nerd_fonts()
        assert isinstance(result, int)
        assert result in [0, 1]

    @patch("subprocess.run")
    def test_check_nerd_fonts_with_nerd_fonts_installed(self, mock_run):
        """Test detection when Nerd Fonts are installed."""
        # Mock fc-list output with Nerd Fonts
        mock_run.return_value = MagicMock(
            stdout="FiraCode Nerd Font\nDejaVu Sans\nGeistMono Nerd Font\n",
            returncode=0
        )

        result = check_nerd_fonts()

        assert result == 1
        mock_run.assert_called_once_with(
            ['fc-list', ':', 'family'],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )

    @patch("subprocess.run")
    def test_check_nerd_fonts_without_nerd_fonts(self, mock_run):
        """Test detection when no Nerd Fonts are installed."""
        # Mock fc-list output without Nerd Fonts
        mock_run.return_value = MagicMock(
            stdout="DejaVu Sans\nLiberation Mono\nUbuntu\n",
            returncode=0
        )

        result = check_nerd_fonts()

        assert result == 0

    @patch("subprocess.run")
    def test_check_nerd_fonts_case_insensitive(self, mock_run):
        """Test that detection is case-insensitive."""
        # Mock with different case
        mock_run.return_value = MagicMock(
            stdout="FiraCode NERD FONT\n",
            returncode=0
        )

        result = check_nerd_fonts()

        assert result == 1

    @patch("subprocess.run")
    def test_check_nerd_fonts_handles_subprocess_error(self, mock_run):
        """Test handling of subprocess errors."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "fc-list")

        result = check_nerd_fonts()

        # Should return 0 on error
        assert result == 0

    @patch("subprocess.run")
    def test_check_nerd_fonts_handles_timeout(self, mock_run):
        """Test handling of subprocess timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("fc-list", 5)

        result = check_nerd_fonts()

        # Should return 0 on timeout
        assert result == 0

    @patch("subprocess.run")
    def test_check_nerd_fonts_handles_file_not_found(self, mock_run):
        """Test handling when fc-list is not found."""
        mock_run.side_effect = FileNotFoundError()

        result = check_nerd_fonts()

        # Should return 0 when fc-list not found
        assert result == 0

    @patch("subprocess.run")
    def test_check_nerd_fonts_handles_generic_exception(self, mock_run):
        """Test handling of generic exceptions."""
        mock_run.side_effect = Exception("Unexpected error")

        result = check_nerd_fonts()

        # Should return 0 on any exception
        assert result == 0

    @patch("subprocess.run")
    def test_check_nerd_fonts_matches_pattern(self, mock_run):
        """Test that the Nerd Font pattern matching works correctly."""
        test_cases = [
            ("FiraCode Nerd Font", True),
            ("Nerd Font Mono", True),
            ("SomeFont NerdFont", True),
            ("nerd font", True),  # Case insensitive
            ("NERD FONT", True),  # Case insensitive
            ("Regular Font", False),
            ("DejaVu Sans", False),
            ("", False),
        ]

        for font_name, should_match in test_cases:
            mock_run.return_value = MagicMock(
                stdout=font_name + "\n",
                returncode=0
            )

            result = check_nerd_fonts()
            expected = 1 if should_match else 0

            assert result == expected, \
                f"Font '{font_name}' should {'match' if should_match else 'not match'} Nerd Font pattern"


class TestGetNerdFontsList:
    """Test the get_nerd_fonts_list function."""

    def test_get_nerd_fonts_list_returns_list_or_none(self):
        """Test that get_nerd_fonts_list returns list or None."""
        result = get_nerd_fonts_list()
        assert result is None or isinstance(result, list)

    @patch("subprocess.run")
    def test_get_nerd_fonts_list_with_fonts(self, mock_run):
        """Test getting list of installed Nerd Fonts."""
        mock_run.return_value = MagicMock(
            stdout="FiraCode Nerd Font\nDejaVu Sans\nGeistMono Nerd Font\n",
            returncode=0
        )

        result = get_nerd_fonts_list()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2
        assert "FiraCode Nerd Font" in result
        assert "GeistMono Nerd Font" in result
        assert "DejaVu Sans" not in result

    @patch("subprocess.run")
    def test_get_nerd_fonts_list_without_fonts(self, mock_run):
        """Test getting list when no Nerd Fonts installed."""
        mock_run.return_value = MagicMock(
            stdout="DejaVu Sans\nLiberation Mono\n",
            returncode=0
        )

        result = get_nerd_fonts_list()

        # Should return None when no Nerd Fonts found
        assert result is None

    @patch("subprocess.run")
    def test_get_nerd_fonts_list_handles_error(self, mock_run):
        """Test error handling in get_nerd_fonts_list."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "fc-list")

        result = get_nerd_fonts_list()

        # Should return None on error
        assert result is None

    @patch("subprocess.run")
    def test_get_nerd_fonts_list_strips_whitespace(self, mock_run):
        """Test that font names are stripped of whitespace."""
        mock_run.return_value = MagicMock(
            stdout="  FiraCode Nerd Font  \n  GeistMono Nerd Font  \n",
            returncode=0
        )

        result = get_nerd_fonts_list()

        assert result is not None
        assert "FiraCode Nerd Font" in result
        assert "  FiraCode Nerd Font  " not in result

    @patch("subprocess.run")
    def test_get_nerd_fonts_list_timeout(self, mock_run):
        """Test timeout handling in get_nerd_fonts_list."""
        mock_run.side_effect = subprocess.TimeoutExpired("fc-list", 5)

        result = get_nerd_fonts_list()

        assert result is None

    @patch("subprocess.run")
    def test_get_nerd_fonts_list_file_not_found(self, mock_run):
        """Test handling when fc-list is not found."""
        mock_run.side_effect = FileNotFoundError()

        result = get_nerd_fonts_list()

        assert result is None


class TestIntegration:
    """Integration tests for Nerd Font detection."""

    def test_check_and_get_consistency(self):
        """Test that check_nerd_fonts and get_nerd_fonts_list are consistent."""
        check_result = check_nerd_fonts()
        list_result = get_nerd_fonts_list()

        if check_result == 1:
            # If check says fonts are installed, list should not be None
            assert list_result is not None
            assert len(list_result) > 0
        else:
            # If check says no fonts, list should be None
            assert list_result is None

    @patch("subprocess.run")
    def test_multiple_nerd_fonts_detected(self, mock_run):
        """Test detection with multiple Nerd Fonts installed."""
        mock_run.return_value = MagicMock(
            stdout=(
                "FiraCode Nerd Font\n"
                "Hack Nerd Font\n"
                "JetBrainsMono Nerd Font\n"
                "DejaVu Sans\n"
                "Ubuntu Mono\n"
            ),
            returncode=0
        )

        check_result = check_nerd_fonts()
        list_result = get_nerd_fonts_list()

        assert check_result == 1
        assert list_result is not None
        assert len(list_result) == 3
        assert "FiraCode Nerd Font" in list_result
        assert "Hack Nerd Font" in list_result
        assert "JetBrainsMono Nerd Font" in list_result

    @patch("subprocess.run")
    def test_empty_fc_list_output(self, mock_run):
        """Test handling of empty fc-list output."""
        mock_run.return_value = MagicMock(
            stdout="",
            returncode=0
        )

        check_result = check_nerd_fonts()
        list_result = get_nerd_fonts_list()

        assert check_result == 0
        assert list_result is None
