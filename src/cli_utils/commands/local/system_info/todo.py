"""Simple TODO app command.

This module provides the command entry point for the TODO app.
The actual Textual application is in todo_app.py.
"""

from cli_utils.commands.local.system_info._todo_app.todo_app import TodoApp


def todo() -> None:
    """Launch the Textual TODO interface."""
    TodoApp().run()
