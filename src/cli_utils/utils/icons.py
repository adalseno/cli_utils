"""Icon utility with intelligent fallback for Nerd Fonts, emoji, and text."""

import os
from typing import Any, Optional

try:
    import nerdfont as nf
    NERDFONT_AVAILABLE = True
except ImportError:
    nf: Any = None  # Placeholder when nerdfont is not installed
    NERDFONT_AVAILABLE = False


class IconManager:
    """Manages icon display with intelligent fallback system."""

    def __init__(self, nerd_font_support: Optional[int] = None):
        """
        Initialize the IconManager.

        Args:
            nerd_font_support: Optional override for Nerd Font support.
                              If None, will be determined from config.
                              1 = enabled, 0 = disabled.
        """
        self._nerd_font_support = nerd_font_support
        self._terminal_supports_emoji = self._check_terminal_emoji_support()

    def _check_terminal_emoji_support(self) -> bool:
        """
        Check if the current terminal likely supports emoji rendering.

        Returns:
            bool: True if terminal likely supports emoji, False otherwise.
        """
        term = os.environ.get("TERM", "").lower()
        term_program = os.environ.get("TERM_PROGRAM", "").lower()
        colorterm = os.environ.get("COLORTERM", "").lower()

        # Modern terminals that support emoji
        emoji_capable_terms = [
            "xterm-256color",
            "kitty",
            "wezterm",
            "alacritty",
            "iterm",
            "vscode",
            "gnome",
            "konsole",
        ]

        # Check TERM variable
        if any(capable in term for capable in emoji_capable_terms):
            return True

        # Check TERM_PROGRAM (macOS, VSCode, etc.)
        if any(capable in term_program for capable in emoji_capable_terms):
            return True

        # Check COLORTERM (modern terminals)
        if "truecolor" in colorterm or "24bit" in colorterm:
            return True

        return False

    def set_nerd_font_support(self, enabled: int):
        """
        Set Nerd Font support status.

        Args:
            enabled: 1 to enable, 0 to disable Nerd Font usage.
        """
        self._nerd_font_support = enabled

    def icon(
        self,
        nerd_icon_name: str,
        emoji_char: str,
        fallback: str,
    ) -> str:
        """
        Get the appropriate icon based on system capabilities.

        Priority order:
        1. Nerd Font icon (if nerd_font_support is enabled and nerdfont package available)
        2. Emoji character (if terminal supports emoji)
        3. Fallback string (text representation)

        Args:
            nerd_icon_name: The Nerd Font icon name (e.g., "nf-md-check")
            emoji_char: The emoji character to use as fallback
            fallback: Plain text string as final fallback

        Returns:
            str: The appropriate icon representation

        Example:
            >>> icons = IconManager(nerd_font_support=1)
            >>> icons.icon("nf-md-check", "✅", "[DONE]")
            ''  # Returns Nerd Font check icon
        """
        # Priority 1: Nerd Font (if enabled and available)
        if self._nerd_font_support == 1 and NERDFONT_AVAILABLE:
            try:
                # nerdfont library uses icons dict
                if nerd_icon_name in nf.icons:
                    return nf.icons[nerd_icon_name]
            except (KeyError, AttributeError):
                pass  # Fall through to next option

        # Priority 2: Emoji (if terminal supports it)
        if self._terminal_supports_emoji:
            return emoji_char

        # Priority 3: Fallback text
        return fallback


# Global icon manager instance - will be initialized from config
_icon_manager: Optional[IconManager] = None


def init_icon_manager(nerd_font_support: int) -> IconManager:
    """
    Initialize the global icon manager with Nerd Font support setting.

    Args:
        nerd_font_support: 1 if Nerd Fonts are available, 0 otherwise

    Returns:
        IconManager: The initialized icon manager instance
    """
    global _icon_manager
    _icon_manager = IconManager(nerd_font_support=nerd_font_support)
    return _icon_manager


def get_icon_manager() -> IconManager:
    """
    Get the global icon manager instance.

    Returns:
        IconManager: The icon manager instance

    Raises:
        RuntimeError: If icon manager hasn't been initialized
    """
    if _icon_manager is None:
        raise RuntimeError(
            "IconManager not initialized. Call init_icon_manager() first."
        )
    return _icon_manager


# Convenience function for easy usage
def icon(nerd_icon_name: str, emoji_char: str, fallback: str) -> str:
    """
    Convenience function to get an icon using the global icon manager.

    Args:
        nerd_icon_name: The Nerd Font icon name
        emoji_char: The emoji character fallback
        fallback: Plain text fallback

    Returns:
        str: The appropriate icon representation

    Example:
        >>> from cli_utils.utils.icons import icon
        >>> check = icon("nf-md-check", "✅", "[DONE]")
    """
    try:
        manager = get_icon_manager()
        return manager.icon(nerd_icon_name, emoji_char, fallback)
    except RuntimeError:
        # If not initialized, use basic fallback
        # This allows graceful degradation
        term = os.environ.get("TERM", "").lower()
        if any(t in term for t in ["xterm", "kitty", "wezterm", "alacritty"]):
            return emoji_char
        return fallback


# Common icon definitions for easy reuse
class Icons:
    """Common icon definitions used throughout the application."""

    @staticmethod
    def check() -> str:
        """Checkmark/completed icon."""
        return icon("nf-md-check", "✅", "[✓]")

    @staticmethod
    def cross() -> str:
        """Cross/error icon."""
        return icon("nf-md-close", "❌", "[✗]")

    @staticmethod
    def circle() -> str:
        """Circle/new task icon."""
        return icon("nf-md-checkbox_blank_circle_outline", "⭕", "[ ]")

    @staticmethod
    def play() -> str:
        """Play/in-progress icon."""
        return icon("nf-md-play", "▶️", "[>]")

    @staticmethod
    def calendar() -> str:
        """Calendar/due date icon."""
        return icon("nf-md-calendar", "📅", "[DATE]")

    @staticmethod
    def clock() -> str:
        """Clock/reminder icon."""
        return icon("nf-md-clock_outline", "⏰", "[TIME]")

    @staticmethod
    def list() -> str:
        """List/category icon."""
        return icon("nf-md-format_list_bulleted", "📋", "[LIST]")

    @staticmethod
    def folder() -> str:
        """Folder icon."""
        return icon("nf-md-folder", "📁", "[FOLDER]")

    @staticmethod
    def file() -> str:
        """File icon."""
        return icon("nf-md-file", "📄", "[FILE]")

    @staticmethod
    def info() -> str:
        """Information icon."""
        return icon("nf-md-information", "ℹ️", "[i]")

    @staticmethod
    def warning() -> str:
        """Warning icon."""
        return icon("nf-md-alert", "⚠️", "[!]")

    @staticmethod
    def star() -> str:
        """Star/favorite icon."""
        return icon("nf-md-star", "⭐", "[*]")

    @staticmethod
    def tag() -> str:
        """Tag icon."""
        return icon("nf-md-tag", "🏷️", "[TAG]")
