# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial project structure with modular architecture
- Auto-discovery plugin system for commands
- Configuration management with YAML and environment variables
- Rich terminal output with colored formatting
- Example text utilities (uppercase, lowercase, titlecase)
- Comprehensive pytest testing framework
- MkDocs documentation with Material theme
- Makefile for common development tasks
- System-wide installation via wrapper script
- Shell wrapper script for global CLI access
- Global installation targets (link-global, install-global)
- Comprehensive documentation (README, Installation Guide, Makefile Reference, etc.)

### Fixed
- RuntimeWarning when running with `python -m cli_utils.main` by creating separate `__main__.py` entry point

### Technical Details
- Python 3.13+ required
- Uses uv as package manager
- Ruff for formatting and linting
- Three-level command hierarchy (category/group/command)
- Supports both local tasks and remote API commands

### Documentation
- Complete user guides and API reference
- Installation guide with multiple options
- Makefile command reference
- Scripts technical documentation

### Development
- Full development environment with Makefile
- Test coverage reporting
- Code quality checks (format, lint)
- Quick start script for new developers
