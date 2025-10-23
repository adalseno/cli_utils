"""Pytest configuration and fixtures for CLI Utils tests.

This module provides shared fixtures and configuration for all tests.
"""

import os
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from cli_utils.config import reset_settings
from cli_utils.main import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Typer CLI test runner.

    Returns:
        CliRunner instance for testing CLI commands
    """
    return CliRunner()


@pytest.fixture
def test_app():
    """Provide the main Typer app for testing.

    Returns:
        Main Typer application instance
    """
    return app


@pytest.fixture(autouse=True)
def reset_config() -> Generator[None, None, None]:
    """Reset configuration before and after each test.

    This ensures tests don't interfere with each other.
    """
    reset_settings()
    yield
    reset_settings()


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Provide a temporary configuration directory for testing.

    Args:
        tmp_path: Pytest's temporary directory fixture

    Yields:
        Path to temporary config directory
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Override the config directory via environment variable
    old_config = os.environ.get("CLI_UTILS_CONFIG_DIR")
    os.environ["CLI_UTILS_CONFIG_DIR"] = str(config_dir)

    yield config_dir

    # Restore original config
    if old_config:
        os.environ["CLI_UTILS_CONFIG_DIR"] = old_config
    else:
        os.environ.pop("CLI_UTILS_CONFIG_DIR", None)


@pytest.fixture
def sample_text() -> str:
    """Provide sample text for testing text utilities.

    Returns:
        Sample text string
    """
    return "Hello World"
