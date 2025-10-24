"""Count test functions in Python test files.

This module provides a command to scan test files and count test functions,
providing a summary of test coverage across the codebase.
"""

import re
from typing import Literal

import typer
from rich.console import Console
from rich.table import Table

from cli_utils.utils.common_options import (
    BrowseOption,
    OptionalDirectoryArg,
    OutputOption,
    RecursiveOption,
    VerboseOption,
)
from cli_utils.utils.directory_handler import get_directory
from cli_utils.utils.output_handler import OutputHandler, create_default_filename

console = Console()

# Regex pattern to match test functions
TEST_PATTERN = re.compile(
    r"(^\s*def\s+(test_\w+)\s*\([^)]*\):)([\s\S]*?)(?=^\s*def\s+test_|\Z)",
    re.MULTILINE,
)

# Pattern to match test classes
TEST_CLASS_PATTERN = re.compile(
    r"^\s*class\s+(Test\w+)\s*\([^)]*\):",
    re.MULTILINE,
)


def count_tests(
    directory: OptionalDirectoryArg = None,
    recursive: RecursiveOption = False,
    pattern: str = typer.Option("test_*.py", "--pattern", "-p", help="File pattern to match test files"),
    browse: BrowseOption = False,
    verbose: VerboseOption = False,
    format: Literal["table", "summary", "json"] = typer.Option("table", "--format", "-f", help="Output format"),
    output: OutputOption = None,
) -> None:
    """Count test functions in Python test files.

    This command scans test files and counts:
    - Total test files
    - Total test functions (functions starting with test_)
    - Total test classes (classes starting with Test)
    - Tests per file

    Args:
        directory: Directory to scan (defaults to current directory if not using --browse)
        recursive: If True, search subdirectories recursively
        pattern: Glob pattern to match test files (default: test_*.py)
        browse: If True, launch a file manager to select directory interactively
        verbose: If True, show individual test function names
        format: Output format (table, summary, or json)
        output: File path to save output. If set to 'browse', use file manager to select location

    Example:
        $ cli-utils local devtools count-tests .
        $ cli-utils local devtools count-tests tests --recursive
        $ cli-utils local devtools count-tests --browse
        $ cli-utils local devtools count-tests -b -r -v
        $ cli-utils local devtools count-tests tests -p "*_test.py"
        $ cli-utils local devtools count-tests . --output test_report.txt
        $ cli-utils local devtools count-tests . --format json --output browse
    """
    # Handle directory selection
    base_path = get_directory(directory=directory, browse=browse)

    # Find test files
    if recursive:
        test_files = sorted(base_path.rglob(pattern))
    else:
        test_files = sorted(base_path.glob(pattern))

    if not test_files:
        console.print(f"[yellow]No test files found matching '{pattern}' in {base_path}[/yellow]")
        return

    # Analyze test files
    results = []
    total_tests = 0
    total_classes = 0

    for test_file in test_files:
        try:
            content = test_file.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Error reading {test_file}: {e}[/red]")
            continue

        # Count test functions
        test_matches = TEST_PATTERN.findall(content)
        test_function_names = [match[1] for match in test_matches]
        num_tests = len(test_function_names)

        # Count test classes
        class_matches = TEST_CLASS_PATTERN.findall(content)
        num_classes = len(class_matches)

        total_tests += num_tests
        total_classes += num_classes

        # Calculate relative path for display
        try:
            rel_path = test_file.relative_to(base_path)
        except ValueError:
            rel_path = test_file

        results.append(
            {
                "file": str(rel_path),
                "path": str(test_file),
                "tests": num_tests,
                "classes": num_classes,
                "test_names": test_function_names,
                "class_names": class_matches,
            }
        )

    # Set up output handler
    extension_map = {"table": "txt", "summary": "txt", "json": "json"}
    default_filename = create_default_filename("test_count", format, extension_map)
    handler = OutputHandler(output=output, default_filename=default_filename)

    # Generate and output report
    if handler.determine_output_path():
        # Generate report as string and save to file
        if format == "json":
            report_content = _generate_json_format(results, total_tests, total_classes, len(test_files))
        elif format == "summary":
            report_content = _generate_summary_format(results, total_tests, total_classes, len(test_files))
        else:  # table
            report_content = _generate_table_format(results, total_tests, total_classes, len(test_files), verbose)

        handler.save_or_print(report_content)
    else:
        # Print report to console
        if format == "json":
            _print_json_format(results, total_tests, total_classes, len(test_files))
        elif format == "summary":
            _print_summary_format(results, total_tests, total_classes, len(test_files))
        else:  # table
            _print_table_format(results, total_tests, total_classes, len(test_files), verbose)


