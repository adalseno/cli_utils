"""Reminders management screen."""

from typing import TYPE_CHECKING, Optional

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Input, Label, Static

from .dtwidgets import DateTimeInput

if TYPE_CHECKING:
    from ..todo_app import TodoApp


class RemindersScreen(ModalScreen):
    """Modal screen for managing task reminders."""

    DEFAULT_CSS = """
    RemindersScreen {
        align: center middle;
    }

    #reminders-dialog {
        width: 70;
        height: auto;
        max-height: 80%;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }

    #reminders-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }

    #task-name-display {
        width: 100%;
        content-align: center middle;
        padding: 0 0 1 0;
        color: $text-muted;
    }

    #reminders-table {
        width: 100%;
        height: auto;
        max-height: 20;
    }

    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0 0 0;
    }

    #button-container Button {
        margin: 0 1;
    }

    #action-buttons {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0;
    }

    #action-buttons Button {
        margin: 0 1;
    }
    """

    def __init__(self, task_id: int, task_name: str) -> None:
        """Initialize the reminders screen.

        Args:
            task_id: ID of the task to manage reminders for
            task_name: Name of the task (for display)
        """
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name

    @property
    def todo_app(self) -> "TodoApp":
        """Return the app instance with proper typing."""
        return self.app  # type: ignore[return-value]

    def compose(self) -> ComposeResult:
        """Compose the reminders dialog."""
        with Vertical(id="reminders-dialog"):
            yield Static("Manage Reminders", id="reminders-title")
            yield Static(f"Task: {self.task_name}", id="task-name-display")

            # Reminders table
            with VerticalScroll():
                yield DataTable(id="reminders-table", cursor_type="row")

            # Action buttons
            with Horizontal(id="action-buttons"):
                yield Button("Add Reminder ➕", variant="success", id="add-reminder")
                yield Button("Edit ✏️", variant="primary", id="edit-reminder")
                yield Button("Delete 🗑️", variant="error", id="delete-reminder")

            # Close button
            with Horizontal(id="button-container"):
                yield Button("Close", variant="default", id="close-button")

    def on_mount(self) -> None:
        """Populate reminders table when mounted."""
        self._refresh_reminders_table()

    def _refresh_reminders_table(self) -> None:
        """Refresh the reminders table with current data."""
        table = self.query_one("#reminders-table", DataTable)
        table.clear(columns=True)

        # Add columns
        table.add_column("ID", key="id", width=8)
        table.add_column("Reminder Date/Time", key="datetime", width=50)

        # Get reminders from database
        reminders = self.todo_app.db.get_reminders(self.task_id)

        # Add rows
        for reminder in reminders:
            table.add_row(
                str(reminder.id),
                reminder.reminder_datetime,
                key=str(reminder.id)
            )

        # Update button states
        self._update_button_states()

    def _update_button_states(self) -> None:
        """Enable/disable edit and delete buttons based on selection."""
        table = self.query_one("#reminders-table", DataTable)
        has_selection = table.cursor_row >= 0 and len(table.rows) > 0

        edit_btn = self.query_one("#edit-reminder", Button)
        delete_btn = self.query_one("#delete-reminder", Button)

        edit_btn.disabled = not has_selection
        delete_btn.disabled = not has_selection

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in the reminders table."""
        self._update_button_states()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "close-button":
            self.dismiss(None)
        elif event.button.id == "add-reminder":
            self._add_reminder()
        elif event.button.id == "edit-reminder":
            self._edit_reminder()
        elif event.button.id == "delete-reminder":
            self._delete_reminder()

    def _add_reminder(self) -> None:
        """Open dialog to add a new reminder."""
        self.app.push_screen(
            ReminderEditScreen(task_id=self.task_id),
            self._handle_reminder_edit_result
        )

    def _edit_reminder(self) -> None:
        """Open dialog to edit selected reminder."""
        table = self.query_one("#reminders-table", DataTable)
        if table.cursor_row < 0:
            return

        # Get selected reminder ID
        row_key = table.get_row_at(table.cursor_row)[0]
        reminder_id = int(row_key)

        # Get reminder data
        reminders = self.todo_app.db.get_reminders(self.task_id)
        reminder = next((r for r in reminders if r.id == reminder_id), None)
        if not reminder:
            return

        # Open edit dialog
        self.app.push_screen(
            ReminderEditScreen(
                task_id=self.task_id,
                reminder_id=reminder.id,
                reminder_datetime=reminder.reminder_datetime
            ),
            self._handle_reminder_edit_result
        )

    def _handle_reminder_edit_result(self, result: bool | None) -> None:
        """Handle result from reminder edit screen.

        Args:
            result: True if reminder was saved, None if cancelled
        """
        if result:
            # Refresh table after adding/editing
            self._refresh_reminders_table()

    def _delete_reminder(self) -> None:
        """Delete the selected reminder."""
        table = self.query_one("#reminders-table", DataTable)
        if table.cursor_row < 0:
            return

        # Get selected reminder ID from the row key
        try:
            row_key = table.get_row_at(table.cursor_row)[0]
            reminder_id = int(row_key)

            # Delete from database
            self.todo_app.db.delete_reminder(reminder_id)

            # Refresh table
            self._refresh_reminders_table()
        except (IndexError, ValueError):
            # Row not found or invalid ID
            pass


class ReminderEditScreen(ModalScreen):
    """Modal screen for adding or editing a reminder."""

    DEFAULT_CSS = """
    ReminderEditScreen {
        align: center middle;
    }

    #reminder-edit-dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }

    #reminder-edit-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }

    #button-container {
        width: 100%;
        height: auto;
        align: center middle;
        padding: 1 0 0 0;
    }

    #button-container Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        task_id: int,
        reminder_id: Optional[int] = None,
        reminder_datetime: str = ""
    ) -> None:
        """Initialize the reminder edit screen.

        Args:
            task_id: ID of the task this reminder belongs to
            reminder_id: ID of reminder being edited (None for new reminder)
            reminder_datetime: Current reminder datetime (for editing)
        """
        super().__init__()
        self.task_id = task_id
        self.reminder_id = reminder_id
        self.reminder_datetime = reminder_datetime

    @property
    def todo_app(self) -> "TodoApp":
        """Return the app instance with proper typing."""
        return self.app  # type: ignore[return-value]

    def compose(self) -> ComposeResult:
        """Compose the reminder edit dialog."""
        with Vertical(id="reminder-edit-dialog"):
            yield Static(
                "Edit Reminder" if self.reminder_id else "Add Reminder",
                id="reminder-edit-title"
            )

            # Reminder datetime
            yield DateTimeInput(
                label="Reminder Date/Time:",
                value=self.reminder_datetime,
                input_id="reminder-datetime",
                input_classes="field-input"
            )

            # Buttons
            with Horizontal(id="button-container"):
                yield Button("Save", variant="primary", id="save-button")
                yield Button("Cancel", variant="default", id="cancel-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-button":
            self._save_reminder()
        elif event.button.id == "cancel-button":
            self.dismiss(None)

    def _save_reminder(self) -> None:
        """Validate and save the reminder."""
        # Get datetime value
        datetime_input = self.query_one("#reminder-datetime", Input)
        reminder_datetime = datetime_input.value.strip()

        # Validate
        if not reminder_datetime:
            # TODO: Show error message
            return

        # Validate datetime format
        try:
            from datetime import datetime
            datetime.strptime(reminder_datetime, "%Y-%m-%d %H:%M")
        except ValueError:
            # TODO: Show error message
            return

        # Save to database
        if self.reminder_id is None:
            # Add new reminder
            self.todo_app.db.add_reminder(self.task_id, reminder_datetime)
        else:
            # Update existing reminder
            self.todo_app.db.update_reminder(self.reminder_id, reminder_datetime)

        self.dismiss(True)
