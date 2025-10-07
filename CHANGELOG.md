# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-07

### Added

- Initial release of IDE Context Porter
- Core canonical context management system (`ai/context/` structure)
- CLI interface with Typer
- Support for 5 IDE adapters:
  - **Cursor**: Full bidirectional support (`.cursorrules`, `.cursorignore`)
  - **VS Code**: Full bidirectional support (`.vscode/AI_RULES.md`, `.vscode/AI_CONTEXT.md`)
  - **Continue.dev**: Full bidirectional support (`.continue/config.json`)
  - **Claude Code**: Export support with manual import instructions
  - **Windsurf**: Full bidirectional support (`.windsurf/config.yaml`)
- CLI commands:
  - `detect`: Detect IDE artifacts in a project
  - `init`: Initialize canonical context structure
  - `import`: Import from IDE to canonical format
  - `export`: Export from canonical to IDE format
  - `convert`: One-step conversion between IDEs
  - `validate`: Validate canonical context
- Safety features:
  - Automatic timestamped backups before overwrites
  - `--dry-run` mode for previewing operations
  - `--force` flag to skip backups
  - Security: Ignores sensitive files (`.env`, `.git`, credentials)
- Developer tooling:
  - Comprehensive test suite (61 tests, 87% coverage)
  - Pre-commit hooks (ruff, black, mypy)
  - GitHub Actions CI/CD workflow
  - Type checking with mypy
  - Code formatting with black and ruff
- Documentation:
  - Comprehensive README with usage examples
  - Contributing guidelines
  - MIT License
  - Example project demo usage

### Technical Details

- Python 3.11+ required
- Built with Typer for CLI
- Uses Rich for beautiful terminal output
- PyYAML for configuration files
- Cross-platform support (Windows, macOS, Linux)
- Offline-first (no network calls or telemetry)
- Idempotent operations

[0.1.0]: https://github.com/djmorgan26/IDE-Context-Converter/releases/tag/v0.1.0
