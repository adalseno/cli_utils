"""SQLite database layer for the todo app."""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, cast


@dataclass
class Category:
    """Category data model."""
    id: int
    name: str
    icon: str
    description: str = ""
    is_system: bool = False


@dataclass
class Task:
    """Task data model."""
    id: int
    name: str
    category_id: int
    status: str  # 'new', 'in_progress', 'completed'
    progress: int  # 0-100
    created_at: str
    updated_at: str
    due_date: Optional[str] = None


@dataclass
class Reminder:
    """Reminder data model (for future use)."""
    id: int
    task_id: int
    reminder_datetime: str


class TodoDatabase:
    """SQLite database manager for todo app."""

    def __init__(self, db_path: str | Path):
        """Initialize database connection.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._seed_default_categories()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            # Categories table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    icon TEXT DEFAULT '📋',
                    is_system INTEGER DEFAULT 0
                )
            """)

            # Tasks table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    status TEXT CHECK(status IN ('new', 'in_progress', 'completed')) DEFAULT 'new',
                    progress INTEGER CHECK(progress >= 0 AND progress <= 100) DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    due_date TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)

            # Reminders table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    reminder_datetime TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
            """)

            # Sent notifications tracking table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sent_notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reminder_id INTEGER NOT NULL,
                    sent_at TEXT NOT NULL,
                    plugin_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (reminder_id) REFERENCES reminders(id) ON DELETE CASCADE
                )
            """)

            conn.commit()

    def _seed_default_categories(self) -> None:
        """Seed default system categories if they don't exist."""
        with self._get_connection() as conn:
            # Check if we already have categories
            cursor = conn.execute("SELECT COUNT(*) as count FROM categories")
            count = cursor.fetchone()["count"]

            if count == 0:
                # Add default categories
                default_categories = [
                    ("Personal", "👤", "Personal tasks", 1),
                    ("Work", "💼", "Work-related tasks", 1),
                ]

                conn.executemany(
                    "INSERT INTO categories (name, icon, description, is_system) VALUES (?, ?, ?, ?)",
                    default_categories
                )
                conn.commit()

    # ==================== Category Methods ====================

    def get_categories(self) -> list[Category]:
        """Get all categories.

        Returns:
            List of Category objects
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, name, icon, description, is_system
                FROM categories
                ORDER BY is_system DESC, name ASC
            """)
            return [
                Category(
                    id=row["id"],
                    name=row["name"],
                    icon=row["icon"],
                    description=row["description"],
                    is_system=bool(row["is_system"])
                )
                for row in cursor.fetchall()
            ]

    def add_category(self, name: str, icon: str = "📋", description: str = "") -> int:
        """Add a new category.

        Args:
            name: Category name
            icon: Category icon/emoji
            description: Category description

        Returns:
            ID of the newly created category
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO categories (name, icon, description, is_system) VALUES (?, ?, ?, 0)",
                (name, icon, description)
            )
            conn.commit()
            assert cursor.lastrowid is not None
            return cursor.lastrowid

    def update_category(self, category_id: int, name: str, icon: str, description: str = "") -> None:
        """Update a category (non-system only).

        Args:
            category_id: ID of the category to update
            name: New category name
            icon: New category icon
            description: New category description
        """
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE categories
                SET name = ?, icon = ?, description = ?
                WHERE id = ? AND is_system = 0
            """, (name, icon, description, category_id))
            conn.commit()

    def delete_category(self, category_id: int) -> None:
        """Delete a category (non-system only).

        Args:
            category_id: ID of the category to delete

        Note:
            Tasks in this category will be moved to the first category (Personal)
        """
        with self._get_connection() as conn:
            # Move tasks to first category (Personal)
            conn.execute("""
                UPDATE tasks
                SET category_id = 1
                WHERE category_id = ?
            """, (category_id,))

            # Delete the category (only if not a system category)
            conn.execute("""
                DELETE FROM categories
                WHERE id = ? AND is_system = 0
            """, (category_id,))
            conn.commit()

    def get_category_task_count(self, category_id: int, exclude_completed: bool = True) -> int:
        """Get the number of tasks in a category.

        Args:
            category_id: ID of the category
            exclude_completed: Whether to exclude completed tasks

        Returns:
            Number of tasks in the category
        """
        with self._get_connection() as conn:
            query = "SELECT COUNT(*) as count FROM tasks WHERE category_id = ?"
            params = [category_id]

            if exclude_completed:
                query += " AND status != 'completed'"

            cursor = conn.execute(query, params)
            return cursor.fetchone()["count"]

    # ==================== Task Methods ====================

    def _sync_status_with_progress(self, status: str, progress: int) -> str:
        """Automatically sync task status based on progress.

        Args:
            status: Current status
            progress: Task progress (0-100)

        Returns:
            Updated status based on progress
        """
        if progress == 100:
            return "completed"
        elif progress > 0:
            return "in_progress"
        else:
            return "new"

    def get_tasks(self, category_id: Optional[int] = None, status: Optional[str] = None) -> list[Task]:
        """Get tasks, optionally filtered by category and/or status.

        Args:
            category_id: Filter by category ID (None = all categories)
            status: Filter by status (None = all statuses)

        Returns:
            List of Task objects
        """
        with self._get_connection() as conn:
            query = """
                SELECT id, name, category_id, status, progress,
                       created_at, updated_at, due_date
                FROM tasks
                WHERE 1=1
            """
            params = []

            if category_id is not None:
                query += " AND category_id = ?"
                params.append(category_id)

            if status is not None:
                query += " AND status = ?"
                params.append(status)

            query += " ORDER BY created_at DESC"

            cursor = conn.execute(query, params)
            return [
                Task(
                    id=row["id"],
                    name=row["name"],
                    category_id=row["category_id"],
                    status=row["status"],
                    progress=row["progress"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                    due_date=row["due_date"]
                )
                for row in cursor.fetchall()
            ]

    def add_task(
        self,
        name: str,
        category_id: int,
        due_date: Optional[str] = None,
        status: str = "new",
        progress: int = 0
    ) -> int:
        """Add a new task.

        Args:
            name: Task name/description
            category_id: ID of the category
            due_date: Due date in ISO format (YYYY-MM-DD)
            status: Task status ('new', 'in_progress', 'completed')
            progress: Task progress (0-100)

        Returns:
            ID of the newly created task
        """
        # Auto-sync status with progress
        status = self._sync_status_with_progress(status, progress)

        now = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (name, category_id, status, progress, created_at, updated_at, due_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, category_id, status, progress, now, now, due_date))
            conn.commit()
            assert cursor.lastrowid is not None
            return cursor.lastrowid

    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        category_id: Optional[int] = None,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        due_date: Optional[str] = None
    ) -> None:
        """Update a task.

        Args:
            task_id: ID of the task to update
            name: New task name (None = no change)
            category_id: New category ID (None = no change)
            status: New status (None = no change)
            progress: New progress (None = no change)
            due_date: New due date (None = no change)
        """
        # If progress is being updated, sync status accordingly
        if progress is not None:
            # Get current status if not provided
            if status is None:
                with self._get_connection() as conn:
                    cursor = conn.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
                    row = cursor.fetchone()
                    if row:
                        status = row["status"]
                    else:
                        status = "new"  # Default if task not found

            # Auto-sync status with progress
            status = self._sync_status_with_progress(cast(str, status), progress)

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)

        if category_id is not None:
            updates.append("category_id = ?")
            params.append(category_id)

        if status is not None:
            updates.append("status = ?")
            params.append(status)

        if progress is not None:
            updates.append("progress = ?")
            params.append(progress)

        if due_date is not None:
            updates.append("due_date = ?")
            params.append(due_date)

        if not updates:
            return  # Nothing to update

        updates.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(task_id)

        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"

        with self._get_connection() as conn:
            conn.execute(query, params)
            conn.commit()

    def delete_task(self, task_id: int) -> None:
        """Delete a task.

        Args:
            task_id: ID of the task to delete
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    def get_task_count(self, status: Optional[str] = None, due_filter: Optional[str] = None) -> int:
        """Get count of tasks, optionally filtered.

        Args:
            status: Filter by status (None = exclude completed)
            due_filter: 'upcoming', 'past', or None

        Returns:
            Number of tasks matching the criteria
        """
        with self._get_connection() as conn:
            query = "SELECT COUNT(*) as count FROM tasks WHERE 1=1"
            params = []

            if status is not None:
                query += " AND status = ?"
                params.append(status)
            elif status is None:
                # By default, exclude completed
                query += " AND status != 'completed'"

            if due_filter == "upcoming":
                today = datetime.now().date().isoformat()
                query += " AND due_date >= ?"
                params.append(today)
            elif due_filter == "past":
                today = datetime.now().date().isoformat()
                query += " AND due_date < ?"
                params.append(today)

            cursor = conn.execute(query, params)
            return cursor.fetchone()["count"]

    # ==================== Reminder Methods ====================

    def get_reminders(self, task_id: int) -> list[Reminder]:
        """Get all reminders for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            List of Reminder objects sorted by reminder_datetime
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, task_id, reminder_datetime
                FROM reminders
                WHERE task_id = ?
                ORDER BY reminder_datetime ASC
            """, (task_id,))
            return [
                Reminder(
                    id=row["id"],
                    task_id=row["task_id"],
                    reminder_datetime=row["reminder_datetime"]
                )
                for row in cursor.fetchall()
            ]

    def get_reminder_count(self, task_id: int) -> int:
        """Get the number of reminders for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            Number of reminders for the task
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) as count FROM reminders WHERE task_id = ?",
                (task_id,)
            )
            return cursor.fetchone()["count"]

    def add_reminder(self, task_id: int, reminder_datetime: str) -> int:
        """Add a new reminder for a task.

        Args:
            task_id: ID of the task
            reminder_datetime: Reminder date/time in ISO format (YYYY-MM-DD HH:MM)

        Returns:
            ID of the newly created reminder
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO reminders (task_id, reminder_datetime) VALUES (?, ?)",
                (task_id, reminder_datetime)
            )
            conn.commit()
            assert cursor.lastrowid is not None
            return cursor.lastrowid

    def update_reminder(self, reminder_id: int, reminder_datetime: str) -> None:
        """Update a reminder's datetime.

        Args:
            reminder_id: ID of the reminder to update
            reminder_datetime: New reminder date/time in ISO format (YYYY-MM-DD HH:MM)
        """
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE reminders SET reminder_datetime = ? WHERE id = ?",
                (reminder_datetime, reminder_id)
            )
            conn.commit()

    def delete_reminder(self, reminder_id: int) -> None:
        """Delete a reminder.

        Args:
            reminder_id: ID of the reminder to delete
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            conn.commit()

    def get_pending_reminders(self, current_time: str) -> list[tuple[Reminder, Task]]:
        """Get reminders that are due and haven't been sent yet.

        Args:
            current_time: Current datetime in ISO format (YYYY-MM-DD HH:MM)

        Returns:
            List of (Reminder, Task) tuples for reminders that need to be sent
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT r.id, r.task_id, r.reminder_datetime,
                       t.id, t.name, t.category_id, t.status, t.progress,
                       t.created_at, t.updated_at, t.due_date
                FROM reminders r
                JOIN tasks t ON r.task_id = t.id
                LEFT JOIN sent_notifications sn ON r.id = sn.reminder_id
                WHERE r.reminder_datetime <= ?
                  AND sn.id IS NULL
                  AND t.status != 'completed'
                ORDER BY r.reminder_datetime ASC
            """, (current_time,))

            results = []
            for row in cursor.fetchall():
                reminder = Reminder(
                    id=row[0],
                    task_id=row[1],
                    reminder_datetime=row[2]
                )
                task = Task(
                    id=row[3],
                    name=row[4],
                    category_id=row[5],
                    status=row[6],
                    progress=row[7],
                    created_at=row[8],
                    updated_at=row[9],
                    due_date=row[10]
                )
                results.append((reminder, task))

            return results

    def mark_notification_sent(
        self,
        reminder_id: int,
        plugin_name: str,
        status: str = "sent"
    ) -> None:
        """Mark a notification as sent.

        Args:
            reminder_id: ID of the reminder that was sent
            plugin_name: Name of the notification plugin used
            status: Status of the notification (sent, error, etc.)
        """
        from datetime import datetime
        sent_at = datetime.now().isoformat()

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO sent_notifications (reminder_id, sent_at, plugin_name, status)
                VALUES (?, ?, ?, ?)
            """, (reminder_id, sent_at, plugin_name, status))
            conn.commit()

    def delete_reminders_for_task(self, task_id: int) -> int:
        """Delete all reminders for a task.

        Args:
            task_id: ID of the task

        Returns:
            Number of reminders deleted
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM reminders WHERE task_id = ?",
                (task_id,)
            )
            conn.commit()
            return cursor.rowcount if cursor.rowcount else 0
