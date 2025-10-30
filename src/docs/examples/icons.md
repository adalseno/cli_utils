# Icon System Guide

This guide explains how to use the intelligent icon system in CLI Utils, which provides automatic Nerd Font detection with smart fallback support.

## Overview

CLI Utils includes a sophisticated icon system that automatically adapts to your terminal's capabilities:

```
┌─────────────────────────────────────┐
│   Icon Selection Priority           │
├─────────────────────────────────────┤
│ 1. Nerd Font Icons (if installed)  │
│    └─> Best visual quality         │
│                                      │
│ 2. Emoji Characters                │
│    └─> Good for modern terminals    │
│                                      │
│ 3. Text Representation              │
│    └─> Works everywhere             │
└─────────────────────────────────────┘
```

This ensures your commands work beautifully on any system, regardless of font or terminal configuration!

## Quick Start

### Basic Usage

The simplest way to use icons is through the `Icons` class:

```python
from cli_utils.utils.icons import Icons
from rich.console import Console

console = Console()

def show_task_status():
    """Display task status with icons."""
    console.print(f"{Icons.check()} Task completed successfully")
    console.print(f"{Icons.cross()} Operation failed")
    console.print(f"{Icons.warning()} Please review this item")
    console.print(f"{Icons.info()} Additional information available")
```

**Output (with Nerd Fonts):**
```
󰄬 Task completed successfully
󰅖 Operation failed
󰀪 Please review this item
󰋽 Additional information available
```

**Output (with emoji fallback):**
```
✅ Task completed successfully
❌ Operation failed
⚠️  Please review this item
ℹ️  Additional information available
```

**Output (text fallback):**
```
[✓] Task completed successfully
[✗] Operation failed
[!] Please review this item
[i] Additional information available
```

## Available Predefined Icons

### Status Icons

```python
from cli_utils.utils.icons import Icons

# Success/completion
Icons.check()      # ✅ / 󰄬 / [✓]
Icons.cross()      # ❌ / 󰅖 / [✗]
Icons.circle()     # ⭕ / 󰄰 / [ ]
Icons.play()       # ▶️  / 󰐊 / [>]
```

### Time and Calendar

```python
Icons.calendar()   # 📅 / 󰃮 / [DATE]
Icons.clock()      # ⏰ / 󰥔 / [TIME]
```

### File System

```python
Icons.folder()     # 📁 / 󰉋 / [FOLDER]
Icons.file()       # 📄 / 󰈙 / [FILE]
Icons.list()       # 📋 / 󰉹 / [LIST]
```

### Information

```python
Icons.info()       # ℹ️  / 󰋽 / [i]
Icons.warning()    # ⚠️  / 󰀪 / [!]
Icons.star()       # ⭐ / 󰓎 / [*]
Icons.tag()        # 🏷️  / 󰓹 / [TAG]
```

## Custom Icons

For icons not in the predefined set, use the `icon()` function:

```python
from cli_utils.utils.icons import icon

def deployment_status():
    """Show deployment with custom icons."""
    rocket = icon("nf-md-rocket", "🚀", "[LAUNCH]")
    console.print(f"{rocket} Deploying to production...")

    package = icon("nf-md-package", "📦", "[PKG]")
    console.print(f"{package} Building package...")

    cloud = icon("nf-md-cloud_upload", "☁️", "[UPLOAD]")
    console.print(f"{cloud} Uploading to cloud...")
```

### Finding Nerd Font Icon Names

Nerd Font icons follow the pattern `nf-{family}-{name}`:

- Material Design: `nf-md-{name}` (e.g., `nf-md-check`, `nf-md-rocket`)
- Font Awesome: `nf-fa-{name}` (e.g., `nf-fa-github`, `nf-fa-home`)
- Devicons: `nf-dev-{name}` (e.g., `nf-dev-python`, `nf-dev-javascript`)
- Octicons: `nf-oct-{name}` (e.g., `nf-oct-mark_github`)

