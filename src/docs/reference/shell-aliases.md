# Shell Aliases and Shortcuts

This guide shows how to create convenient shell shortcuts for frequently used CLI Utils commands.

## Quick Setup

### Automatic Installation

```bash
# Add aliases to your shell configuration
make install-aliases
```

This will add a source line to your `~/.zshrc` that loads the aliases.

### Manual Installation

Add this line to your `~/.zshrc`:

```bash
# CLI Utils shortcuts
source /path/to/cli_utils/scripts/shell-aliases.sh
```

Then reload your shell:

```bash
source ~/.zshrc
```

## Available Shortcuts

### Text Utilities

| Shortcut | Command | Example | Output |
|----------|---------|---------|--------|
| `textup` | uppercase | `textup "hello"` | `HELLO` |
| `textlow` | lowercase | `textlow "HELLO"` | `hello` |
| `texttitle` | titlecase | `texttitle "hello world"` | `Hello World` |
| `textupc` | uppercase + copy | `textupc "hello"` | `HELLO` (+ clipboard) |
| `textlowc` | lowercase + copy | `textlowc "HELLO"` | `hello` (+ clipboard) |

### General Shortcuts

| Shortcut | Expands To | Example |
|----------|------------|---------|
| `cu` | `cli-utils` | `cu --help` |
| `cul` | `cli-utils local` | `cul text_utils uppercase test` |
| `cur` | `cli-utils remote` | `cur api fetch` |
| `cuv` | `cli-utils version` | `cuv` |
| `cuc` | `cli-utils config` | `cuc` |

### Pipe-Friendly Functions

| Function | Description | Example |
|----------|-------------|---------|
| `textup_pipe` | Uppercase from stdin or args | `echo "hello" \| textup_pipe` |
| `textlow_pipe` | Lowercase from stdin or args | `cat file.txt \| textlow_pipe` |

## Usage Examples

### Basic Text Conversion

```bash
# Uppercase
textup "hello world"
# Output: HELLO WORLD

# Lowercase
textlow "HELLO WORLD"
# Output: hello world

# Title case
texttitle "hello world"
# Output: Hello World
```

### With Clipboard

```bash
# Convert and copy to clipboard (requires pyperclip)
textupc "important text"
# Output: IMPORTANT TEXT
# (Also copied to clipboard)
```

### Using Shortcuts

```bash
# Instead of: cli-utils --help
cu --help

# Instead of: cli-utils version
cuv

# Instead of: cli-utils local text_utils uppercase "test"
cul text_utils uppercase "test"
```

### Pipe Usage

```bash
# Convert stdin to uppercase
echo "hello" | textup_pipe
# Output: HELLO

# Convert file contents
cat myfile.txt | textlow_pipe

# Chain commands
cat file.txt | textlow_pipe | grep "search term"
```

### Real-World Examples

```bash
# Convert filename to lowercase
NEW_NAME=$(textlow "MY_FILE.TXT")
mv "MY_FILE.TXT" "$NEW_NAME"

# Uppercase git branch name
BRANCH=$(git branch --show-current | textup_pipe)
echo "Current branch (uppercase): $BRANCH"

# Title case for headers
echo "processing results" | texttitle
# Output: Processing Results

# Multiple arguments
textup one two three
# Output: ONE (only first arg, use quotes for multiple words)

textup "one two three"
# Output: ONE TWO THREE (correct)
```

## Custom Aliases

You can add your own aliases to `~/.zshrc`:

### Simple Alias

```bash
# Simple command alias
alias mycommand='cli-utils local text_utils uppercase'

# Usage
mycommand "hello"
```

### Function with Logic

```bash
# Function with default value
textup_default() {
    if [ $# -eq 0 ]; then
        echo "Usage: textup_default <text>"
        return 1
    fi
    cli-utils local text_utils uppercase "$@"
}

# Function with multiple operations
text_process() {
    local text="$1"
    echo "Original: $text"
    echo "Uppercase: $(textup "$text")"
    echo "Lowercase: $(textlow "$text")"
    echo "Titlecase: $(texttitle "$text")"
}

# Usage
text_process "Hello World"
```

### Advanced: Combine with Other Tools

```bash
# Uppercase clipboard content (Linux with xclip)
clip_upper() {
    xclip -o -selection clipboard | textup_pipe | xclip -selection clipboard
}

# Uppercase clipboard content (macOS)
clip_upper() {
    pbpaste | textup_pipe | pbcopy
}

# Convert and save to file
text_upper_save() {
    textup "$1" > output.txt
    echo "Saved to output.txt"
}
```

## Zsh-Specific Features

### Global Aliases (Zsh Only)

```bash
# Add to ~/.zshrc
alias -g TUP='| textup_pipe'
alias -g TLOW='| textlow_pipe'
alias -g TTITLE='| texttitle_pipe'

# Usage - can be used anywhere in the command line
echo "hello" TUP
# Same as: echo "hello" | textup_pipe

cat file.txt TLOW
# Same as: cat file.txt | textlow_pipe
```

### Suffix Aliases (Zsh Only)

```bash
# Automatically process .upper files
alias -s upper=textup

# Usage
# Create file: echo "hello" > test.upper
# Run: ./test.upper
# (Will automatically run through textup)
```

## Tips & Tricks

### 1. Tab Completion

With aliases, you can still use tab completion:

```bash
cu <TAB>          # Shows cli-utils commands
cul <TAB>         # Shows local commands
textup <TAB>      # Tab completes arguments if configured
```

### 2. Command History

Aliases appear in your shell history:

```bash
history | grep textup
# Shows all textup commands you've run
```

### 3. Combining with Find

```bash
# Uppercase all .txt filenames
find . -name "*.txt" -exec bash -c 'textup "$(basename {})"' \;

# Convert text in multiple files
for file in *.txt; do
    cat "$file" | textup_pipe > "${file}.upper"
done
```

### 4. Environment Variables

```bash
# Store transformed text in variables
UPPER=$(textup "hello world")
echo $UPPER
# Output: HELLO WORLD
```

## Troubleshooting

### Aliases Not Found

**Problem:** `textup: command not found`

**Solution:**
```bash
# Check if aliases are loaded
type textup

# Reload shell configuration
source ~/.zshrc

# Verify the source line is in ~/.zshrc
grep "shell-aliases.sh" ~/.zshrc
```

### Function Not Working with Pipes

**Problem:** Pipe doesn't work with regular functions

**Solution:** Use the `_pipe` variants:
```bash
# Wrong
echo "hello" | textup
# Output: (might not work correctly)

# Correct
echo "hello" | textup_pipe
# Output: HELLO
```

### Path Issues

**Problem:** Aliases work, but commands don't execute

**Solution:**
```bash
# Check if cli-utils is in PATH
which cli-utils

# If not, use full path in aliases
textup() {
    ~/bin/cli-utils local text_utils uppercase "$@"
}
```

## Performance

Shell functions add minimal overhead:

- **Direct command**: ~50ms
- **Via alias/function**: ~50ms (same, just shell parsing)
- **Via pipe function**: ~100ms (extra stdin processing)

For most use cases, the difference is negligible.

## Uninstalling

To remove the aliases:

```bash
# Remove the source line from ~/.zshrc
# Then reload
source ~/.zshrc
```

Or temporarily disable:

```bash
# Unset specific functions
unset -f textup
unset -f textlow

# Unalias
unalias cu
```

## See Also

- [Installation Guide](../getting-started/installation.md) - Installation guide
- [README.md](../README.md) - Project overview
- [scripts/shell-aliases.sh](../scripts/shell-aliases.sh) - Alias definitions
