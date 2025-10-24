"""Output handling utilities for CLI commands.

This module provides utilities for handling command output, including
saving to files, interactive file selection, and console output.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .file_picker import save_file

console = Console()


class OutputHandler:
    """Handle output for CLI commands (console or file)."""

    def __init__(
        self,
        output: Optional[str] = None,
        default_filename: str = "output.txt",
        start_dir: str = "."
    ):
        """Initialize the output handler.

        Args:
            output: Output specification - None for console, "browse" for interactive,
                   or a file path for direct save
            default_filename: Default filename to suggest in browse mode
            start_dir: Starting directory for file browser
        """
        self.output = output
        self.default_filename = default_filename
        self.start_dir = start_dir
        self._output_path: Optional[str] = None

    def determine_output_path(self) -> Optional[str]:
        """Determine the output file path based on configuration.

        Returns:
            File path to save to, or None if outputting to console
        """
        if not self.output:
            return None

        if self.output.lower() == "browse":
            # Use file manager to select save location
            output_path = save_file(
                default_filename=self.default_filename,
                start_dir=self.start_dir
            )
            if output_path is None:
                console.print("[yellow]No output file selected. Cancelled.[/yellow]")
                raise typer.Abort()
            return output_path
        else:
            # Use provided file path
            return self.output

    def save_or_print(self, content: str) -> None:
        """Save content to file or print to console.

        Args:
            content: Content to output
        """
        output_path = self.determine_output_path()

        if output_path:
            # Save to file
            try:
                Path(output_path).write_text(content, encoding='utf-8')
                console.print(f"[green]Report saved to:[/green] {output_path}")
            except Exception as e:
                console.print(f"[red]Error saving report: {e}[/red]")
                raise typer.Abort()
        else:
            # Print to console
            print(content)


def get_extension_for_format(format_type: str, format_map: dict[str, str]) -> str:
    """Get file extension for a given format type.

    Args:
        format_type: The format type (e.g., "json", "text", "markdown")
        format_map: Dictionary mapping format types to extensions

    Returns:
        File extension without dot (e.g., "json", "txt", "md")
    """
    return format_map.get(format_type, "txt")


def create_default_filename(base_name: str, format_type: str, format_map: dict[str, str]) -> str:
    """Create a default filename for a given format.

    Args:
        base_name: Base name for the file (e.g., "code_report", "test_count")
        format_type: The format type
        format_map: Dictionary mapping format types to extensions

    Returns:
        Default filename with appropriate extension
    """
    extension = get_extension_for_format(format_type, format_map)
    return f"{base_name}.{extension}"
