#!/usr/bin/env python3
"""Migrate category icons from emoji to Nerd Font icons.

This script updates existing categories in the database to use Nerd Font icons
instead of emoji, while maintaining the fallback system.
"""

from pathlib import Path
from cli_utils.config import get_settings
from cli_utils.commands.local.system_info._todo_app.database import TodoDatabase
from cli_utils.utils.icons import icon

# Initialize settings to set up icon manager
get_settings()

# Connect to database
db_path = Path.home() / ".config" / "cli_utils" / "todo.db"
db = TodoDatabase(db_path)

# Icon mapping: emoji -> (nerd_font_name, emoji, text_fallback)
ICON_MIGRATIONS = {
    "👤": ("nf-md-account", "👤", "[USER]"),
    "💼": ("nf-md-briefcase", "💼", "[WORK]"),
    "📋": ("nf-md-format_list_bulleted", "📋", "[LIST]"),
    "✅": ("nf-md-check", "✅", "[DONE]"),
    "📁": ("nf-md-folder", "📁", "[FOLDER]"),
    "⭐": ("nf-md-star", "⭐", "[STAR]"),
    "🏷️": ("nf-md-tag", "🏷️", "[TAG]"),
}

print("=" * 60)
print("CATEGORY ICON MIGRATION")
print("=" * 60)
print()

categories = db.get_categories()

print(f"Found {len(categories)} categories")
print()

updated_count = 0
for cat in categories:
    old_icon = cat.icon

    # Check if this icon needs migration
    if old_icon in ICON_MIGRATIONS:
        nerd_name, emoji, fallback = ICON_MIGRATIONS[old_icon]
        new_icon = icon(nerd_name, emoji, fallback)

        print(f"Updating category '{cat.name}':")
        print(f"  Old icon: {old_icon} (code: {repr(old_icon)})")
        print(f"  New icon: {new_icon} (code: {repr(new_icon)})")

        # Update in database directly (bypassing is_system check for migration)
        import sqlite3
        with db._get_connection() as conn:
            conn.execute("""
                UPDATE categories
                SET icon = ?
                WHERE id = ?
            """, (new_icon, cat.id))
            conn.commit()
        updated_count += 1
    else:
        print(f"Skipping category '{cat.name}' (icon: {cat.icon}) - no migration needed")

print()
print("=" * 60)
print(f"Migration complete: {updated_count} categories updated")
print("=" * 60)

if updated_count > 0:
    print()
    print("Verification:")
    categories = db.get_categories()
    for cat in categories:
        print(f"  {cat.name}: {cat.icon} (code: {repr(cat.icon)})")
