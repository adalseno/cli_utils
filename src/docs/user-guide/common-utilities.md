# Common Utilities

This guide explains the reusable utilities available in CLI Utils that make it easy to add common functionality to your commands.

## Overview

CLI Utils provides a set of common utilities that implement frequently-used patterns like directory browsing, file selection, output handling, and more. Using these utilities ensures consistency across commands and reduces code duplication.

## Available Utilities

### CLI Options (`cli_utils.utils.common_options`)

Pre-defined `Annotated` types for common CLI options that you can use directly in your command functions.

#### `RecursiveOption`

Add a `--recursive/-r` option to search directories recursively.

**Usage:**
```python
from cli_utils.utils.common_options import RecursiveOption

def my_command(
    recursive: RecursiveOption = False,
) -> None:
    """My command with recursive option."""
    if recursive:
        # Search recursively
        files = path.rglob("*.py")
    else:
        # Search only current directory
        files = path.glob("*.py")
```

**What it provides:**
- Option: `--recursive` / `-r`
- Type: `bool`
- Default: `False`
- Help text: "Search directories recursively"

#### `BrowseOption`

Add a `--browse/-b` option to interactively select directories using a file manager.

**Usage:**
```python
from cli_utils.utils.common_options import BrowseOption

def my_command(
    browse: BrowseOption = False,
) -> None:
    """My command with browse option."""
    # Use with directory_handler (see below)
```

**What it provides:**
- Option: `--browse` / `-b`
- Type: `bool`
- Default: `False`
- Help text: "Browse for directory using file manager (yazi/mc)"

#### `OutputOption`

Add a `--output/-o` option to save command output to a file.

**Usage:**
```python
from cli_utils.utils.common_options import OutputOption

def my_command(
    output: OutputOption = None,
) -> None:
    """My command with output option."""
    # Use with output_handler (see below)
```

**What it provides:**
- Option: `--output` / `-o`
- Type: `Optional[str]`
- Default: `None`
- Help text: "Save output to file (use 'browse' to select location interactively)"
- Special value: `"browse"` for interactive file selection

#### `VerboseOption`

Add a `--verbose/-v` option for detailed output.

**Usage:**
```python
from cli_utils.utils.common_options import VerboseOption

def my_command(
    verbose: VerboseOption = False,
) -> None:
    """My command with verbose option."""
    if verbose:
        console.print("[dim]Detailed information...[/dim]")
```

**What it provides:**
- Option: `--verbose` / `-v`
- Type: `bool`
- Default: `False`
- Help text: "Show detailed output"

#### `OptionalDirectoryArg`

Add an optional directory argument (positional parameter).

**Usage:**
```python
from cli_utils.utils.common_options import OptionalDirectoryArg

def my_command(
    directory: OptionalDirectoryArg = None,
) -> None:
    """My command with optional directory argument."""
    # Use with directory_handler (see below)
```

**What it provides:**
- Argument: `[DIRECTORY]`
- Type: `Optional[str]`
- Default: `None`
- Help text: "Directory to analyze (defaults to current directory)"

### Directory Handler (`cli_utils.utils.directory_handler`)

Utilities for handling directory selection with support for browse mode.

#### `get_directory()`

Get a directory path from argument, browse mode, or default.

**Function Signature:**
```python
def get_directory(
    directory: Optional[str] = None,
    browse: bool = False,
    default: str = "."
) -> Path
```

**Parameters:**
- `directory` - Directory path from command argument
- `browse` - Whether to use interactive file browser
- `default` - Default directory if none provided (default: `"."`)

**Returns:**
- `Path` object for the selected directory

**Raises:**
- `typer.Abort` if browse mode is cancelled

**Usage:**
```python
from pathlib import Path
from cli_utils.utils.common_options import BrowseOption, OptionalDirectoryArg
from cli_utils.utils.directory_handler import get_directory

def my_command(
    directory: OptionalDirectoryArg = None,
    browse: BrowseOption = False,
) -> None:
    """Analyze files in a directory."""
    # Handles browse mode, provided directory, or default
    base_path = get_directory(directory=directory, browse=browse)

    # Now you have a Path object to work with
    files = list(base_path.glob("*.py"))
```

