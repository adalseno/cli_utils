"""CLI Utils - A modern CLI application for managing scripts and utilities.

This package provides a flexible framework for organizing and managing
Python scripts for both local tasks and remote API interactions.
"""

__version__ = "0.1.0"

from cli_utils.config import get_settings
from cli_utils.main import app

__all__ = ["app", "get_settings", "__version__"]
