"""Clipboard utilities for CLI Utils.

This module provides cross-platform clipboard support using native system tools
when available, falling back to Python packages if needed.
"""

import subprocess
import sys
from typing import Optional

from rich.console import Console

console = Console()


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard using available methods.

    Tries multiple methods in order of preference:
    1. Native system tools (xclip, xsel, wl-copy on Linux; pbcopy on macOS)
    2. Python pyperclip package (if installed)

    Args:
        text: Text to copy to clipboard

    Returns:
        True if successful, False otherwise

    Example:
        >>> if copy_to_clipboard("Hello"):
        ...     print("Copied!")
    """
    # Try platform-specific native tools first
    if sys.platform == "linux":
        return _copy_linux(text)
    elif sys.platform == "darwin":
        return _copy_macos(text)
    elif sys.platform == "win32":
        return _copy_windows(text)
    else:
        # Fall back to pyperclip for unknown platforms
        return _copy_pyperclip(text)


def _copy_linux(text: str) -> bool:
    """Copy to clipboard on Linux using native tools.

    Tries in order: wl-copy (Wayland), xclip, xsel

    Args:
        text: Text to copy

    Returns:
        True if successful
    """
    # Check if we have a display (X11 or Wayland)
    import os

    has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))

    if not has_display:
        # No display available, inform user
        console.print(
            "[yellow]Warning: No display available (SSH/headless session). "
            "Clipboard unavailable.[/yellow]"
        )
        # Try pyperclip anyway (might work in some cases)
        return _copy_pyperclip(text)

    # Try wl-clipboard (Wayland)
    if _try_command(["wl-copy"], text):
        console.print("[dim]✓ Copied to clipboard (wl-copy)[/dim]")
        return True

    # Try xclip
    if _try_command(["xclip", "-selection", "clipboard"], text):
        console.print("[dim]✓ Copied to clipboard (xclip)[/dim]")
        return True

    # Try xsel
    if _try_command(["xsel", "--clipboard", "--input"], text):
        console.print("[dim]✓ Copied to clipboard (xsel)[/dim]")
        return True

    # Fall back to pyperclip
    if _copy_pyperclip(text):
        return True

    # Show installation help
    console.print(
        "[yellow]Warning: No clipboard tool found. "
        "Install xclip, xsel, or wl-clipboard:[/yellow]"
    )
    console.print("[dim]  sudo apt install xclip[/dim]")
    return False


def _copy_macos(text: str) -> bool:
    """Copy to clipboard on macOS using pbcopy.

    Args:
        text: Text to copy

    Returns:
        True if successful
    """
    if _try_command(["pbcopy"], text):
        console.print("[dim]✓ Copied to clipboard (pbcopy)[/dim]")
        return True

    # Fall back to pyperclip
    if _copy_pyperclip(text):
        return True

    console.print("[yellow]Warning: pbcopy not found[/yellow]")
    return False


def _copy_windows(text: str) -> bool:
    """Copy to clipboard on Windows using clip.

    Args:
        text: Text to copy

    Returns:
        True if successful
    """
    if _try_command(["clip"], text):
        console.print("[dim]✓ Copied to clipboard (clip)[/dim]")
        return True

    # Fall back to pyperclip
    if _copy_pyperclip(text):
        return True

    console.print("[yellow]Warning: clip command not found[/yellow]")
    return False


def _copy_pyperclip(text: str) -> bool:
    """Copy using pyperclip Python package.

    Args:
        text: Text to copy

    Returns:
        True if successful
    """
    try:
        import pyperclip

        pyperclip.copy(text)
        console.print("[dim]✓ Copied to clipboard (pyperclip)[/dim]")
        return True
    except ImportError:
        return False
    except Exception as e:
        console.print(f"[yellow]Warning: Clipboard error: {e}[/yellow]")
        return False


def _try_command(cmd: list[str], text: str) -> bool:
    """Try to run a clipboard command.

    Args:
        cmd: Command to run (as list)
        text: Text to pipe to command

    Returns:
        True if command succeeded
    """
    try:
        # Start process in background - xclip/xsel stay running to serve clipboard
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Write data and close stdin
        process.stdin.write(text.encode("utf-8"))
        process.stdin.close()

        # Give it a brief moment to start
        import time
        time.sleep(0.05)

        # Check process status
        poll_result = process.poll()

        if poll_result is None:
            # Still running - normal for xclip/xsel
            return True
        elif poll_result == 0:
            # Exited successfully - normal for wl-copy
            return True
        else:
            # Exited with error
            return False

    except FileNotFoundError:
        # Command not found
        return False
    except Exception:
        # Any other error
        return False


def get_clipboard_info() -> dict[str, Optional[str]]:
    """Get information about available clipboard tools.

    Returns:
        Dictionary with clipboard tool information
    """
    info = {
        "platform": sys.platform,
        "available_tools": [],
        "recommended": None,
    }

    if sys.platform == "linux":
        if _command_exists("wl-copy"):
            info["available_tools"].append("wl-copy (Wayland)")
            info["recommended"] = "wl-copy"
        if _command_exists("xclip"):
            info["available_tools"].append("xclip")
            if not info["recommended"]:
                info["recommended"] = "xclip"
        if _command_exists("xsel"):
            info["available_tools"].append("xsel")
            if not info["recommended"]:
                info["recommended"] = "xsel"
    elif sys.platform == "darwin":
        if _command_exists("pbcopy"):
            info["available_tools"].append("pbcopy")
            info["recommended"] = "pbcopy"
    elif sys.platform == "win32":
        if _command_exists("clip"):
            info["available_tools"].append("clip")
            info["recommended"] = "clip"

    # Check for pyperclip
    try:
        import pyperclip  # noqa: F401

        info["available_tools"].append("pyperclip (Python)")
        if not info["recommended"]:
            info["recommended"] = "pyperclip"
    except ImportError:
        pass

    return info


def _command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH.

    Args:
        cmd: Command name to check

    Returns:
        True if command exists
    """
    try:
        result = subprocess.run(
            ["which", cmd] if sys.platform != "win32" else ["where", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1,
        )
        return result.returncode == 0
    except Exception:
        return False