**What it does:**
1. If `browse=True`: Opens file manager for interactive selection
2. Else if `directory` is provided: Uses that path
3. Else: Uses the `default` directory
4. Returns resolved `Path` object
5. Shows confirmation message when browsing

**Supported File Managers:**
- **yazi** (recommended) - Modern, fast terminal file manager
- **mc** (Midnight Commander) - Classic dual-pane file manager
- **ranger** - Vim-like file manager
- **lf** - Simple terminal file manager

### Output Handler (`cli_utils.utils.output_handler`)

Utilities for handling command output (console or file) with support for interactive file selection.

#### `OutputHandler` Class

Manages output destination (console vs file) with browse mode support.

**Class Signature:**
```python
class OutputHandler:
    def __init__(
        self,
        output: Optional[str] = None,
        default_filename: str = "output.txt",
        start_dir: str = "."
    )
```

**Parameters:**
- `output` - Output specification (None=console, "browse"=interactive, or file path)
- `default_filename` - Default filename for browse mode
- `start_dir` - Starting directory for file browser

**Methods:**

##### `determine_output_path() -> Optional[str]`

Determine the output file path based on configuration.

**Returns:**
- File path to save to, or `None` if outputting to console

**Raises:**
- `typer.Abort` if browse mode is cancelled

##### `save_or_print(content: str) -> None`

Save content to file or print to console.

**Parameters:**
- `content` - String content to output

**Usage:**
```python
from cli_utils.utils.common_options import OutputOption
from cli_utils.utils.output_handler import OutputHandler, create_default_filename

def my_command(
    output: OutputOption = None,
    format: str = "text",
) -> None:
    """Generate a report."""
    # Set up output handler with appropriate filename
    extension_map = {"text": "txt", "json": "json", "markdown": "md"}
    default_filename = create_default_filename("my_report", format, extension_map)
    handler = OutputHandler(output=output, default_filename=default_filename)

    # Generate your content
    report_content = generate_report()

    # Handle output automatically
    if handler.determine_output_path():
        # Will save to file
        handler.save_or_print(report_content)
    else:
        # Will print to console (you can use rich formatting here)
        console.print(report_content)
```

#### Helper Functions

##### `create_default_filename()`

Create a default filename based on format.

**Function Signature:**
```python
def create_default_filename(
    base_name: str,
    format_type: str,
    format_map: dict[str, str]
) -> str
```

**Parameters:**
- `base_name` - Base name for the file (e.g., "report", "metrics")
- `format_type` - The format type (e.g., "json", "text")
- `format_map` - Dict mapping format types to file extensions

**Returns:**
- Filename with appropriate extension (e.g., "report.json")

**Example:**
```python
from cli_utils.utils.output_handler import create_default_filename

extension_map = {"text": "txt", "json": "json", "markdown": "md"}
filename = create_default_filename("metrics", "json", extension_map)
# Returns: "metrics.json"
```

##### `get_extension_for_format()`

Get file extension for a format type.

**Function Signature:**
```python
def get_extension_for_format(
    format_type: str,
    format_map: dict[str, str]
) -> str
```

### File Picker (`cli_utils.utils.file_picker`)

Low-level utilities for file manager integration.

#### `pick_directory()`

Launch file manager to select a directory.

**Function Signature:**
```python
def pick_directory(
    start_dir: str = ".",
    preferred_manager: Optional[FileManager] = None,
) -> Optional[str]
```

**Parameters:**
- `start_dir` - Starting directory for file manager
- `preferred_manager` - Specific file manager to use ("yazi", "mc", "ranger", "lf")

**Returns:**
- Selected directory path, or `None` if cancelled

**Note:** Usually you should use `get_directory()` instead, which wraps this function.

#### `save_file()`

Launch file manager to select a save location.

**Function Signature:**
```python
def save_file(
    default_filename: str = "output.txt",
    start_dir: str = ".",
    preferred_manager: Optional[FileManager] = None,
) -> Optional[str]
```

**Parameters:**
- `default_filename` - Suggested filename
- `start_dir` - Starting directory
- `preferred_manager` - Specific file manager to use

**Returns:**
- Selected file path (directory + filename), or `None` if cancelled

**Note:** Usually you should use `OutputHandler` instead, which wraps this function.

### Icons (`cli_utils.utils.icons`)

