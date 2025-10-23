# Command Groups

Command groups help organize related commands together for better usability and maintainability.

## Group Structure

CLI Utils uses a hierarchical command structure:

```
cli-utils <category> <group> <command> [arguments] [options]
```

Example:
```bash
cli-utils local text-utils uppercase "hello"
         └────┘ └─────────┘ └───────┘
       category    group     command
```

## Categories

### Local Commands

Commands that run locally on your machine:

- File operations
- Text processing
- System utilities
- Data manipulation

Path: `src/cli_utils/commands/local/<group>/`

### Remote Commands

Commands that interact with remote APIs:

- API calls
- Web scraping
- Cloud service management
- Data fetching

Path: `src/cli_utils/commands/remote/<group>/`

## Creating a New Group

1. Create a directory under the appropriate category:

```bash
mkdir -p src/cli_utils/commands/local/my_new_group
```

2. Add an `__init__.py` file:

```bash
touch src/cli_utils/commands/local/my_new_group/__init__.py
```

3. Add command files:

```bash
touch src/cli_utils/commands/local/my_new_group/command1.py
touch src/cli_utils/commands/local/my_new_group/command2.py
```

That's it! The group is automatically discovered and available via CLI.

## Example Groups

### Text Utils (`text_utils`)

Text manipulation commands:

```bash
cli-utils local text-utils uppercase "text"
cli-utils local text-utils lowercase "TEXT"
cli-utils local text-utils titlecase "text"
```

### File Operations (`file_ops`)

File manipulation commands (to be implemented):

```bash
cli-utils local file-ops copy source.txt dest.txt
cli-utils local file-ops rename old.txt new.txt
```

### System Info (`system_info`)

System information commands (to be implemented):

```bash
cli-utils local system-info disk-usage
cli-utils local system-info cpu-info
```

## Group Naming Conventions

- Use lowercase with underscores: `text_utils`, `file_ops`
- CLI automatically converts to kebab-case: `text-utils`, `file-ops`
- Choose descriptive, functional names
- Keep group names concise but clear

## Group Organization Tips

1. **Logical grouping**: Group commands by functionality, not implementation
2. **Flat is better**: Avoid deep nesting; keep it at 3 levels maximum
3. **Single responsibility**: Each group should have a clear, focused purpose
4. **Reasonable size**: Aim for 5-15 commands per group

## Next Steps

- Learn how to [Add Commands](adding-commands.md)
- Check out [Examples](../examples/text-utils.md)