def _print_table_format(
    results: list[dict], total_tests: int, total_classes: int, total_files: int, verbose: bool
) -> None:
    """Print results in table format."""
    if not results:
        return

    # Create table
    table = Table(title="Test Count Summary", show_header=True, header_style="bold cyan")
    table.add_column("File", style="yellow", no_wrap=False)
    table.add_column("Tests", justify="right", style="green")
    table.add_column("Classes", justify="right", style="blue")

    for result in results:
        table.add_row(
            result["file"],
            str(result["tests"]),
            str(result["classes"]),
        )

    console.print(table)
    console.print()

    # Print verbose output if requested
    if verbose:
        console.print("[bold cyan]Test Functions by File:[/bold cyan]")
        for result in results:
            if result["test_names"]:
                console.print(f"\n[yellow]{result['file']}[/yellow]")
                for test_name in result["test_names"]:
                    console.print(f"  • [green]{test_name}[/green]")
        console.print()

    # Print totals
    console.print("[bold cyan]Totals:[/bold cyan]")
    console.print(f"  Files     : {total_files}")
    console.print(f"  Tests     : {total_tests}")
    console.print(f"  Classes   : {total_classes}")

    if total_files > 0:
        avg_tests = total_tests / total_files
        console.print(f"  Avg/File  : {avg_tests:.1f}")


def _print_summary_format(results: list[dict], total_tests: int, total_classes: int, total_files: int) -> None:
    """Print results in summary format."""
    console.print("[bold cyan]Test Count Summary[/bold cyan]")
    console.print(f"  Files     : {total_files}")
    console.print(f"  Tests     : {total_tests}")
    console.print(f"  Classes   : {total_classes}")

    if total_files > 0:
        avg_tests = total_tests / total_files
        console.print(f"  Avg/File  : {avg_tests:.1f}")


def _print_json_format(results: list[dict], total_tests: int, total_classes: int, total_files: int) -> None:
    """Print results in JSON format."""
    import json

    # Prepare JSON output (exclude test_names from file results unless needed)
    files = [
        {
            "file": r["file"],
            "path": r["path"],
            "tests": r["tests"],
            "classes": r["classes"],
            "test_names": r["test_names"],
            "class_names": r["class_names"],
        }
        for r in results
    ]

    output = {
        "summary": {
            "total_files": total_files,
            "total_tests": total_tests,
            "total_classes": total_classes,
            "average_tests_per_file": round(total_tests / total_files, 2) if total_files > 0 else 0,
        },
        "files": files,
    }

    console.print(json.dumps(output, indent=2))


def _generate_table_format(
    results: list[dict], total_tests: int, total_classes: int, total_files: int, verbose: bool
) -> str:
    """Generate results in table format as a string."""
    from io import StringIO

    from rich.console import Console as RichConsole

    # Create a string buffer to capture output
    buffer = StringIO()
    temp_console = RichConsole(file=buffer, force_terminal=False, width=120)

    if not results:
        return ""

    # Create table
    table = Table(title="Test Count Summary", show_header=True, header_style="bold cyan")
    table.add_column("File", style="yellow", no_wrap=False)
    table.add_column("Tests", justify="right", style="green")
    table.add_column("Classes", justify="right", style="blue")

    for result in results:
        table.add_row(
            result["file"],
            str(result["tests"]),
            str(result["classes"]),
        )

    temp_console.print(table)
    temp_console.print()

    # Print verbose output if requested
    if verbose:
        temp_console.print("[bold cyan]Test Functions by File:[/bold cyan]")
        for result in results:
            if result["test_names"]:
                temp_console.print(f"\n[yellow]{result['file']}[/yellow]")
                for test_name in result["test_names"]:
                    temp_console.print(f"  • [green]{test_name}[/green]")
        temp_console.print()

    # Print totals
    temp_console.print("[bold cyan]Totals:[/bold cyan]")
    temp_console.print(f"  Files     : {total_files}")
    temp_console.print(f"  Tests     : {total_tests}")
    temp_console.print(f"  Classes   : {total_classes}")

    if total_files > 0:
        avg_tests = total_tests / total_files
        temp_console.print(f"  Avg/File  : {avg_tests:.1f}")

    return buffer.getvalue()


def _generate_summary_format(results: list[dict], total_tests: int, total_classes: int, total_files: int) -> str:
    """Generate results in summary format as a string."""
    lines = []
    lines.append("Test Count Summary")
    lines.append(f"  Files     : {total_files}")
    lines.append(f"  Tests     : {total_tests}")
    lines.append(f"  Classes   : {total_classes}")

    if total_files > 0:
        avg_tests = total_tests / total_files
        lines.append(f"  Avg/File  : {avg_tests:.1f}")

    return "\n".join(lines)


def _generate_json_format(results: list[dict], total_tests: int, total_classes: int, total_files: int) -> str:
    """Generate results in JSON format as a string."""
    import json

    # Prepare JSON output
    files = [
        {
            "file": r["file"],
            "path": r["path"],
            "tests": r["tests"],
            "classes": r["classes"],
            "test_names": r["test_names"],
            "class_names": r["class_names"],
        }
        for r in results
    ]

    output = {
        "summary": {
            "total_files": total_files,
            "total_tests": total_tests,
            "total_classes": total_classes,
            "average_tests_per_file": round(total_tests / total_files, 2) if total_files > 0 else 0,
        },
        "files": files,
    }

    return json.dumps(output, indent=2)
