"""Windsurf IDE adapter."""

from pathlib import Path

from rich.console import Console

from ideporter.adapters.base import BaseAdapter
from ideporter.utils import load_yaml, safe_read, safe_write, save_yaml

console = Console()


class WindsurfAdapter(BaseAdapter):
    """Adapter for Windsurf IDE (.windsurf/config.yaml)."""

    @property
    def name(self) -> str:
        """Get the adapter name."""
        return "windsurf"

    def detect(self) -> bool:
        """Detect if Windsurf artifacts exist."""
        windsurf_dir = self.project_path / ".windsurf"
        config_file = windsurf_dir / "config.yaml"
        return config_file.exists() or windsurf_dir.exists()

    def import_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Import from .windsurf/config.yaml to canonical format."""
        windsurf_dir = self.project_path / ".windsurf"
        config_file = windsurf_dir / "config.yaml"

        if not config_file.exists():
            console.print("[yellow]⊘[/yellow] No .windsurf/config.yaml found")
            return

        try:
            config = load_yaml(config_file)
            console.print(f"[green]✓[/green] Read {config_file}")

            # Extract AI rules if they exist
            ai_rules = config.get("ai_rules", "")
            ai_context = config.get("ai_context", "")

            if ai_rules:
                rules_content = "# AI Project Rules\n\n"
                rules_content += ai_rules

                rules_file = canonical_dir / "rules.md"
                safe_write(rules_file, rules_content, force=force, dry_run=dry_run)

            if ai_context:
                context_content = "# Project Context\n\n"
                context_content += ai_context

                context_file = canonical_dir / "context.md"
                safe_write(context_file, context_content, force=force, dry_run=dry_run)

            console.print("[green]✓[/green] Imported Windsurf context to canonical format")

        except Exception as e:
            console.print(f"[red]✗[/red] Failed to parse config.yaml: {e}")

    def export_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Export from canonical format to .windsurf/config.yaml."""
        windsurf_dir = self.project_path / ".windsurf"
        config_file = windsurf_dir / "config.yaml"

        # Create .windsurf directory if it doesn't exist
        if not dry_run:
            windsurf_dir.mkdir(exist_ok=True)

        # Load existing config or create new one
        if config_file.exists():
            try:
                config = load_yaml(config_file)
            except Exception:
                console.print("[yellow]⊘[/yellow] Invalid config.yaml, creating new one")
                config = {}
        else:
            config = {}

        # Read canonical content
        rules_file = canonical_dir / "rules.md"
        context_file = canonical_dir / "context.md"

        if rules_file.exists():
            rules_content = safe_read(rules_file)
            # Strip markdown header if present
            if rules_content.startswith("# "):
                lines = rules_content.split("\n", 1)
                if len(lines) > 1:
                    rules_content = lines[1].strip()

            config["ai_rules"] = rules_content

        if context_file.exists():
            context_content = safe_read(context_file)
            # Strip markdown header if present
            if context_content.startswith("# "):
                lines = context_content.split("\n", 1)
                if len(lines) > 1:
                    context_content = lines[1].strip()

            config["ai_context"] = context_content

        if config:
            save_yaml(config_file, config, force=force, dry_run=dry_run)
            console.print("[green]✓[/green] Exported canonical context to Windsurf format")
        else:
            console.print("[yellow]⊘[/yellow] No content to export")
