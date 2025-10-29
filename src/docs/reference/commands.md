# Command Reference

Complete reference for all available commands in CLI Utils.

## Command Structure

```bash
cli-utils [CATEGORY] [GROUP] [COMMAND] [OPTIONS] [ARGUMENTS]
```

- **CATEGORY**: `local` or `remote`
- **GROUP**: Command group (e.g., `text_utils`, `devtools`)
- **COMMAND**: Specific command to execute
- **OPTIONS**: Flags like `--help`, `--copy`, `--format`
- **ARGUMENTS**: Required or optional values

## Local Commands

Commands that operate locally on your system.

### Text Utils (`text_utils`)

Text transformation and manipulation commands.

#### `uppercase`

Convert text to uppercase.

**Usage:**
```bash
cli-utils local text_utils uppercase [OPTIONS] TEXT
```

**Arguments:**
- `TEXT` - Text to convert to uppercase (required)

**Options:**
- `--copy`, `-c` - Copy result to clipboard
- `--help` - Show help message

**Examples:**
```bash
# Basic usage
cli-utils local text_utils uppercase "hello world"
# Output: HELLO WORLD

# Copy to clipboard
cli-utils local text_utils uppercase --copy "hello"

# Using shell alias
textup "hello world"

# From pipe
echo "hello" | textup_pipe
```

#### `lowercase`

Convert text to lowercase.

**Usage:**
```bash
cli-utils local text_utils lowercase [OPTIONS] TEXT
```

**Arguments:**
- `TEXT` - Text to convert to lowercase (required)

**Options:**
- `--copy`, `-c` - Copy result to clipboard
- `--help` - Show help message

**Examples:**
```bash
# Basic usage
cli-utils local text_utils lowercase "HELLO WORLD"
# Output: hello world

# Copy to clipboard
cli-utils local text_utils lowercase --copy "HELLO"

# Using shell alias
textlow "HELLO WORLD"

# From pipe
echo "HELLO" | textlow_pipe
```

#### `titlecase`

Convert text to title case (capitalize each word).

**Usage:**
```bash
cli-utils local text_utils titlecase [OPTIONS] TEXT
```

**Arguments:**
- `TEXT` - Text to convert to title case (required)

**Options:**
- `--copy`, `-c` - Copy result to clipboard
- `--help` - Show help message

**Examples:**
```bash
# Basic usage
cli-utils local text_utils titlecase "hello world"
# Output: Hello World

# Copy to clipboard
cli-utils local text_utils titlecase --copy "hello"

# Using shell alias
texttitle "hello world"

# From pipe
echo "hello world" | texttitle_pipe
```

### Developer Tools (`devtools`)

Code analysis and testing utilities.

#### `code-report`

Analyze Python files and generate metrics reports.

**Usage:**
```bash
cli-utils local devtools code-report [OPTIONS] [DIRECTORY]
```

**Arguments:**
- `DIRECTORY` - Directory to analyze (optional, defaults to current directory)

**Options:**
- `--recursive`, `-r` - Search directories recursively
- `--format`, `-f` - Output format: `text` (default), `json`, or `markdown`
- `--browse`, `-b` - Browse for directory using file manager (yazi/mc)
- `--output`, `-o` - Save output to file (use 'browse' for interactive selection)
- `--help` - Show help message

**Output Metrics:**
- Line counts (excluding blank lines and comments)
- Number of classes, functions, and methods
- Percentage of total lines per file
- Methods per class breakdown

**Examples:**
```bash
# Analyze current directory
cli-utils local devtools code-report .

# Analyze specific directory recursively
cli-utils local devtools code-report src --recursive

# Generate JSON report
cli-utils local devtools code-report . --format json

# Generate markdown report
cli-utils local devtools code-report . --format markdown

# Browse for directory
cli-utils local devtools code-report --browse

# Browse and analyze recursively
cli-utils local devtools code-report -b -r

# Save to file
cli-utils local devtools code-report . --output report.txt

# Browse for save location
cli-utils local devtools code-report . -o browse

# Complete example: browse directory, analyze recursively, save as JSON
cli-utils local devtools code-report -b -r -f json -o browse
```

**Output Formats:**

*Text (default):*
```
├── analyze_file.py          (  150 lines, 2 classes, 3 functions, 8 methods, 15.2% of total)
    - FileAnalyzer: 5 methods
    - CodeMetrics: 3 methods
└── utils.py                 (  200 lines, 3 classes, 2 functions, 10 methods, 20.2% of total)

Total:
  Files     : 2
  Lines     : 350
  Classes   : 5
  Functions : 5
  Methods   : 18
```

