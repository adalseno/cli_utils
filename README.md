# CLI Utils

A modern, extensible CLI application for organizing and managing Python scripts for both local tasks and remote API interactions.

## Features

- **Auto-Discovery**: Commands are automatically discovered and loaded from organized directories
- **Modular Architecture**: Easily add new commands by creating Python files in the right location
- **Rich Output**: Beautiful terminal output using the Rich library
- **Type-Safe**: Full type hints throughout the codebase
- **Well-Tested**: Comprehensive test suite with pytest
- **Documented**: Complete documentation with MkDocs and auto-generated API docs
- **Configurable**: Flexible configuration via YAML files and environment variables

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cli_utils
```

2. Create virtual environment and install:
```bash
uv venv
source .venv/bin/activate  # On Linux/macOS
uv pip install -e .
```

3. Install development dependencies (optional):
```bash
uv pip install -e ".[dev]"
```

### Making CLI Available System-wide

To use `cli-utils` from anywhere on your system:

```bash
# Option 1: Create symlink (recommended for development)
make link-global

# Option 2: Copy to ~/bin (more stable)
make install-global

# Verify installation
make check-global
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

### Shell Aliases and Shortcuts

For frequently used commands, install convenient shell shortcuts:

```bash
# Add shortcuts to your ~/.zshrc
make install-aliases

# Reload your shell
source ~/.zshrc
```

Now you can use short commands:

```bash
textup "hello world"              # HELLO WORLD
textlow "HELLO WORLD"             # hello world
texttitle "hello world"           # Hello World
cu --help                         # cli-utils --help
cuv                               # cli-utils version
```

See [docs/SHELL_ALIASES.md](docs/SHELL_ALIASES.md) for all available shortcuts.

### Basic Usage

```bash
# Get help
cli-utils --help

# Convert text to uppercase
cli-utils local text-utils uppercase "hello world"

# Convert text to lowercase
cli-utils local text-utils lowercase "HELLO WORLD"

# View configuration
cli-utils config

# Check version
cli-utils version
```

## Project Structure

```
cli_utils/
├── src/
│   ├── cli_utils/
│   │   ├── main.py              # Main entry point
│   │   ├── config.py            # Configuration management
│   │   ├── core/                # Core utilities
│   │   │   └── plugin_loader.py # Auto-discovery system
│   │   ├── commands/            # Command modules
│   │   │   ├── local/           # Local task commands
│   │   │   │   ├── text_utils/  # Text manipulation
│   │   │   │   ├── file_ops/    # File operations
│   │   │   │   └── system_info/ # System information
│   │   │   └── remote/          # Remote API commands
│   │   │       └── api_example/
│   │   └── utils/               # Shared utilities
│   ├── docs/                    # MkDocs documentation
│   └── tests/                   # Test suite
├── pyproject.toml
└── mkdocs.yml
```

## Adding New Commands

Adding a new command is incredibly easy:

1. Create a Python file in the appropriate group:
```bash
touch src/cli_utils/commands/local/text_utils/reverse.py
```

2. Write your command:
```python
import typer
from rich.console import Console

console = Console()

def reverse(text: str = typer.Argument(..., help="Text to reverse")) -> None:
    """Reverse the input text."""
    result = text[::-1]
    console.print(f"[green]{result}[/green]")
```

3. That's it! The command is automatically available:
```bash
cli-utils local text-utils reverse "hello"
# Output: olleh
```

## Development

The project includes a comprehensive Makefile to automate common tasks.

### Quick Reference

```bash
make help          # Show all available commands
make test          # Run tests
make test-cov      # Run tests with coverage
make format        # Format code with ruff
make lint          # Run linting checks
make check         # Format and lint
make docs-build    # Build documentation
make docs-serve    # Serve documentation locally
make qa            # Run full quality assurance
make clean         # Clean up temporary files
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
make test TEST=src/tests/test_core/test_config.py

# Run with custom pytest arguments
make test ARGS="--no-cov -v"

# Run tests matching a pattern
make test ARGS="-k test_uppercase"

# Run with coverage report
make test-cov
```

### Code Formatting & Linting

```bash
# Format code
make format

# Run linting
make lint

# Auto-fix linting issues
make lint-fix

# Format and lint in one command
make check
```

### Documentation

```bash
# Serve documentation locally (http://127.0.0.1:8000)
make docs-serve

# Build static documentation
make docs-build
```

### Other Useful Commands

```bash
# Clean temporary files
make clean

# Run full QA suite (clean, format, lint, test)
make qa

# Create a new command group interactively
make init

# Show project structure
make tree

# Open coverage report in browser
make coverage-open
```

## Configuration

Configuration is stored in `~/.config/cli-utils/config.yaml`:

```yaml
# API settings
api:
  timeout: 60
  max_retries: 5

# Custom settings
preferences:
  output_format: json
```

Environment variables:
- `CLI_UTILS_LOG_LEVEL`: Set logging level
- `CLI_UTILS_API_TIMEOUT`: API timeout in seconds
- `CLI_UTILS_MAX_RETRIES`: Maximum retry attempts

## Documentation

Full documentation is available at `src/docs/` or by running:

```bash
mkdocs serve
```

Then visit `http://localhost:8000`

## Technology Stack

- **CLI Framework**: Typer with Rich
- **Package Manager**: uv
- **Testing**: pytest with pytest-cov
- **Documentation**: MkDocs with Material theme
- **Code Quality**: Ruff (formatter & linter)
- **Type Checking**: Python type hints

## License

[GPL-3.0](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Acknowledgments

This project was developed with assistance from [Claude Code](https://claude.com/claude-code), Anthropic's official CLI for Claude. Claude Code helped with:

- Project architecture and structure design
- Implementation of the auto-discovery plugin system
- Comprehensive testing framework setup
- Documentation generation and organization
- Development tooling and automation (Makefile, etc.)
- Best practices for Python CLI applications

## Future Plans

- Web interface using Flask/FastAPI
- Containerization with Podman
- Additional command groups (file operations, system info, etc.)
- Plugin system for third-party commands