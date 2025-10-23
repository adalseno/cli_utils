# Text Utils Examples

The text utils group provides commands for common text manipulation tasks.

## Uppercase

Convert text to uppercase:

```bash
cli-utils local text-utils uppercase "hello world"
# Output: HELLO WORLD
```

With clipboard support (requires pyperclip):

```bash
cli-utils local text-utils uppercase "hello world" --copy
# Output: HELLO WORLD
# ✓ Copied to clipboard
```

## Lowercase

Convert text to lowercase:

```bash
cli-utils local text-utils lowercase "HELLO WORLD"
# Output: hello world
```

## Title Case

Convert text to title case:

```bash
cli-utils local text-utils titlecase "hello world"
# Output: Hello World
```

## Use Cases

### Processing File Names

```bash
# Convert filename to lowercase
NEW_NAME=$(cli-utils local text-utils lowercase "MY_FILE.TXT")
mv "MY_FILE.TXT" "$NEW_NAME"
```

### Formatting Output

```bash
# Format headers
HEADER=$(cli-utils local text-utils uppercase "important notice")
echo "$HEADER"
```

### Batch Processing

```bash
# Process multiple strings
for word in "hello" "world" "test"; do
    cli-utils local text-utils titlecase "$word"
done
```

## Adding More Text Utils

You can easily add more text utilities. Here's an example:

```python
# src/cli_utils/commands/local/text_utils/reverse.py
import typer
from rich.console import Console

console = Console()


def reverse(
    text: str = typer.Argument(..., help="Text to reverse"),
) -> None:
    """Reverse the input text."""
    result = text[::-1]
    console.print(f"[green]{result}[/green]")
```

Then use it:

```bash
cli-utils local text-utils reverse "hello"
# Output: olleh
```
