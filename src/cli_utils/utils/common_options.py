"""Common CLI option definitions for reuse across commands.

This module provides reusable Annotated types for common CLI options,
ensuring consistency across commands and reducing code duplication.
"""

from typing import Annotated, Optional

import typer

# Common option: Recursive directory search
RecursiveOption = Annotated[bool, typer.Option("--recursive", "-r", help="Search directories recursively")]

# Common option: Browse for directory using file manager
BrowseOption = Annotated[
    bool,
    typer.Option(
        "--browse",
        "-b",
        help="Browse for directory using file manager (yazi/mc)",
    ),
]

# Common option: Output file path
OutputOption = Annotated[
    Optional[str],
    typer.Option(
        "--output",
        "-o",
        help="Save output to file (use 'browse' to select location interactively)",
    ),
]

# Common option: Verbose output
VerboseOption = Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed output")]

# Common argument: Optional directory
# Note: Default value must be set with = in the function signature, not in Annotated
OptionalDirectoryArg = Annotated[
    Optional[str], typer.Argument(help="Directory to analyze (defaults to current directory)")
]
