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
~/.config/cli_utils/config.yaml
```

### Example Configuration

```yaml
# Display settings
display:
  nerd_font_support: 1  # Auto-detected (1=enabled, 0=disabled)

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

## Icon and Display Settings

### Nerd Font Support

CLI Utils automatically detects if you have [Nerd Fonts](https://www.nerdfonts.com/) installed on your system. Nerd Fonts provide beautiful icons that enhance the visual appearance of the TODO app and other components.

The detection happens automatically on first run and the result is saved to your config file:

```yaml
display:
  nerd_font_support: 1  # 1 = Nerd Fonts available, 0 = not available
```

#### Check Nerd Font Status

You can check if Nerd Fonts are detected:

```bash
make check-nerdfonts
```

This will show:
- Whether Nerd Fonts are installed
- List of detected Nerd Fonts (if any)
- Instructions for installing Nerd Fonts

#### Icon Fallback System

The icon system has a 3-tier fallback mechanism:

1. **Nerd Font Icons** (if available) - Beautiful, consistent icons
2. **Emoji** (if terminal supports them) - Unicode emoji characters
3. **Text Representation** (always works) - Simple ASCII characters

This ensures the app works perfectly regardless of your font setup!

#### Installing Nerd Fonts

To get the best visual experience:

1. Visit [Nerd Fonts Downloads](https://www.nerdfonts.com/font-downloads)
2. Download and install your preferred font (FiraCode, JetBrainsMono, Hack, etc.)
3. Configure your terminal to use the Nerd Font
4. Restart your terminal
5. Run `make check-nerdfonts` to verify detection

#### Manual Override

If you want to force enable or disable Nerd Font usage, edit your config file:

```yaml
display:
  nerd_font_support: 0  # Force disable Nerd Fonts
```

Then restart the application. To re-enable auto-detection, delete this line from the config.

#### Migrating Existing Categories

If you're upgrading from an older version that used emoji icons, you can migrate your TODO app categories to use Nerd Fonts:

```bash
make migrate-icons
```

This will:
- Update all categories in the database to use Nerd Font icons
- Replace emoji (👤, 💼, etc.) with Nerd Font equivalents
- Preserve category names and descriptions

**Note:** This is a one-time migration. New categories created after installing the icon system will automatically use Nerd Fonts.

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
- Nerd Font support status
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
