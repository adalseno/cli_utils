# Installation

## Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended)

## Installing with uv

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cli-utils.git
cd cli-utils
```

2. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
uv pip install -e .
```

3. Install development dependencies (optional):

```bash
uv pip install -e ".[dev]"
```

## Verifying Installation

Check that the installation was successful:

```bash
cli-utils --help
cli-utils version
```

You should see the CLI help message and version information.

## Next Steps

- Follow the [Quick Start Guide](quickstart.md) to learn the basics
- Read about [Configuration](../user-guide/configuration.md)
- Learn how to [Add Commands](../user-guide/adding-commands.md)
