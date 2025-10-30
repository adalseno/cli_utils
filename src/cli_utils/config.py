"""Configuration management for CLI Utils.

This module handles loading and managing configuration from multiple sources:
- Environment variables
- .env files
- YAML configuration files
- Default values
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from cli_utils.utils.nerd_font_check import check_nerd_fonts


@dataclass
class Settings:
    """Application settings and configuration.

    Attributes:
        config_dir: Directory for user configuration files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        api_timeout: Default timeout for API requests in seconds
        max_retries: Maximum number of retries for failed API requests
        nerd_font_support: Whether Nerd Fonts are installed (1=yes, 0=no)
        custom_config: Additional custom configuration loaded from YAML
    """

    config_dir: Path = field(default_factory=lambda: Path.home() / ".config" / "cli_utils")
    log_level: str = "INFO"
    api_timeout: int = 30
    max_retries: int = 3
    nerd_font_support: int = 0
    custom_config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize configuration after dataclass creation."""
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load environment variables from .env file
        load_dotenv()

        # Override with environment variables if present
        self.log_level = os.getenv("CLI_UTILS_LOG_LEVEL", self.log_level)
        self.api_timeout = int(os.getenv("CLI_UTILS_API_TIMEOUT", str(self.api_timeout)))
        self.max_retries = int(os.getenv("CLI_UTILS_MAX_RETRIES", str(self.max_retries)))

        # Load custom configuration from YAML if exists
        self._load_yaml_config()

        # Check for Nerd Font support
        self._detect_nerd_fonts()

        # Initialize icon manager with detected Nerd Font support
        self._init_icon_manager()

    def _load_yaml_config(self) -> None:
        """Load configuration from YAML file if it exists."""
        config_file = self.config_dir / "config.yaml"

        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    self.custom_config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                # If YAML is invalid, log warning but don't crash
                print(f"Warning: Could not load config from {config_file}: {e}")
                self.custom_config = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value from custom config.

        Args:
            key: Configuration key (supports dot notation for nested keys)
            default: Default value if key is not found

        Returns:
            Configuration value or default

        Example:
            >>> settings.get("api.github.token")
            >>> settings.get("features.enabled", [])
        """
        keys = key.split(".")
        value = self.custom_config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def save_config(self, config: dict[str, Any]) -> None:
        """Save configuration to YAML file.

        Args:
            config: Configuration dictionary to save
        """
        config_file = self.config_dir / "config.yaml"

        try:
            with open(config_file, "w") as f:
                yaml.safe_dump(config, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config to {config_file}: {e}")

    def _detect_nerd_fonts(self) -> None:
        """Detect if Nerd Fonts are installed and update configuration."""
        # First check if it's already set in custom config
        config_value = self.get("display.nerd_font_support")

        if config_value is not None:
            # Use the value from config file
            self.nerd_font_support = int(config_value)
        else:
            # Auto-detect Nerd Fonts
            self.nerd_font_support = check_nerd_fonts()

            # Save the detected value to config for future use
            if not self.custom_config:
                self.custom_config = {}
            if "display" not in self.custom_config:
                self.custom_config["display"] = {}
            self.custom_config["display"]["nerd_font_support"] = self.nerd_font_support
            self.save_config(self.custom_config)

    def _init_icon_manager(self) -> None:
        """Initialize the global icon manager with detected Nerd Font support."""
        try:
            from cli_utils.utils.icons import init_icon_manager
            init_icon_manager(self.nerd_font_support)
        except ImportError:
            # Icon manager not available, skip initialization
            pass


# Global settings instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get the global settings instance.

    Returns:
        Settings instance (creates one if it doesn't exist)
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset the global settings instance (useful for testing)."""
    global _settings
    _settings = None
