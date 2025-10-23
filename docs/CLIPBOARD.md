# Clipboard Support in CLI Utils

✅ **Status**: Fully working with xclip, xsel, and wl-clipboard!

## Understanding Linux Clipboards

Linux has multiple clipboard mechanisms, which can be confusing:

### X11 Clipboards

1. **PRIMARY** - Selection clipboard (middle-click paste)
   - Content: Whatever you select with mouse
   - Paste: Middle mouse button
   - Tools: `xclip`, `xsel`

2. **CLIPBOARD** - Standard clipboard (Ctrl+C/V)
   - Content: Explicitly copied with Ctrl+C
   - Paste: Ctrl+V (or Ctrl+Shift+V in terminals)
   - Tools: `xclip -selection clipboard`, `xsel --clipboard`

3. **SECONDARY** - Rarely used

### Wayland Clipboard

- Simpler: One clipboard
- Tool: `wl-clipboard` (`wl-copy` / `wl-paste`)

## How CLI Utils Handles Clipboard

The `--copy` flag attempts to copy in this order:

1. **Wayland**: `wl-copy` (if on Wayland)
2. **X11**: `xclip -selection clipboard` ✅
3. **X11**: `xsel --clipboard --input` ✅
4. **Fallback**: `pyperclip` (Python package)

The implementation uses `subprocess.Popen` to run clipboard tools in the background,
since xclip and xsel stay running to serve clipboard requests (this is normal behavior).

## Current Limitations

### SSH/Remote Sessions

**Problem**: X clipboard tools require a display server.

**Symptoms**:
```bash
cli-utils local text_utils uppercase "test" --copy
# Output: Warning: No display available (SSH/headless session)
```

**Solutions**:
- Use SSH with X forwarding: `ssh -X user@host`
- Copy output manually: `cli-utils local text_utils uppercase "test" | xclip -selection clipboard`
- Use without `--copy`: `cli-utils local text_utils uppercase "test"`

### Terminal Clipboard vs X Clipboard

**Problem**: Terminal emulators often have their own clipboard.

**Example**:
```bash
echo "test" | xclip -selection clipboard
# Then try Ctrl+Shift+V in terminal - might not work!
# But works in GUI apps (browser, editor, etc.)
```

**Why**: Some terminals use GTK/Qt clipboard, not X clipboard directly.

**Solution**: Use the output directly instead:
```bash
# Instead of copying, save to variable
RESULT=$(cli-utils local text_utils uppercase "hello")
echo $RESULT
```

## Working Examples

### 1. Using --copy Flag (Recommended!)

```bash
# Copy to clipboard automatically
cli-utils local text_utils uppercase "hello world" --copy
# ✓ Copied to clipboard (xclip)

# Verify it worked
xclip -selection clipboard -o
# Output: HELLO WORLD

# Now paste in GUI apps with Ctrl+V
```

### 2. Using Shell Shortcuts

```bash
# With shortcuts (after make install-aliases)
textup "hello world" --copy
textlow "HELLO WORLD" --copy
texttitle "hello world" --copy
```

### 3. Manual Clipboard (Alternative)

```bash
# Pipe to xclip yourself
cli-utils local text_utils uppercase "hello world" | xclip -selection clipboard
```

### 3. Variables (Best for Scripts)

```bash
# Capture in variable
UPPER=$(cli-utils local text_utils uppercase "hello world")
echo "Result: $UPPER"

# Use in scripts
process_text() {
    local result=$(cli-utils local text_utils uppercase "$1")
    echo "$result" > output.txt
}
```

### 4. Piping (Most Flexible)

```bash
# Chain commands
cli-utils local text_utils uppercase "hello" | grep "HELLO"

# Save to file
cli-utils local text_utils uppercase "hello" > output.txt

# Both display and save
cli-utils local text_utils uppercase "hello" | tee output.txt
```

## Testing Your Clipboard Setup

### Check Display

```bash
echo $DISPLAY
# Should show something like :0 or :1
# If empty, clipboard won't work
```

### Test xclip

```bash
# Copy
echo "test" | xclip -selection clipboard

# Paste (to verify)
xclip -selection clipboard -o
# Should output: test

# Try in GUI app
# Open browser/editor and press Ctrl+V
```

### Test wl-clipboard (Wayland)

```bash
# Copy
echo "test" | wl-copy

# Paste (to verify)
wl-paste
# Should output: test
```

## Installation

### Ubuntu/Debian

```bash
# X11
sudo apt install xclip
# or
sudo apt install xsel

# Wayland
sudo apt install wl-clipboard
```

### Fedora

```bash
# X11
sudo dnf install xclip xsel

# Wayland
sudo dnf install wl-clipboard
```

### Arch

```bash
# X11
sudo pacman -S xclip xsel

# Wayland
sudo pacman -S wl-clipboard
```

## Recommended Approach

For most use cases, **don't use `--copy`**. Instead:

### For Terminal Use

```bash
# Just view the output
textup "hello world"

# Save to variable
RESULT=$(textup "hello world")
```

### For GUI Use

```bash
# Output and manually copy
textup "hello world"
# Then select with mouse and copy

# Or pipe to xclip
textup "hello world" | xclip -selection clipboard
```

### For Scripts

```bash
#!/bin/bash
# Process and save
result=$(cli-utils local text_utils uppercase "$input")
echo "$result" > output.txt

# Or use directly
cli-utils local text_utils uppercase "$input" | some-other-command
```

## Alternative: Custom Clipboard Function

Add to your `~/.zshrc`:

```bash
# Copy command output to clipboard
cup() {
    "$@" | xclip -selection clipboard
    echo "Copied to clipboard!"
}

# Usage
cup textup "hello world"
cup cli-utils local text_utils uppercase "test"
```

Or for Wayland:

```bash
cup() {
    "$@" | wl-copy
    echo "Copied to clipboard!"
}
```

## Troubleshooting

### "No clipboard tool found"

**Solution**: Install xclip
```bash
sudo apt install xclip
```

### "No display available"

**Cause**: SSH session without X forwarding

**Solutions**:
1. Use SSH with X forwarding: `ssh -X user@host`
2. Don't use `--copy` flag
3. Pipe output manually: `... | xclip -selection clipboard`

### Clipboard works but paste doesn't

**Cause**: Terminal using different clipboard mechanism

**Test**:
```bash
# Copy with xclip
echo "test" | xclip -selection clipboard

# Try pasting in:
# - GUI app (browser, text editor) - should work
# - Terminal with Ctrl+Shift+V - might not work
```

**Solution**: Use GUI apps or pipe output directly

### xclip hangs/times out

**Cause**: No X display or display not accessible

**Check**:
```bash
echo $DISPLAY
xdpyinfo
```

## Best Practices

1. ✅ **Use output directly** - Most reliable
2. ✅ **Save to variables** - For scripts
3. ✅ **Pipe to files** - For persistence
4. ⚠️ **Use `--copy` sparingly** - Environment-dependent
5. ⚠️ **Test your clipboard** - Before relying on it

## Summary

The `--copy` flag is a convenience feature that works best in GUI environments. For most CLI use cases, piping, variables, or manual copying are more reliable.

**Recommended workflow**:
```bash
# Quick view
textup "hello"

# Use in script
RESULT=$(textup "hello")

# Save to file
textup "hello" > output.txt

# Manual copy (most reliable)
textup "hello"
# Then select and Ctrl+Shift+C
```
