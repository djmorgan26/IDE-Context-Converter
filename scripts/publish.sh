#!/usr/bin/env bash
set -e  # Exit immediately if a command exits with a non-zero status.

# === CONFIG ===
PACKAGE_NAME="ide_context_porter"
PYPI_REPOSITORY="pypi"  # or "testpypi" if testing

# === CLEAN OLD BUILDS ===
echo "🧹 Cleaning old build artifacts..."
rm -rf dist build *.egg-info

# === BUILD PACKAGE ===
echo "📦 Building the package..."
python -m build

# === VERIFY DISTRIBUTION ===
echo "🔍 Checking distribution with Twine..."
twine check dist/*

# === UPLOAD TO PYPI ===
echo "🚀 Uploading to ${PYPI_REPOSITORY}..."
twine upload --repository ${PYPI_REPOSITORY} dist/*

# === DONE ===
echo "✅ Successfully published ${PACKAGE_NAME}!"
