"""Plugin loader for dynamically discovering and loading commands.

This module provides functionality to automatically discover and load command modules
from the commands directory, organizing them into groups (local/remote) and
sub-groups (text_utils, file_ops, etc.).
"""

import importlib
import inspect
from pathlib import Path
from typing import Any

import typer
from rich.console import Console

console = Console()


class PluginLoader:
    """Loads and registers commands from the commands directory.

    Attributes:
        commands_dir: Path to the commands directory
        app: Main Typer application instance
    """

    def __init__(self, commands_dir: Path, app: typer.Typer) -> None:
        """Initialize the plugin loader.

        Args:
            commands_dir: Path to the commands directory
            app: Main Typer application instance
        """
        self.commands_dir = commands_dir
        self.app = app
        self.loaded_commands: dict[str, int] = {}

    def load_all_commands(self) -> None:
        """Discover and load all commands from the commands directory.

        This method scans the commands directory structure:
        - commands/local/text_utils/*.py
        - commands/local/file_ops/*.py
        - commands/remote/api_example/*.py

        And automatically registers them with Typer.
        """
        if not self.commands_dir.exists():
            console.print(f"[yellow]Warning: Commands directory not found: {self.commands_dir}[/yellow]")
            return

        # Load commands from 'local' and 'remote' groups
        for category in ["local", "remote"]:
            category_path = self.commands_dir / category
            if category_path.exists() and category_path.is_dir():
                self._load_category(category, category_path)

        # Print summary
        total = sum(self.loaded_commands.values())
        if total > 0:
            console.print(f"[green]✓ Loaded {total} commands[/green]")

    def _load_category(self, category_name: str, category_path: Path) -> None:
        """Load all command groups from a category (local or remote).

        Args:
            category_name: Name of the category (e.g., 'local', 'remote')
            category_path: Path to the category directory
        """
        # Create a sub-app for this category
        category_app = typer.Typer(
            name=category_name,
            help=f"{category_name.capitalize()} commands",
            no_args_is_help=True,
        )

        command_count = 0

        # Iterate through command groups (subdirectories)
        for group_path in category_path.iterdir():
            if group_path.is_dir() and not group_path.name.startswith("_"):
                group_count = self._load_command_group(category_name, group_path, category_app)
                command_count += group_count

        # Only add the category if it has commands
        if command_count > 0:
            self.app.add_typer(category_app, name=category_name)
            self.loaded_commands[category_name] = command_count

    def _load_command_group(self, category_name: str, group_path: Path, parent_app: typer.Typer) -> int:
        """Load all commands from a command group directory.

        Args:
            category_name: Name of the category (e.g., 'local', 'remote')
            group_path: Path to the command group directory
            parent_app: Parent Typer application to register commands to

        Returns:
            Number of commands loaded from this group
        """
        group_name = group_path.name
        command_count = 0

        # Create a sub-app for this command group
        group_app = typer.Typer(
            name=group_name,
            help=f"{group_name.replace('_', ' ').title()} commands",
            no_args_is_help=True,
        )

        # Load all Python files in this group
        for py_file in group_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue

            try:
                # Import the module
                module_name = f"cli_utils.commands.{category_name}.{group_name}.{py_file.stem}"
                module = importlib.import_module(module_name)

                # Look for Typer commands in the module
                for _name, obj in inspect.getmembers(module):
                    if self._is_typer_command(obj):
                        # Register the command
                        group_app.command()(obj)
                        command_count += 1
                    elif isinstance(obj, typer.Typer):
                        # If the module exports a Typer app, add it
                        parent_app.add_typer(obj, name=py_file.stem)
                        command_count += 1

            except Exception as e:
                console.print(f"[red]Error loading {py_file}: {e}[/red]")

        # Only add the group if it has commands
        if command_count > 0:
            parent_app.add_typer(group_app, name=group_name)

        return command_count

    @staticmethod
    def _is_typer_command(obj: Any) -> bool:
        """Check if an object is a Typer command function.

        Args:
            obj: Object to check

        Returns:
            True if the object is a Typer command function
        """
        return (
            callable(obj)
            and not inspect.isclass(obj)
            and not obj.__name__.startswith("_")
            and inspect.isfunction(obj)
            and obj.__module__.startswith("cli_utils.commands")
        )


def create_plugin_loader(app: typer.Typer) -> PluginLoader:
    """Create and return a plugin loader instance.

    Args:
        app: Main Typer application instance

    Returns:
        Configured PluginLoader instance
    """
    # Get the commands directory path
    base_dir = Path(__file__).parent.parent
    commands_dir = base_dir / "commands"

    return PluginLoader(commands_dir, app)