**Resources:**
- [Nerd Fonts Cheat Sheet](https://www.nerdfonts.com/cheat-sheet)
- [Material Design Icons](https://pictogrammers.com/library/mdi/)

## Real-World Examples

### Example 1: TODO App Task Display

```python
from cli_utils.utils.icons import Icons

class TaskDisplay:
    """Display tasks with appropriate status icons."""

    def show_task(self, task_name: str, status: str, due_date: str = None, has_reminder: bool = False):
        # Map status to icons
        status_icons = {
            "new": Icons.circle(),
            "in_progress": Icons.play(),
            "completed": Icons.check(),
        }

        icon = status_icons.get(status, Icons.circle())
        parts = [f"{icon} {task_name}"]

        # Add metadata with icons
        if due_date:
            parts.append(f"{Icons.calendar()} {due_date}")

        if has_reminder:
            parts.append(f"{Icons.clock()} Reminder set")

        console.print(" ".join(parts))


# Usage
display = TaskDisplay()
display.show_task("Buy groceries", "new", "2025-11-01", True)
display.show_task("Write report", "in_progress", "2025-10-30")
display.show_task("Call dentist", "completed")
```

**Output (with Nerd Fonts):**
```
󰄰 Buy groceries 󰃮 2025-11-01 󰥔 Reminder set
󰐊 Write report 󰃮 2025-10-30
󰄬 Call dentist
```

### Example 2: File Operations with Icons

```python
from pathlib import Path
from cli_utils.utils.icons import Icons, icon

def show_directory_tree(path: Path, max_depth: int = 2):
    """Display directory structure with icons."""

    def scan_directory(dir_path: Path, depth: int = 0):
        if depth > max_depth:
            return

        indent = "  " * depth

        for item in sorted(dir_path.iterdir()):
            if item.is_dir():
                console.print(f"{indent}{Icons.folder()} {item.name}/")
                scan_directory(item, depth + 1)
            else:
                # Different icons based on file type
                if item.suffix == ".py":
                    file_icon = icon("nf-dev-python", "🐍", "[PY]")
                elif item.suffix == ".md":
                    file_icon = icon("nf-md-language_markdown", "📝", "[MD]")
                elif item.suffix == ".json":
                    file_icon = icon("nf-md-code_json", "📊", "[JSON]")
                else:
                    file_icon = Icons.file()

                console.print(f"{indent}{file_icon} {item.name}")

    scan_directory(path)
```

### Example 3: Build Status Report

```python
from cli_utils.utils.icons import Icons, icon

def build_report(tests_passed: int, tests_failed: int, warnings: int):
    """Generate a build report with icons."""
    console.print("\n[bold]Build Report[/bold]")
    console.print("─" * 40)

    # Tests
    if tests_failed == 0:
        console.print(f"{Icons.check()} All tests passed ({tests_passed})")
    else:
        console.print(f"{Icons.cross()} {tests_failed} tests failed")
        console.print(f"{Icons.info()} {tests_passed} tests passed")

    # Warnings
    if warnings > 0:
        console.print(f"{Icons.warning()} {warnings} warnings")

    # Overall status
    if tests_failed == 0 and warnings == 0:
        success = icon("nf-md-check_circle", "✅", "[SUCCESS]")
        console.print(f"\n{success} Build successful!")
    else:
        failure = icon("nf-md-alert_circle", "❌", "[FAILED]")
        console.print(f"\n{failure} Build completed with issues")


# Usage
build_report(tests_passed=42, tests_failed=0, warnings=3)
```

## Advanced Usage

### Checking Icon Support

You can check what icon system is being used:

```python
from cli_utils.utils.icons import get_icon_manager

def check_icon_support():
    """Display current icon support level."""
    manager = get_icon_manager()

    if manager._nerd_font_support == 1:
        console.print("[green]󰄬 Nerd Fonts are available![/green]")
        console.print("You're getting the best visual experience!")
    elif manager._terminal_supports_emoji:
        console.print("[yellow]Using emoji icons[/yellow]")
        console.print("Nerd Fonts not detected, but emoji work fine!")
    else:
        console.print("[dim]Using text icons[/dim]")
        console.print("For better icons, install Nerd Fonts!")
```

### Dynamic Icon Selection

```python
from cli_utils.utils.icons import icon

def get_priority_icon(priority: str) -> str:
    """Get icon based on priority level."""
    priority_map = {
        "critical": icon("nf-md-alert", "🔴", "[!!!]"),
        "high": icon("nf-md-chevron_double_up", "⬆️", "[HIGH]"),
        "medium": icon("nf-md-minus", "➖", "[MED]"),
        "low": icon("nf-md-chevron_down", "⬇️", "[LOW]"),
    }
    return priority_map.get(priority, Icons.info())


def show_task(name: str, priority: str):
    """Display task with priority icon."""
    priority_icon = get_priority_icon(priority)
    console.print(f"{priority_icon} {name}")


# Usage
show_task("Fix critical bug", "critical")
show_task("Update documentation", "low")
```

## Testing with Icons

### Unit Testing

When writing tests for commands that use icons, you can control the icon behavior:

```python
import pytest
from cli_utils.utils.icons import IconManager

def test_task_display_with_nerd_fonts():
    """Test task display with Nerd Fonts enabled."""
    # Create manager with Nerd Fonts enabled
    manager = IconManager(nerd_font_support=1)

    # Your test logic here
    icon_str = manager.icon("nf-md-check", "✅", "[DONE]")
    assert icon_str != "[DONE]"  # Should use Nerd Font or emoji


def test_task_display_without_nerd_fonts():
    """Test task display with Nerd Fonts disabled."""
    # Create manager with Nerd Fonts disabled
    manager = IconManager(nerd_font_support=0)

    # Your test logic here
    icon_str = manager.icon("nf-md-check", "✅", "[DONE]")
    # Will use emoji or text fallback
    assert icon_str in ["✅", "[DONE]"]
```

### Integration Testing

For integration tests, the icon system will use whatever is configured in your test environment:

```python
def test_build_report_output(capsys):
    """Test that build report produces output."""
    from myapp.build import build_report

    build_report(tests_passed=10, tests_failed=0, warnings=2)

    captured = capsys.readouterr()
    # Should contain "tests passed" regardless of icon system
    assert "tests passed" in captured.out.lower()
```

## Configuration

### Checking Nerd Font Status

Use the Makefile target to check if Nerd Fonts are installed:

```bash
make check-nerdfonts
```

This will show:
- Whether Nerd Fonts are detected
- List of installed Nerd Fonts
- Instructions for installation if needed

### Manual Configuration

The icon system configuration is stored in `~/.config/cli_utils/config.yaml`:

```yaml
display:
  nerd_font_support: 1  # 1 = enabled, 0 = disabled
```

To force disable Nerd Fonts (useful for testing text fallback):

```yaml
display:
  nerd_font_support: 0
```

### Migrating Existing Data

If you have an existing TODO app database with emoji icons, you can migrate them to Nerd Fonts:

```bash
# Migrate all category icons from emoji to Nerd Fonts
make migrate-icons
```

**What it does:**
- Scans all categories in the TODO app database
- Replaces emoji icons (👤, 💼, 📋, etc.) with Nerd Font equivalents
- Preserves category names, descriptions, and other data
- Works on both system and custom categories

**When to use:**
- After upgrading to a version with the icon system
- When you first install Nerd Fonts and want existing categories to use them
- If you manually edited the database and want to restore Nerd Font icons

## Installing Nerd Fonts

For the best visual experience, install Nerd Fonts:

### Quick Installation

1. **Download a Nerd Font:**
   - Visit [Nerd Fonts Downloads](https://www.nerdfonts.com/font-downloads)
   - Popular choices: FiraCode, JetBrainsMono, Hack, Meslo

2. **Install the font:**
   - **Linux:** Copy `.ttf` files to `~/.local/share/fonts/` and run `fc-cache -fv`
   - **macOS:** Double-click the font file and click "Install Font"
   - **Windows:** Right-click the font file and select "Install"

3. **Configure your terminal:**
   - Set your terminal to use the Nerd Font you installed
   - Restart the terminal

4. **Verify installation:**
   ```bash
   make check-nerdfonts
   ```

### Popular Nerd Fonts

| Font | Best For | Features |
|------|----------|----------|
| **FiraCode** | General coding | Programming ligatures |
| **JetBrainsMono** | IDEs | Designed for long coding sessions |
| **Hack** | Small screens | Excellent readability |
| **Meslo** | Consistency | Based on Apple's Menlo |

## Best Practices

### 1. Always Use Predefined Icons When Available

```python
# ✅ Good - Uses predefined icon
from cli_utils.utils.icons import Icons
console.print(f"{Icons.check()} Done")

# ❌ Bad - Hardcoded emoji
console.print("✅ Done")
```

### 2. Provide Good Fallbacks

```python
# ✅ Good - Clear text fallback
icon("nf-md-rocket", "🚀", "[LAUNCH]")

# ❌ Bad - Unclear fallback
icon("nf-md-rocket", "🚀", "[R]")
```

### 3. Use Icons Consistently

```python
# ✅ Good - Consistent icon usage for same concept
status_icons = {
    "pending": Icons.circle(),
    "running": Icons.play(),
    "done": Icons.check(),
}

# ❌ Bad - Mixing different icon types
# Using Icons.circle() sometimes, hardcoded "○" other times
```

### 4. Don't Overuse Icons

```python
# ✅ Good - Icons add clarity
console.print(f"{Icons.check()} Build successful")
console.print(f"{Icons.warning()} 3 warnings found")

# ❌ Bad - Too many icons
console.print(f"{Icons.folder()} Processing {Icons.file()} files in {Icons.folder()} directory...")
```

## Troubleshooting

### Icons Not Displaying

**Problem:** Icons show as boxes or question marks

**Solution:**
1. Install a Nerd Font
2. Configure your terminal to use it
3. Run `make check-nerdfonts` to verify

### Emoji Not Working

**Problem:** Emoji show as `??` or boxes

**Solution:**
- Update your terminal emulator
- Try a modern terminal: kitty, wezterm, alacritty, iTerm2

### Want to Force Text Mode

**Problem:** Need plain text output (e.g., for CI/CD logs)

**Solution:**
Edit `~/.config/cli_utils/config.yaml`:
```yaml
display:
  nerd_font_support: 0
```

## See Also

- [Configuration Guide](../user-guide/configuration.md) - Icon system configuration
- [Common Utilities](../user-guide/common-utilities.md) - Other utilities
- [TODO App](todo-app.md) - Real-world icon usage example
