# Configuration

CLI Utils supports multiple configuration sources to customize its behavior.

## Configuration Sources

Configuration is loaded in the following priority order (later sources override earlier ones):

1. Default values
2. YAML configuration file
3. Environment variables

## Configuration File

The main configuration file is located at:

```
~/.config/cli-utils/config.yaml
```

### Example Configuration

```yaml
# API settings
api:
  timeout: 60
  max_retries: 5
  github:
    token: your_github_token_here

# Feature flags
features:
  debug: false
  experimental: false

# Custom settings
preferences:
  output_format: json
  color_scheme: dark
```

## Environment Variables

The following environment variables can be used to override settings:

- `CLI_UTILS_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `CLI_UTILS_API_TIMEOUT`: Set API timeout in seconds
- `CLI_UTILS_MAX_RETRIES`: Set maximum number of retries for API calls
- `CLI_UTILS_CONFIG_DIR`: Override the configuration directory location

### Example

```bash
export CLI_UTILS_LOG_LEVEL=DEBUG
export CLI_UTILS_API_TIMEOUT=60
cli-utils local text-utils uppercase "hello"
```

## Accessing Configuration in Commands

You can access configuration in your commands using the `get_settings()` function:

```python
from cli_utils.config import get_settings

def my_command():
    settings = get_settings()

    # Access built-in settings
    timeout = settings.api_timeout

    # Access custom config with dot notation
    github_token = settings.get("api.github.token")
    output_format = settings.get("preferences.output_format", "json")
```

## Viewing Current Configuration

You can view your current configuration at any time:

```bash
cli-utils config
```

This displays:
- Configuration directory location
- Log level
- API timeout
- Max retries
- Custom configuration file location

## Configuration for Development

When developing, you can use a `.env` file in your project root:

```bash
# .env
CLI_UTILS_LOG_LEVEL=DEBUG
CLI_UTILS_API_TIMEOUT=120
```

The `.env` file is automatically loaded when the application starts.

## Best Practices

1. **Never commit sensitive data**: Keep API tokens and credentials in environment variables or local config files
2. **Use .env for development**: Store development settings in `.env` (add it to `.gitignore`)
3. **Document custom settings**: If you add custom configuration options, document them
4. **Provide defaults**: Always provide sensible defaults for optional settings
