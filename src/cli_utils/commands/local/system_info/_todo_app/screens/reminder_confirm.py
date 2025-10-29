"""Confirmation screen for removing reminders when task is completed."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static


class ReminderConfirmScreen(ModalScreen):
    """Modal screen for confirming reminder removal on task completion."""

    CSS = """
    ReminderConfirmScreen {
        align: center middle;
    }

    #confirm-dialog {
        width: 50;
        height: auto;
        background: $panel;
        border: thick $primary;
        padding: 1 2;
    }

    #confirm-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $warning;
        padding: 0 0 1 0;
    }

    #confirm-message {
        width: 100%;
        padding: 1 0;
    }

    #confirm-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0 0 0;
    }

    #confirm-buttons Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        task_id: int,
        task_name: str,
        reminder_count: int,
        *args,
        **kwargs
    ):
        """Initialize the confirmation screen.

        Args:
            task_id: ID of the task being completed
            task_name: Name of the task
            reminder_count: Number of reminders to be removed
        """
        super().__init__(*args, **kwargs)
        self.task_id = task_id
        self.task_name = task_name
        self.reminder_count = reminder_count

    def compose(self) -> ComposeResult:
        """Create the confirmation dialog."""
        with Vertical(id="confirm-dialog"):
            yield Static("⚠️  Remove Reminders?", id="confirm-title")

            message = (
                f"Task '{self.task_name}' is being marked as completed.\n\n"
                f"This task has {self.reminder_count} reminder(s) scheduled.\n\n"
                "Do you want to remove the associated reminders?"
            )
            yield Label(message, id="confirm-message")

            with Vertical(id="confirm-buttons"):
                yield Button("Remove Reminders", variant="warning", id="btn-confirm")
                yield Button("Keep Reminders", variant="default", id="btn-keep")
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-confirm":
            # User confirmed - remove reminders
            self.dismiss(True)
        elif event.button.id == "btn-keep":
            # User wants to keep reminders - complete task but don't remove
            self.dismiss(False)
        elif event.button.id == "btn-cancel":
            # User cancelled - don't complete task
            self.dismiss(None)
