# Makefile for CLI Utils project
# Automates common development tasks

.PHONY: help install install-dev test test-cov test-watch clean format lint check docs-build docs-serve run version check-nerdfonts migrate-icons

# Default target - show help
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
UV := uv
TEST ?= .
ARGS ?=

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)CLI Utils - Available Make Targets$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make test                                    # Run all tests"
	@echo "  make test TEST=test_config.py                # Run specific test file"
	@echo "  make test TEST=test_core ARGS='--no-cov -v'  # Run with custom args"
	@echo "  make test ARGS='-k test_uppercase'           # Run tests matching pattern"

install: ## Install project dependencies
	@echo "$(BLUE)Installing project dependencies...$(NC)"
	$(UV) sync
	@echo "$(GREEN)✓ Installation complete$(NC)"

install-dev: ## Install project with development dependencies
	@echo "$(BLUE)Installing project with dev dependencies...$(NC)"
	$(UV) sync --all-extras
	@echo "$(GREEN)✓ Development installation complete$(NC)"

test: ## Run tests (use TEST=path and ARGS='flags' to customize)
	@echo "$(BLUE)Running tests...$(NC)"
	$(UV) run pytest $(TEST) $(ARGS)

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(UV) run pytest --cov=cli_utils --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	$(UV) run ptw -- --testmon

clean: ## Clean up temporary files and caches
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	rm -rf src/site/ 2>/dev/null || true
	rm -rf dist/ 2>/dev/null || true
	rm -rf build/ 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	$(UV) run ruff format .
	@echo "$(GREEN)✓ Code formatted$(NC)"

lint: ## Run linting checks with ruff
	@echo "$(BLUE)Running linter...$(NC)"
	$(UV) run ruff check .

lint-fix: ## Run linting and auto-fix issues
	@echo "$(BLUE)Running linter with auto-fix...$(NC)"
	$(UV) run ruff check . --fix
	@echo "$(GREEN)✓ Linting complete$(NC)"

check: format lint ## Format and lint code
	@echo "$(GREEN)✓ All checks passed$(NC)"

docs-build: ## Build documentation with MkDocs
	@echo "$(BLUE)Building documentation...$(NC)"
	$(UV) run mkdocs build
	@echo "$(GREEN)✓ Documentation built in src/site/$(NC)"

docs-serve: ## Serve documentation locally
	@echo "$(BLUE)Starting documentation server...$(NC)"
	@echo "$(YELLOW)Visit http://127.0.0.1:8000$(NC)"
	$(UV) run mkdocs serve

docs-deploy: ## Deploy documentation to GitHub Pages (if configured)
	@echo "$(BLUE)Deploying documentation...$(NC)"
	$(UV) run mkdocs gh-deploy
	@echo "$(GREEN)✓ Documentation deployed$(NC)"

run: ## Run the CLI application with help
	@echo "$(BLUE)Running CLI Utils...$(NC)"
	$(UV) run python -m cli_utils.main --help

version: ## Display version information
	@echo "$(BLUE)CLI Utils Version Info$(NC)"
	$(UV) run python -m cli_utils.main version

# Development workflow targets
dev-setup: install-dev check-nerdfonts ## Complete development setup
	@echo "$(BLUE)Setting up development environment...$(NC)"
	@echo "$(GREEN)✓ Development environment ready$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Run tests: make test"
	@echo "  2. Format code: make format"
	@echo "  3. Build docs: make docs-serve"

check-nerdfonts: ## Check if Nerd Fonts are installed and update config
	@echo "$(BLUE)Checking for Nerd Fonts...$(NC)"
	@$(UV) run python scripts/check_nerdfonts.py

migrate-icons: ## Migrate TODO app category icons from emoji to Nerd Fonts
	@echo "$(BLUE)Migrating category icons to Nerd Fonts...$(NC)"
	@$(UV) run python scripts/migrate_category_icons.py

qa: clean format lint-fix test-cov ## Run full quality assurance (clean, format, lint, test)
	@echo "$(GREEN)✓ Quality assurance complete$(NC)"

ci: lint test-cov ## Run CI checks (lint and test with coverage)
	@echo "$(GREEN)✓ CI checks passed$(NC)"

