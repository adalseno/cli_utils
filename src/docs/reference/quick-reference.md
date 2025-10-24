# CLI Utils - Quick Reference Card

## Installation

```bash
# Install dependencies
make install-dev

# Install globally (symlink - recommended)
make link-global

# Install shell shortcuts
make install-aliases
source ~/.zshrc
```

## Shell Shortcuts (After `make install-aliases`)

### Text Conversion
```bash
textup "hello world"       # HELLO WORLD
textlow "HELLO WORLD"      # hello world
texttitle "hello world"    # Hello World
```

### General Shortcuts
```bash
cu --help                  # cli-utils --help
cul text_utils uppercase   # cli-utils local text_utils uppercase
cuv                        # Show version
cuc                        # Show config
```

### With Pipes
```bash
echo "hello" | textup_pipe       # HELLO
cat file.txt | textlow_pipe      # lowercase each line
```

## Full Commands

```bash
# Text utilities
cli-utils local text_utils uppercase "text"
cli-utils local text_utils lowercase "TEXT"
cli-utils local text_utils titlecase "text"

# With clipboard (requires pyperclip)
cli-utils local text_utils uppercase --copy "text"

# Developer tools
cli-utils local devtools code-report .
cli-utils local devtools code-report src --recursive
cli-utils local devtools code-report . -r -f json
cli-utils local devtools code-report . --format markdown
cli-utils local devtools code-report --browse          # Interactive directory picker
cli-utils local devtools code-report -b -r             # Browse + recursive

cli-utils local devtools count-tests tests             # Count test functions
cli-utils local devtools count-tests tests -r          # Recursive test count
cli-utils local devtools count-tests tests -r -v       # Verbose (show test names)
cli-utils local devtools count-tests -b -r             # Browse + count tests

# Configuration
cli-utils config
cli-utils version
```

## Development

```bash
# Testing
make test                           # Run all tests
make test TEST=test_config.py       # Run specific test
make test ARGS="-k test_uppercase"  # Run by pattern
make test-cov                       # With coverage

# Code Quality
make format                         # Format code
make lint                           # Check linting
make check                          # Format + lint
make qa                             # Full QA suite

# Documentation
make docs-serve                     # Serve at localhost:8000
make docs-build                     # Build static docs

# Utilities
make clean                          # Clean temp files
make tree                           # Show structure
make run                            # Run CLI with help
```

## Adding New Commands

```bash
# 1. Create file
touch src/cli_utils/commands/local/text_utils/reverse.py

# 2. Write function
cat > src/cli_utils/commands/local/text_utils/reverse.py << 'EOF'
import typer
from rich.console import Console

console = Console()

def reverse(text: str = typer.Argument(..., help="Text to reverse")) -> None:
    """Reverse the input text."""
    console.print(f"[green]{text[::-1]}[/green]")
EOF

# 3. Test it - automatically available!
cli-utils local text_utils reverse "hello"
```

## Configuration

**Location:** `~/.config/cli-utils/config.yaml`

```yaml
api:
  timeout: 60
  max_retries: 5
  github:
    token: your_token

preferences:
  output_format: json
```

**Environment Variables:**
- `CLI_UTILS_LOG_LEVEL` - Logging level
- `CLI_UTILS_API_TIMEOUT` - API timeout (seconds)
- `CLI_UTILS_MAX_RETRIES` - Max retry attempts

## File Structure

```
cli_utils/
├── src/
│   ├── cli_utils/
│   │   ├── __main__.py          # Entry point
│   │   ├── main.py              # App logic
│   │   ├── config.py            # Configuration
│   │   ├── core/
│   │   │   └── plugin_loader.py # Auto-discovery
│   │   └── commands/
│   │       ├── local/           # Local commands
│   │       │   └── text_utils/
│   │       └── remote/          # Remote API commands
│   ├── docs/                    # Documentation
│   └── tests/                   # Tests
├── scripts/
│   ├── cli-utils                # Wrapper script
│   └── shell-aliases.sh         # Shell shortcuts
├── Makefile                     # Build automation
└── pyproject.toml              # Project config
```

## Troubleshooting

```bash
# Command not found
which cli-utils                  # Check if in PATH
make check-global               # Verify installation

# Shortcuts not working
type textup                     # Check if loaded
source ~/.zshrc                 # Reload shell

# Tests failing
make clean && make test         # Clean and retest

# Dependencies out of date
make install-dev                # Reinstall dependencies
```

## Common Workflows

### Daily Development
```bash
make test           # Run tests frequently
make format         # Format before commit
make qa            # Full check before push
```

### Before Commit
```bash
make check         # Format + lint
make test-cov      # Tests with coverage
git add . && git commit -m "message"
```

### After Updates
```bash
git pull
make install-dev
# Changes immediately available (if using symlink)
```

## Help & Documentation

```bash
make help                       # Show all make commands
cli-utils --help               # CLI help
cli-utils local --help         # Category help
cli-utils local text_utils --help  # Group help
```

**Documentation:**
- [Project Overview](../../README.md) - README at project root
- [Installation Guide](../getting-started/installation.md) - Detailed installation
- [Shell Aliases](shell-aliases.md) - Alias guide
- [Makefile Guide](makefile.md) - Makefile reference

## Examples

```bash
# Convert text
textup "hello world"

# Process files
cat names.txt | textlow_pipe > names_lower.txt

# Analyze code
cli-utils local devtools code-report src --recursive

# Generate metrics in JSON
cli-utils local devtools code-report . -r -f json > metrics.json

# In scripts
#!/bin/bash
UPPER=$(textup "$1")
echo "Uppercase: $UPPER"

# Chain commands
echo "hello world" | textup_pipe | tee output.txt
```

## Tips

- Use tab completion: `cli-utils <TAB>`
- Quote multi-word arguments: `textup "hello world"`
- Use pipes for file processing: `cat file | textup_pipe`
- Check logs: `CLI_UTILS_LOG_LEVEL=DEBUG cli-utils ...`
