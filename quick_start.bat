@echo off
REM Edge Safety Monitor - Quick Start Script for Windows
REM This script automates the initial setup

echo ========================================
echo Edge Safety Monitor - Quick Start
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure Python is installed and in PATH
    pause
    exit /b 1
)
echo      Virtual environment created!
echo.

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo      Virtual environment activated!
echo.

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo      Pip upgraded!
echo.

echo [4/4] Installing dependencies...
echo      This may take several minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
    echo You can try installing them manually later
)
echo      Dependencies installed!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Test your environment: python scripts\test_baseline.py
echo   2. Download datasets:     python scripts\download_datasets.py
echo   3. Check GETTING_STARTED.md for detailed instructions
echo.
echo To activate virtual environment in the future:
echo   venv\Scripts\activate
echo.
pause