*JSON:*
```json
{
  "total_files": 2,
  "total_lines": 350,
  "total_classes": 5,
  "total_functions": 5,
  "total_methods": 18,
  "files": [...]
}
```

*Markdown:*
```markdown
| File | Lines | Classes | Functions | Methods | % of Total |
|------|-------|---------|-----------|---------|------------|
| `analyze_file.py` | 150 | 2 | 3 | 8 | 42.9% |
| `utils.py` | 200 | 3 | 2 | 10 | 57.1% |
```

**See Also:**
- [Devtools Examples](../examples/devtools.md) - Detailed usage examples
- [Quick Reference](quick-reference.md) - Quick command overview

#### `count-tests`

Count test functions in Python test files.

**Usage:**
```bash
cli-utils local devtools count-tests [OPTIONS] [DIRECTORY]
```

**Arguments:**
- `DIRECTORY` - Directory to scan (optional, defaults to current directory)

**Options:**
- `--recursive`, `-r` - Search directories recursively
- `--pattern`, `-p` - File pattern to match (default: `test_*.py`)
- `--browse`, `-b` - Browse for directory using file manager
- `--verbose`, `-v` - Show individual test function names
- `--format`, `-f` - Output format: `table` (default), `summary`, or `json`
- `--output`, `-o` - Save output to file (use 'browse' for interactive selection)
- `--help` - Show help message

**What It Counts:**
- Total test files
- Total test functions (starting with `test_`)
- Total test classes (starting with `Test`)
- Tests per file
- Average tests per file

**Examples:**
```bash
# Count tests in current directory
cli-utils local devtools count-tests .

# Count tests recursively
cli-utils local devtools count-tests tests --recursive

# Show verbose output with test names
cli-utils local devtools count-tests tests -r -v

# Browse for test directory
cli-utils local devtools count-tests --browse

# Custom pattern for test files
cli-utils local devtools count-tests tests -p "*_test.py"

# Output as JSON
cli-utils local devtools count-tests tests -r -f json

# Summary format
cli-utils local devtools count-tests tests -r -f summary

# Save to file
cli-utils local devtools count-tests tests --output test_report.txt

# Browse for save location
cli-utils local devtools count-tests tests -o browse

# Complete example: browse, recursive, verbose, save as JSON
cli-utils local devtools count-tests -b -r -v -f json -o browse
```

**Output Formats:**

*Table (default):*
```
           Test Count Summary
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┓
┃ File               ┃ Tests ┃ Classes ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━┩
│ test_text_utils.py │     4 │       0 │
│ test_config.py     │     5 │       1 │
└────────────────────┴───────┴─────────┘

Totals:
  Files     : 2
  Tests     : 9
  Classes   : 1
  Avg/File  : 4.5
```

*Summary:*
```
Test Count Summary
  Files     : 2
  Tests     : 9
  Classes   : 1
  Avg/File  : 4.5
```

*JSON:*
```json
{
  "summary": {
    "total_files": 2,
    "total_tests": 9,
    "total_classes": 1,
    "average_tests_per_file": 4.5
  },
  "files": [...]
}
```

**See Also:**
- [Devtools Examples](../examples/devtools.md) - Detailed usage examples

### System Info (`system_info`)

System information and management commands.

#### `todo`

Launch an interactive terminal-based TODO application with task management, reminders, and desktop notifications.

**Usage:**
```bash
cli-utils local system_info todo
```

**Features:**
- Task management with categories
- Progress tracking (0-100%)
- Due date monitoring
- Multiple reminders per task
- Desktop notifications
- Background reminder daemon
- Smart lists (All, Upcoming, Past Due, Completed)

**Keyboard Shortcuts:**
- `n` - New task/category
- `e` - Edit selected item
- `d` - Delete selected item
- `Space` - Toggle task completion
- `r` - Manage task reminders
- `k` - Switch to categories view
- `t` - Switch to tasks view
- `q` - Quit application

**Examples:**
```bash
# Launch the TODO app
cli-utils local system_info todo

# The app opens in full-screen terminal mode with:
# - Left sidebar with smart lists and categories
# - Center panel with task list
# - Bottom input bar for quick task entry
# - Footer with keyboard shortcuts
```

**Reminder Service:**
```bash
# Install background reminder service (auto-start at login)
make install-todo-service

# Check service status
make check-todo-service

# Manually control service
systemctl --user status todo-reminder.service
systemctl --user start todo-reminder.service
systemctl --user stop todo-reminder.service

# View logs
journalctl --user -u todo-reminder.service -f
# Or
tail -f ~/.config/cli_utils/logs/reminder_daemon.log

# Uninstall service
make uninstall-todo-service
```

