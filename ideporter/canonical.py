"""Canonical context management for IDE Context Porter."""

from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console

from ideporter.utils import ensure_directory, load_yaml, safe_write, save_yaml

console = Console()

# Default canonical directory structure
CANONICAL_DIR = "ai/context"
CANONICAL_FILES = {
    "rules.md": "# AI Project Rules\n\nDefine your AI assistant's behavior and project-specific instructions here.\n",
    "context.md": "# Project Context\n\nArchitectural notes, domain knowledge, and other context for AI assistants.\n",
    "ignore.txt": "# Ignore patterns (glob-like)\n# Add file patterns that should be excluded from AI context\n\nnode_modules/\ndist/\nbuild/\n*.log\n.env\n",
    "extensions.json": '{\n  "recommendations": []\n}\n',
    "manifest.yaml": "",  # Generated dynamically
}


class CanonicalContext:
    """Manages the canonical AI context representation."""

    def __init__(self, base_path: Path):
        """Initialize canonical context manager.

        Args:
            base_path: Base path of the project
        """
        self.base_path = base_path
        self.context_dir = base_path / CANONICAL_DIR

    def exists(self) -> bool:
        """Check if canonical context directory exists.

        Returns:
            True if context directory exists
        """
        return self.context_dir.exists()

    def validate(self) -> dict[str, Any]:
        """Validate the canonical context structure.

        Returns:
            Validation report with status and issues
        """
        issues = []
        warnings = []

        if not self.exists():
            return {
                "valid": False,
                "issues": ["Canonical context directory does not exist"],
                "warnings": [],
            }

        # Check for required files
        rules_file = self.context_dir / "rules.md"
        manifest_file = self.context_dir / "manifest.yaml"

        if not rules_file.exists():
            issues.append("Missing required file: rules.md")
        elif rules_file.stat().st_size == 0:
            warnings.append("rules.md is empty")

        if not manifest_file.exists():
            warnings.append("Missing manifest.yaml (will be auto-generated)")

        # Check for optional files
        context_file = self.context_dir / "context.md"
        if context_file.exists() and context_file.stat().st_size == 0:
            warnings.append("context.md exists but is empty")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
        }

    def initialize(self, dry_run: bool = False) -> None:
        """Initialize the canonical context structure.

        Args:
            dry_run: Only preview the operation if True
        """
        if dry_run:
            console.print(f"[yellow]DRY RUN:[/yellow] Would initialize {self.context_dir}")
            for filename in CANONICAL_FILES:
                console.print(f"  [dim]Would create: {filename}[/dim]")
            return

        # Create directory
        ensure_directory(self.context_dir, dry_run=dry_run)

        # Create files
        for filename, default_content in CANONICAL_FILES.items():
            file_path = self.context_dir / filename

            # Skip if file already exists
            if file_path.exists():
                console.print(f"[yellow]⊘[/yellow] Skipped {filename} (already exists)")
                continue

            # Generate manifest dynamically
            if filename == "manifest.yaml":
                manifest_data = self._create_manifest()
                save_yaml(file_path, manifest_data, dry_run=dry_run)
            else:
                safe_write(file_path, default_content, dry_run=dry_run)

        console.print(f"[green]✓[/green] Initialized canonical context at {self.context_dir}")

    def _create_manifest(self, adapters_used: list[str] | None = None) -> dict[str, Any]:
        """Create a manifest dictionary.

        Args:
            adapters_used: List of adapter names that were used

        Returns:
            Manifest data dictionary
        """
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "adapters_used": adapters_used or [],
        }

    def update_manifest(
        self, adapter_name: str, dry_run: bool = False, force: bool = False
    ) -> None:
        """Update the manifest with adapter usage.

        Args:
            adapter_name: Name of the adapter that was used
            dry_run: Only preview the operation if True
            force: Skip backup creation if True
        """
        manifest_file = self.context_dir / "manifest.yaml"

        # Load existing manifest or create new one
        if manifest_file.exists():
            manifest = load_yaml(manifest_file)
        else:
            manifest = self._create_manifest()

        # Update fields
        manifest["last_updated"] = datetime.now().isoformat()

        adapters_used = manifest.get("adapters_used", [])
        if adapter_name not in adapters_used:
            adapters_used.append(adapter_name)
        manifest["adapters_used"] = adapters_used

        # Save manifest
        save_yaml(manifest_file, manifest, force=force, dry_run=dry_run)

    def get_rules(self) -> str:
        """Get the content of rules.md.

        Returns:
            Rules content
        """
        rules_file = self.context_dir / "rules.md"
        if not rules_file.exists():
            return ""
        return rules_file.read_text(encoding="utf-8")

    def get_context(self) -> str:
        """Get the content of context.md.

        Returns:
            Context content
        """
        context_file = self.context_dir / "context.md"
        if not context_file.exists():
            return ""
        return context_file.read_text(encoding="utf-8")

    def get_ignore_patterns(self) -> list[str]:
        """Get ignore patterns from ignore.txt.

        Returns:
            List of ignore patterns
        """
        ignore_file = self.context_dir / "ignore.txt"
        if not ignore_file.exists():
            return []

        content = ignore_file.read_text(encoding="utf-8")
        patterns = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
        return patterns

    def get_extensions(self) -> list[str]:
        """Get recommended extensions from extensions.json.

        Returns:
            List of extension IDs
        """
        import json

        extensions_file = self.context_dir / "extensions.json"
        if not extensions_file.exists():
            return []

        content = extensions_file.read_text(encoding="utf-8")
        data: dict[str, Any] = json.loads(content)
        recommendations: list[str] = data.get("recommendations", [])
        return recommendations
