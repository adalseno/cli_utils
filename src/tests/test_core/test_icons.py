"""Tests for icon utility with Nerd Font fallback system."""

import os
from unittest.mock import MagicMock, patch

import pytest

from cli_utils.utils.icons import IconManager, Icons, icon, init_icon_manager, get_icon_manager


class TestIconManager:
    """Test the IconManager class."""

    def test_icon_manager_with_nerd_fonts_enabled(self):
        """Test IconManager when Nerd Fonts are enabled."""
        manager = IconManager(nerd_font_support=1)

        # Should attempt to use Nerd Fonts
        result = manager.icon("nf-md-check", "✅", "[DONE]")

        # Result should be a string (either Nerd Font or fallback)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icon_manager_with_nerd_fonts_disabled(self):
        """Test IconManager when Nerd Fonts are disabled."""
        manager = IconManager(nerd_font_support=0)

        # Should use emoji fallback (if terminal supports it) or text
        result = manager.icon("nf-md-check", "✅", "[DONE]")

        # Result should be either emoji or text fallback
        assert result in ["✅", "[DONE]"]

    def test_icon_manager_emoji_fallback(self):
        """Test that emoji is used when Nerd Fonts are disabled and terminal supports emoji."""
        with patch.dict(os.environ, {"TERM": "xterm-256color"}):
            manager = IconManager(nerd_font_support=0)
            result = manager.icon("nf-md-check", "✅", "[DONE]")

            # Should use emoji on xterm
            assert result == "✅"

    def test_icon_manager_text_fallback(self):
        """Test that text is used when terminal doesn't support emoji."""
        with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
            manager = IconManager(nerd_font_support=0)
            result = manager.icon("nf-md-check", "✅", "[DONE]")

            # Should use text fallback on basic terminal
            assert result == "[DONE]"

    def test_icon_manager_terminal_detection(self):
        """Test terminal emoji capability detection."""
        test_cases = [
            ("xterm-256color", True),
            ("kitty", True),
            ("wezterm", True),
            ("alacritty", True),
            ("dumb", False),
            ("vt100", False),
        ]

        for term_value, should_support_emoji in test_cases:
            with patch.dict(os.environ, {"TERM": term_value}, clear=True):
                manager = IconManager(nerd_font_support=0)
                assert manager._terminal_supports_emoji == should_support_emoji, \
                    f"TERM={term_value} should {'support' if should_support_emoji else 'not support'} emoji"

    def test_icon_manager_colorterm_detection(self):
        """Test COLORTERM environment variable detection."""
        with patch.dict(os.environ, {"COLORTERM": "truecolor"}, clear=True):
            manager = IconManager(nerd_font_support=0)
            assert manager._terminal_supports_emoji is True

    def test_icon_manager_term_program_detection(self):
        """Test TERM_PROGRAM environment variable detection."""
        with patch.dict(os.environ, {"TERM_PROGRAM": "iTerm.app"}, clear=True):
            manager = IconManager(nerd_font_support=0)
            assert manager._terminal_supports_emoji is True

    def test_set_nerd_font_support(self):
        """Test dynamically changing Nerd Font support."""
        manager = IconManager(nerd_font_support=0)

        # Initially disabled
        assert manager._nerd_font_support == 0

        # Enable it
        manager.set_nerd_font_support(1)
        assert manager._nerd_font_support == 1


class TestIconsClass:
    """Test the Icons utility class."""

    def test_icons_check(self):
        """Test Icons.check() method."""
        result = Icons.check()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_cross(self):
        """Test Icons.cross() method."""
        result = Icons.cross()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_circle(self):
        """Test Icons.circle() method."""
        result = Icons.circle()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_play(self):
        """Test Icons.play() method."""
        result = Icons.play()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_calendar(self):
        """Test Icons.calendar() method."""
        result = Icons.calendar()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_clock(self):
        """Test Icons.clock() method."""
        result = Icons.clock()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_list(self):
        """Test Icons.list() method."""
        result = Icons.list()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_folder(self):
        """Test Icons.folder() method."""
        result = Icons.folder()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_file(self):
        """Test Icons.file() method."""
        result = Icons.file()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_info(self):
        """Test Icons.info() method."""
        result = Icons.info()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_warning(self):
        """Test Icons.warning() method."""
        result = Icons.warning()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_star(self):
        """Test Icons.star() method."""
        result = Icons.star()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icons_tag(self):
        """Test Icons.tag() method."""
        result = Icons.tag()
        assert isinstance(result, str)
        assert len(result) > 0


