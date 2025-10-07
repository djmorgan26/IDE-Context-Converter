"""VS Code adapter."""

from pathlib import Path

from rich.console import Console

from ideporter.adapters.base import BaseAdapter
from ideporter.utils import safe_read, safe_write

console = Console()


class VSCodeAdapter(BaseAdapter):
    """Adapter for VS Code (.vscode/AI_RULES.md, .vscode/AI_CONTEXT.md)."""

    @property
    def name(self) -> str:
        """Get the adapter name."""
        return "vscode"

    def detect(self) -> bool:
        """Detect if VS Code artifacts exist."""
        vscode_dir = self.project_path / ".vscode"
        if not vscode_dir.exists():
            return False

        ai_rules = vscode_dir / "AI_RULES.md"
        ai_context = vscode_dir / "AI_CONTEXT.md"
        settings = vscode_dir / "settings.json"

        return ai_rules.exists() or ai_context.exists() or settings.exists()

    def import_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Import from .vscode/AI_RULES.md and AI_CONTEXT.md to canonical format."""
        vscode_dir = self.project_path / ".vscode"

        if not vscode_dir.exists():
            console.print("[yellow]⊘[/yellow] No .vscode directory found")
            return

        ai_rules = vscode_dir / "AI_RULES.md"
        ai_context = vscode_dir / "AI_CONTEXT.md"
        extensions_file = vscode_dir / "extensions.json"

        # Import rules
        if ai_rules.exists():
            rules_content = safe_read(ai_rules)
            rules_out = canonical_dir / "rules.md"
            safe_write(rules_out, rules_content, force=force, dry_run=dry_run)
            console.print(f"[green]✓[/green] Imported {ai_rules}")
        else:
            console.print("[yellow]⊘[/yellow] No AI_RULES.md found")

        # Import context
        if ai_context.exists():
            context_content = safe_read(ai_context)
            context_out = canonical_dir / "context.md"
            safe_write(context_out, context_content, force=force, dry_run=dry_run)
            console.print(f"[green]✓[/green] Imported {ai_context}")
        else:
            console.print("[yellow]⊘[/yellow] No AI_CONTEXT.md found")

        # Import extensions
        if extensions_file.exists():
            extensions_out = canonical_dir / "extensions.json"
            extensions_content = safe_read(extensions_file)
            safe_write(extensions_out, extensions_content, force=force, dry_run=dry_run)
            console.print(f"[green]✓[/green] Imported {extensions_file}")

        console.print("[green]✓[/green] Imported VS Code context to canonical format")

    def export_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Export from canonical format to .vscode/AI_RULES.md and AI_CONTEXT.md."""
        vscode_dir = self.project_path / ".vscode"

        # Create .vscode directory if it doesn't exist
        if not dry_run:
            vscode_dir.mkdir(exist_ok=True)

        rules_file = canonical_dir / "rules.md"
        context_file = canonical_dir / "context.md"
        extensions_file = canonical_dir / "extensions.json"

        # Export rules
        if rules_file.exists():
            rules_content = safe_read(rules_file)
            ai_rules = vscode_dir / "AI_RULES.md"
            safe_write(ai_rules, rules_content, force=force, dry_run=dry_run)
        else:
            console.print("[yellow]⊘[/yellow] No rules.md to export")

        # Export context
        if context_file.exists():
            context_content = safe_read(context_file)
            ai_context = vscode_dir / "AI_CONTEXT.md"
            safe_write(ai_context, context_content, force=force, dry_run=dry_run)
        else:
            console.print("[yellow]⊘[/yellow] No context.md to export")

        # Export extensions
        if extensions_file.exists():
            extensions_out = vscode_dir / "extensions.json"
            extensions_content = safe_read(extensions_file)
            safe_write(extensions_out, extensions_content, force=force, dry_run=dry_run)

        console.print("[green]✓[/green] Exported canonical context to VS Code format")
