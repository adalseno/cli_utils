"""Base classes for notification plugins."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class NotificationAction(Enum):
    """Actions that can be taken on a notification."""
    DISMISSED = "dismissed"  # User dismissed the notification
    SNOOZED = "snoozed"      # User snoozed (not implemented yet)
    EXPIRED = "expired"      # Notification expired naturally
    ERROR = "error"          # Error sending notification


@dataclass
class NotificationResult:
    """Result of sending a notification.

    Attributes:
        success: Whether the notification was sent successfully
        action: What happened to the notification
        notification_id: System-specific notification ID (if applicable)
        error_message: Error message if failed
    """
    success: bool
    action: NotificationAction
    notification_id: Optional[str] = None
    error_message: Optional[str] = None


class NotificationPlugin(ABC):
    """Base class for notification plugins.

    Notification plugins are responsible for sending reminders through
    different channels (desktop notifications, email, SMS, etc.).
    """

    @abstractmethod
    def send(
        self,
        title: str,
        message: str,
        task_id: int,
        reminder_id: int,
        urgency: str = "normal"
    ) -> NotificationResult:
        """Send a notification.

        Args:
            title: Notification title
            message: Notification message body
            task_id: ID of the task this reminder is for
            reminder_id: ID of the reminder being sent
            urgency: Urgency level (low, normal, critical)

        Returns:
            NotificationResult with status and action taken
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this notification method is available on this system.

        Returns:
            True if the notification method can be used
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this notification plugin."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of this notification plugin."""
        pass
