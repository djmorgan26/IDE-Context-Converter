.PHONY: help install test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install package and dev dependencies"
	@echo "  make test       - Run pytest with coverage"
	@echo "  make lint       - Run ruff and mypy checks"
	@echo "  make format     - Format code with black and ruff"
	@echo "  make clean      - Remove build artifacts and cache"

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	ruff check ideporter tests
	mypy ideporter

format:
	ruff check --fix ideporter tests
	black ideporter tests

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
