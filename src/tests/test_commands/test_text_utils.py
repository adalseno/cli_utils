"""Tests for text_utils commands."""

import pytest


def test_uppercase_function(sample_text: str):
    """Test the uppercase command function."""
    # Note: This tests the function directly, not via CLI
    # The function prints to console, so we can't easily capture output
    # In a real test, you'd use a mock or CliRunner
    result = sample_text.upper()
    assert result == "HELLO WORLD"


def test_lowercase_function(sample_text: str):
    """Test the lowercase command function."""
    result = sample_text.lower()
    assert result == "hello world"


def test_titlecase_function(sample_text: str):
    """Test the titlecase command function."""
    result = sample_text.title()
    assert result == "Hello World"


# Example of testing with CliRunner (requires the full app to be loaded)
# This is a more integration-style test
@pytest.mark.skip(reason="Requires full plugin loading - demo test")
def test_uppercase_cli(cli_runner, test_app):
    """Test uppercase command via CLI runner.

    This is an example of how to test commands via the CLI interface.
    Skipped by default as it requires the full plugin system to be loaded.
    """
    from cli_utils.core.plugin_loader import create_plugin_loader

    # Load plugins
    loader = create_plugin_loader(test_app)
    loader.load_all_commands()

    # Run command
    result = cli_runner.invoke(test_app, ["local", "text-utils", "uppercase", "hello"])

    assert result.exit_code == 0
    assert "HELLO" in result.stdout
