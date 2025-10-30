# TODO App

A full-featured terminal-based TODO application with reminders, built using the Textual TUI framework.

## Overview

The TODO app provides a modern, interactive interface for managing tasks with categories, progress tracking, due dates, and reminder notifications.

## Features

- **Task Management**: Create, edit, delete, and toggle tasks
- **Categories**: Organize tasks into customizable categories
- **Progress Tracking**: Track task completion percentage
- **Due Dates**: Set and monitor task deadlines
- **Reminders**: Schedule reminder notifications for tasks
- **Smart Lists**: Pre-built filters (All, Upcoming, Past Due, Completed)
- **Desktop Notifications**: Get notified when reminders are due
- **Background Service**: Auto-start reminder daemon at login
- **Smart Icons**: Automatic Nerd Font detection with emoji/text fallback

## Quick Start

### Launch the App

```bash
# Launch the TODO app
cli-utils local system-info todo
```

The app will open in a full-screen terminal interface with:
- **Left sidebar**: Smart lists and categories
- **Center panel**: Task list
- **Bottom bar**: Keyboard shortcuts

### Basic Usage

**Navigate:**
- `↑`/`↓` or `j`/`k` - Move between items
- `Tab` - Switch between sidebar and task list

**Manage Tasks:**
- `n` - Create new task
- `e` - Edit selected task
- `d` - Delete selected task
- `Space` - Toggle task completion
- `r` - Manage reminders for selected task

**Switch Views:**
- `k` - Show categories view (when in tasks)
- `t` - Show tasks view (when in categories)

**Exit:**
- `q` - Quit application

## Task Management

### Creating Tasks

1. Press `n` or type in the input box at the bottom
2. Fill in the task details:
   - **Name**: Task description (required)
   - **Category**: Select from dropdown
   - **Status**: New, In Progress, or Completed
   - **Progress**: 0-100%
   - **Due Date**: YYYY-MM-DD format
3. Press `Save` or `Enter`

**Example:**
```
Name: Complete project documentation
Category: Work
Status: In Progress
Progress: 50
Due Date: 2025-11-15
```

### Editing Tasks

1. Select a task
2. Press `e` to open edit screen
3. Modify any field
4. Press `Save`

### Completing Tasks

**Toggle Status:**
- Select a task and press `Space` to mark as completed/incomplete

**Manual Completion:**
- Edit the task and set Status to "Completed" or Progress to 100%

**With Reminders:**
When completing a task that has reminders, you'll see a confirmation dialog:
- **Remove Reminders**: Delete all reminders for the task
- **Keep Reminders**: Complete task but keep reminders active
- **Cancel**: Don't complete the task

## Categories

### Using Categories

Categories help organize tasks into logical groups. Built-in system categories:
- 📝 General (default)
- 💼 Work
- 🏠 Personal
- 📚 Study

### Managing Categories

1. Press `k` to switch to categories view
2. Use the same shortcuts:
   - `n` - New category
   - `e` - Edit category (custom categories only)
   - `d` - Delete category (custom categories only)
   - `t` - Return to tasks view

### Creating Custom Categories

1. In categories view, press `n`
2. Enter format: `CategoryName:Icon`
   - Example: `Shopping:🛒`
   - Example: `Health:💪`

## Reminders

### Setting Reminders

1. Select a task
2. Press `r` to open reminders screen
3. Click `Add` to create a new reminder
4. Enter date/time in format: `YYYY-MM-DD HH:MM`
   - Example: `2025-11-15 09:00`
5. Save the reminder

**Multiple Reminders:**
You can set multiple reminders for a single task (e.g., one day before, one hour before).

### Managing Reminders

**Edit:**
1. Select a reminder
2. Click `Edit` or press `e`
3. Update the date/time
4. Save

**Delete:**
1. Select a reminder
2. Click `Delete` or press `d`
3. Confirm deletion

### Reminder Notifications

