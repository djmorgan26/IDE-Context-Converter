"""Continue.dev adapter."""

import json
from pathlib import Path

from rich.console import Console

from ideporter.adapters.base import BaseAdapter
from ideporter.utils import load_json, safe_read, save_json

console = Console()


class ContinueAdapter(BaseAdapter):
    """Adapter for Continue.dev (.continue/config.json)."""

    @property
    def name(self) -> str:
        """Get the adapter name."""
        return "continue"

    def detect(self) -> bool:
        """Detect if Continue artifacts exist."""
        continue_dir = self.project_path / ".continue"
        config_file = continue_dir / "config.json"
        return config_file.exists()

    def import_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Import from .continue/config.json to canonical format."""
        continue_dir = self.project_path / ".continue"
        config_file = continue_dir / "config.json"

        if not config_file.exists():
            console.print("[yellow]⊘[/yellow] No .continue/config.json found")
            return

        try:
            config = load_json(config_file)
            console.print(f"[green]✓[/green] Read {config_file}")

            # Extract project prompts if they exist
            project_prompts = config.get("projectPrompts", [])

            if project_prompts:
                # Combine all prompts into rules
                rules_content = "# AI Project Rules\n\n"
                rules_content += "## Continue.dev Project Prompts\n\n"

                for prompt in project_prompts:
                    if isinstance(prompt, str):
                        rules_content += f"{prompt}\n\n"
                    elif isinstance(prompt, dict):
                        name = prompt.get("name", "Unnamed")
                        content = prompt.get("content", "")
                        rules_content += f"### {name}\n\n{content}\n\n"

                from ideporter.utils import safe_write

                rules_file = canonical_dir / "rules.md"
                safe_write(rules_file, rules_content, force=force, dry_run=dry_run)

            console.print("[green]✓[/green] Imported Continue context to canonical format")

        except json.JSONDecodeError as e:
            console.print(f"[red]✗[/red] Failed to parse config.json: {e}")

    def export_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Export from canonical format to .continue/config.json."""
        continue_dir = self.project_path / ".continue"
        config_file = continue_dir / "config.json"

        # Create .continue directory if it doesn't exist
        if not dry_run:
            continue_dir.mkdir(exist_ok=True)

        # Load existing config or create new one
        if config_file.exists():
            try:
                config = load_json(config_file)
            except json.JSONDecodeError:
                console.print("[yellow]⊘[/yellow] Invalid config.json, creating new one")
                config = {}
        else:
            config = {}

        # Read canonical rules
        rules_file = canonical_dir / "rules.md"
        if rules_file.exists():
            rules_content = safe_read(rules_file)

            # Create a reference to the canonical context
            project_prompts = config.get("projectPrompts", [])

            # Add a reference prompt pointing to canonical location
            reference_prompt = {
                "name": "AI Context (Canonical)",
                "content": f"See project AI context at: ai/context/rules.md\n\n{rules_content[:500]}...",
            }

            # Check if we already have this reference
            has_reference = any(
                isinstance(p, dict) and p.get("name") == "AI Context (Canonical)"
                for p in project_prompts
            )

            if not has_reference:
                project_prompts.append(reference_prompt)

            config["projectPrompts"] = project_prompts

            save_json(config_file, config, force=force, dry_run=dry_run)
            console.print("[green]✓[/green] Exported canonical context to Continue format")
        else:
            console.print("[yellow]⊘[/yellow] No rules.md to export")
