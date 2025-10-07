"""Pytest configuration and fixtures."""


import pytest


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def canonical_context(temp_project):
    """Create a canonical context structure."""
    from ideporter.canonical import CanonicalContext

    canonical = CanonicalContext(temp_project)
    canonical.initialize(dry_run=False)
    return canonical


@pytest.fixture
def sample_rules():
    """Sample rules content."""
    return """# AI Project Rules

## Code Style
- Use Python 3.11+
- Follow PEP 8
- Use type hints

## Testing
- Write pytest tests
- Aim for 80% coverage
"""


@pytest.fixture
def sample_context():
    """Sample context content."""
    return """# Project Context

## Architecture
This is a CLI tool built with Typer.

## Domain
Developer tooling for AI IDE integration.
"""


@pytest.fixture
def sample_ignore():
    """Sample ignore patterns."""
    return """# Ignore patterns
node_modules/
dist/
*.log
.env
"""
