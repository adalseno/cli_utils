# API Commands Examples

This guide shows how to create and use commands that interact with remote APIs.

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
