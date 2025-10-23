# Installation Guide

This guide covers different ways to install and use CLI Utils.

## Table of Contents

- [Development Installation](#development-installation)
- [System-wide Installation](#system-wide-installation)
- [Installation Methods Comparison](#installation-methods-comparison)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)

## Development Installation

For local development and testing:

```bash
# Clone the repository
git clone <repository-url>
cd cli_utils

# Create virtual environment and install dependencies
make install-dev

# Test the installation
make test
make version
```

## System-wide Installation

There are two ways to make `cli-utils` available system-wide:

### Option 1: Symlink (Recommended for Development)

This creates a symlink in `~/bin` that points to your development version. Changes to the code are immediately available.

```bash
# Create symlink
make link-global

# Verify installation
make check-global

# Test it works
cli-utils --help
cli-utils version
```

**Advantages:**
- ✅ Immediate reflection of code changes
- ✅ Easy to update (just git pull and dependencies update)
- ✅ Only one copy of the code

**Disadvantages:**
- ⚠️ Requires the project directory to stay in place
- ⚠️ Depends on the virtual environment being intact

### Option 2: Copy Installation

This copies the wrapper script to `~/bin`. More stable but requires reinstallation after changes.

```bash
# Copy to ~/bin
make install-global

# Verify installation
make check-global

# Test it works
cli-utils --help
cli-utils version
```

**Advantages:**
- ✅ More stable (doesn't break if you move the project)
- ✅ Still uses the virtual environment from the original location

**Disadvantages:**
- ⚠️ Requires running `make install-global` after updates
- ⚠️ Still depends on the virtual environment location

### Ensuring ~/bin is in PATH

For either option, make sure `~/bin` is in your PATH. Add this to your `~/.zshrc`:

```bash
export PATH="$HOME/bin:$PATH"
```

Then reload your shell:

```bash
source ~/.zshrc
```

Or for bash users (`~/.bashrc`):

```bash
export PATH="$HOME/bin:$PATH"
```

## Installation Methods Comparison

| Method | Updates | Stability | Use Case |
|--------|---------|-----------|----------|
| **Development** | Manual (`git pull`) | Low (can break) | Active development |
| **Symlink** | Automatic | Medium | Testing, frequent changes |
| **Copy** | Manual (`make install-global`) | High | Production use |

## Verifying Installation

### Check if installed globally

```bash
make check-global
```

This will show:
- Whether the CLI is installed in `~/bin`
- Whether it's a symlink or copy
- Test output of the help command

### Manual verification

```bash
# Check if the file exists
ls -la ~/bin/cli-utils

# Check if it's executable
file ~/bin/cli-utils

# Check if it's in PATH
which cli-utils

# Test it runs
cli-utils --help
cli-utils version
```

## How the Wrapper Script Works

The `scripts/cli-utils` wrapper script:

1. **Finds the project root** - Even if symlinked, it resolves to the actual location
2. **Locates the virtual environment** - Looks for `.venv` in the project root
3. **Runs the CLI** - Uses the venv's Python with correct PYTHONPATH

The script handles three scenarios:

1. **Already in the correct venv** → Uses Python directly
2. **Venv exists** → Uses venv's Python with proper PYTHONPATH
3. **No venv found** → Shows helpful error message

## Uninstalling

To remove the global installation:

```bash
make uninstall-global
```

This only removes the file from `~/bin`. Your development installation remains intact.

## Updating

### If using symlink (link-global)

```bash
cd /path/to/cli_utils
git pull
make install-dev  # Update dependencies if needed
# Changes are immediately available via cli-utils command
```

### If using copy (install-global)

```bash
cd /path/to/cli_utils
git pull
make install-dev     # Update dependencies
make install-global  # Reinstall the wrapper script
```

## Troubleshooting

### Command not found

**Problem:** `cli-utils: command not found`

**Solutions:**
1. Check if installed: `ls -la ~/bin/cli-utils`
2. Check PATH: `echo $PATH | grep "$HOME/bin"`
3. Add to PATH in `~/.zshrc`: `export PATH="$HOME/bin:$PATH"`
4. Reload shell: `source ~/.zshrc`

### Virtual environment not found

**Problem:** `Error: Virtual environment not found at /path/to/.venv`

**Solutions:**
1. Install dependencies: `cd /path/to/cli_utils && make install-dev`
2. Recreate venv: `uv venv && make install-dev`

### Permission denied

**Problem:** `Permission denied` when running `cli-utils`

**Solutions:**
1. Make script executable: `chmod +x ~/bin/cli-utils`
2. Or reinstall: `make link-global` or `make install-global`

### Wrong version showing

**Problem:** Running old version after update

**Solutions:**
1. If using copy install: `make install-global` to reinstall
2. Check which command is being used: `which cli-utils`
3. Clear any shell command cache: `hash -r` or restart shell

### ImportError or ModuleNotFoundError

**Problem:** Python can't find modules

**Solutions:**
1. Ensure dependencies are installed: `make install-dev`
2. Check virtual environment: `ls -la /path/to/cli_utils/.venv`
3. Reinstall: `uv venv && make install-dev`

### Changes not reflected

**Problem:** Code changes don't show up when running `cli-utils`

**Solutions:**
1. If using copy install, reinstall: `make install-global`
2. If using symlink, check: `make check-global`
3. Verify you're editing the correct project: `readlink ~/bin/cli-utils`

## Advanced: Multiple Installations

You can have both development and global installations:

```bash
# Development: Run from project directory
cd /path/to/cli_utils
python -m cli_utils.main --help
# or
make run

# Global: Run from anywhere
cli-utils --help
```

## Alternative: uv run (Development Only)

For development, you can also use `uv run` directly:

```bash
cd /path/to/cli_utils
uv run python -m cli_utils.main --help
uv run python -m cli_utils.main local text_utils uppercase "hello"
```

This is what the Makefile uses internally.

## Shell Completion (Optional)

Enable shell completion for better UX:

```bash
# For zsh
cli-utils --install-completion zsh

# For bash
cli-utils --install-completion bash
```

Then restart your shell or source your rc file.
