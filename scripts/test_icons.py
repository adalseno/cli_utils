#!/usr/bin/env python3
"""Test icon rendering to verify Nerd Font support."""

from cli_utils.config import get_settings
from cli_utils.utils.icons import Icons, get_icon_manager

# Initialize settings
settings = get_settings()
manager = get_icon_manager()

print("=" * 60)
print("ICON SYSTEM DIAGNOSTIC")
print("=" * 60)
print()

print("Configuration:")
print(f"  Config dir: {settings.config_dir}")
print(f"  Nerd Font support (detected): {settings.nerd_font_support}")
print(f"  Icon manager initialized: {manager is not None}")
print(f"  Icon manager Nerd Font support: {manager._nerd_font_support}")
print()

print("Icon Rendering Test:")
print("-" * 60)

icons_test = [
    ("Check (completed)", Icons.check(), "✅", ""),
    ("Cross (failed)", Icons.cross(), "❌", ""),
    ("Circle (new)", Icons.circle(), "⭕", ""),
    ("Play (in progress)", Icons.play(), "▶️", ""),
    ("Calendar (due date)", Icons.calendar(), "📅", ""),
    ("Clock (reminder)", Icons.clock(), "⏰", ""),
]

for name, icon_result, emoji, nerd in icons_test:
    code = repr(icon_result)
    print(f"  {name:25} {icon_result}  (code: {code})")

print()
print("-" * 60)
print("What you should see:")
print()
if settings.nerd_font_support == 1:
    print("  ✓ If Nerd Fonts are working:")
    print("    You should see special glyphs (like , , )")
    print("    NOT emoji (✅ ❌ ⭕)")
    print()
    print("  ✗ If you see emoji instead:")
    print("    1. Your terminal might not be using a Nerd Font")
    print("    2. Check your terminal font settings")
    print("    3. Install and select a Nerd Font (FiraCode NF, JetBrainsMono NF, etc.)")
else:
    print("  Nerd Fonts not detected on system")
    print("  Falling back to emoji")
    print("  Run 'make check-nerdfonts' for installation instructions")

print()
print("=" * 60)