class TestIconFunction:
    """Test the icon() convenience function."""

    def test_icon_function_returns_string(self):
        """Test that icon() returns a string."""
        result = icon("nf-md-rocket", "🚀", "[ROCKET]")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_icon_function_with_uninitialized_manager(self):
        """Test icon() function works even if manager not initialized."""
        # This should gracefully fall back to emoji or text
        with patch("cli_utils.utils.icons.get_icon_manager", side_effect=RuntimeError("Not initialized")):
            with patch.dict(os.environ, {"TERM": "xterm-256color"}):
                result = icon("nf-md-test", "🎯", "[TEST]")
                assert result == "🎯"

    def test_icon_function_with_basic_terminal(self):
        """Test icon() function with basic terminal (no emoji support)."""
        with patch("cli_utils.utils.icons.get_icon_manager", side_effect=RuntimeError("Not initialized")):
            with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
                result = icon("nf-md-test", "🎯", "[TEST]")
                assert result == "[TEST]"


class TestIconManagerInitialization:
    """Test icon manager initialization and singleton pattern."""

    def test_init_icon_manager(self):
        """Test initializing the icon manager."""
        manager = init_icon_manager(nerd_font_support=1)

        assert manager is not None
        assert isinstance(manager, IconManager)
        assert manager._nerd_font_support == 1

    def test_get_icon_manager_after_init(self):
        """Test getting the icon manager after initialization."""
        # Initialize first
        init_icon_manager(nerd_font_support=1)

        # Then get it
        manager = get_icon_manager()
        assert manager is not None
        assert isinstance(manager, IconManager)

    def test_get_icon_manager_before_init_raises_error(self):
        """Test that get_icon_manager raises error if not initialized."""
        # Reset the global manager
        import cli_utils.utils.icons as icons_module
        icons_module._icon_manager = None

        with pytest.raises(RuntimeError, match="IconManager not initialized"):
            get_icon_manager()


class TestIconFallbackScenarios:
    """Test various fallback scenarios."""

    def test_nerd_font_priority(self):
        """Test that Nerd Fonts have priority when available."""
        manager = IconManager(nerd_font_support=1)

        # With Nerd Fonts enabled, should try to use them first
        result = manager.icon("nf-md-check", "✅", "[DONE]")

        # Should not be the text fallback
        assert result != "[DONE]"

    def test_emoji_priority_over_text(self):
        """Test that emoji is preferred over text when terminal supports it."""
        with patch.dict(os.environ, {"TERM": "xterm-256color"}):
            manager = IconManager(nerd_font_support=0)
            result = manager.icon("nf-md-test", "🎯", "[TEST]")

            # Should use emoji, not text
            assert result == "🎯"

    def test_text_as_last_resort(self):
        """Test that text is used as last resort."""
        with patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
            manager = IconManager(nerd_font_support=0)
            result = manager.icon("nf-md-test", "🎯", "[TEST]")

            # Should use text fallback
            assert result == "[TEST]"


class TestNerdFontAvailability:
    """Test Nerd Font icon availability."""

    def test_nerd_font_icons_exist(self):
        """Test that expected Nerd Font icons exist in the library."""
        try:
            import nerdfont as nf

            # Icons we're using in the app
            expected_icons = [
                "nf-md-check",
                "nf-md-close",
                "nf-md-checkbox_blank_circle_outline",
                "nf-md-play",
                "nf-md-calendar",
                "nf-md-clock_outline",
                "nf-md-format_list_bulleted",
            ]

            for icon_name in expected_icons:
                assert icon_name in nf.icons, f"Icon {icon_name} should exist in nerdfont library"

        except ImportError:
            pytest.skip("nerdfont library not available")

    def test_nerd_font_returns_string(self):
        """Test that Nerd Font icons return strings."""
        try:
            import nerdfont as nf

            icon_value = nf.icons.get("nf-md-check")
            assert isinstance(icon_value, str)
            assert len(icon_value) > 0

        except ImportError:
            pytest.skip("nerdfont library not available")


class TestIntegrationWithConfig:
    """Test integration between icon system and config."""

    def test_config_initializes_icon_manager(self):
        """Test that getting settings initializes icon manager."""
        from cli_utils.config import get_settings, reset_settings

        # Reset settings to ensure clean state
        reset_settings()

        # Get settings (should initialize icon manager)
        settings = get_settings()

        # Icon manager should be initialized
        try:
            manager = get_icon_manager()
            assert manager is not None
        except RuntimeError:
            pytest.fail("Icon manager should be initialized after get_settings()")

        # Clean up
        reset_settings()

    def test_config_nerd_font_support_field(self):
        """Test that Settings has nerd_font_support field."""
        from cli_utils.config import get_settings, reset_settings

        reset_settings()
        settings = get_settings()

        # Should have nerd_font_support attribute
        assert hasattr(settings, "nerd_font_support")
        assert settings.nerd_font_support in [0, 1]

        # Clean up
        reset_settings()
