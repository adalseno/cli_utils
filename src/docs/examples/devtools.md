# Devtools Examples

The devtools group provides commands for analyzing and reporting on Python codebases.

## Code Report

Analyze Python files in a directory and generate reports with code metrics.

## Count Tests

Count test functions in Python test files and get a summary of test coverage.

### Basic Usage

Analyze the current directory:

```bash
cli-utils local devtools code-report .
```

Output:
```
├── analyze_file.py          (  150 lines, 2 classes, 3 functions, 8 methods, 15.2% of total)
    - FileAnalyzer: 5 methods
    - CodeMetrics: 3 methods
├── gather_reports.py        (  120 lines, 1 classes, 5 functions, 4 methods, 12.1% of total)
    - ReportGatherer: 4 methods
└── utils.py                 (  200 lines, 3 classes, 2 functions, 10 methods, 20.2% of total)
    - TextFormatter: 4 methods
    - JsonFormatter: 3 methods
    - MarkdownFormatter: 3 methods

Total:
  Files     : 3
  Lines     : 470
  Classes   : 6
  Functions : 10
  Methods   : 22
```

### Analyze Specific Directory

```bash
cli-utils local devtools code-report src/cli_utils
```

### Recursive Analysis

Search subdirectories recursively:

```bash
cli-utils local devtools code-report . --recursive
# or use the short flag
cli-utils local devtools code-report . -r
```

### Interactive Directory Selection

Use the `--browse` flag to select a directory interactively using your terminal file manager (Yazi or Midnight Commander):

```bash
# Browse for directory using file manager
cli-utils local devtools code-report --browse

# Browse and analyze recursively
cli-utils local devtools code-report --browse --recursive

# Browse and output as JSON
cli-utils local devtools code-report --browse --format json

# Short flags
cli-utils local devtools code-report -b -r -f json
```

The command will:
1. Auto-detect available file managers (tries Yazi first, then Midnight Commander, Ranger, or lf)
2. Open the file manager starting at the current directory (or specified directory)
3. Let you navigate and select a directory
4. Analyze the selected directory

Supported file managers:
- **Yazi** (preferred) - Modern, fast terminal file manager
- **Midnight Commander (mc)** - Classic dual-pane file manager
- **Ranger** - Vim-like file manager
- **lf** - Simple terminal file manager

### Output Formats

#### JSON Format

Get structured JSON output for programmatic use:

```bash
cli-utils local devtools code-report . --format json
```

Output:
```json
{
  "total_files": 3,
  "total_lines": 470,
  "total_classes": 6,
  "total_functions": 10,
  "total_methods": 22,
  "files": [
    {
      "file": "analyze_file.py",
      "path": "/home/user/project/analyze_file.py",
      "lines": 150,
      "classes": 2,
      "functions": 3,
      "methods": 8,
      "percent": 15.2,
      "class_methods": {
        "FileAnalyzer": 5,
        "CodeMetrics": 3
      }
    }
  ]
}
```

#### Markdown Format

Generate markdown tables for documentation:

```bash
cli-utils local devtools code-report . --format markdown
```

Output:
```markdown
| File | Lines | Classes | Functions | Methods | % of Total |
|------|-------|---------|-----------|---------|------------|
| `analyze_file.py` | 150 | 2 | 3 | 8 | 15.2% |
| `gather_reports.py` | 120 | 1 | 5 | 4 | 12.1% |
| `utils.py` | 200 | 3 | 2 | 10 | 20.2% |

**Total:**
- Files: 3
- Lines: 470
- Classes: 6
- Functions: 10
- Methods: 22
```

### Saving Output to File

Save the report to a file instead of printing to the console:

```bash
# Save to a specific file path
cli-utils local devtools code-report . --output report.txt

# Save JSON output
cli-utils local devtools code-report . --format json --output metrics.json

# Save markdown report
cli-utils local devtools code-report . --format markdown --output code-metrics.md
```

#### Interactive File Save with Browse

Use `browse` as the output value to select the save location interactively with your file manager:

```bash
# Browse for save location (will suggest appropriate extension based on format)
cli-utils local devtools code-report . --output browse

# Browse for directory to analyze AND save location
cli-utils local devtools code-report --browse --format json --output browse

# Short flags
cli-utils local devtools code-report -b -f json -o browse
```

When you use `--output browse`, the file manager will open and let you navigate to the directory where you want to save the file. The default filename will be set based on the format:
- `code_report.txt` for text format
- `code_report.json` for JSON format
- `code_report.md` for markdown format

You can navigate to your desired directory and press Enter to save with the default filename, or you can also rename the file manually after saving.

### Short Flags

Use short flags for convenience:

