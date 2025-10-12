#!/bin/bash
# Edge Safety Monitor - Quick Start Script for Linux/Mac
# This script automates the initial setup

echo "========================================"
echo "Edge Safety Monitor - Quick Start"
echo "========================================"
echo ""

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "Please ensure Python 3.8+ is installed"
    exit 1
fi
echo "     Virtual environment created!"
echo ""

echo "[2/4] Activating virtual environment..."
source venv/bin/activate
echo "     Virtual environment activated!"
echo ""

echo "[3/4] Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo "     Pip upgraded!"
echo ""

echo "[4/4] Installing dependencies..."
echo "     This may take several minutes..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "WARNING: Some packages may have failed to install"
    echo "You can try installing them manually later"
fi
echo "     Dependencies installed!"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Test your environment: python scripts/test_baseline.py"
echo "  2. Download datasets:     python scripts/download_datasets.py"
echo "  3. Check GETTING_STARTED.md for detailed instructions"
echo ""
echo "To activate virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""