# Project structure targets
tree: ## Show project structure
	@echo "$(BLUE)Project Structure:$(NC)"
	@tree -I '__pycache__|*.pyc|.pytest_cache|.ruff_cache|htmlcov|.venv|*.egg-info|site' -L 3 || \
		find . -not -path '*/\.*' -not -path '*/__pycache__/*' -not -path '*/htmlcov/*' \
		-not -path '*/.venv/*' -not -path '*/site/*' | head -50

init: ## Initialize a new command group
	@echo "$(BLUE)Command Group Creation$(NC)"
	@read -p "Category (local/remote): " category; \
	read -p "Group name (e.g., text_utils): " group; \
	mkdir -p src/cli_utils/commands/$$category/$$group; \
	touch src/cli_utils/commands/$$category/$$group/__init__.py; \
	echo "$(GREEN)✓ Created src/cli_utils/commands/$$category/$$group/$(NC)"

# Utility targets
.PHONY: install-uv
install-uv: ## Install uv package manager (if not present)
	@which uv > /dev/null || (echo "$(YELLOW)Installing uv...$(NC)" && curl -LsSf https://astral.sh/uv/install.sh | sh)

shell: ## Start an interactive Python shell with project loaded
	@echo "$(BLUE)Starting Python shell...$(NC)"
	$(UV) run python

coverage-open: ## Open coverage report in browser
	@echo "$(BLUE)Opening coverage report...$(NC)"
	@command -v xdg-open > /dev/null && xdg-open htmlcov/index.html || \
		command -v open > /dev/null && open htmlcov/index.html || \
		echo "$(YELLOW)Please open htmlcov/index.html manually$(NC)"

build: ## Build distribution packages
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(UV) build
	@echo "$(GREEN)✓ Packages built in dist/$(NC)"

# Git helpers
.PHONY: git-status
git-status: ## Show git status with helpful formatting
	@echo "$(BLUE)Git Status:$(NC)"
	@git status

# Container targets (for future use)
.PHONY: container-build container-run
container-build: ## Build Podman container (future)
	@echo "$(YELLOW)Container support coming soon...$(NC)"

container-run: ## Run application in container (future)
	@echo "$(YELLOW)Container support coming soon...$(NC)"

# System-wide installation targets
.PHONY: install-global uninstall-global link-global check-global install-aliases install-todo-service uninstall-todo-service check-todo-service
install-global: ## Install CLI globally by copying to ~/bin
	@echo "$(BLUE)Installing CLI Utils globally...$(NC)"
	@mkdir -p ~/bin
	@cp scripts/cli-utils ~/bin/cli-utils
	@chmod +x ~/bin/cli-utils
	@echo "$(GREEN)✓ Installed to ~/bin/cli-utils$(NC)"
	@echo ""
	@echo "$(YELLOW)Make sure ~/bin is in your PATH$(NC)"
	@echo "Add this to your ~/.zshrc if needed:"
	@echo "  export PATH=\"\$$HOME/bin:\$$PATH\""
	@echo ""
	@echo "Test with: cli-utils --help"

link-global: ## Create symlink in ~/bin (recommended for development)
	@echo "$(BLUE)Creating symlink in ~/bin...$(NC)"
	@mkdir -p ~/bin
	@ln -sf "$(CURDIR)/scripts/cli-utils" ~/bin/cli-utils
	@echo "$(GREEN)✓ Symlinked $(CURDIR)/scripts/cli-utils -> ~/bin/cli-utils$(NC)"
	@echo ""
	@echo "$(YELLOW)Make sure ~/bin is in your PATH$(NC)"
	@echo "Add this to your ~/.zshrc if needed:"
	@echo "  export PATH=\"\$$HOME/bin:\$$PATH\""
	@echo ""
	@echo "Test with: cli-utils --help"

uninstall-global: ## Remove CLI from ~/bin
	@echo "$(BLUE)Uninstalling CLI Utils from ~/bin...$(NC)"
	@rm -f ~/bin/cli-utils
	@echo "$(GREEN)✓ Removed ~/bin/cli-utils$(NC)"

check-global: ## Check if CLI is installed globally and working
	@echo "$(BLUE)Checking global installation...$(NC)"
	@if [ -f ~/bin/cli-utils ]; then \
		echo "$(GREEN)✓ Found ~/bin/cli-utils$(NC)"; \
		if [ -L ~/bin/cli-utils ]; then \
			echo "  Type: Symlink"; \
			echo "  Target: $$(readlink ~/bin/cli-utils)"; \
		else \
			echo "  Type: Copy"; \
		fi; \
		echo ""; \
		echo "Testing command:"; \
		~/bin/cli-utils --help 2>&1 | head -10; \
	else \
		echo "$(YELLOW)✗ Not found in ~/bin/cli-utils$(NC)"; \
		echo "Install with: make install-global or make link-global"; \
	fi

install-aliases: ## Add shell aliases to ~/.zshrc
	@echo "$(BLUE)Installing shell aliases...$(NC)"
	@ALIASES_PATH="$(CURDIR)/scripts/shell-aliases.sh"; \
	if grep -q "$$ALIASES_PATH" ~/.zshrc 2>/dev/null; then \
		echo "$(YELLOW)Aliases already configured in ~/.zshrc$(NC)"; \
	else \
		echo "" >> ~/.zshrc; \
		echo "# CLI Utils shortcuts" >> ~/.zshrc; \
		echo "source $$ALIASES_PATH" >> ~/.zshrc; \
		echo "$(GREEN)✓ Added to ~/.zshrc$(NC)"; \
	fi; \
	echo ""; \
	echo "$(YELLOW)Reload your shell or run:$(NC)"; \
	echo "  source ~/.zshrc"; \
	echo ""; \
	echo "$(YELLOW)Available shortcuts:$(NC)"; \
	echo "  textup, textlow, texttitle - Text conversion"; \
	echo "  cu, cul, cur, cuv, cuc     - CLI shortcuts"; \
	echo ""; \
	echo "See src/docs/reference/shell-aliases.md for details"

# TODO app reminder service targets
install-todo-service: ## Install and enable TODO app reminder service (systemd)
	@echo "$(BLUE)Installing TODO app reminder service...$(NC)"
	@mkdir -p ~/.config/systemd/user
	@# Replace PROJECT_DIR placeholder with actual path
	@sed 's|%h/Projects/Fadim/2025/cli_utils|$(CURDIR)|g' todo-reminder.service > ~/.config/systemd/user/todo-reminder.service
	@echo "$(GREEN)✓ Service file installed to ~/.config/systemd/user/$(NC)"
	@echo "  Project path: $(CURDIR)"
	@echo ""
	@echo "$(BLUE)Enabling and starting service...$(NC)"
	@systemctl --user daemon-reload
	@systemctl --user enable todo-reminder.service
	@systemctl --user start todo-reminder.service
	@echo "$(GREEN)✓ Service enabled and started$(NC)"
	@echo ""
	@echo "$(YELLOW)Service commands:$(NC)"
	@echo "  systemctl --user status todo-reminder.service  # Check status"
	@echo "  systemctl --user stop todo-reminder.service    # Stop service"
	@echo "  systemctl --user restart todo-reminder.service # Restart service"
	@echo "  journalctl --user -u todo-reminder.service -f  # View logs"
	@echo ""
	@echo "$(YELLOW)Service logs also available at:$(NC)"
	@echo "  ~/.config/cli_utils/logs/reminder_daemon.log"

uninstall-todo-service: ## Stop and remove TODO app reminder service
	@echo "$(BLUE)Removing TODO app reminder service...$(NC)"
	@systemctl --user stop todo-reminder.service 2>/dev/null || true
	@systemctl --user disable todo-reminder.service 2>/dev/null || true
	@rm -f ~/.config/systemd/user/todo-reminder.service
	@systemctl --user daemon-reload
	@echo "$(GREEN)✓ Service removed$(NC)"

check-todo-service: ## Check TODO app reminder service status
	@echo "$(BLUE)Checking TODO reminder service...$(NC)"
	@if [ -f ~/.config/systemd/user/todo-reminder.service ]; then \
		echo "$(GREEN)✓ Service file found$(NC)"; \
		echo ""; \
		echo "Service status:"; \
		systemctl --user status todo-reminder.service --no-pager || true; \
		echo ""; \
		echo "$(YELLOW)Recent logs:$(NC)"; \
		journalctl --user -u todo-reminder.service -n 10 --no-pager || true; \
	else \
		echo "$(YELLOW)✗ Service not installed$(NC)"; \
		echo "Install with: make install-todo-service"; \
	fi
