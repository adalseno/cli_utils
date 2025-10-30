"""Utility to detect if Nerd Fonts are installed on the system."""

import re
import subprocess
from typing import Optional


def check_nerd_fonts() -> int:
    """
    Check if Nerd Fonts are installed on the system using fontconfig's fc-list.

    Returns:
        int: 1 if Nerd Fonts are found, 0 otherwise.

    Note:
        This function requires fontconfig to be installed on the system.
        On Linux/macOS, fc-list is typically available through the fontconfig package.
    """
    try:
        # Run the fc-list command to get all font families
        result = subprocess.run(
            ['fc-list', ':', 'family'],
            capture_output=True,
            text=True,
            check=True,
            timeout=5  # Add timeout to prevent hanging
        )
        font_families = result.stdout.strip().split('\n')

        # Filter for Nerd Fonts using a regex pattern
        # Nerd Fonts typically have "Nerd Font" in their name
        nerd_font_pattern = re.compile(r'.*Nerd\s*Font.*', re.IGNORECASE)
        nerd_fonts = [font for font in font_families if nerd_font_pattern.search(font)]

        if nerd_fonts:
            return 1
        else:
            return 0

    except subprocess.CalledProcessError:
        # fc-list command failed
        return 0
    except subprocess.TimeoutExpired:
        # fc-list took too long
        return 0
    except FileNotFoundError:
        # Fontconfig (fc-list) not found
        return 0
    except Exception:
        # Any other error
        return 0


def get_nerd_fonts_list() -> Optional[list[str]]:
    """
    Get a list of all installed Nerd Fonts.

    Returns:
        Optional[list[str]]: List of Nerd Font family names, or None if not found/error.
    """
    try:
        result = subprocess.run(
            ['fc-list', ':', 'family'],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        font_families = result.stdout.strip().split('\n')

        nerd_font_pattern = re.compile(r'.*Nerd\s*Font.*', re.IGNORECASE)
        nerd_fonts = [font.strip() for font in font_families if nerd_font_pattern.search(font)]

        return nerd_fonts if nerd_fonts else None

    except Exception:
        return None
