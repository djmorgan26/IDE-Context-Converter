@echo off
setlocal enabledelayedexpansion
title Publish Python Package to PyPI

REM === CONFIG ===
set PACKAGE_NAME=ide_context_porter
set PYPI_REPOSITORY=pypi
echo ======================================
echo Publishing !PACKAGE_NAME! to !PYPI_REPOSITORY!
echo ======================================

REM === CLEAN OLD BUILDS ===
echo 🧹 Cleaning old build artifacts...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%D in (*.egg-info) do rmdir /s /q "%%D"

REM === BUILD PACKAGE ===
echo 📦 Building the package...
python -m build
if %errorlevel% neq 0 (
    echo ❌ Build failed!
    exit /b %errorlevel%
)

REM === VERIFY DISTRIBUTION ===
echo 🔍 Checking distribution with Twine...
twine check dist/*
if %errorlevel% neq 0 (
    echo ❌ Twine check failed!
    exit /b %errorlevel%
)

REM === UPLOAD TO PYPI ===
echo 🚀 Uploading to %PYPI_REPOSITORY%...
twine upload --repository %PYPI_REPOSITORY% dist/*
if %errorlevel% neq 0 (
    echo ❌ Upload failed!
    exit /b %errorlevel%
)

REM === DONE ===
echo ✅ Successfully published %PACKAGE_NAME%!
pause
