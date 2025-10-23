"""Convert text to title case.

This module provides a command to convert input text to title case.
"""

import typer
from rich.console import Console

from cli_utils.utils.clipboard import copy_to_clipboard

console = Console()


def titlecase(
    text: str = typer.Argument(..., help="Text to convert to title case"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy result to clipboard"),
) -> None:
    """Convert text to Title Case.

    Args:
        text: The text to convert to title case
        copy: If True, copy the result to clipboard (uses xclip/xsel/wl-copy on Linux)

    Example:
        $ cli-utils local text-utils titlecase "hello world"
        Hello World

        $ cli-utils local text-utils titlecase "hello world" --copy
        Hello World
        ✓ Copied to clipboard
    """
    result = text.title()

    console.print(f"[green]{result}[/green]")

    if copy:
        copy_to_clipboard(result)
