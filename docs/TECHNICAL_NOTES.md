# Technical Notes

## RuntimeWarning Fix

### The Problem

Previously, when running the CLI with `python -m cli_utils.main`, you would see:

```
RuntimeWarning: 'cli_utils.main' found in sys.modules after import of package 'cli_utils',
but prior to execution of 'cli_utils.main'; this may result in unpredictable behaviour
```

### Why It Happened

When you run `python -m cli_utils.main`:

1. Python loads the package `cli_utils`
2. Then it loads `cli_utils.main` as the `__main__` module
3. But code in the package also imports from `cli_utils.main` (e.g., in `__init__.py`)
4. This creates **two references** to the same module:
   - One as `__main__` (the running module)
   - One as `cli_utils.main` (the imported module)

Python's import system detects this inconsistency and warns about it because:
- The same module code exists in memory twice
- Changes to module-level state in one won't reflect in the other
- It can lead to subtle bugs (singletons not being singletons, etc.)

### The Solution

We created a separate `__main__.py` entry point:

**Before:**
```
cli_utils/
├── main.py          # Both entry point AND importable module
└── __init__.py      # Imports from main.py
```

**After:**
```
cli_utils/
├── __main__.py      # Entry point ONLY (python -m cli_utils)
├── main.py          # Importable module
└── __init__.py      # Imports from main.py
```

**File: `src/cli_utils/__main__.py`**
```python
from cli_utils.main import run

if __name__ == "__main__":
    run()
```

**File: `src/cli_utils/main.py`**
```python
# No more if __name__ == "__main__" at the bottom
def run() -> None:
    loader = create_plugin_loader(app)
    loader.load_all_commands()
    app()
```

### Why This Works

Now when you run `python -m cli_utils`:

1. Python looks for `cli_utils/__main__.py` (standard behavior)
2. `__main__.py` imports and calls `run()` from `cli_utils.main`
3. `cli_utils.main` exists only as an importable module, not as `__main__`
4. No duplicate module references ✅
5. No warning ✅

### Usage

All these now work cleanly without warnings:

```bash
# Direct module execution
python -m cli_utils --help

# Via wrapper script
~/bin/cli-utils --help

# Via uv
uv run python -m cli_utils --help

# Via entry point (after installation)
cli-utils --help
```

### Related Files Updated

1. `src/cli_utils/__main__.py` - New entry point
2. `src/cli_utils/main.py` - Removed `if __name__ == "__main__"`
3. `scripts/cli-utils` - Changed from `-m cli_utils.main` to `-m cli_utils`
4. `pyproject.toml` - Entry point already used `cli_utils.main:app` (no change needed)

### Best Practices

This pattern is the Python standard for packages:

- `__main__.py` - Entry point for `-m` execution
- `main.py` or similar - Importable application code
- Keep them separate to avoid circular dependencies and warnings

### References

- [PEP 338 - Executing modules as scripts](https://www.python.org/dev/peps/pep-0338/)
- [Python Documentation - __main__](https://docs.python.org/3/library/__main__.html)
- [Python runpy module](https://docs.python.org/3/library/runpy.html)

## Additional Technical Decisions

### Why Three-Level Command Hierarchy?

```
cli-utils <category> <group> <command>
          └──────┘   └────┘   └──────┘
          local/      text_    uppercase
          remote      utils
```

**Benefits:**
- Clear organization (local vs remote, by functionality)
- Easy to navigate with tab completion
- Prevents command name conflicts
- Scales well (can add many commands without clutter)

### Why Auto-Discovery?

Instead of manually registering commands, we use:

```python
def _load_command_group(self, category_name: str, group_path: Path, ...):
    for py_file in group_path.glob("*.py"):
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if self._is_typer_command(obj):
                group_app.command()(obj)
```

**Benefits:**
- Zero boilerplate for new commands
- Just create a file, write a function, done
- Less chance of forgetting to register
- DRY principle (Don't Repeat Yourself)

### Why Separate config.py?

Configuration is separate from main application logic:

**Benefits:**
- Can be imported anywhere without circular dependencies
- Testable in isolation
- Singleton pattern for settings
- Multiple configuration sources (env, yaml, defaults)

### Why uv?

We chose `uv` over `pip`:

**Benefits:**
- 10-100x faster than pip
- Better dependency resolution
- Built-in virtual environment management
- Modern Python packaging tool
- Compatible with pip requirements

### File Naming Conventions

- `lowercase.py` - Command modules
- `__init__.py` - Package markers
- `UPPERCASE.md` - Documentation (README, INSTALL, etc.)
- `Makefile` - Build automation (no extension)

## Performance Considerations

### Plugin Loading

Plugin loading happens once at startup:

```python
def run():
    loader = create_plugin_loader(app)
    loader.load_all_commands()  # ~0.1s for 3 commands
    app()
```

**Future optimization:**
- Lazy loading for large command sets
- Caching of command metadata
- Async plugin loading

### Virtual Environment Usage

The wrapper script uses the venv Python directly:

```bash
"$VENV_PYTHON" -m cli_utils "$@"
```

**vs** activating the venv:

```bash
source .venv/bin/activate
python -m cli_utils "$@"
```

**Benefits of direct execution:**
- Faster (no shell initialization)
- No environment pollution
- Works in non-interactive shells

## Future Improvements

- [ ] Command caching for faster subsequent runs
- [ ] Shell completion generation
- [ ] Plugin system for third-party commands
- [ ] Web interface (Flask/FastAPI)
- [ ] Container support (Podman)
- [ ] CI/CD pipeline configuration
- [ ] Pre-commit hooks
- [ ] Command aliases
- [ ] Interactive mode (REPL)
- [ ] Progress bars for long operations
