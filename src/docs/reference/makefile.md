# Makefile Quick Reference Guide

This document provides a quick reference for all available Make targets in the CLI Utils project.

## Essential Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands with descriptions |
| `make install` | Install project dependencies |
| `make install-dev` | Install project with development dependencies |

## Testing

| Command | Example | Description |
|---------|---------|-------------|
| `make test` | `make test` | Run all tests with coverage |
| `make test TEST=<path>` | `make test TEST=src/tests/test_config.py` | Run specific test file(s) |
| `make test ARGS=<flags>` | `make test ARGS="--no-cov -v"` | Run tests with custom pytest flags |
| `make test TEST=<path> ARGS=<flags>` | `make test TEST=test_core ARGS="-v"` | Combine both parameters |
| `make test-cov` | `make test-cov` | Run tests with detailed coverage report |
| `make test ARGS="-k <pattern>"` | `make test ARGS="-k test_uppercase"` | Run tests matching a pattern |

### Test Examples

```bash
# Run all tests
make test

# Run specific test file
make test TEST=src/tests/test_core/test_config.py

# Run all tests in a directory
make test TEST=src/tests/test_core

# Run without coverage (faster)
make test ARGS="--no-cov"

# Run with verbose output
make test ARGS="-v"

# Run specific test by name pattern
make test ARGS="-k test_uppercase"

# Run tests in parallel (requires pytest-xdist)
make test ARGS="-n auto"

# Run failed tests from last run
make test ARGS="--lf"
```

## Code Quality

| Command | Description |
|---------|-------------|
| `make format` | Format code with ruff |
| `make lint` | Run linting checks (read-only) |
| `make lint-fix` | Run linting and auto-fix issues |
| `make check` | Format and lint in one command |
| `make qa` | Run full QA: clean, format, lint, test with coverage |
| `make ci` | Run CI checks: lint and test with coverage |

## Documentation

| Command | Description |
|---------|-------------|
| `make docs-build` | Build documentation to `src/site/` |
| `make docs-serve` | Serve documentation at http://127.0.0.1:8000 |
| `make docs-deploy` | Deploy documentation to GitHub Pages |

## Maintenance

| Command | Description |
|---------|-------------|
| `make clean` | Remove temporary files, caches, and build artifacts |
| `make tree` | Show project structure (requires `tree` or uses `find`) |
| `make coverage-open` | Open HTML coverage report in browser |

## Development Workflow

| Command | Description |
|---------|-------------|
| `make dev-setup` | Complete development environment setup (includes Nerd Font check) |
| `make check-nerdfonts` | Check if Nerd Fonts are installed on the system |
| `make migrate-icons` | Migrate TODO app category icons from emoji to Nerd Fonts |
| `make run` | Run the CLI application with help |
| `make version` | Display version information |
| `make shell` | Start interactive Python shell with project loaded |
| `make build` | Build distribution packages |

## Project Setup

| Command | Description |
|---------|-------------|
| `make init` | Interactively create a new command group |
| `make git-status` | Show git status with formatting |

## Global Installation

| Command | Description |
|---------|-------------|
| `make link-global` | Create symlink in ~/bin (recommended for dev) |
| `make install-global` | Copy script to ~/bin (more stable) |
| `make uninstall-global` | Remove from ~/bin |
| `make check-global` | Verify global installation status |

## Future Features

| Command | Description |
|---------|-------------|
| `make container-build` | Build Podman container (coming soon) |
| `make container-run` | Run in container (coming soon) |

## Common Workflows

### Daily Development

```bash
# Start of day
make dev-setup          # Ensure environment is ready
make test               # Run tests

# During development
make format             # Format your code
make lint               # Check for issues
make test               # Run tests frequently

# Before committing
make check              # Format and lint
make test-cov           # Ensure good coverage
```

### Pre-commit Checklist

```bash
make qa                 # Runs: clean, format, lint-fix, test-cov
# Review output, then commit
```

### CI/CD Pipeline

```bash
make ci                 # Runs: lint, test-cov
```

### Checking Nerd Font Support

```bash
# Check if Nerd Fonts are installed
make check-nerdfonts

# This will show:
# - Whether Nerd Fonts are detected
# - List of installed Nerd Fonts
# - Installation instructions if needed
```

**What it does:**
- Scans your system fonts using `fc-list`
- Detects any installed Nerd Fonts
- Shows up to 5 detected fonts
- Provides installation guidance if needed

**Why it matters:**
- Nerd Fonts provide beautiful icons in the TODO app
- Fallback to emoji or text if not available
- Part of `make dev-setup` workflow

### Migrating Category Icons

```bash
# Migrate TODO app category icons to Nerd Fonts
make migrate-icons
```

**What it does:**
- Updates all TODO app categories in the database
- Replaces emoji icons with Nerd Font equivalents
- Preserves category names and descriptions

**When to use:**
- After upgrading to a version with icon system support
- After installing Nerd Fonts for the first time
- If you want to convert emoji categories to Nerd Font icons

**Example output:**
```
CATEGORY ICON MIGRATION
============================================================

Found 2 categories

Updating category 'Personal':
  Old icon: 👤 (code: '👤')
  New icon: 󰀄 (code: '\U000f0004')
Updating category 'Work':
  Old icon: 💼 (code: '💼')
  New icon: 󰃖 (code: '\U000f00d6')

============================================================
Migration complete: 2 categories updated
============================================================
```

### Creating New Commands

```bash
# Option 1: Use interactive helper
make init

# Option 2: Manual
mkdir -p src/cli_utils/commands/local/my_group
touch src/cli_utils/commands/local/my_group/__init__.py
# Create your command files...
```

### Debugging Tests

```bash
# Run with verbose output and stop at first failure
make test ARGS="-vv -x"

# Run specific test with print statements visible
make test TEST=test_file.py ARGS="-s"

# Drop into debugger on failure
make test ARGS="--pdb"

# Show test durations
make test ARGS="--durations=10"
```

## Tips & Tricks

1. **Combine TEST and ARGS**: You can use both parameters together
   ```bash
   make test TEST=src/tests/test_core ARGS="-v --no-cov"
   ```

2. **Use tab completion**: Type `make` and press TAB to see available targets

3. **Multiple test files**: You can specify multiple test files
   ```bash
   make test TEST="src/tests/test_config.py src/tests/test_commands/"
   ```

4. **Quiet mode**: Add `-s` to make for silent operation
   ```bash
   make -s test
   ```

5. **Dry run**: Use `make -n <target>` to see what would be executed
   ```bash
   make -n test
   ```

## Environment Variables

You can override the UV binary if needed:
```bash
UV=/path/to/uv make test
```

## Getting Help

```bash
# Show all available commands
make help

# See what a command will do (dry-run)
make -n test

# Check Makefile for details
cat Makefile
```
