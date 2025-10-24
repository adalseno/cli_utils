# API Commands Examples

This guide shows how to create and use commands that interact with remote APIs.

## Weather API Example

A simple example command that fetches weather data from the Open-Meteo API.

### Basic Usage

Get weather information for a city:

```bash
cli-utils remote api-example weather milan
```

Output:
```
{'latitude': 45.48, 'longitude': 9.199999, 'generationtime_ms': 0.004291534423828125,
'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 128.0}
```

### Copy to Clipboard

Copy the result to your clipboard:

```bash
cli-utils remote api-example weather milan --copy
# or use the short flag
cli-utils remote api-example weather milan -c
```

The JSON output will be formatted and copied to your clipboard, ready to paste into other applications.

### Available Cities

The example currently supports:
- `mellieha` - Mellieha, Malta
- `milan` - Milan, Italy
- `paris` - Paris, France

### How It Works

This example demonstrates:
1. **Making API requests** - Using the `requests` library to fetch data
2. **Parsing JSON responses** - Converting API responses to Python dictionaries
3. **Clipboard integration** - Using the `copy_to_clipboard` utility
4. **Rich console output** - Displaying colored output with Rich

### Source Code

Location: `src/cli_utils/commands/remote/api_example/weather.py`

```python
"""Get weather for a specific city."""

import requests
import typer
from rich.console import Console

from cli_utils.utils.clipboard import copy_to_clipboard

console = Console()

def weather(
    city: str = typer.Argument(..., help="City to get weather for"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy result to clipboard"),
) -> None:
    """Get city weather.

    Example:
        $ cli-utils remote api-example weather milan
        $ cli-utils remote api-example weather milan --copy
    """
    cities = {
        "mellieha": {"latitude": "35.57", "longitude": "14.21"},
        "milan": {"latitude": "45.47", "longitude": "9.19"},
        "paris": {"latitude": "48.86", "longitude": "2.35"},
    }

    if city.lower() in cities:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={cities[city]['latitude']}&longitude={cities[city]['longitude']}"

        response = requests.get(url)
        result = response.json()

        console.print(f"[green]{result}[/green]")

        if copy:
            import json
            copy_to_clipboard(json.dumps(result, indent=2))
    else:
        console.print(f"[red]City {city} not found[/red]")
```

## Creating an API Command

Here's a template for creating API commands:

```python
# src/cli_utils/commands/remote/github/user_info.py
"""Fetch GitHub user information."""

import typer
import requests
from rich.console import Console
from rich.table import Table

from cli_utils.config import get_settings

console = Console()


def user_info(
    username: str = typer.Argument(..., help="GitHub username"),
) -> None:
    """Fetch and display GitHub user information.

    Args:
        username: GitHub username to look up

    Example:
        $ cli-utils remote github user-info octocat
    """
    settings = get_settings()
    timeout = settings.api_timeout

    try:
        response = requests.get(
            f"https://api.github.com/users/{username}",
            timeout=timeout,
        )
        response.raise_for_status()

        data = response.json()

        # Display in a nice table
        table = Table(title=f"GitHub User: {username}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Name", data.get("name", "N/A"))
        table.add_row("Bio", data.get("bio", "N/A"))
        table.add_row("Public Repos", str(data.get("public_repos", 0)))
        table.add_row("Followers", str(data.get("followers", 0)))

        console.print(table)

    except requests.RequestException as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
```

## Authentication

For APIs requiring authentication:

```python
def authenticated_api(
    endpoint: str = typer.Argument(..., help="API endpoint"),
) -> None:
    """Make authenticated API request."""
    settings = get_settings()

    # Get API token from config
    api_token = settings.get("api.service_name.token")

    if not api_token:
        console.print("[red]Error: API token not configured[/red]")
        console.print("Add it to ~/.config/cli-utils/config.yaml:")
        console.print("api:\n  service_name:\n    token: your_token_here")
        raise typer.Exit(1)

    headers = {"Authorization": f"Bearer {api_token}"}

    response = requests.get(
        endpoint,
        headers=headers,
        timeout=settings.api_timeout,
    )
    # ... handle response
```

## Error Handling

Always handle common API errors:

```python
try:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

except requests.Timeout:
    console.print("[red]Error: Request timed out[/red]")
    raise typer.Exit(1)

except requests.HTTPError as e:
    if e.response.status_code == 404:
        console.print("[red]Error: Resource not found[/red]")
    elif e.response.status_code == 401:
        console.print("[red]Error: Unauthorized - check your API key[/red]")
    else:
        console.print(f"[red]HTTP Error: {e}[/red]")
    raise typer.Exit(1)

except requests.RequestException as e:
    console.print(f"[red]Error: {e}[/red]")
    raise typer.Exit(1)
```

## Retry Logic

For flaky APIs, implement retry logic:

```python
from cli_utils.config import get_settings

def fetch_with_retry(url: str) -> dict:
    """Fetch URL with retry logic."""
    settings = get_settings()
    max_retries = settings.max_retries

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=settings.api_timeout)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            if attempt == max_retries - 1:
                raise
            console.print(f"[yellow]Retry {attempt + 1}/{max_retries}...[/yellow]")
```

## Best Practices

1. **Use timeouts**: Always set a timeout for requests
2. **Handle errors**: Provide clear error messages
3. **Use configuration**: Store API keys in config, not code
4. **Respect rate limits**: Add delays if needed
5. **Show progress**: Use Rich progress bars for long operations
6. **Validate input**: Check parameters before making requests
7. **Cache when appropriate**: Consider caching API responses

## Next Steps

- Learn about [Configuration](../user-guide/configuration.md)
- See how to [Add Commands](../user-guide/adding-commands.md)
