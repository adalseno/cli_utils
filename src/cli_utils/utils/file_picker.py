"""File and directory picker utilities for terminal file managers.

This module provides integration with terminal file managers like Yazi and
Midnight Commander to allow interactive directory selection.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Literal, Optional

from rich.console import Console
from rich.prompt import Prompt

console = Console()

FileManager = Literal["yazi", "mc", "ranger", "lf"]


def _normalize_to_directory(selected_path: str) -> Optional[str]:
    """Normalize a selected path to a directory.

    If a file was selected, returns its parent directory.
    If a directory was selected, returns it.
    If the path doesn't exist, returns None.

    Args:
        selected_path: Path selected by user (file or directory)

    Returns:
        Directory path or None if invalid
    """
    if not selected_path:
        return None

    # If a file was selected, use its parent directory
    if os.path.isfile(selected_path):
        return os.path.dirname(selected_path)
    # If a directory was selected, use it
    elif os.path.isdir(selected_path):
        return selected_path

    return None


def detect_available_file_managers() -> list[FileManager]:
    """Detect which terminal file managers are installed.

    Returns:
        List of available file managers in order of preference
    """
    managers: list[FileManager] = ["yazi", "mc", "ranger", "lf"]
    available = []

    for manager in managers:
        if shutil.which(manager):
            available.append(manager)

    return available


def pick_directory_with_yazi(start_dir: str = ".") -> Optional[str]:
    """Launch Yazi file manager to pick a directory.

    Args:
        start_dir: Starting directory for Yazi

    Returns:
        Selected directory path or None if cancelled
    """
    tmp_file = None
    try:
        # Create temporary file for Yazi to write selection
        fd, tmp_file = tempfile.mkstemp(prefix="yazi-chooser-", suffix=".txt")
        os.close(fd)

        # Launch Yazi with chooser file
        # User should press Enter on a directory to select it
        result = subprocess.run(
            ["yazi", f"--chooser-file={tmp_file}", str(start_dir)],
            check=False,
        )

        # Check if user cancelled (non-zero exit code other than selection)
        if result.returncode != 0 and result.returncode != 1:
            return None

        # Read selected path
        if os.path.exists(tmp_file):
            with open(tmp_file, "r") as f:
                selected = f.read().strip()
            return _normalize_to_directory(selected)

        return None

    except FileNotFoundError:
        console.print("[yellow]Yazi not found. Install it or use another file manager.[/yellow]")
        return None
    except Exception as e:
        console.print(f"[red]Error launching Yazi: {e}[/red]")
        return None
    finally:
        # Clean up temp file
        if tmp_file and os.path.exists(tmp_file):
            os.unlink(tmp_file)


def pick_directory_with_mc(start_dir: str = ".") -> Optional[str]:
    """Launch Midnight Commander to pick a directory.

    Args:
        start_dir: Starting directory for MC

    Returns:
        Selected directory path or None if cancelled
    """
    pwd_file = None
    try:
        # Create temporary file for MC to write current directory
        fd, pwd_file = tempfile.mkstemp(prefix="mc-pwd-", suffix=".txt")
        os.close(fd)

        # Launch MC with printwd option
        # MC will write the current directory to pwd_file on exit
        subprocess.run(
            ["mc", f"--printwd={pwd_file}", str(start_dir)],
            check=False,
        )

        # Read selected directory
        if os.path.exists(pwd_file):
            with open(pwd_file, "r") as f:
                selected = f.read().strip()
            return _normalize_to_directory(selected)

        return None

    except FileNotFoundError:
        console.print("[yellow]Midnight Commander not found. Install it or use another file manager.[/yellow]")
        return None
    except Exception as e:
        console.print(f"[red]Error launching Midnight Commander: {e}[/red]")
        return None
    finally:
        # Clean up temp file
        if pwd_file and os.path.exists(pwd_file):
            os.unlink(pwd_file)


def pick_directory_with_ranger(start_dir: str = ".") -> Optional[str]:
    """Launch Ranger file manager to pick a directory.

    Args:
        start_dir: Starting directory for Ranger

    Returns:
        Selected directory path or None if cancelled
    """
    chooser_file = None
    try:
        # Create temporary file for Ranger to write selection
        fd, chooser_file = tempfile.mkstemp(prefix="ranger-chooser-", suffix=".txt")
        os.close(fd)

        # Launch Ranger with chooser option
        subprocess.run(
            ["ranger", f"--choosefile={chooser_file}", str(start_dir)],
            check=False,
        )

        # Read selected path
        if os.path.exists(chooser_file):
            with open(chooser_file, "r") as f:
                selected = f.read().strip()
            return _normalize_to_directory(selected)

        return None

    except FileNotFoundError:
        console.print("[yellow]Ranger not found. Install it or use another file manager.[/yellow]")
        return None
    except Exception as e:
        console.print(f"[red]Error launching Ranger: {e}[/red]")
        return None
    finally:
        # Clean up temp file
        if chooser_file and os.path.exists(chooser_file):
            os.unlink(chooser_file)


def pick_directory_with_lf(start_dir: str = ".") -> Optional[str]:
    """Launch lf file manager to pick a directory.

    Args:
        start_dir: Starting directory for lf

    Returns:
        Selected directory path or None if cancelled
    """
    tmp_file = None
    try:
        # Create temporary file for lf to write selection
        fd, tmp_file = tempfile.mkstemp(prefix="lf-chooser-", suffix=".txt")
        os.close(fd)

        # Launch lf with selection file
        subprocess.run(
            ["lf", "-selection-path", tmp_file, str(start_dir)],
            check=False,
        )

        # Read selected path
        if os.path.exists(tmp_file):
            with open(tmp_file, "r") as f:
                selected = f.read().strip()
            return _normalize_to_directory(selected)

        return None

    except FileNotFoundError:
        console.print("[yellow]lf not found. Install it or use another file manager.[/yellow]")
        return None
    except Exception as e:
        console.print(f"[red]Error launching lf: {e}[/red]")
        return None
    finally:
        # Clean up temp file
        if tmp_file and os.path.exists(tmp_file):
            os.unlink(tmp_file)


def pick_directory(
    start_dir: str = ".",
    preferred_manager: Optional[FileManager] = None,
) -> Optional[str]:
    """Pick a directory using an available terminal file manager.

    This function auto-detects available file managers and uses the preferred
    one, or falls back to the first available manager in order of preference:
    yazi > mc > ranger > lf

    Args:
        start_dir: Starting directory for the file manager
        preferred_manager: Preferred file manager to use (if available)

    Returns:
        Selected directory path or None if cancelled or no file manager available

    Example:
        >>> directory = pick_directory()
        >>> if directory:
        ...     print(f"Selected: {directory}")
    """
    available = detect_available_file_managers()

    if not available:
        console.print("[red]No terminal file manager found![/red]")
        console.print("Please install one of: yazi, mc, ranger, or lf")
        return None

    # Use preferred manager if specified and available
    if preferred_manager and preferred_manager in available:
        manager = preferred_manager
    else:
        # Use first available manager
        manager = available[0]

    console.print(f"[dim]Opening {manager}... (select a directory and press Enter to confirm)[/dim]")

    # Launch the appropriate file manager
    if manager == "yazi":
        return pick_directory_with_yazi(start_dir)
    elif manager == "mc":
        return pick_directory_with_mc(start_dir)
    elif manager == "ranger":
        return pick_directory_with_ranger(start_dir)
    elif manager == "lf":
        return pick_directory_with_lf(start_dir)

    return None


def save_file(
    default_filename: str = "output.txt",
    start_dir: str = ".",
    preferred_manager: Optional[FileManager] = None,
    allow_custom_name: bool = True,
) -> Optional[str]:
    """Pick a file path to save to using an available terminal file manager.

    This function uses a file manager to navigate and select/create a file path
    for saving output. The user can navigate to a directory and the default
    filename will be used, or they can specify a custom filename while preserving
    the extension.

    Args:
        default_filename: Default filename to suggest for saving
        start_dir: Starting directory for the file manager
        preferred_manager: Preferred file manager to use (if available)
        allow_custom_name: If True, prompt user to customize filename (default: True)

    Returns:
        Selected file path or None if cancelled or no file manager available

    Example:
        >>> filepath = save_file(default_filename="report.json")
        >>> if filepath:
        ...     with open(filepath, 'w') as f:
        ...         f.write(content)
    """
    available = detect_available_file_managers()

    if not available:
        console.print("[red]No terminal file manager found![/red]")
        console.print("Please install one of: yazi, mc, ranger, or lf")
        return None

    # Use preferred manager if specified and available
    if preferred_manager and preferred_manager in available:
        manager = preferred_manager
    else:
        # Use first available manager
        manager = available[0]

    console.print(f"[dim]Opening {manager}...[/dim]")
    console.print("[cyan]→ Navigate to the directory where you want to save the file[/cyan]")
    console.print("[cyan]→ Press Enter on the folder to select it (you'll customize the filename next)[/cyan]")

    # For file saving, we'll use the directory picker and then append the default filename
    # This provides a simple but effective way to choose the save location
    if manager == "yazi":
        selected_dir = pick_directory_with_yazi(start_dir)
    elif manager == "mc":
        selected_dir = pick_directory_with_mc(start_dir)
    elif manager == "ranger":
        selected_dir = pick_directory_with_ranger(start_dir)
    elif manager == "lf":
        selected_dir = pick_directory_with_lf(start_dir)
    else:
        return None

    if selected_dir:
        # Extract extension from default filename
        default_path = Path(default_filename)
        default_stem = default_path.stem
        default_ext = default_path.suffix

        # Prompt for custom filename if enabled
        if allow_custom_name:
            console.print(f"\n[green]✓ Directory selected:[/green] {selected_dir}")
            console.print(f"\n[cyan]Default filename:[/cyan] {default_filename}")
            console.print(f"[dim]Press Enter to use default, or type a custom name (extension '{default_ext}' will be preserved)[/dim]")

            custom_name = Prompt.ask(
                "[cyan]Filename[/cyan]",
                default=default_stem,
                show_default=True
            ).strip()

            # If user just pressed Enter (returned default) or custom name matches default, use default filename
            if custom_name == default_stem or not custom_name:
                final_filename = default_filename
            else:
                # User provided a custom name, use it but preserve extension
                # Remove any extension user might have added
                custom_path = Path(custom_name)
                final_stem = custom_path.stem if custom_path.stem else custom_name
                final_filename = f"{final_stem}{default_ext}"
        else:
            final_filename = default_filename

        # Combine selected directory with final filename
        file_path = os.path.join(selected_dir, final_filename)
        console.print(f"[green]Save location:[/green] {file_path}")
        return file_path

    return None
