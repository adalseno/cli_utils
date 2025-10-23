"""Convert text to lowercase.

This module provides a command to convert input text to lowercase.
"""

import typer
from rich.console import Console

from cli_utils.utils.clipboard import copy_to_clipboard

console = Console()


def lowercase(
    text: str = typer.Argument(..., help="Text to convert to lowercase"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy result to clipboard"),
) -> None:
    """Convert text to lowercase.

    Args:
        text: The text to convert to lowercase
        copy: If True, copy the result to clipboard (uses xclip/xsel/wl-copy on Linux)

    Example:
        $ cli-utils local text-utils lowercase "HELLO WORLD"
        hello world

        $ cli-utils local text-utils lowercase "HELLO WORLD" --copy
        hello world
        ✓ Copied to clipboard
    """
    result = text.lower()

    console.print(f"[green]{result}[/green]")

    if copy:
        copy_to_clipboard(result)
