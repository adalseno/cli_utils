"""Notification plugin system for todo reminders."""

from .base import NotificationPlugin, NotificationResult
from .desktop import DesktopNotificationPlugin

__all__ = [
    "NotificationPlugin",
    "NotificationResult",
    "DesktopNotificationPlugin",
]
