from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, ListView, Static

from .database import TodoDatabase
from .screens.categories import CategoryView
from .screens.task_edit import TaskEditScreen
from .screens.tasks import TaskView
from .screens.widgets import CategoryItem, SmartListItem, TaskItem


class TodoApp(App):
    """Main Textual App with persistent sidebar and dynamic content area."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        """Initialize the app.

        Args:
            db_path: Path to the database file. If None, uses ~/.config/cli_utils/todo.db
        """
        super().__init__()

        # Initialize database
        if db_path is None:
            db_path = Path.home() / ".config" / "cli_utils" / "todo.db"
        self.db = TodoDatabase(db_path)

        # UI state
        self.smart_list: list[SmartListItem] = []
        self.categories: list[CategoryItem] = []
        self.current_view: str = "all"  # all, upcoming, past, completed, or category_<id>
        self.editing_task_id: int | None = None
        self.editing_category_id: int | None = None
        self.category_mode: bool = False  # When True, we're managing categories

        # Initialize UI lists
        self._init_default_lists()
        
    def build_smart_list(self) -> None:
        """Build smart list items with task counts from database."""
        smart_items = [
            ("all", "All", "📝"),
            ("upcoming", "Upcoming", "📅"),
            ("past", "Past", "📆"),
            ("completed", "Completed", "✅"),
        ]
        for smart_id, name, icon in smart_items:
            count = self._get_smart_list_count(smart_id)
            self.smart_list.append(SmartListItem(smart_id, name, count, icon))

        
        

    def build_default_categories(self) -> None:
        """Load categories from database."""
        categories = self.db.get_categories()
        for cat in categories:
            count = self.db.get_category_task_count(cat.id)
            self.categories.append(
                CategoryItem(cat.id, cat.name, count, cat.icon, cat.is_system)
            )
            
    def _init_default_lists(self) -> None:
        """Initialize smart lists and categories from database."""
        self.build_smart_list()
        self.build_default_categories()

    def _get_smart_list_count(self, smart_id: str) -> int:
        """Get count for smart lists from database.

        Args:
            smart_id: ID of the smart list ('all', 'upcoming', 'past', 'completed')

        Returns:
            Count of tasks matching the criteria
        """
        if smart_id == "all":
            return self.db.get_task_count(status=None)
        elif smart_id == "upcoming":
            return self.db.get_task_count(due_filter="upcoming")
        elif smart_id == "past":
            return self.db.get_task_count(due_filter="past")
        elif smart_id == "completed":
            return self.db.get_task_count(status="completed")
        return 0

    CSS_PATH = "todo_app.tcss"

    # Static bindings - always available
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Compose global layout."""
        yield Header()
        with Horizontal(id="body"):
            # Sidebar placeholder container
            yield Container(id="sidebar")
            with Container(id="content"):
                yield TaskView(id="task-view")
                yield CategoryView(id="category-view")
        yield Footer()

    

    def on_mount(self) -> None:
        """Start with the task view visible."""
        self.query_one("#task-view").display = True
        self.query_one("#category-view").display = False
        sidebar = self.query_one("#sidebar")
        # Mount them inside the sidebar
        smart_list = ListView(*self.smart_list, id="smart-list")
        category_list = VerticalScroll(ListView(*self.categories, id="category-list-bar"), id="category-list-bar-container")

        sidebar.mount_all([
            Label("Smart Lists", id="smart-list-title"),
            smart_list,
            Label("Categories", id="category-list-title"),
            category_list,
])
        

    def action_show_categories(self) -> None:
        """Switch to category view."""
        task_view = self.query_one("#task-view")
        category_view = self.query_one("#category-view", CategoryView)

        task_view.display = False
        category_view.display = True

        # Reload categories
        category_view.load_categories()

        # Set focus to the categories list to activate view bindings
        category_list = self.query_one("#categories-list-view", ListView)
        category_list.focus()

    def action_show_tasks(self) -> None:
        """Switch back to task view."""
        task_view = self.query_one("#task-view", TaskView)
        category_view = self.query_one("#category-view")

        task_view.display = True
        category_view.display = False

        # Reload tasks with current filter
        if self.current_view.startswith("category_"):
            cat_id = int(self.current_view.split("_")[1])
            task_view.load_tasks("category", cat_id)
        else:
            task_view.load_tasks(self.current_view)

        # Set focus to the task list to activate view bindings
        task_list = self.query_one("#task-list", ListView)
        task_list.focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selection in any ListView."""
        # Check if it's a smart list item
        if isinstance(event.item, SmartListItem):
            self.current_view = event.item.smart_id
            # Switch to task view and load filtered tasks
            self.action_show_tasks()
            self.query_one(TaskView).load_tasks(self.current_view)
        # Check if it's a category item in sidebar
        elif isinstance(event.item, CategoryItem) and event.control.id == "category-list-bar":
            self.current_view = f"category_{event.item.category_id}"
            # Switch to task view and load category tasks
            self.action_show_tasks()
            self.query_one(TaskView).load_tasks("category", event.item.category_id)

    def refresh_sidebar(self) -> None:
        """Refresh sidebar counts for smart lists and categories."""
        # Refresh smart list counts
        smart_list = self.query_one("#smart-list", ListView)
        for item in smart_list.children:
            if isinstance(item, SmartListItem):
                count = self._get_smart_list_count(item.smart_id)
                item.task_count = count
                # Update the static child
                static = item.query_one(Static)
                static.update(f"{item.icon} {item.list_name} [dim]({count})[/dim]")

        # Refresh category list counts
        category_list = self.query_one("#category-list-bar", ListView)
        for item in category_list.children:
            if isinstance(item, CategoryItem):
                count = self.db.get_category_task_count(item.category_id)
                item.task_count = count
                # Update the static child
                static = item.query_one(Static)
                static.update(f"{item.icon} {item.category_name} [dim]({count})[/dim]")

    def action_delete_item(self) -> None:
        """Delete the currently selected item (task or category)."""
        task_view = self.query_one("#task-view")
        category_view = self.query_one("#category-view")

        if task_view.display:
            # Delete task
            task_list = self.query_one("#task-list", ListView)
            if task_list.index is not None:
                selected_item = task_list.highlighted_child
                if selected_item and isinstance(selected_item, TaskItem):
                    self.db.delete_task(selected_item.task_id)
                    # Reload with current filter
                    if self.current_view.startswith("category_"):
                        cat_id = int(self.current_view.split("_")[1])
                        self.query_one(TaskView).load_tasks("category", cat_id)
                    else:
                        self.query_one(TaskView).load_tasks(self.current_view)
                    self.refresh_sidebar()

        elif category_view.display:
            # Delete category
            category_list = self.query_one("#categories-list-view", ListView)
            if category_list.index is not None:
                selected_item = category_list.highlighted_child
                if selected_item and isinstance(selected_item, CategoryItem):
                    # Don't allow deleting system categories
                    if not selected_item.is_system:
                        self.db.delete_category(selected_item.category_id)
                        self.query_one(CategoryView).load_categories()
                        self.refresh_sidebar()

    def action_toggle_task(self) -> None:
        """Toggle task status between new and completed."""
        task_view = self.query_one("#task-view")
        category_view = self.query_one("#category-view")

        # Only allow toggle in task view
        if not task_view.display or category_view.display:
            return

        task_list = self.query_one("#task-list", ListView)
        if task_list.index is not None:
            selected_item = task_list.highlighted_child
            if selected_item and isinstance(selected_item, TaskItem):
                # Toggle between 'new' and 'completed'
                new_status = "completed" if selected_item.status != "completed" else "new"

                # Check for reminders before completing
                if new_status == "completed":
                    self._check_and_complete_task(selected_item.task_id, new_status)
                else:
                    # Uncompleting task - just update directly
                    self.db.update_task(selected_item.task_id, status=new_status)
                    self._reload_tasks()
                    self.refresh_sidebar()

    def action_edit_item(self) -> None:
        """Edit the currently selected item (task or category)."""
        task_view = self.query_one("#task-view")
        category_view = self.query_one("#category-view")

        if task_view.display:
            # Edit task - open modal screen
            task_list = self.query_one("#task-list", ListView)
            if task_list.index is not None:
                selected_item = task_list.highlighted_child
                if selected_item and isinstance(selected_item, TaskItem):
                    # Get full task data from database
                    tasks = self.db.get_tasks()
                    task = next((t for t in tasks if t.id == selected_item.task_id), None)
                    if task:
                        self._open_task_edit_screen(task)

        elif category_view.display:
            # Edit category
            category_list = self.query_one("#categories-list-view", ListView)
            if category_list.index is not None:
                selected_item = category_list.highlighted_child
                if selected_item and isinstance(selected_item, CategoryItem):
                    # Don't allow editing system categories
                    if not selected_item.is_system:
                        # Pre-fill the input with category name and icon
                        category_input = self.query_one("#category-input", Input)
                        category_input.value = f"{selected_item.category_name}:{selected_item.icon}"
                        category_input.focus()
                        # Store the category ID being edited
                        self.editing_category_id = selected_item.category_id

    def _open_task_edit_screen(self, task=None) -> None:
        """Open the task edit screen.

        Args:
            task: Task object to edit, or None for new task
        """
        if task:
            # Edit existing task
            screen = TaskEditScreen(
                task_id=task.id,
                task_name=task.name,
                category_id=task.category_id,
                status=task.status,
                progress=task.progress,
                due_date=task.due_date,
            )
        else:
            # New task - use current category if viewing one
            category_id = 1
            if self.current_view.startswith("category_"):
                try:
                    category_id = int(self.current_view.split("_")[1])
                except (ValueError, IndexError):
                    pass
            screen = TaskEditScreen(category_id=category_id)

        self.push_screen(screen, self._handle_task_edit_result)

    def _handle_task_edit_result(self, task_data: dict | None) -> None:
        """Handle the result from the task edit screen.

        Args:
            task_data: Dictionary with task data, or None if cancelled
        """
        if task_data is None:
            return  # User cancelled

        # The task_data should have a task_id if editing, None if creating
        # We'll add it to the data dict when opening the edit screen
        task_id = task_data.get("task_id")

        if task_id:
            # Check if task is being completed
            current_task = next((t for t in self.db.get_tasks() if t.id == task_id), None)
            if current_task:
                old_status = current_task.status
                old_progress = current_task.progress
                new_status = task_data["status"]
                new_progress = task_data["progress"]

                # Check if transitioning to completed state
                is_completing = (
                    (old_status != "completed" and new_status == "completed") or
                    (old_progress < 100 and new_progress >= 100)
                )

                if is_completing:
                    # Store task data for later use in callback
                    self._pending_task_data = task_data
                    self._check_and_complete_task(task_id, new_status, new_progress)
                    return

            # Update existing task (not completing)
            self.db.update_task(
                task_id,
                name=task_data["name"],
                category_id=task_data["category_id"],
                status=task_data["status"],
                progress=task_data["progress"],
                due_date=task_data["due_date"],
            )
        else:
            # Create new task
            self.db.add_task(
                name=task_data["name"],
                category_id=task_data["category_id"],
                status=task_data["status"],
                progress=task_data["progress"],
                due_date=task_data["due_date"],
            )

        # Reload tasks and refresh sidebar
        self._reload_tasks()
        self.refresh_sidebar()

    def action_cancel_input(self) -> None:
        """Cancel input and clear editing state."""
        task_view = self.query_one("#task-view")
        category_view = self.query_one("#category-view")

        if task_view.display:
            task_input = self.query_one("#task-input", Input)
            if task_input.has_focus:
                task_input.value = ""
                task_input.blur()
                self.editing_task_id = None

        elif category_view.display:
            category_input = self.query_one("#category-input", Input)
            if category_input.has_focus:
                category_input.value = ""
                category_input.blur()
                self.editing_category_id = None

    async def action_submit_input(self) -> None:
        """Submit the current input (same as pressing Enter)."""
        task_view = self.query_one("#task-view")
        category_view = self.query_one("#category-view")

        if task_view.display:
            task_input = self.query_one("#task-input", Input)
            if task_input.has_focus:
                # Trigger the submit
                await task_input.action_submit()

        elif category_view.display:
            category_input = self.query_one("#category-input", Input)
            if category_input.has_focus:
                # Trigger the submit
                await category_input.action_submit()

    def _reload_tasks(self) -> None:
        """Reload tasks with current filter."""
        if self.current_view.startswith("category_"):
            cat_id = int(self.current_view.split("_")[1])
            self.query_one(TaskView).load_tasks("category", cat_id)
        else:
            self.query_one(TaskView).load_tasks(self.current_view)

    def _check_and_complete_task(
        self,
        task_id: int,
        new_status: str,
        new_progress: int | None = None
    ) -> None:
        """Check for reminders and show confirmation before completing task.

        Args:
            task_id: ID of the task being completed
            new_status: New status for the task
            new_progress: New progress value (if applicable)
        """
        # Get reminder count for this task
        reminder_count = self.db.get_reminder_count(task_id)

        if reminder_count > 0:
            # Get task name
            tasks = self.db.get_tasks()
            task = next((t for t in tasks if t.id == task_id), None)
            if task:
                # Store completion info for callback
                self._completion_info = {
                    "task_id": task_id,
                    "status": new_status,
                    "progress": new_progress
                }

                # Show confirmation dialog
                from .screens.reminder_confirm import ReminderConfirmScreen
                self.push_screen(
                    ReminderConfirmScreen(
                        task_id=task_id,
                        task_name=task.name,
                        reminder_count=reminder_count
                    ),
                    self._handle_reminder_confirmation
                )
                return

        # No reminders or task not found - complete directly
        self._complete_task_directly(task_id, new_status, new_progress)

    def _handle_reminder_confirmation(self, result: bool | None) -> None:
        """Handle confirmation dialog result.

        Args:
            result: True to remove reminders, False to keep, None to cancel
        """
        if result is None:
            # User cancelled - don't complete task
            # Clear pending task data if it exists
            if hasattr(self, '_pending_task_data'):
                delattr(self, '_pending_task_data')
            return

        # Get stored completion info
        if not hasattr(self, '_completion_info'):
            return

        info = self._completion_info
        task_id = info["task_id"]

        # Remove reminders if user confirmed
        if result is True:
            self.db.delete_reminders_for_task(task_id)

        # Complete the task
        self._complete_task_directly(task_id, info["status"], info["progress"])

        # Cleanup
        delattr(self, '_completion_info')

    def _complete_task_directly(
        self,
        task_id: int,
        new_status: str,
        new_progress: int | None = None
    ) -> None:
        """Complete the task without confirmation.

        Args:
            task_id: ID of the task to complete
            new_status: New status for the task
            new_progress: New progress value (if applicable)
        """
        # Check if we have pending task data from edit screen
        if hasattr(self, '_pending_task_data'):
            task_data = self._pending_task_data
            self.db.update_task(
                task_id,
                name=task_data["name"],
                category_id=task_data["category_id"],
                status=task_data["status"],
                progress=task_data["progress"],
                due_date=task_data["due_date"],
            )
            delattr(self, '_pending_task_data')
        else:
            # Simple status update (from toggle)
            if new_progress is not None:
                self.db.update_task(task_id, status=new_status, progress=new_progress)
            else:
                self.db.update_task(task_id, status=new_status)

        # Reload tasks and refresh sidebar
        self._reload_tasks()
        self.refresh_sidebar()


if __name__ == "__main__":
    TodoApp().run()
