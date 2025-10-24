"""Analyze Python files in a directory.

This module provides a command to analyze Python source files and generate
reports with metrics like line counts, classes, functions, and methods.
"""

from typing import Literal

import typer
from rich.console import Console

from cli_utils.utils.common_options import BrowseOption, OptionalDirectoryArg, OutputOption, RecursiveOption
from cli_utils.utils.directory_handler import get_directory
from cli_utils.utils.output_handler import OutputHandler, create_default_filename

console = Console()


def code_report(
    directory: OptionalDirectoryArg = None,
    recursive: RecursiveOption = False,
    format: Literal["text", "json", "markdown"] = typer.Option("text", "--format", "-f", help="Output format"),
    browse: BrowseOption = False,
    output: OutputOption = None,
) -> None:
    """Analyze Python files in a directory.

    This command scans Python files and generates a report with metrics including:
    - Line counts (excluding blank lines and comments)
    - Number of classes, functions, and methods
    - Percentage of total lines per file

    Args:
        directory: Directory to analyze (defaults to current directory if not using --browse)
        recursive: If True, search subdirectories recursively
        format: Output format (text, json, or markdown)
        browse: If True, launch a file manager (Yazi/MC) to select directory interactively
        output: File path to save output. If set to 'browse', use file manager to select location

    Example:
        $ cli-utils local devtools code-report .
        $ cli-utils local devtools code-report src --recursive
        $ cli-utils local devtools code-report . --format json
        $ cli-utils local devtools code-report --browse
        $ cli-utils local devtools code-report --browse --recursive
        $ cli-utils local devtools code-report . --output report.txt
        $ cli-utils local devtools code-report . --format json --output browse
    """
    # Import locally to avoid exposing utility functions as commands
    from . import _utils

    # Handle directory selection
    base_path = get_directory(directory=directory, browse=browse)

    # Perform analysis
    reports, total_lines = _utils.gather_reports(base_path, recursive)

    # Check if any files were found
    if not reports:
        console.print(f"[yellow]No Python files found in {base_path}[/yellow]")
        return

    # Set up output handler
    extension_map = {"text": "txt", "json": "json", "markdown": "md"}
    default_filename = create_default_filename("code_report", format, extension_map)
    handler = OutputHandler(output=output, default_filename=default_filename)

    # Generate and output report
    if handler.determine_output_path():
        # Generate report as string and save to file
        if format == "text":
            report_content = _utils.generate_text_report(reports, total_lines)
        elif format == "json":
            report_content = _utils.generate_json_report(reports, total_lines)
        else:  # markdown
            report_content = _utils.generate_markdown_report(reports, total_lines)

        handler.save_or_print(report_content)
    else:
        # Print report to console
        if format == "text":
            _utils.print_text_report(reports, total_lines)
        elif format == "json":
            _utils.print_json_report(reports, total_lines)
        else:  # markdown
            _utils.print_markdown_report(reports, total_lines)