**Data Storage:**
- Database: `~/.config/cli_utils/todo.db`
- Logs: `~/.config/cli_utils/logs/reminder_daemon.log`

**Requirements:**
- **For notifications**: `libnotify-bin` package (provides `notify-send`)
  ```bash
  sudo apt install libnotify-bin
  ```

**See Also:**
- [TODO App Guide](../examples/todo-app.md) - Complete usage guide with examples
- [Makefile Reference](makefile.md) - Service installation commands

## Remote Commands

Commands that interact with external APIs.

### API Examples (`api_example`)

Example commands demonstrating API integration.

#### `weather`

Get weather information for a city.

**Usage:**
```bash
cli-utils remote api_example weather [OPTIONS] CITY
```

**Arguments:**
- `CITY` - City name (required). Supported: `mellieha`, `milan`, `paris`

**Options:**
- `--copy`, `-c` - Copy result to clipboard (formatted JSON)
- `--help` - Show help message

**Examples:**
```bash
# Get weather for Milan
cli-utils remote api_example weather milan

# Get weather and copy to clipboard
cli-utils remote api_example weather paris --copy

# Short form
cli-utils remote api_example weather mellieha -c
```

**Output:**
```python
{
  'latitude': 45.48,
  'longitude': 9.199999,
  'generationtime_ms': 0.004291534423828125,
  'utc_offset_seconds': 0,
  'timezone': 'GMT',
  'timezone_abbreviation': 'GMT',
  'elevation': 128.0
}
```

**Supported Cities:**
- `mellieha` - Mellieha, Malta (35.57°N, 14.21°E)
- `milan` - Milan, Italy (45.47°N, 9.19°E)
- `paris` - Paris, France (48.86°N, 2.35°E)

**API Used:**
- Open-Meteo API (https://api.open-meteo.com)
- No authentication required
- Free and open source

**See Also:**
- [API Commands Examples](../examples/api-commands.md) - API integration guide

## Global Commands

Commands available at the top level.

### `config`

Show current configuration.

**Usage:**
```bash
cli-utils config
```

**Output:**
Displays current configuration settings from `~/.config/cli-utils/config.yaml`.

### `version`

Show CLI Utils version.

**Usage:**
```bash
cli-utils version
```

**Output:**
```
CLI Utils version X.Y.Z
```

**Shell Alias:**
```bash
cuv  # Short form
```

## Common Patterns

### Using Browse Mode

Many commands support `--browse` / `-b` to interactively select directories:

```bash
# Browse for directory to analyze
cli-utils local devtools code-report --browse

# Browse for test directory
cli-utils local devtools count-tests -b
```

Requires one of these file managers:
- **yazi** (recommended)
- **mc** (Midnight Commander)
- **ranger**
- **lf**

Install with: `sudo apt install yazi` or `sudo apt install mc`

### Saving Output

Commands with `--output` / `-o` support saving to files:

```bash
# Direct file path
cli-utils local devtools code-report . -o report.txt

# Browse for save location
cli-utils local devtools code-report . -o browse

# Combines with format
cli-utils local devtools code-report . -f json -o metrics.json
```

Default filenames based on format:
- Text: `.txt`
- JSON: `.json`
- Markdown: `.md`

### Clipboard Integration

Commands with `--copy` / `-c` copy output to clipboard:

```bash
# Copy text transformation
textup --copy "hello"

# Copy API result
cli-utils remote api_example weather milan --copy
```

Requires clipboard tool:
- **Linux**: `xclip`, `xsel`, or `wl-clipboard`
- **macOS**: `pbcopy` (built-in)
- **Windows**: `clip` (built-in)
- **Fallback**: `pyperclip` Python package

### Combining Options

Most commands support multiple options together:

```bash
# Browse + recursive + JSON + save
cli-utils local devtools code-report -b -r -f json -o browse

# Browse + recursive + verbose + JSON + save
cli-utils local devtools count-tests -b -r -v -f json -o browse

# Multiple text transformations
echo "hello" | textup_pipe | tee uppercase.txt
```

## Getting Help

```bash
# General help
cli-utils --help

# Category help
cli-utils local --help
cli-utils remote --help

# Group help
cli-utils local text_utils --help
cli-utils local devtools --help

# Command help
cli-utils local text_utils uppercase --help
cli-utils local devtools code-report --help
```

## Next Steps

- [Examples](../examples/) - Detailed usage examples for each command
- [Quick Reference](quick-reference.md) - Cheat sheet for common operations
- [Adding Commands](../user-guide/adding-commands.md) - Create your own commands