Smart icon system with automatic Nerd Font detection and fallback support.

#### Icon System Overview

CLI Utils includes an intelligent icon system that automatically adapts to your terminal's capabilities:

1. **Nerd Font Icons** - If you have Nerd Fonts installed, beautiful icons are used
2. **Emoji Fallback** - If your terminal supports emoji, Unicode emoji are used
3. **Text Fallback** - Simple ASCII text representations for basic terminals

The system detects your setup automatically on first run!

#### Using Predefined Icons

The easiest way to use icons is through the `Icons` class:

**Usage:**
```python
from cli_utils.utils.icons import Icons

def my_command():
    """Command using predefined icons."""
    console.print(f"{Icons.check()} Task completed")
    console.print(f"{Icons.cross()} Operation failed")
    console.print(f"{Icons.calendar()} Due: 2025-11-01")
    console.print(f"{Icons.clock()} Reminder set")
```

**Available Icons:**

| Method | Nerd Font | Emoji | Text |
|--------|-----------|-------|------|
| `Icons.check()` | 󰄬 | ✅ | [✓] |
| `Icons.cross()` | 󰅖 | ❌ | [✗] |
| `Icons.circle()` | 󰄰 | ⭕ | [ ] |
| `Icons.play()` | 󰐊 | ▶️ | [>] |
| `Icons.calendar()` | 󰃮 | 📅 | [DATE] |
| `Icons.clock()` | 󰥔 | ⏰ | [TIME] |
| `Icons.list()` | 󰉹 | 📋 | [LIST] |
| `Icons.folder()` | 󰉋 | 📁 | [FOLDER] |
| `Icons.file()` | 󰈙 | 📄 | [FILE] |
| `Icons.info()` | 󰋽 | ℹ️ | [i] |
| `Icons.warning()` | 󰀪 | ⚠️ | [!] |
| `Icons.star()` | 󰓎 | ⭐ | [*] |
| `Icons.tag()` | 󰓹 | 🏷️ | [TAG] |

#### Using Custom Icons

For custom icons, use the `icon()` function:

**Function Signature:**
```python
def icon(
    nerd_icon_name: str,
    emoji_char: str,
    fallback: str
) -> str
```

**Parameters:**
- `nerd_icon_name` - Nerd Font icon name (e.g., "nf-md-rocket")
- `emoji_char` - Emoji character to use as fallback
- `fallback` - Plain text string as final fallback

**Usage:**
```python
from cli_utils.utils.icons import icon

def my_command():
    """Command using custom icons."""
    rocket = icon("nf-md-rocket", "🚀", "[ROCKET]")
    console.print(f"{rocket} Launching...")

    heart = icon("nf-md-heart", "❤️", "[LOVE]")
    console.print(f"{heart} Favorite item")
```

#### Icon Manager

For advanced usage, you can work with the `IconManager` directly:

**Usage:**
```python
from cli_utils.utils.icons import get_icon_manager

def my_command():
    """Command checking icon support."""
    manager = get_icon_manager()

    # Check what's being used
    if manager._nerd_font_support == 1:
        console.print("Using Nerd Font icons!")
    elif manager._terminal_supports_emoji:
        console.print("Using emoji icons")
    else:
        console.print("Using text icons")
```

#### Real-World Example

Here's how the TODO app uses icons:

```python
from cli_utils.utils.icons import Icons

class TaskItem:
    """Display a task with status icon."""

    def render(self, status: str, text: str, due_date: str = None):
        # Get appropriate status icon
        status_icons = {
            "new": Icons.circle(),
            "in_progress": Icons.play(),
            "completed": Icons.check()
        }
        icon = status_icons.get(status, Icons.circle())

        # Build display
        parts = [f"{icon} {text}"]

        if due_date:
            parts.append(f"{Icons.calendar()} {due_date}")

        return " ".join(parts)
```

**Output examples:**
- With Nerd Fonts: `󰄰 Buy groceries 󰃮 2025-11-01`
- With Emoji: `⭕ Buy groceries 📅 2025-11-01`
- Text fallback: `[ ] Buy groceries [DATE] 2025-11-01`

#### Testing Icons

When testing, you can control icon behavior:

