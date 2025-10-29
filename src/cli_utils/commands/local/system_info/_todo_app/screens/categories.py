from typing import TYPE_CHECKING

from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import DescendantFocus, DescendantBlur
from textual.widgets import Input, ListView, Static

from .widgets import CategoryItem

if TYPE_CHECKING:
    from ..todo_app import TodoApp


class CategoryView(Vertical):
    """Category management view."""

    BINDINGS = [
        ("e", "edit_category", "Edit"),
        ("d", "delete_category", "Delete"),
        ("t", "show_tasks", "Tasks"),
        Binding("escape", "cancel_input", "Cancel", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._input_focused = False

    @property
    def todo_app(self) -> "TodoApp":
        """Return the app instance with proper typing."""
        return self.app  # type: ignore[return-value]

    def compose(self):
        yield Static("All Categories", id="categories-header")
        yield VerticalScroll(ListView(id="categories-list-view"), id="categories-container")
        yield Horizontal(Input(placeholder="Add a new category (format: name:icon)...", id="category-input"), id="category-input-container")

    def on_mount(self) -> None:
        """Load categories when the view is mounted."""
        self.load_categories()

    def load_categories(self) -> None:
        """Load categories from database."""
        category_list = self.query_one("#categories-list-view", ListView)
        category_list.clear()

        db = self.todo_app.db
        categories = db.get_categories()

        # Add categories to the list
        for cat in categories:
            count = db.get_category_task_count(cat.id)
            category_item = CategoryItem(
                category_id=cat.id,
                name=cat.name,
                count=count,
                icon=cat.icon,
                is_system=cat.is_system
            )
            category_list.append(category_item)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle category input submission."""
        if event.input.id == "category-input":
            input_text = event.value.strip()
            if input_text:
                # Parse input: "name:icon" or just "name"
                if ":" in input_text:
                    name, icon = input_text.split(":", 1)
                    name = name.strip()
                    icon = icon.strip()
                else:
                    name = input_text
                    icon = "📋"

                db = self.todo_app.db

                # Check if we're editing an existing category
                if self.todo_app.editing_category_id is not None:
                    # Update existing category
                    db.update_category(self.todo_app.editing_category_id, name=name, icon=icon)
                    self.todo_app.editing_category_id = None
                else:
                    # Add new category to database
                    db.add_category(name=name, icon=icon)

                # Clear input
                event.input.value = ""

                # Reload categories
                self.load_categories()

                # Refresh sidebar
                self.todo_app.refresh_sidebar()

    def action_edit_category(self) -> None:
        """Proxy to app's edit action."""
        self.todo_app.action_edit_item()

    def action_delete_category(self) -> None:
        """Proxy to app's delete action."""
        self.todo_app.action_delete_item()

    def action_cancel_input(self) -> None:
        """Cancel input and clear editing state."""
        category_input = self.query_one("#category-input", Input)
        if category_input.has_focus:
            category_input.value = ""
            category_input.blur()
            self.todo_app.editing_category_id = None

    def action_show_tasks(self) -> None:
        """Switch to tasks view."""
        self.todo_app.action_show_tasks()

    # TODO: Fix escape binding visibility - it should show in footer when input is focused
    # Current implementation doesn't display the binding despite check_action returning True
    # Consider alternative approaches: custom footer, direct binding manipulation, or Textual updates
    def on_descendant_focus(self, event: DescendantFocus) -> None:
        """Track when input is focused to show escape binding."""
        if isinstance(event.widget, Input) and event.widget.id == "category-input":
            self._input_focused = True
            self.app.refresh_bindings()

    def on_descendant_blur(self, event: DescendantBlur) -> None:
        """Track when input loses focus to hide escape binding."""
        if isinstance(event.widget, Input) and event.widget.id == "category-input":
            self._input_focused = False
            self.app.refresh_bindings()

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        """Check if an action is currently available."""
        if action == "cancel_input":
            # Only show/enable cancel_input when input is focused
            return self._input_focused if self._input_focused else None
        return True