```bash
# Recursive with JSON output
cli-utils local devtools code-report . -r -f json

# Markdown format
cli-utils local devtools code-report src -f markdown

# Browse interactively with recursive analysis
cli-utils local devtools code-report -b -r

# Browse with JSON output
cli-utils local devtools code-report -b -f json

# Save output to file with short flag
cli-utils local devtools code-report . -o report.txt
```

## Use Cases

### Project Overview

Get a quick overview of your project structure:

```bash
cli-utils local devtools code-report . --recursive
```

### Compare Directories

Compare code metrics between different parts of your project:

```bash
# Analyze source code
cli-utils local devtools code-report src --recursive

# Analyze tests
cli-utils local devtools code-report tests --recursive
```

### Generate Documentation

Create markdown reports for project documentation:

```bash
# Using output redirection
cli-utils local devtools code-report src --format markdown > docs/code-metrics.md

# Using --output flag (recommended)
cli-utils local devtools code-report src --format markdown --output docs/code-metrics.md

# Interactive selection
cli-utils local devtools code-report src --format markdown --output browse
```

### CI/CD Integration

Use JSON output in CI/CD pipelines:

```bash
# Generate metrics report using output redirection
cli-utils local devtools code-report . -r -f json > metrics.json

# Generate metrics report using --output flag (recommended)
cli-utils local devtools code-report . -r -f json --output metrics.json

# Parse with jq
cat metrics.json | jq '.total_lines'
```

### Code Review

Identify large files or complex modules:

```bash
# Get JSON output
cli-utils local devtools code-report src -r -f json | \
  jq '.files[] | select(.lines > 200) | {file: .file, lines: .lines}'
```

### Pre-commit Hook

Add code metrics to your pre-commit hooks:

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Generating code metrics..."
cli-utils local devtools code-report src --recursive
```

## What's Analyzed

The code report analyzes:

- **Lines**: Meaningful lines (excluding blank lines and comments)
- **Classes**: Number of class definitions
- **Functions**: Standalone functions (not methods)
- **Methods**: Functions defined inside classes
- **Class Methods**: Breakdown of methods per class
- **Percentage**: Each file's contribution to total line count

## Metrics Explained

### Meaningful Lines

The tool counts only meaningful lines of code, excluding:
- Blank lines
- Comment-only lines (starting with `#`)

### Functions vs Methods

- **Functions**: Top-level functions or functions outside classes
- **Methods**: Functions defined inside class bodies

### Class Method Breakdown

For each class, the report shows how many methods it contains:

```
├── utils.py                 (  200 lines, 3 classes, 2 functions, 10 methods, 20.2% of total)
    - TextFormatter: 4 methods
    - JsonFormatter: 3 methods
    - MarkdownFormatter: 3 methods
```

## Tips

- Use `--recursive` to analyze entire project trees
- JSON format is great for automation and scripting
- Markdown format is perfect for documentation
- Combine with shell tools like `jq` for advanced filtering
- Add to your Makefile for quick project statistics
- Use `--browse` for quick interactive directory selection without typing paths
- The file manager integration works great over SSH connections

## Count Tests

The `count-tests` command scans test files and counts test functions and classes.

### Basic Usage

Count tests in a directory:

```bash
cli-utils local devtools count-tests tests
```

Output:
```
                  Test Count Summary
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━┓
┃ File                             ┃ Tests ┃ Classes ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━┩
│ test_commands/test_text_utils.py │     4 │       0 │
│ test_core/test_config.py         │     4 │       0 │
└──────────────────────────────────┴───────┴─────────┘

Totals:
  Files     : 2
  Tests     : 8
  Classes   : 0
  Avg/File  : 4.0
```

### Recursive Scanning

Search subdirectories recursively:

```bash
cli-utils local devtools count-tests tests --recursive
# Short flag
cli-utils local devtools count-tests tests -r
```

### Verbose Mode

Show individual test function names:

```bash
cli-utils local devtools count-tests tests -r -v
```

Output includes test names:
```
Test Functions by File:

test_commands/test_text_utils.py
  • test_uppercase_function
  • test_lowercase_function
  • test_titlecase_function
  • test_uppercase_cli
```

### Custom File Pattern

Match different test file naming conventions:

```bash
# Default pattern: test_*.py
cli-utils local devtools count-tests tests

# Match *_test.py files
cli-utils local devtools count-tests tests -p "*_test.py"

# Match both patterns (use shell expansion)
cli-utils local devtools count-tests tests -p "**/*test*.py"
```

### Interactive Directory Selection

Use the `--browse` flag with file manager:

```bash
# Browse for test directory
cli-utils local devtools count-tests --browse

# Browse and scan recursively
cli-utils local devtools count-tests -b -r

# Browse with verbose output
cli-utils local devtools count-tests -b -r -v
```

