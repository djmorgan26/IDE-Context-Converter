"""Cursor IDE adapter."""

from pathlib import Path

from rich.console import Console

from ideporter.adapters.base import BaseAdapter
from ideporter.utils import safe_read, safe_write

console = Console()


class CursorAdapter(BaseAdapter):
    """Adapter for Cursor IDE (.cursorrules, .cursorignore)."""

    @property
    def name(self) -> str:
        """Get the adapter name."""
        return "cursor"

    def detect(self) -> bool:
        """Detect if Cursor artifacts exist."""
        cursorrules = self.project_path / ".cursorrules"
        cursorignore = self.project_path / ".cursorignore"
        return cursorrules.exists() or cursorignore.exists()

    def import_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Import from .cursorrules and .cursorignore to canonical format."""
        cursorrules = self.project_path / ".cursorrules"
        cursorignore = self.project_path / ".cursorignore"

        rules_content = ""
        ignore_content = ""

        # Read .cursorrules
        if cursorrules.exists():
            rules_content = safe_read(cursorrules)
            console.print(f"[green]✓[/green] Read {cursorrules}")
        else:
            console.print("[yellow]⊘[/yellow] No .cursorrules found")

        # Read .cursorignore
        if cursorignore.exists():
            ignore_content = safe_read(cursorignore)
            console.print(f"[green]✓[/green] Read {cursorignore}")
        else:
            console.print("[yellow]⊘[/yellow] No .cursorignore found")

        # Write to canonical format
        if rules_content:
            rules_file = canonical_dir / "rules.md"
            # Wrap in markdown if not already formatted
            if not rules_content.startswith("#"):
                rules_content = f"# AI Project Rules\n\n{rules_content}"
            safe_write(rules_file, rules_content, force=force, dry_run=dry_run)

        if ignore_content:
            ignore_file = canonical_dir / "ignore.txt"
            safe_write(ignore_file, ignore_content, force=force, dry_run=dry_run)

        console.print("[green]✓[/green] Imported Cursor context to canonical format")

    def export_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Export from canonical format to .cursorrules and .cursorignore."""
        rules_file = canonical_dir / "rules.md"
        ignore_file = canonical_dir / "ignore.txt"

        # Export rules
        if rules_file.exists():
            rules_content = safe_read(rules_file)
            cursorrules = self.project_path / ".cursorrules"
            safe_write(cursorrules, rules_content, force=force, dry_run=dry_run)
        else:
            console.print("[yellow]⊘[/yellow] No rules.md to export")

        # Export ignore patterns
        if ignore_file.exists():
            ignore_content = safe_read(ignore_file)
            cursorignore = self.project_path / ".cursorignore"
            safe_write(cursorignore, ignore_content, force=force, dry_run=dry_run)
        else:
            console.print("[yellow]⊘[/yellow] No ignore.txt to export")

        console.print("[green]✓[/green] Exported canonical context to Cursor format")
