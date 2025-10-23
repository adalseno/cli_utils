"""Tests for configuration management."""

from pathlib import Path

import yaml

from cli_utils.config import Settings, get_settings


def test_settings_initialization():
    """Test that Settings can be initialized with defaults."""
    settings = Settings()

    assert settings.log_level == "INFO"
    assert settings.api_timeout == 30
    assert settings.max_retries == 3
    assert isinstance(settings.config_dir, Path)


def test_get_settings_singleton():
    """Test that get_settings returns the same instance."""
    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2


def test_settings_get_method():
    """Test the get method for retrieving custom config values."""
    settings = Settings()
    settings.custom_config = {"api": {"github": {"token": "test123"}}}

    assert settings.get("api.github.token") == "test123"
    assert settings.get("api.github.url", "default") == "default"
    assert settings.get("nonexistent", "fallback") == "fallback"


def test_save_and_load_config(tmp_path: Path):
    """Test saving and loading configuration from YAML."""
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    settings = Settings(config_dir=config_dir)

    # Save config
    test_config = {"api": {"timeout": 60}, "features": {"debug": True}}
    settings.save_config(test_config)

    # Verify file exists
    config_file = config_dir / "config.yaml"
    assert config_file.exists()

    # Load and verify
    with open(config_file, "r") as f:
        loaded = yaml.safe_load(f)

    assert loaded == test_config