### Output Formats

#### Table Format (Default)

```bash
cli-utils local devtools count-tests tests -r
```

#### Summary Format

Compact summary without the table:

```bash
cli-utils local devtools count-tests tests -r -f summary
```

Output:
```
Test Count Summary
  Files     : 2
  Tests     : 8
  Classes   : 0
  Avg/File  : 4.0
```

#### JSON Format

For programmatic use:

```bash
cli-utils local devtools count-tests tests -r -f json
```

Output:
```json
{
  "summary": {
    "total_files": 2,
    "total_tests": 8,
    "total_classes": 0,
    "average_tests_per_file": 4.0
  },
  "files": [
    {
      "file": "test_commands/test_text_utils.py",
      "path": "/path/to/test_text_utils.py",
      "tests": 4,
      "classes": 0,
      "test_names": [
        "test_uppercase_function",
        "test_lowercase_function",
        "test_titlecase_function",
        "test_uppercase_cli"
      ],
      "class_names": []
    }
  ]
}
```

### Saving Output to File

Save the test count report to a file:

```bash
# Save to a specific file path
cli-utils local devtools count-tests tests --output test_report.txt

# Save JSON output
cli-utils local devtools count-tests tests -r --format json --output test-report.json

# Save summary format
cli-utils local devtools count-tests tests -r --format summary --output summary.txt
```

#### Interactive File Save with Browse

Use `browse` as the output value to select the save location interactively:

```bash
# Browse for save location (will suggest appropriate extension based on format)
cli-utils local devtools count-tests tests --output browse

# Browse for directory to analyze AND save location
cli-utils local devtools count-tests --browse -r --format json --output browse

# Short flags
cli-utils local devtools count-tests -b -r -f json -o browse
```

When you use `--output browse`, the file manager will open and let you navigate to the directory where you want to save the file. The default filename will be set based on the format:
- `test_count.txt` for table and summary formats
- `test_count.json` for JSON format

### Use Cases

#### CI/CD Integration

Check test coverage in CI:

```bash
# Get test count as JSON using output redirection
cli-utils local devtools count-tests tests -r -f json > test-report.json

# Get test count as JSON using --output flag (recommended)
cli-utils local devtools count-tests tests -r -f json --output test-report.json

# Parse with jq
TOTAL_TESTS=$(cat test-report.json | jq '.summary.total_tests')
echo "Total tests: $TOTAL_TESTS"
```

#### Pre-commit Hook

Ensure tests are added:

```bash
#!/bin/bash
# .git/hooks/pre-commit

TEST_COUNT=$(cli-utils local devtools count-tests tests -r -f json | jq '.summary.total_tests')
if [ "$TEST_COUNT" -lt 1 ]; then
    echo "Error: No tests found!"
    exit 1
fi
```

#### Compare Test Coverage

Track test growth over time:

```bash
# Before changes (using output redirection)
cli-utils local devtools count-tests tests -r -f summary > before.txt

# Before changes (using --output flag, recommended)
cli-utils local devtools count-tests tests -r -f summary --output before.txt

# After changes
cli-utils local devtools count-tests tests -r -f summary --output after.txt

# Compare
diff before.txt after.txt
```

## Example: Add to Makefile

```makefile
.PHONY: code-metrics
code-metrics:
	@echo "Generating code metrics..."
	@cli-utils local devtools code-report src --recursive

.PHONY: code-metrics-json
code-metrics-json:
	@echo "Generating code metrics JSON..."
	@cli-utils local devtools code-report src -r -f json --output metrics.json
	@echo "Metrics saved to metrics.json"

.PHONY: code-metrics-md
code-metrics-md:
	@echo "Generating code metrics markdown..."
	@cli-utils local devtools code-report src -r -f markdown --output docs/code-metrics.md
	@echo "Metrics saved to docs/code-metrics.md"

.PHONY: test-count
test-count:
	@echo "Counting tests..."
	@cli-utils local devtools count-tests tests --recursive

.PHONY: test-count-verbose
test-count-verbose:
	@cli-utils local devtools count-tests tests -r -v

.PHONY: test-count-json
test-count-json:
	@echo "Generating test count JSON..."
	@cli-utils local devtools count-tests tests -r -f json --output test-report.json
	@echo "Test report saved to test-report.json"
```

Then use:
```bash
make code-metrics          # Display metrics in console
make code-metrics-json     # Save metrics as JSON
make code-metrics-md       # Save metrics as markdown
make test-count            # Display test count in console
make test-count-verbose    # Display with test names
make test-count-json       # Save test count as JSON
```
