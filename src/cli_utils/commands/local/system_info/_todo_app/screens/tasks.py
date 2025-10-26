from typing import TYPE_CHECKING

from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.widgets import Input, ListView, Static

from .widgets import TaskItem

if TYPE_CHECKING:
    from ..todo_app import TodoApp

class TaskView(Vertical):
    """Main task list view."""

    BINDINGS = [
        ("n", "new_task", "New"),
        ("e", "edit_task", "Edit"),
        ("d", "delete_task", "Delete"),
        ("space", "toggle_task", "Toggle"),
        ("escape", "cancel_input", "Cancel"),
    ]

    @property
    def todo_app(self) -> "TodoApp":
        """Return the app instance with proper typing."""
        return self.app  # type: ignore[return-value]
    
    class TasksLoaded(Message):
        """Message sent when tasks need to be loaded."""
        def __init__(self, filter_type: str = "all", filter_id: int | None = None) -> None:
            super().__init__()
            self.filter_type = filter_type
            self.filter_id = filter_id

    def compose(self):
        yield Static("All Tasks", id="tasks-header")
        yield VerticalScroll(ListView(id="task-list"), id="tasks-container")
        yield Horizontal(Input(placeholder="Add a new task...", id="task-input"), id="input-container")

    def on_mount(self) -> None:
        """Load tasks when the view is mounted."""
        # Delay loading until after layout is calculated
        self.call_after_refresh(self.load_tasks)

    def load_tasks(self, filter_type: str = "all", filter_id: int | None = None) -> None:
        """Load tasks from database based on filter.

        Args:
            filter_type: Type of filter ('all', 'upcoming', 'past', 'completed', 'category')
            filter_id: Category ID if filter_type is 'category'
        """
        task_list = self.query_one("#task-list", ListView)
        task_list.clear()

        db = self.todo_app.db

        # Update header based on filter
        header = self.query_one("#tasks-header", Static)

        if filter_type == "all":
            tasks = db.get_tasks(status=None)
            header.update("All Tasks")
        elif filter_type == "upcoming":
            # Get tasks with due dates in the future
            from datetime import datetime
            tasks = [t for t in db.get_tasks() if t.due_date and t.due_date >= datetime.now().date().isoformat()]
            header.update("📅 Upcoming Tasks")
        elif filter_type == "past":
            # Get tasks with past due dates
            from datetime import datetime
            tasks = [t for t in db.get_tasks() if t.due_date and t.due_date < datetime.now().date().isoformat()]
            header.update("📆 Past Due Tasks")
        elif filter_type == "completed":
            tasks = db.get_tasks(status="completed")
            header.update("✅ Completed Tasks")
        elif filter_type == "category" and filter_id is not None:
            tasks = db.get_tasks(category_id=filter_id)
            # Get category name
            categories = db.get_categories()
            cat_name = next((c.name for c in categories if c.id == filter_id), "Category")
            header.update(f"📋 {cat_name}")
        else:
            tasks = []

        # Add tasks to the list
        for task in tasks:
            task_item = TaskItem(
                task_id=task.id,
                text=task.name,
                timestamp=task.created_at[:10],  # Just the date part
                category_id=task.category_id,
                due_date=task.due_date,
                status=task.status
            )
            # Add progress attribute
            task_item.progress = task.progress
            task_list.append(task_item)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle task input submission - opens edit screen with pre-filled name."""
        if event.input.id == "task-input":
            task_text = event.value.strip()
            if task_text:
                # Determine which category to use
                category_id = 1  # default
                if self.todo_app.current_view.startswith("category_"):
                    # Extract category ID from current view
                    try:
                        category_id = int(self.todo_app.current_view.split("_")[1])
                    except (ValueError, IndexError):
                        category_id = 1

                # Open edit screen with pre-filled task name
                from .task_edit import TaskEditScreen
                screen = TaskEditScreen(
                    task_name=task_text,
                    category_id=category_id
                )

                # Clear input
                event.input.value = ""
                event.input.blur()

                # Open the edit screen
                self.todo_app.push_screen(screen, self.todo_app._handle_task_edit_result)

    def action_edit_task(self) -> None:
        """Proxy to app's edit action."""
        self.todo_app.action_edit_item()

    def action_delete_task(self) -> None:
        """Proxy to app's delete action."""
        self.todo_app.action_delete_item()

    def action_toggle_task(self) -> None:
        """Proxy to app's toggle action."""
        self.todo_app.action_toggle_task()

    def action_cancel_input(self) -> None:
        """Cancel input and clear editing state."""
        task_input = self.query_one("#task-input", Input)
        if task_input.has_focus:
            task_input.value = ""
            task_input.blur()
            self.todo_app.editing_task_id = None

    def action_new_task(self) -> None:
        """Create a new task via edit screen."""
        self.todo_app._open_task_edit_screen()
