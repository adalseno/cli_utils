# Adding Commands

One of the key features of CLI Utils is how easy it is to add new commands. This guide will show you how.

## Command Structure

Commands are organized in a three-level hierarchy:

1. **Category**: `local` or `remote`
2. **Group**: A functional grouping (e.g., `text_utils`, `file_ops`)
3. **Command**: Individual command files

## Creating a New Command

### Step 1: Choose Location

Decide where your command should go:

- **Local tasks**: `src/cli_utils/commands/local/<group>/`
- **Remote API calls**: `src/cli_utils/commands/remote/<group>/`

### Step 2: Create or Use a Group

Create a new group directory if needed, or use an existing one:

```bash
mkdir -p src/cli_utils/commands/local/my_group
touch src/cli_utils/commands/local/my_group/__init__.py
```

### Step 3: Create Your Command File

Create a new Python file with your command:

```python
# src/cli_utils/commands/local/my_group/hello.py
"""Say hello to someone.

This module provides a simple greeting command.
"""

import typer
from rich.console import Console

console = Console()


def hello(
    name: str = typer.Argument(..., help="Name to greet"),
    formal: bool = typer.Option(False, "--formal", "-f", help="Use formal greeting"),
) -> None:
    """Say hello to someone.

    Args:
        name: The name of the person to greet
        formal: If True, use a formal greeting

    Example:
        $ cli-utils local my-group hello Alice
        Hello, Alice!
    """
    if formal:
        greeting = f"Good day, {name}!"
    else:
        greeting = f"Hello, {name}!"

    console.print(f"[green]{greeting}[/green]")
```

### Step 4: That's It!

Your command is automatically discovered and loaded. No registration needed!

```bash
cli-utils local my-group hello Alice
# Output: Hello, Alice!

cli-utils local my-group hello Alice --formal
# Output: Good day, Alice!
```

## Best Practices

### 1. Type Hints

Always use type hints for better IDE support and documentation:

```python
def my_command(
    text: str,
    count: int = 1,
    verbose: bool = False,
) -> None:
    ...
```

### 2. Docstrings

Write comprehensive docstrings:

```python
def my_command(text: str) -> None:
    """Brief description.

    Longer description with more details about what
    this command does and when to use it.

    Args:
        text: Description of the text parameter

    Example:
        $ cli-utils local group my-command "test"
    """
    ...
```

### 3. Use Rich for Output

Use Rich console for beautiful output:

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def my_command() -> None:
    # Simple colored output
    console.print("[green]Success![/green]")

    # Tables
    table = Table(title="Results")
    table.add_column("Name")
    table.add_column("Value")
    console.print(table)

    # Panels
    console.print(Panel("Important message", border_style="cyan"))
```

### 4. Handle Errors Gracefully

Use try-except blocks and provide helpful error messages:

```python
def my_command(file_path: str) -> None:
    try:
        with open(file_path) as f:
            content = f.read()
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(1)
```

## Command Templates

### Simple Command

```python
import typer
from rich.console import Console

console = Console()


def my_command(
    arg: str = typer.Argument(..., help="Description"),
) -> None:
    """Brief description."""
    console.print(f"[green]{arg}[/green]")
```

### Command with Options

```python
import typer
from rich.console import Console

console = Console()


def my_command(
    input_text: str = typer.Argument(..., help="Input text"),
    output_file: str = typer.Option(None, "--output", "-o", help="Output file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Brief description."""
    if verbose:
        console.print(f"[dim]Processing: {input_text}[/dim]")

    # Process...

    if output_file:
        with open(output_file, "w") as f:
            f.write(result)
        console.print(f"[green]Saved to {output_file}[/green]")
    else:
        console.print(result)
```

### API Command

```python
import typer
import requests
from rich.console import Console

console = Console()


def fetch_data(
    endpoint: str = typer.Argument(..., help="API endpoint"),
    api_key: str = typer.Option(None, "--api-key", help="API key"),
) -> None:
    """Fetch data from an API."""
    try:
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        console.print(data)

    except requests.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
```

## Testing Your Command

Create tests in `src/tests/test_commands/`:

```python
# src/tests/test_commands/test_my_group.py
from cli_utils.commands.local.my_group import hello


def test_hello_command():
    # Test your command logic
    ...
```

Run tests:

```bash
pytest
```

## Using Common Utilities

CLI Utils provides reusable utilities for common patterns like directory browsing, file selection, and output handling. See the [Common Utilities](common-utilities.md) guide for details on:

- **Common Options**: Pre-defined `Annotated` types for `--recursive`, `--browse`, `--output`, `--verbose`
- **Directory Handler**: Easy directory selection with file manager support
- **Output Handler**: Handle console vs file output with browse mode
- **File Picker**: Low-level file manager integration
- **Clipboard**: Cross-platform clipboard support

**Example using common utilities:**

```python
from cli_utils.utils.common_options import (
    BrowseOption,
    OptionalDirectoryArg,
    OutputOption,
    RecursiveOption,
)
from cli_utils.utils.directory_handler import get_directory
from cli_utils.utils.output_handler import OutputHandler, create_default_filename

def my_command(
    directory: OptionalDirectoryArg = None,
    recursive: RecursiveOption = False,
    browse: BrowseOption = False,
    output: OutputOption = None,
) -> None:
    """My command with common utilities."""
    # Get directory with browse support
    base_path = get_directory(directory=directory, browse=browse)

    # Process files
    files = base_path.rglob("*.py") if recursive else base_path.glob("*.py")
    result = f"Found {len(list(files))} files"

    # Handle output
    handler = OutputHandler(output=output, default_filename="report.txt")
    handler.save_or_print(result)
```

This gives your command automatic support for:
- `--browse` / `-b` - Interactive directory selection
- `--recursive` / `-r` - Recursive file search
- `--output` / `-o` - Save to file or use browse mode for save location

See [Common Utilities](common-utilities.md) for complete documentation.

## Next Steps

- **[Common Utilities](common-utilities.md)** - Learn about reusable utilities
- **[Command Groups](command-groups.md)** - Organize related commands
- **[Examples](../examples/text-utils.md)** - See real command examples
- **[Command Reference](../reference/commands.md)** - Browse all available commands
