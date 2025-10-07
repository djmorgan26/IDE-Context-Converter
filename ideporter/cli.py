"""CLI interface for IDE Context Porter."""

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ideporter.adapters import ADAPTERS, get_adapter
from ideporter.canonical import CanonicalContext

app = typer.Typer(
    name="ide-context-porter",
    help="Universal CLI tool to import, export, and convert AI project instructions between IDEs",
    add_completion=False,
)

console = Console()


@app.command()
def detect(
    path: Path | None = typer.Argument(
        None, help="Path to project (defaults to current directory)"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Detect IDE-specific artifacts and print a report."""
    project_path = path or Path.cwd()

    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        raise typer.Exit(1)

    detections = {}

    for adapter_name, adapter_class in ADAPTERS.items():
        adapter = adapter_class(project_path)
        detected = adapter.detect()
        detections[adapter_name] = detected

    if json_output:
        output = {
            "project_path": str(project_path.absolute()),
            "detections": detections,
        }
        print(json.dumps(output, indent=2))
    else:
        console.print("\n[bold]IDE Detection Report[/bold]")
        console.print(f"Project: {project_path.absolute()}\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("IDE", style="cyan")
        table.add_column("Status", style="green")

        for adapter_name, detected in detections.items():
            status = "✓ Detected" if detected else "⊘ Not found"
            style = "green" if detected else "dim"
            table.add_row(adapter_name.upper(), status, style=style)

        console.print(table)


@app.command()
def init(
    path: Path | None = typer.Argument(
        None, help="Path to project (defaults to current directory)"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview operations without making changes"),
) -> None:
    """Initialize the canonical ai/context/ structure with starter templates."""
    project_path = path or Path.cwd()

    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        raise typer.Exit(1)

    canonical = CanonicalContext(project_path)

    if canonical.exists() and not dry_run:
        console.print(
            f"[yellow]⊘[/yellow] Canonical context already exists at {canonical.context_dir}"
        )
        console.print("[dim]Existing files will be preserved[/dim]")

    canonical.initialize(dry_run=dry_run)

    if not dry_run:
        console.print(f"\n[green]✓[/green] Canonical context initialized at {canonical.context_dir}")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Edit ai/context/rules.md with your AI instructions")
        console.print("  2. Run 'ide-context-porter export --to <ide>' to sync to your IDE")


@app.command(name="import")
def import_context(
    from_ide: str = typer.Option(..., "--from", help="Source IDE (cursor, vscode, continue, claude, windsurf)"),
    path: Path | None = typer.Option(None, "--path", help="Path to project (defaults to current directory)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files without backup"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview operations without making changes"),
) -> None:
    """Import context from IDE-specific files to canonical format."""
    project_path = path or Path.cwd()

    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        raise typer.Exit(1)

    try:
        adapter_class = get_adapter(from_ide)
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1) from None

    # Initialize canonical context if it doesn't exist
    canonical = CanonicalContext(project_path)
    if not canonical.exists():
        console.print("[yellow]⊘[/yellow] Canonical context not found, initializing...")
        canonical.initialize(dry_run=dry_run)

    # Run import
    adapter = adapter_class(project_path)
    console.print(f"\n[bold]Importing from {from_ide.upper()}[/bold]")

    adapter.import_context(canonical.context_dir, force=force, dry_run=dry_run)

    # Update manifest
    if not dry_run:
        canonical.update_manifest(from_ide, dry_run=dry_run, force=force)

    console.print("\n[green]✓[/green] Import complete")


@app.command(name="export")
def export_context(
    to_ide: str = typer.Option(..., "--to", help="Target IDE (cursor, vscode, continue, claude, windsurf)"),
    path: Path | None = typer.Option(None, "--path", help="Path to project (defaults to current directory)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files without backup"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview operations without making changes"),
) -> None:
    """Export context from canonical format to IDE-specific files."""
    project_path = path or Path.cwd()

    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        raise typer.Exit(1)

    try:
        adapter_class = get_adapter(to_ide)
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1) from None

    # Check canonical context exists
    canonical = CanonicalContext(project_path)
    if not canonical.exists():
        console.print(f"[red]✗[/red] Canonical context not found at {canonical.context_dir}")
        console.print("[dim]Run 'ide-context-porter init' first[/dim]")
        raise typer.Exit(1)

    # Validate canonical context
    validation = canonical.validate()
    if not validation["valid"]:
        console.print("[red]✗[/red] Canonical context validation failed:")
        for issue in validation["issues"]:
            console.print(f"  • {issue}")
        raise typer.Exit(1)

    # Run export
    adapter = adapter_class(project_path)
    console.print(f"\n[bold]Exporting to {to_ide.upper()}[/bold]")

    adapter.export_context(canonical.context_dir, force=force, dry_run=dry_run)

    # Update manifest
    if not dry_run:
        canonical.update_manifest(to_ide, dry_run=dry_run, force=force)

    console.print("\n[green]✓[/green] Export complete")


@app.command()
def convert(
    from_ide: str = typer.Option(..., "--from", help="Source IDE"),
    to_ide: str = typer.Option(..., "--to", help="Target IDE"),
    path: Path | None = typer.Option(None, "--path", help="Path to project (defaults to current directory)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files without backup"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview operations without making changes"),
) -> None:
    """Convert context from one IDE format to another (import → export in one step)."""
    project_path = path or Path.cwd()

    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Converting {from_ide.upper()} → {to_ide.upper()}[/bold]\n")

    # Step 1: Import
    console.print(f"[bold cyan]Step 1:[/bold cyan] Importing from {from_ide.upper()}")
    try:
        adapter_class = get_adapter(from_ide)
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1) from None

    canonical = CanonicalContext(project_path)
    if not canonical.exists():
        console.print("[dim]Initializing canonical context...[/dim]")
        canonical.initialize(dry_run=dry_run)

    adapter = adapter_class(project_path)
    adapter.import_context(canonical.context_dir, force=force, dry_run=dry_run)

    if not dry_run:
        canonical.update_manifest(from_ide, dry_run=dry_run, force=force)

    # Step 2: Export
    console.print(f"\n[bold cyan]Step 2:[/bold cyan] Exporting to {to_ide.upper()}")
    try:
        adapter_class = get_adapter(to_ide)
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise typer.Exit(1) from None

    adapter = adapter_class(project_path)
    adapter.export_context(canonical.context_dir, force=force, dry_run=dry_run)

    if not dry_run:
        canonical.update_manifest(to_ide, dry_run=dry_run, force=force)

    console.print(f"\n[green]✓[/green] Conversion complete: {from_ide.upper()} → {to_ide.upper()}")


@app.command()
def validate(
    path: Path | None = typer.Argument(
        None, help="Path to project (defaults to current directory)"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Verify canonical files exist and are non-empty."""
    project_path = path or Path.cwd()

    if not project_path.exists():
        console.print(f"[red]✗[/red] Path does not exist: {project_path}")
        raise typer.Exit(1)

    canonical = CanonicalContext(project_path)
    validation = canonical.validate()

    if json_output:
        print(json.dumps(validation, indent=2))
    else:
        console.print("\n[bold]Validation Report[/bold]")
        console.print(f"Project: {project_path.absolute()}")
        console.print(f"Canonical: {canonical.context_dir}\n")

        if validation["valid"]:
            console.print("[green]✓ Validation passed[/green]")
        else:
            console.print("[red]✗ Validation failed[/red]")

        if validation["issues"]:
            console.print("\n[bold red]Issues:[/bold red]")
            for issue in validation["issues"]:
                console.print(f"  • {issue}")

        if validation["warnings"]:
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for warning in validation["warnings"]:
                console.print(f"  • {warning}")

    if not validation["valid"]:
        raise typer.Exit(1)


@app.callback()
def main() -> None:
    """IDE Context Porter - Move your project's AI prompts and context between IDEs."""
    pass


if __name__ == "__main__":
    app()