```python
from cli_utils.utils.icons import IconManager

def test_with_nerd_fonts():
    """Test with Nerd Fonts enabled."""
    manager = IconManager(nerd_font_support=1)
    icon_str = manager.icon("nf-md-check", "✅", "[DONE]")
    # Will use Nerd Font icon

def test_without_nerd_fonts():
    """Test with Nerd Fonts disabled."""
    manager = IconManager(nerd_font_support=0)
    icon_str = manager.icon("nf-md-check", "✅", "[DONE]")
    # Will use emoji or text based on terminal
```

### Clipboard (`cli_utils.utils.clipboard`)

Cross-platform clipboard utilities.

#### `copy_to_clipboard()`

Copy text to system clipboard.

**Function Signature:**
```python
def copy_to_clipboard(text: str) -> bool
```

**Parameters:**
- `text` - String to copy to clipboard

**Returns:**
- `True` if successful, `False` otherwise

**Usage:**
```python
from cli_utils.utils.clipboard import copy_to_clipboard

def my_command(
    text: str,
    copy: bool = typer.Option(False, "--copy", "-c"),
) -> None:
    """Transform text and optionally copy to clipboard."""
    result = text.upper()
    console.print(f"[green]{result}[/green]")

    if copy:
        copy_to_clipboard(result)
```

**Supported Clipboard Tools:**
- **Linux**: xclip, xsel, wl-clipboard
- **macOS**: pbcopy (built-in)
- **Windows**: clip (built-in)
- **Fallback**: pyperclip Python package

## Complete Example

Here's a complete example showing how to use multiple common utilities together:

```python
"""Example command using common utilities."""

from typing import Literal
import typer
from rich.console import Console

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


def analyze_files(
    directory: OptionalDirectoryArg = None,
    recursive: RecursiveOption = False,
    format: Literal["text", "json"] = typer.Option("text", "--format", "-f"),
    browse: BrowseOption = False,
    verbose: VerboseOption = False,
    output: OutputOption = None,
) -> None:
    """Analyze files in a directory.

    Args:
        directory: Directory to analyze (defaults to current directory)
        recursive: If True, search subdirectories recursively
        format: Output format (text or json)
        browse: If True, use file manager to select directory
        verbose: If True, show detailed output
        output: Save output to file (use 'browse' to select location)

    Example:
        $ cli-utils local mygroup analyze-files .
        $ cli-utils local mygroup analyze-files --browse --recursive
        $ cli-utils local mygroup analyze-files -b -r -f json -o browse
    """
    # 1. Get directory (handles browse mode)
    base_path = get_directory(directory=directory, browse=browse)

    if verbose:
        console.print(f"[dim]Analyzing: {base_path}[/dim]")

    # 2. Find files (using recursive option)
    if recursive:
        files = list(base_path.rglob("*.py"))
    else:
        files = list(base_path.glob("*.py"))

    if verbose:
        console.print(f"[dim]Found {len(files)} files[/dim]")

    # 3. Process files and generate output
    if format == "json":
        import json
        result = json.dumps({"files": [str(f) for f in files]}, indent=2)
    else:
        result = f"Found {len(files)} Python files in {base_path}"

    # 4. Handle output (console or file, with browse support)
    extension_map = {"text": "txt", "json": "json"}
    default_filename = create_default_filename("analysis", format, extension_map)
    handler = OutputHandler(output=output, default_filename=default_filename)

    if handler.determine_output_path():
        # Save to file
        handler.save_or_print(result)
    else:
        # Print to console
        console.print(result)
```

**This example supports all these usage patterns:**

```bash
# Basic usage
cli-utils local mygroup analyze-files .

# Browse for directory
cli-utils local mygroup analyze-files --browse

# Recursive search
cli-utils local mygroup analyze-files . --recursive

# Verbose output
cli-utils local mygroup analyze-files . --verbose

# JSON format
cli-utils local mygroup analyze-files . --format json

# Save to specific file
cli-utils local mygroup analyze-files . --output report.txt

# Browse for save location
cli-utils local mygroup analyze-files . --output browse

# Combine everything
cli-utils local mygroup analyze-files -b -r -v -f json -o browse
```

## Best Practices

### 1. Use Common Options for Consistency

Always use the pre-defined option types for common features:

