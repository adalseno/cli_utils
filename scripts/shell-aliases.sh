#!/bin/bash
# Shell aliases and functions for CLI Utils
# Source this file in your ~/.zshrc or ~/.bashrc:
#   source /path/to/cli_utils/scripts/shell-aliases.sh

# ============================================================================
# Text Utilities Shortcuts
# ============================================================================

# Convert text to uppercase
textup() {
    cli-utils local text_utils uppercase "$@"
}

# Convert text to lowercase
textlow() {
    cli-utils local text_utils lowercase "$@"
}

# Convert text to title case
texttitle() {
    cli-utils local text_utils titlecase "$@"
}

# ============================================================================
# Advanced Text Utilities with Options
# ============================================================================

# Uppercase and copy to clipboard (requires xclip/xsel/wl-clipboard)
textupc() {
    cli-utils local text_utils uppercase --copy "$@"
}

# Lowercase and copy to clipboard (requires xclip/xsel/wl-clipboard)
textlowc() {
    cli-utils local text_utils lowercase --copy "$@"
}

# Titlecase and copy to clipboard (requires xclip/xsel/wl-clipboard)
texttitlec() {
    cli-utils local text_utils titlecase --copy "$@"
}

# ============================================================================
# CLI Utils Shortcuts
# ============================================================================

# Quick access to CLI utils
alias cu='cli-utils'

# Local commands shortcut
alias cul='cli-utils local'

# Remote commands shortcut (when implemented)
alias cur='cli-utils remote'

# Show CLI version
alias cuv='cli-utils version'

# Show CLI config
alias cuc='cli-utils config'

# ============================================================================
# Pipe-Friendly Functions
# ============================================================================

# Read from stdin if no arguments provided
textup_pipe() {
    if [ $# -eq 0 ]; then
        # Read from stdin
        while IFS= read -r line; do
            cli-utils local text_utils uppercase "$line"
        done
    else
        # Use arguments
        cli-utils local text_utils uppercase "$@"
    fi
}

textlow_pipe() {
    if [ $# -eq 0 ]; then
        while IFS= read -r line; do
            cli-utils local text_utils lowercase "$line"
        done
    else
        cli-utils local text_utils lowercase "$@"
    fi
}

# ============================================================================
# Usage Examples
# ============================================================================
#
# Basic usage:
#   textup "hello world"           → HELLO WORLD
#   textlow "HELLO WORLD"          → hello world
#   texttitle "hello world"        → Hello World
#
# With clipboard (requires xclip, xsel, or wl-clipboard):
#   textupc "hello world"          → HELLO WORLD (and copies to clipboard)
#   textlowc "HELLO"               → hello (and copies to clipboard)
#   texttitlec "hello"             → Hello (and copies to clipboard)
#
# Shortcuts:
#   cu --help                      → cli-utils --help
#   cul text_utils uppercase test → cli-utils local text_utils uppercase test
#   cuv                            → cli-utils version
#
# Pipe usage:
#   echo "hello" | textup_pipe     → HELLO
#   cat file.txt | textlow_pipe    → converts each line to lowercase
#
# ============================================================================

# Optional: Enable autocompletion for shortcuts
# (uncomment if you have shell completion installed)
# complete -F _cli_utils_completion cu
# complete -F _cli_utils_completion cul
# complete -F _cli_utils_completion cur
