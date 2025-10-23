"""Main CLI application entry point.

This module creates the main Typer application and automatically loads
all commands from the commands directory using the plugin loader.
"""

import typer
from rich.console import Console
from rich.panel import Panel

from cli_utils.config import get_settings
from cli_utils.core.plugin_loader import create_plugin_loader

# Create rich console for enhanced output
console = Console()

# Create main Typer app with rich support
app = typer.Typer(
    name="cli-utils",
    help="A modern CLI application to organize and manage Python scripts",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Display version information."""
    from importlib.metadata import version as get_version

    try:
        app_version = get_version("cli-utils")
    except Exception:
        app_version = "0.1.0"

    console.print(
        Panel.fit(
            f"[bold cyan]CLI Utils[/bold cyan] v{app_version}\n"
            "[dim]A modern CLI application for managing scripts and utilities[/dim]",
            border_style="cyan",
        )
    )


@app.command()
def config() -> None:
    """Display current configuration."""
    settings = get_settings()

    config_info = f"""[bold]Configuration Settings[/bold]

[cyan]Config Directory:[/cyan] {settings.config_dir}
[cyan]Log Level:[/cyan] {settings.log_level}
[cyan]API Timeout:[/cyan] {settings.api_timeout}s
[cyan]Max Retries:[/cyan] {settings.max_retries}

[dim]Custom config loaded from: {settings.config_dir / "config.yaml"}[/dim]
"""

    console.print(Panel(config_info, border_style="cyan", title="Configuration"))


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """CLI Utils - Manage your scripts and utilities with ease."""
    if verbose:
        settings = get_settings()
        settings.log_level = "DEBUG"
        console.print("[dim]Verbose mode enabled[/dim]")


def run() -> None:
    """Load plugins and run the application.

    This function is called when the package is installed and run via the entry point.
    """
    # Load all commands using the plugin loader
    loader = create_plugin_loader(app)
    loader.load_all_commands()

    # Run the Typer app
    app()
