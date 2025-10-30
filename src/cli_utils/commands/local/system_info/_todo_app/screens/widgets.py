"""Reusable Textual widgets for the TODO app."""

from textual.app import ComposeResult
from textual.widgets import ListItem, Static

from cli_utils.utils.icons import Icons


class SmartListItem(ListItem):
    """A smart list item (All, Upcoming, Past, Completed)."""

    def __init__(self, smart_id: str, name: str, count: int = 0, icon: str | None = None) -> None:
        """
        Args:
            smart_id: Identifier for the smart list (all, upcoming, past, completed)
            name: The list name
            count: Number of tasks in this list
            icon: Emoji or icon for the list (defaults to Icons.list())
        """
        super().__init__()
        self.smart_id = smart_id
        self.list_name = name
        self.task_count = count
        self.icon = icon if icon is not None else Icons.list()

    def compose(self) -> ComposeResult:
        """Compose the list item contents."""
        yield Static(f"{self.icon} {self.list_name} [dim]({self.task_count})[/dim]")


class CategoryItem(ListItem):
    """A category list item."""

    def __init__(
        self,
        category_id: int,
        name: str,
        count: int = 0,
        icon: str | None = None,
        is_system: bool = False,
    ) -> None:
        """
        Args:
            category_id: Unique identifier for the category
            name: The category name
            count: Number of tasks in this category
            icon: Icon/emoji for the category (defaults to Icons.list())
            is_system: Whether this is a system category (cannot be edited/deleted)
        """
        super().__init__()
        self.category_id = category_id
        self.category_name = name
        self.task_count = count
        self.icon = icon if icon is not None else Icons.list()
        self.is_system = is_system

    def compose(self) -> ComposeResult:
        """Compose the category list item contents."""
        yield Static(f"{self.icon} {self.category_name} [dim]({self.task_count})[/dim]")


class TaskItem(ListItem):
    """A list item representing a task."""

    def __init__(
        self,
        task_id: int,
        text: str,
        timestamp: str,
        category_id: int | None = None,
        due_date: str | None = None,
        status: str = "todo",
        progress: int = 0,
        reminder_count: int = 0,
    ) -> None:
        """
        Args:
            task_id: Unique identifier for the task
            text: Task description
            timestamp: When the task was created
            category_id: ID of the category this task belongs to
            due_date: Optional due date (YYYY-MM-DD)
            status: Task status (todo, completed)
            progress: Task completion progress (0-100)
            reminder_count: Number of reminders set for this task
        """
        super().__init__()
        self.task_id = task_id
        self.task_text = text
        self.timestamp = timestamp
        self.category_id = category_id
        self.due_date = due_date
        self.status = status
        self.progress = progress
        self.reminder_count = reminder_count

    def compose(self) -> ComposeResult:
        """Compose the task list item contents."""
        # Build status indicator using Icons
        status_icons = {
            "new": Icons.circle(),
            "in_progress": Icons.play(),
            "completed": Icons.check()
        }
        status_icon = status_icons.get(self.status, Icons.circle())

        # Build the display text
        parts = [f"{status_icon} {self.task_text}"]

        # Add progress bar if task has progress > 0
        if self.progress > 0:
            # Create a simple text-based progress bar
            bar_length = 10
            filled = int(bar_length * self.progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            parts.append(f"[dim]{bar} {self.progress}%[/dim]")

        # Add due date if present
        if self.due_date:
            parts.append(f"[dim]{Icons.calendar()} {self.due_date}[/dim]")

        # Add reminder indicator if task has reminders
        if self.reminder_count > 0:
            parts.append(f"[dim]{Icons.clock()} {self.reminder_count}[/dim]")

        yield Static(" ".join(parts))
