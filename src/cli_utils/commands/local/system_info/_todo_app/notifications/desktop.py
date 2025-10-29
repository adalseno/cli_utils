"""Desktop notification plugin using notify-send."""

import shutil
import subprocess
from typing import Optional

from .base import NotificationAction, NotificationPlugin, NotificationResult


class DesktopNotificationPlugin(NotificationPlugin):
    """Desktop notification plugin using notify-send (Linux).

    This plugin sends desktop notifications using the notify-send command,
    which is available on most Linux desktop environments.
    """

    def __init__(self, app_name: str = "TodoApp"):
        """Initialize the desktop notification plugin.

        Args:
            app_name: Application name to show in notifications
        """
        self.app_name = app_name

    def send(
        self,
        title: str,
        message: str,
        task_id: int,
        reminder_id: int,
        urgency: str = "normal"
    ) -> NotificationResult:
        """Send a desktop notification using notify-send.

        Args:
            title: Notification title
            message: Notification message body
            task_id: ID of the task this reminder is for
            reminder_id: ID of the reminder being sent
            urgency: Urgency level (low, normal, critical)

        Returns:
            NotificationResult with status and action taken
        """
        if not self.is_available():
            return NotificationResult(
                success=False,
                action=NotificationAction.ERROR,
                error_message="notify-send is not available on this system"
            )

        try:
            # Build the notify-send command
            cmd = [
                "notify-send",
                f"--app-name={self.app_name}",
                f"--urgency={urgency}",
                "--icon=calendar",
                title,
                message
            ]

            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return NotificationResult(
                    success=True,
                    action=NotificationAction.DISMISSED,  # We assume dismissed for now
                    notification_id=None  # notify-send doesn't return IDs
                )
            else:
                return NotificationResult(
                    success=False,
                    action=NotificationAction.ERROR,
                    error_message=f"notify-send failed: {result.stderr}"
                )

        except subprocess.TimeoutExpired:
            return NotificationResult(
                success=False,
                action=NotificationAction.ERROR,
                error_message="notify-send timed out"
            )
        except Exception as e:
            return NotificationResult(
                success=False,
                action=NotificationAction.ERROR,
                error_message=f"Error sending notification: {str(e)}"
            )

    def is_available(self) -> bool:
        """Check if notify-send is available.

        Returns:
            True if notify-send command is available
        """
        return shutil.which("notify-send") is not None

    @property
    def name(self) -> str:
        """Human-readable name of this notification plugin."""
        return "Desktop Notifications"

    @property
    def description(self) -> str:
        """Description of this notification plugin."""
        return "Send desktop notifications using notify-send (Linux)"
