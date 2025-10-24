"""Get weather for a specific city.

This module provides an example of a command that fetches weather data from an API.
"""

import requests
import typer
from rich.console import Console

from cli_utils.utils.clipboard import copy_to_clipboard

console = Console()



def weather(
    city: str = typer.Argument(..., help="City to get weather for"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy result to clipboard"),
)-> None:
    """Get city weather.

    Args:
        city: City to get weather for
        copy: If True, copy the result to clipboard (uses xclip/xsel/wl-copy on Linux)

    Example:
        $ cli-utils remote api_examples weather "milan"
        {'latitude': 45.48, 'longitude': 9.199999, 'generationtime_ms': 0.004291534423828125,
        'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 128.0}

        $ cli-utils remote api_examples weather "milan" --copy
        {'latitude': 45.48, 'longitude': 9.199999, 'generationtime_ms': 0.004291534423828125,
        'utc_offset_seconds': 0, 'timezone': 'GMT', 'timezone_abbreviation': 'GMT', 'elevation': 128.0}
        ✓ Copied to clipboard
    """

    cities ={"mellieha":{"latitude": "35.57", "longitude": "14.21"},
            "milan":{"latitude": "45.47", "longitude": "9.19"},
            "paris":{"latitude": "48.86", "longitude": "2.35"},}
    
    if city.lower() in cities:
        url = "https://api.open-meteo.com/v1/forecast?latitude=" + cities[city]["latitude"] + "&longitude=" + cities[city]["longitude"]

        response = requests.get(url)
        result = response.json()

        console.print(f"[green]{result}[/green]")

        if copy:
            import json
            copy_to_clipboard(json.dumps(result, indent=2))
    else:
        console.print(f"[red]City {city} not found[/red]")