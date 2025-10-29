"""Reminder daemon for sending task notifications.

This daemon runs in the background and periodically checks for due reminders,
sending notifications through registered plugins.

Usage:
    python -m cli_utils.commands.local.system_info._todo_app.reminder_daemon start
    python -m cli_utils.commands.local.system_info._todo_app.reminder_daemon stop
"""

import sys
import time
import signal
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from .database import TodoDatabase
from .notifications import NotificationPlugin, DesktopNotificationPlugin


class ReminderDaemon:
    """Background daemon that checks and sends reminders."""

    def __init__(
        self,
        db_path: str | Path | None = None,
        check_interval: int = 60,  # Check every 60 seconds
        plugins: List[NotificationPlugin] | None = None
    ):
        """Initialize the reminder daemon.

        Args:
            db_path: Path to the todo database
            check_interval: How often to check for reminders (seconds)
            plugins: List of notification plugins to use
        """
        if db_path is None:
            db_path = Path.home() / ".config" / "cli_utils" / "todo.db"

        self.db = TodoDatabase(db_path)
        self.check_interval = check_interval
        self.running = False

        # Initialize plugins
        if plugins is None:
            plugins = [DesktopNotificationPlugin()]

        # Filter to only available plugins
        self.plugins = [p for p in plugins if p.is_available()]

        if not self.plugins:
            logging.warning("No notification plugins available!")

        # Setup logging
        log_dir = Path.home() / ".config" / "cli_utils" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "reminder_daemon.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("ReminderDaemon")

    def start(self):
        """Start the reminder daemon."""
        self.logger.info("Starting reminder daemon...")
        self.logger.info(f"Loaded {len(self.plugins)} notification plugin(s)")
        for plugin in self.plugins:
            self.logger.info(f"  - {plugin.name}: {plugin.description}")

        self.running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # Main loop
        try:
            while self.running:
                self._check_and_send_reminders()
                time.sleep(self.check_interval)
        except Exception as e:
            self.logger.error(f"Daemon error: {e}", exc_info=True)
        finally:
            self.logger.info("Reminder daemon stopped")

    def stop(self):
        """Stop the reminder daemon."""
        self.logger.info("Stopping reminder daemon...")
        self.running = False

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}")
        self.stop()

    def _check_and_send_reminders(self):
        """Check for due reminders and send notifications."""
        try:
            # Get current time in the format used by reminders
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Get pending reminders
            pending = self.db.get_pending_reminders(current_time)

            if not pending:
                return  # No reminders due

            self.logger.info(f"Found {len(pending)} pending reminder(s)")

            # Send notifications
            for reminder, task in pending:
                self._send_reminder(reminder, task)

        except Exception as e:
            self.logger.error(f"Error checking reminders: {e}", exc_info=True)

    def _send_reminder(self, reminder, task):
        """Send a reminder notification.

        Args:
            reminder: Reminder object
            task: Task object
        """
        title = f"⏰ Reminder: {task.name}"
        message = f"Task: {task.name}\n"

        if task.due_date:
            message += f"Due: {task.due_date}\n"

        if task.progress > 0:
            message += f"Progress: {task.progress}%"

        # Try each plugin until one succeeds
        for plugin in self.plugins:
            try:
                self.logger.info(
                    f"Sending reminder {reminder.id} for task '{task.name}' via {plugin.name}"
                )

                result = plugin.send(
                    title=title,
                    message=message,
                    task_id=task.id,
                    reminder_id=reminder.id
                )

                if result.success:
                    self.logger.info(
                        f"Successfully sent reminder {reminder.id} via {plugin.name}"
                    )
                    # Mark as sent in database
                    self.db.mark_notification_sent(
                        reminder.id,
                        plugin.name,
                        "sent"
                    )
                    return  # Successfully sent, stop trying other plugins
                else:
                    self.logger.warning(
                        f"Failed to send reminder {reminder.id} via {plugin.name}: "
                        f"{result.error_message}"
                    )

            except Exception as e:
                self.logger.error(
                    f"Error sending reminder {reminder.id} via {plugin.name}: {e}",
                    exc_info=True
                )

        # If we get here, all plugins failed
        self.logger.error(f"Failed to send reminder {reminder.id} with all plugins")
        # Mark as error in database
        self.db.mark_notification_sent(reminder.id, "none", "error")


def main():
    """Main entry point for the daemon."""
    if len(sys.argv) < 2:
        print("Usage: reminder_daemon.py [start|stop]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        daemon = ReminderDaemon()
        daemon.start()
    elif command == "stop":
        # TODO: Implement proper daemon stop (requires PID file)
        print("Stop command not yet implemented")
        print("Use Ctrl+C or kill the process manually")
        sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        print("Usage: reminder_daemon.py [start|stop]")
        sys.exit(1)


if __name__ == "__main__":
    main()
