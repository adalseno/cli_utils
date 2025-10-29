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

```bash
# Clone the repository
git clone https://github.com/adalseno/cli_utils.git
cd cli_utils

# Install with development dependencies
make install-dev

# Verify installation
make test
```

For detailed installation instructions, see the [Installation Guide](src/docs/getting-started/installation.md).

### Basic Usage

```bash
# Get help
cli-utils --help

# Convert text to uppercase
cli-utils local text-utils uppercase "hello world"

# Launch interactive TODO app with reminders
cli-utils local system-info todo

# View configuration
cli-utils config

# Check version
cli-utils version
```

### Development

```bash
make help          # Show all available commands
make test          # Run tests
make test-cov      # Run tests with coverage
make format        # Format code with ruff
make lint          # Run linting checks
make docs-serve    # Serve documentation locally
```

See the [Makefile Reference](src/docs/reference/makefile.md) for all available commands.

## Documentation

📚 **[View Full Documentation Online](https://adalseno.github.io/cli_utils)**

The complete documentation is also available in the [src/docs](src/docs/) folder:

- **Getting Started**
  - [Installation](src/docs/getting-started/installation.md)
  - [Quick Start](src/docs/getting-started/quickstart.md)
- **User Guide**
  - [Configuration](src/docs/user-guide/configuration.md)
  - [Adding Commands](src/docs/user-guide/adding-commands.md)
  - [Command Groups](src/docs/user-guide/command-groups.md)
- **Reference**
  - [Quick Reference](src/docs/reference/quick-reference.md)
  - [Makefile Guide](src/docs/reference/makefile.md)
  - [Shell Aliases](src/docs/reference/shell-aliases.md)
  - [Scripts](src/docs/reference/scripts.md)
- **Examples**
  - [Text Utils](src/docs/examples/text-utils.md)
  - [Devtools](src/docs/examples/devtools.md)
  - [TODO App](src/docs/examples/todo-app.md)
  - [Clipboard](src/docs/examples/clipboard.md)
  - [API Commands](src/docs/examples/api-commands.md)

Or serve the documentation locally:

```bash
make docs-serve
# Visit http://127.0.0.1:8000
```

## Project Structure

```
cli_utils/
├── src/
│   ├── cli_utils/           # Main package
│   │   ├── main.py          # Entry point
│   │   ├── config.py        # Configuration management
│   │   ├── core/            # Core utilities
│   │   └── commands/        # Command modules
│   │       ├── local/       # Local task commands
│   │       │   ├── text_utils/
│   │       │   ├── devtools/
│   │       │   └── ...
│   │       └── remote/      # Remote API commands
│   ├── docs/                # MkDocs documentation
│   └── tests/               # Test suite
├── scripts/                 # Helper scripts
├── Makefile                 # Build automation
└── pyproject.toml          # Project configuration
```

## Technology Stack

- **CLI Framework**: Typer with Rich
- **Package Manager**: uv
- **Testing**: pytest with pytest-cov
- **Documentation**: MkDocs with Material theme
- **Code Quality**: Ruff (formatter & linter)

## License

[GPL-3.0](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting: `make qa`
5. Submit a pull request

## Acknowledgments

This project was developed with assistance from [Claude Code](https://claude.com/claude-code), Anthropic's official CLI for Claude.
