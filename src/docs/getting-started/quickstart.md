# Quick Start Guide

This guide will help you get started with CLI Utils in just a few minutes.

## Basic Usage

### Getting Help

CLI Utils has built-in help for all commands:

```bash
# General help
cli-utils --help

# Help for a category
cli-utils local --help

# Help for a command group
cli-utils local text-utils --help

# Help for a specific command
cli-utils local text-utils uppercase --help
```

### Using Text Utilities

The text utilities provide simple text manipulation commands:

```bash
# Convert to uppercase
cli-utils local text-utils uppercase "hello world"
# Output: HELLO WORLD

# Convert to lowercase
cli-utils local text-utils lowercase "HELLO WORLD"
# Output: hello world

# Convert to title case
cli-utils local text-utils titlecase "hello world"
# Output: Hello World
```

### Configuration

View your current configuration:

```bash
cli-utils config
```

Configuration is stored in `~/.config/cli-utils/config.yaml` and can be customized.

### Version Information

Check the installed version:

```bash
cli-utils version
```

## Next Steps

- Learn about [Configuration](../user-guide/configuration.md)
- Discover how to [Add Your Own Commands](../user-guide/adding-commands.md)
- Explore [Examples](../examples/text-utils.md)
