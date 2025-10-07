"""IDE adapters for context import/export."""

from ideporter.adapters.base import BaseAdapter
from ideporter.adapters.claude import ClaudeAdapter
from ideporter.adapters.continue_adapter import ContinueAdapter
from ideporter.adapters.cursor import CursorAdapter
from ideporter.adapters.vscode import VSCodeAdapter
from ideporter.adapters.windsurf import WindsurfAdapter

# Registry of available adapters
ADAPTERS: dict[str, type[BaseAdapter]] = {
    "cursor": CursorAdapter,
    "vscode": VSCodeAdapter,
    "continue": ContinueAdapter,
    "claude": ClaudeAdapter,
    "windsurf": WindsurfAdapter,
}


def get_adapter(name: str) -> type[BaseAdapter]:
    """Get an adapter by name.

    Args:
        name: Adapter name (cursor, vscode, etc.)

    Returns:
        Adapter class

    Raises:
        ValueError: If adapter not found
    """
    if name not in ADAPTERS:
        available = ", ".join(ADAPTERS.keys())
        raise ValueError(f"Unknown adapter '{name}'. Available: {available}")
    return ADAPTERS[name]


__all__ = [
    "BaseAdapter",
    "CursorAdapter",
    "VSCodeAdapter",
    "ContinueAdapter",
    "ClaudeAdapter",
    "WindsurfAdapter",
    "ADAPTERS",
    "get_adapter",
]
