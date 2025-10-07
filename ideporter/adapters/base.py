"""Base adapter interface for IDE context import/export."""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseAdapter(ABC):
    """Base class for IDE adapters."""

    def __init__(self, project_path: Path):
        """Initialize adapter.

        Args:
            project_path: Path to the project root
        """
        self.project_path = project_path

    @abstractmethod
    def detect(self) -> bool:
        """Detect if this IDE's artifacts exist in the project.

        Returns:
            True if IDE artifacts are detected
        """
        pass

    @abstractmethod
    def import_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Import context from IDE-specific files to canonical format.

        Args:
            canonical_dir: Path to canonical context directory
            force: Skip backups if True
            dry_run: Only preview operations if True
        """
        pass

    @abstractmethod
    def export_context(
        self, canonical_dir: Path, force: bool = False, dry_run: bool = False
    ) -> None:
        """Export context from canonical format to IDE-specific files.

        Args:
            canonical_dir: Path to canonical context directory
            force: Skip backups if True
            dry_run: Only preview operations if True
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the adapter name.

        Returns:
            Adapter name
        """
        pass