```python
# ✅ Good - Uses common options
from cli_utils.utils.common_options import RecursiveOption

def my_command(recursive: RecursiveOption = False):
    pass

# ❌ Bad - Reimplements the same thing
def my_command(recursive: bool = typer.Option(False, "-r", "--recursive")):
    pass
```

### 2. Combine Directory Handler with Browse Option

Always use `get_directory()` when you have a browse option:

```python
# ✅ Good - Uses directory handler
from cli_utils.utils.directory_handler import get_directory

def my_command(directory: OptionalDirectoryArg = None, browse: BrowseOption = False):
    base_path = get_directory(directory=directory, browse=browse)

# ❌ Bad - Reimplements directory handling
def my_command(directory: Optional[str] = None, browse: bool = False):
    if browse:
        # ... custom browse logic ...
    else:
        base_path = Path(directory or ".")
```

### 3. Use Output Handler for File Saving

Always use `OutputHandler` for commands that can save output:

```python
# ✅ Good - Uses output handler
from cli_utils.utils.output_handler import OutputHandler, create_default_filename

def my_command(output: OutputOption = None):
    handler = OutputHandler(output=output, default_filename="report.txt")
    handler.save_or_print(content)

# ❌ Bad - Manual file handling
def my_command(output: Optional[str] = None):
    if output:
        with open(output, 'w') as f:
            f.write(content)
    else:
        print(content)
```

### 4. Provide Appropriate Default Filenames

Use format-specific extensions in default filenames:

```python
# ✅ Good - Format-specific filename
extension_map = {"text": "txt", "json": "json", "markdown": "md"}
default_filename = create_default_filename("report", format, extension_map)

# ❌ Bad - Generic filename
default_filename = "output.txt"  # Doesn't respect format
```

### 5. Handle Browse Cancellation

The utility functions handle cancellation automatically:

```python
# ✅ Good - Utilities handle cancellation with typer.Abort()
base_path = get_directory(directory=directory, browse=browse)
# If user cancels, typer.Abort() is raised automatically

# No need to manually check for None
```

## Testing Commands with Common Utilities

When testing commands that use common utilities:

```python
import pytest
from pathlib import Path

def test_my_command_basic(tmp_path):
    """Test without browse mode."""
    from cli_utils.commands.local.mygroup.mycommand import my_command

    # Create test directory
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    (test_dir / "test.py").write_text("# test")

    # Test with direct path (no browse)
    my_command(directory=str(test_dir), browse=False)

def test_my_command_with_output(tmp_path):
    """Test output to file."""
    output_file = tmp_path / "output.txt"
    my_command(output=str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert len(content) > 0
```

## Migration Guide

If you have existing commands that implement these patterns manually, here's how to migrate:

### Before (Manual Implementation)

```python
def old_command(
    directory: Optional[str] = typer.Argument(None),
    recursive: bool = typer.Option(False, "--recursive", "-r"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
):
    # Manual directory handling
    base_path = Path(directory or ".").resolve()

    # Manual recursive search
    if recursive:
        files = base_path.rglob("*.py")
    else:
        files = base_path.glob("*.py")

    # Manual output handling
    result = generate_output()
    if output:
        Path(output).write_text(result)
    else:
        print(result)
```

### After (Using Common Utilities)

```python
from cli_utils.utils.common_options import (
    OptionalDirectoryArg,
    RecursiveOption,
    OutputOption,
)
from cli_utils.utils.directory_handler import get_directory
from cli_utils.utils.output_handler import OutputHandler

def new_command(
    directory: OptionalDirectoryArg = None,
    recursive: RecursiveOption = False,
    output: OutputOption = None,
):
    # Automatic directory handling (no browse support yet, but easy to add)
    base_path = get_directory(directory=directory, browse=False)

    # Same recursive search
    if recursive:
        files = base_path.rglob("*.py")
    else:
        files = base_path.glob("*.py")

    # Automatic output handling with browse support
    result = generate_output()
    handler = OutputHandler(output=output, default_filename="report.txt")
    handler.save_or_print(result)
```

## See Also

- [Adding Commands](adding-commands.md) - How to create new commands
- [Command Reference](../reference/commands.md) - Documentation of all commands
- [Devtools Examples](../examples/devtools.md) - Real-world usage of common utilities
