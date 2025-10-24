"""Directory handling utilities for CLI commands.

This module provides utilities for handling directory selection,
including interactive browsing and path resolution.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .file_picker import pick_directory

console = Console()


def get_directory(
    directory: Optional[str] = None,
    browse: bool = False,
    default: str = "."
) -> Path:
    """Get directory path, either from argument, browse mode, or default.

    Args:
        directory: Directory path provided as argument
        browse: Whether to use interactive file browser
        default: Default directory if none provided

    Returns:
        Resolved Path object for the directory

    Raises:
        typer.Abort: If browse mode is cancelled
    """
    if browse:
        # Use file manager to select directory
        start_dir = directory if directory else default
        selected = pick_directory(start_dir=start_dir)

        if selected is None:
            console.print("[yellow]No directory selected. Cancelled.[/yellow]")
            raise typer.Abort()

        base_path = Path(selected).resolve()
        console.print(f"[green]Selected:[/green] {base_path}")
        return base_path
    else:
        # Use provided directory or default to current directory
        return Path(directory if directory else default).resolve()