When a reminder is due, you'll receive a desktop notification with:
- Task name
- Due date (if set)
- Current progress (if > 0%)

**Example Notification:**
```
⏰ Reminder: Complete project documentation
Task: Complete project documentation
Due: 2025-11-15
Progress: 50%
```

## Background Service

The reminder daemon runs in the background and checks for due reminders every 60 seconds.

### Installing the Service

```bash
# Install and enable auto-start at login
make install-todo-service
```

This will:
1. Copy the service file to `~/.config/systemd/user/`
2. Enable auto-start at login
3. Start the service immediately

### Managing the Service

**Check Status:**
```bash
# View service status
systemctl --user status todo-reminder.service

# Or use make target
make check-todo-service
```

**Control Service:**
```bash
# Stop service
systemctl --user stop todo-reminder.service

# Start service
systemctl --user start todo-reminder.service

# Restart service
systemctl --user restart todo-reminder.service
```

**View Logs:**
```bash
# Live logs from systemd
journalctl --user -u todo-reminder.service -f

# Or view daemon log file
tail -f ~/.config/cli_utils/logs/reminder_daemon.log
```

### Uninstalling the Service

```bash
# Stop and remove service
make uninstall-todo-service
```

## Smart Lists

Pre-built filters for quick task access:

### All Tasks
Shows all tasks regardless of status or due date.

### Upcoming
Tasks with due dates in the future.

### Past Due
Tasks with due dates that have passed.

### Completed
Tasks marked as completed.

## Data Storage

### Database Location
```
~/.config/cli_utils/todo.db
```

The app uses SQLite for data storage. All tasks, categories, and reminders are stored locally.

### Log Files
```
~/.config/cli_utils/logs/reminder_daemon.log
```

Daemon activity, notifications sent, and errors are logged here.

### Backup

To backup your tasks:
```bash
# Copy the database file
cp ~/.config/cli_utils/todo.db ~/backup/todo_backup.db

# Restore from backup
cp ~/backup/todo_backup.db ~/.config/cli_utils/todo.db
```

## Keyboard Reference

### Global
- `q` - Quit application
- `↑`/`↓` - Navigate up/down
- `Enter` - Select item
- `Esc` - Cancel input

### Task View
- `n` - New task
- `e` - Edit task
- `d` - Delete task
- `Space` - Toggle completion
- `r` - Manage reminders
- `k` - Switch to categories

### Category View
- `n` - New category
- `e` - Edit category
- `d` - Delete category
- `t` - Switch to tasks

## Examples

### Daily Workflow

**Morning Setup:**
```bash
# Launch app
cli-utils local system-info todo

# Review upcoming tasks (click "Upcoming" in sidebar)
# Set reminders for important tasks (press 'r')
# Update progress on ongoing tasks (press 'e')
```

**During the Day:**
- Receive reminder notifications
- Toggle tasks as complete (press `Space`)
- Add new tasks as they come up (press `n`)

**End of Day:**
- Review completed tasks (click "Completed")
- Plan tomorrow's tasks
- Set reminders for morning tasks

### Project Management Example

1. **Create Project Category:**
   - Press `k` for categories
   - Press `n` and enter: `MyProject:📊`

2. **Add Project Tasks:**
   ```
   Task 1: Research and planning
   Category: MyProject
   Status: New
   Due: 2025-11-10

   Task 2: Implementation
   Category: MyProject
   Status: New
   Due: 2025-11-20

   Task 3: Testing
   Category: MyProject
   Status: New
   Due: 2025-11-25
   ```

3. **Set Reminders:**
   - Day before each due date at 9:00 AM
   - Morning of due date at 8:00 AM

4. **Track Progress:**
   - Update progress percentage as you work
   - Toggle to completed when done

## Tips and Tricks

### Efficient Task Entry
Type directly in the input box at bottom of screen. The app will open the edit screen with the name pre-filled.

