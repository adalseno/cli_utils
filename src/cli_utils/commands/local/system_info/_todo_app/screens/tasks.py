from typing import TYPE_CHECKING

from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import DescendantFocus, DescendantBlur
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
        ("r", "manage_reminders", "Reminders"),
        ("k", "show_categories", "Categories"),
        Binding("escape", "cancel_input", "Cancel", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_focused = False

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
            # Get reminder count for this task
            reminder_count = db.get_reminder_count(task.id)

            task_item = TaskItem(
                task_id=task.id,
                text=task.name,
                timestamp=task.created_at[:10],  # Just the date part
                category_id=task.category_id,
                due_date=task.due_date,
                status=task.status,
                reminder_count=reminder_count
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

    def action_manage_reminders(self) -> None:
        """Open reminders management for selected task."""
        task_list = self.query_one("#task-list", ListView)
        if task_list.index is not None:
            selected_item = task_list.highlighted_child
            if selected_item and isinstance(selected_item, TaskItem):
                # Open RemindersScreen with callback
                from .reminders import RemindersScreen
                self.app.push_screen(
                    RemindersScreen(
                        task_id=selected_item.task_id,
                        task_name=selected_item.task_text
                    ),
                    self._handle_reminders_closed
                )

    def _handle_reminders_closed(self, result: None) -> None:
        """Handle when reminders screen is closed.

        Args:
            result: Always None for reminders screen
        """
        # Refresh the task list to update reminder count
        if self.todo_app.current_view.startswith("category_"):
            cat_id = int(self.todo_app.current_view.split("_")[1])
            self.load_tasks("category", cat_id)
        else:
            self.load_tasks(self.todo_app.current_view)

    def action_show_categories(self) -> None:
        """Switch to categories view."""
        self.todo_app.action_show_categories()

    # TODO: Fix escape binding visibility - it should show in footer when input is focused
    # Current implementation doesn't display the binding despite check_action returning True
    # Consider alternative approaches: custom footer, direct binding manipulation, or Textual updates
    def on_descendant_focus(self, event: DescendantFocus) -> None:
        """Track when input is focused to show escape binding."""
        if isinstance(event.widget, Input) and event.widget.id == "task-input":
            self._input_focused = True
            self.app.refresh_bindings()

    def on_descendant_blur(self, event: DescendantBlur) -> None:
        """Track when input loses focus to hide escape binding."""
        if isinstance(event.widget, Input) and event.widget.id == "task-input":
            self._input_focused = False
            self.app.refresh_bindings()

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        """Check if an action is currently available."""
        if action == "cancel_input":
            # Only show/enable cancel_input when input is focused
            return self._input_focused if self._input_focused else None
        return True
