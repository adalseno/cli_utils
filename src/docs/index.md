# CLI Utils Documentation

Welcome to **CLI Utils** - a modern CLI application designed to organize and manage your Python scripts for both local tasks and remote API interactions.

## Features

- **Modular Architecture**: Easily add new commands by creating Python files in organized directories
- **Auto-Discovery**: Commands are automatically discovered and loaded from the commands directory
- **Command Groups**: Organize related commands into groups (e.g., text_utils, file_ops)
- **Rich Output**: Beautiful terminal output using Rich library
- **Type-Safe**: Full type hints throughout the codebase
- **Well-Tested**: Comprehensive test suite with pytest
- **Documented**: Auto-generated API documentation from docstrings

## Quick Example

```bash
# Convert text to uppercase
cli-utils local text-utils uppercase "hello world"

# Get help for any command
cli-utils --help
cli-utils local --help
cli-utils local text-utils --help
```

## Project Structure

```
cli_utils/
├── src/
│   ├── cli_utils/
│   │   ├── main.py           # Main entry point
│   │   ├── config.py         # Configuration management
│   │   ├── core/             # Core utilities
│   │   │   └── plugin_loader.py
│   │   ├── commands/         # Command modules
│   │   │   ├── local/        # Local task commands
│   │   │   │   ├── text_utils/
│   │   │   │   ├── file_ops/
│   │   │   │   └── system_info/
│   │   │   └── remote/       # Remote API commands
│   │   └── utils/            # Shared utilities
│   ├── docs/                 # Documentation
│   └── tests/                # Test suite
├── pyproject.toml
└── mkdocs.yml
```

## Getting Started

Check out the [Installation Guide](getting-started/installation.md) to get started with CLI Utils.

## Design Philosophy

CLI Utils is built with the following principles:

- **Modularity**: Each command is self-contained and independent
- **Discoverability**: Auto-load commands from directories without manual registration
- **Type Safety**: Full type hints for better IDE support and fewer bugs
- **Documentation**: Comprehensive docstrings on everything
- **Testability**: Easy to test individual components
- **Extensibility**: Simple to add new commands without modifying core code