### Keyboard-First Workflow
All operations can be performed with keyboard shortcuts - no mouse needed!

### Reminder Strategy
- Set reminders 24 hours before for important tasks
- Set reminders 1 hour before for time-sensitive tasks
- Use multiple reminders for critical deadlines

### Progress Tracking
- Use 0% for not started
- Use 25%, 50%, 75% for active tasks
- Use 100% to auto-complete tasks

### Category Colors
Use emojis in category names for visual distinction:
- 🔥 Urgent
- ⭐ Priority
- 📅 Scheduled
- 💡 Ideas

## Troubleshooting

### Notifications Not Working

**Check if notify-send is installed:**
```bash
which notify-send
# If not found, install: sudo apt install libnotify-bin
```

**Check service status:**
```bash
make check-todo-service
```

**View daemon logs:**
```bash
tail -f ~/.config/cli_utils/logs/reminder_daemon.log
```

### Service Won't Start

**Check journalctl:**
```bash
journalctl --user -u todo-reminder.service -n 50
```

**Common issues:**
- Python environment not found: Ensure uv is installed
- Project path incorrect: Reinstall with `make install-todo-service`
- Database permissions: Check `~/.config/cli_utils/todo.db` permissions

### Database Issues

**Reset database (WARNING: deletes all data):**
```bash
rm ~/.config/cli_utils/todo.db
# Restart app to recreate
```

### Icons Showing Emoji Instead of Nerd Fonts

If you see emoji (👤 💼 ✅) instead of Nerd Font icons:

**For new categories (created after icon system install):**
1. Check if Nerd Fonts are installed:
   ```bash
   make check-nerdfonts
   ```

2. Ensure your terminal is using a Nerd Font
3. Restart the terminal and app

**For existing categories (created before icon system):**

Categories store their icons in the database. To migrate emoji to Nerd Fonts:

```bash
# Migrate all category icons
make migrate-icons
```

This will convert all emoji icons to their Nerd Font equivalents while preserving category data.

**What the migration does:**
- Updates Personal (👤 → 󰀄)
- Updates Work (💼 → 󰃖)
- Updates any custom categories with emoji icons
- Safe to run multiple times

## Architecture

### Components

**Main App (todo_app.py)**
- Textual TUI application
- Task and category views
- Sidebar navigation

**Database (database.py)**
- SQLite backend
- Task, category, and reminder storage
- Notification tracking

**Reminder Daemon (reminder_daemon.py)**
- Background service
- 60-second check interval
- Plugin-based notification system

**Notification Plugins**
- Base plugin architecture
- Desktop notification plugin (notify-send)
- Extensible for email, SMS, etc.

### Technology Stack

- **UI Framework**: Textual (Python TUI framework)
- **Database**: SQLite3
- **CLI Framework**: Typer
- **Service Manager**: systemd (Linux)
- **Notifications**: notify-send (Linux desktop)

## Future Enhancements

Potential features for future development:

- **Additional Notification Plugins**: Email, SMS, webhook
- **Task Priorities**: High, medium, low priority levels
- **Subtasks**: Break down tasks into smaller steps
- **Tags**: Cross-category task organization
- **Search**: Find tasks by name, date, or content
- **Recurring Tasks**: Automatic task creation on schedule
- **Export/Import**: JSON/CSV export for backup
- **Task Dependencies**: Link tasks with prerequisites
- **Time Tracking**: Log time spent on tasks
- **Reports**: Generate productivity reports

## Contributing

The TODO app is part of the CLI Utils project. To contribute:

1. Source code: `src/cli_utils/commands/local/system_info/_todo_app/`
2. Follow the project's contribution guidelines
3. Add tests for new features
4. Update documentation

## See Also

- [Command Reference](../reference/commands.md) - All CLI commands
- [Quick Reference](../reference/quick-reference.md) - Quick command guide
- [Makefile Reference](../reference/makefile.md) - Build automation
