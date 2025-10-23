"""Convert text to uppercase.

This module provides a command to convert input text to uppercase.
"""

import typer
from rich.console import Console

from cli_utils.utils.clipboard import copy_to_clipboard

console = Console()


def uppercase(
    text: str = typer.Argument(..., help="Text to convert to uppercase"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy result to clipboard"),
) -> None:
    """Convert text to UPPERCASE.

    Args:
        text: The text to convert to uppercase
        copy: If True, copy the result to clipboard (uses xclip/xsel/wl-copy on Linux)

    Example:
        $ cli-utils local text-utils uppercase "hello world"
        HELLO WORLD

        $ cli-utils local text-utils uppercase "hello world" --copy
        HELLO WORLD
        ✓ Copied to clipboard
    """
    result = text.upper()

    console.print(f"[green]{result}[/green]")

    if copy:
        copy_to_clipboard(result)
