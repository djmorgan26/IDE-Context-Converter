"""Utility functions for IDE Context Porter."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console

console = Console()


def create_backup(file_path: Path) -> Path:
    """Create a timestamped backup of a file.

    Args:
        file_path: Path to the file to backup

    Returns:
        Path to the backup file
    """
    if not file_path.exists():
        return file_path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f"{file_path.suffix}.{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    console.print(f"[dim]Created backup: {backup_path}[/dim]")
    return backup_path


def safe_write(
    file_path: Path, content: str, force: bool = False, dry_run: bool = False
) -> None:
    """Safely write content to a file with backup and dry-run support.

    Args:
        file_path: Path to write to
        content: Content to write
        force: Skip backup creation if True
        dry_run: Only preview the operation if True
    """
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] Would write to {file_path}")
        console.print("[dim]Content preview (first 200 chars):[/dim]")
        console.print(f"[dim]{content[:200]}...[/dim]")
        return

    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create backup if file exists and force is not set
    if file_path.exists() and not force:
        create_backup(file_path)

    # Write the file
    file_path.write_text(content, encoding="utf-8")
    console.print(f"[green]✓[/green] Wrote {file_path}")


def safe_read(file_path: Path) -> str:
    """Safely read a file with error handling.

    Args:
        file_path: Path to read from

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return file_path.read_text(encoding="utf-8")


def load_yaml(file_path: Path) -> dict[str, Any]:
    """Load and parse a YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed YAML as dictionary
    """
    content = safe_read(file_path)
    return yaml.safe_load(content) or {}


def save_yaml(file_path: Path, data: dict[str, Any], force: bool = False, dry_run: bool = False) -> None:
    """Save data to a YAML file.

    Args:
        file_path: Path to save to
        data: Data to serialize
        force: Skip backup creation if True
        dry_run: Only preview the operation if True
    """
    content = yaml.safe_dump(data, default_flow_style=False, sort_keys=False)
    safe_write(file_path, content, force=force, dry_run=dry_run)


def load_json(file_path: Path) -> dict[str, Any]:
    """Load and parse a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON as dictionary
    """
    content = safe_read(file_path)
    result: dict[str, Any] = json.loads(content)
    return result


def save_json(
    file_path: Path, data: dict[str, Any], force: bool = False, dry_run: bool = False
) -> None:
    """Save data to a JSON file.

    Args:
        file_path: Path to save to
        data: Data to serialize
        force: Skip backup creation if True
        dry_run: Only preview the operation if True
    """
    content = json.dumps(data, indent=2, ensure_ascii=False)
    safe_write(file_path, content, force=force, dry_run=dry_run)


def is_ignored_path(path: Path) -> bool:
    """Check if a path should be ignored for security/safety.

    Args:
        path: Path to check

    Returns:
        True if path should be ignored
    """
    ignored_names = {
        ".env",
        ".git",
        "node_modules",
        "dist",
        "build",
        "__pycache__",
        ".venv",
        "venv",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    # Check if any part of the path matches ignored names
    for part in path.parts:
        if part in ignored_names:
            return True

    # Check for credential files
    if path.name.endswith((".key", ".pem", ".p12", ".pfx")):
        return True

    return False


def ensure_directory(path: Path, dry_run: bool = False) -> None:
    """Ensure a directory exists.

    Args:
        path: Directory path to create
        dry_run: Only preview the operation if True
    """
    if dry_run:
        if not path.exists():
            console.print(f"[yellow]DRY RUN:[/yellow] Would create directory {path}")
        return

    path.mkdir(parents=True, exist_ok=True)
