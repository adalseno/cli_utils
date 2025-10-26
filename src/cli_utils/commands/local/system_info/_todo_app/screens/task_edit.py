"""Task edit/create screen."""

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Static

if TYPE_CHECKING:
    from ..todo_app import TodoApp
    
class TaskEditScreen(ModalScreen):
    """Modal screen for editing or creating a task."""

    DEFAULT_CSS = """
    TaskEditScreen {
        align: center middle;
    }

    #edit-dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }

    #edit-title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        padding: 0 0 1 0;
    }

    .field-label {
        width: 15;
        padding: 1 1 0 0;
        text-align: right;
    }

    .field-input {
        width: 1fr;
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
        task_id: int | None = None,
        task_name: str = "",
        category_id: int = 1,
        status: str = "new",
        progress: int = 0,
        due_date: str | None = None,
    ) -> None:
        """Initialize the task edit screen.

        Args:
            task_id: ID of task being edited (None for new task)
            task_name: Current task name
            category_id: Current category ID
            status: Current task status
            progress: Current progress (0-100)
            due_date: Current due date (YYYY-MM-DD format)
        """
        super().__init__()
        self.task_id = task_id
        self.task_name = task_name
        self.category_id = category_id
        self.status = status
        self.progress = progress
        self.due_date = due_date or ""

    @property
    def todo_app(self) -> "TodoApp":
        """Return the app instance with proper typing."""
        return self.app  # type: ignore[return-value]
    
    def compose(self) -> ComposeResult:
        """Compose the edit dialog."""
        with Vertical(id="edit-dialog"):
            yield Static(
                "Edit Task" if self.task_id else "New Task",
                id="edit-title"
            )

            # Task name
            with Horizontal():
                yield Label("Name:", classes="field-label")
                yield Input(
                    value=self.task_name,
                    placeholder="Task name...",
                    id="task-name",
                    classes="field-input"
                )

            # Category
            with Horizontal():
                yield Label("Category:", classes="field-label")
                yield Select(
                    options=[("Loading...", 0)],  # Dummy option, will be populated in on_mount
                    id="task-category",
                    classes="field-input",
                    allow_blank=False
                )

            # Status
            with Horizontal():
                yield Label("Status:", classes="field-label")
                yield Select(
                    options=[
                        ("New", "new"),
                        ("In Progress", "in_progress"),
                        ("Completed", "completed"),
                    ],
                    value=self.status,
                    id="task-status",
                    classes="field-input"
                )

            # Progress
            with Horizontal():
                yield Label("Progress:", classes="field-label")
                yield Input(
                    value=str(self.progress),
                    placeholder="0-100",
                    id="task-progress",
                    classes="field-input"
                )

            # Due date
            with Horizontal():
                yield Label("Due Date:", classes="field-label")
                yield Input(
                    value=self.due_date,
                    placeholder="YYYY-MM-DD",
                    id="task-due-date",
                    classes="field-input"
                )

            # Buttons
            with Horizontal(id="button-container"):
                yield Button("Save", variant="primary", id="save-button")
                yield Button("Cancel", variant="default", id="cancel-button")

    def on_mount(self) -> None:
        """Populate category dropdown when mounted."""
        # Get categories from the app database
        categories = self.todo_app.db.get_categories()
        category_select = self.query_one("#task-category", Select)

        # Convert categories to Select options (label, value pairs)
        options = [(cat.name, cat.id) for cat in categories]

        # Set options first
        category_select.set_options(options)

        # Then set the value after options are populated
        try:
            category_select.value = self.category_id
        except Exception:
            # If category_id is invalid, select the first option
            if options:
                category_select.value = options[0][1]

        # Focus on name input
        self.query_one("#task-name", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save-button":
            self._save_task()
        elif event.button.id == "cancel-button":
            self.dismiss(None)

    def _save_task(self) -> None:
        """Validate and save the task."""
        # Get values from inputs
        name = self.query_one("#task-name", Input).value.strip()
        category_id = self.query_one("#task-category", Select).value
        status = self.query_one("#task-status", Select).value
        progress_str = self.query_one("#task-progress", Input).value.strip()
        due_date = self.query_one("#task-due-date", Input).value.strip()

        # Validate
        if not name:
            # TODO: Show error message
            return

        # Validate progress
        try:
            progress = int(progress_str) if progress_str else 0
            if progress < 0 or progress > 100:
                # TODO: Show error message
                return
        except ValueError:
            # TODO: Show error message
            return

        # Validate due date format if provided
        if due_date:
            try:
                from datetime import datetime
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                # TODO: Show error message
                return

        # Return the task data (status will be auto-synced in database layer)
        task_data = {
            "task_id": self.task_id,  # Will be None for new tasks
            "name": name,
            "category_id": category_id,
            "status": status,
            "progress": progress,
            "due_date": due_date if due_date else None,
        }

        self.dismiss(task_data)
