#!/bin/bash

# Edge Safety Monitor - Local Deployment Script
# This script helps deploy the system locally without Docker

set -e

echo "=========================================="
echo "🦺 Edge Safety Monitor - Local Deployment"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking prerequisites..."
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.12+"
    exit 1
fi

PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📝 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "📝 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "📝 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check model file
echo ""
echo "📝 Checking model file..."
if [ -f "models/ppe_detection_4classes/best.pt" ]; then
    MODEL_SIZE=$(du -h models/ppe_detection_4classes/best.pt | cut -f1)
    echo "✅ Model found (${MODEL_SIZE})"
else
    echo "⚠️  Model not found!"
    echo "   Please ensure Git LFS is installed and run: git lfs pull"
    exit 1
fi

# Create output directories
echo ""
echo "📝 Creating output directories..."
mkdir -p outputs/safety_monitoring
mkdir -p logs
echo "✅ Directories ready"

# Test imports
echo ""
echo "📝 Testing Python imports..."
$PYTHON_CMD -c "
import cv2
import torch
from ultralytics import YOLO
print('✅ All imports successful')
" 2>&1

echo ""
echo "=========================================="
echo "✅ Local Deployment Complete!"
echo "=========================================="
echo ""
echo "🎯 Quick Start Commands:"
echo ""
echo "# Activate virtual environment first:"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "source venv/Scripts/activate"
else
    echo "source venv/bin/activate"
fi
echo ""
echo "# Real-time webcam monitoring:"
echo "python real_time_safety_monitor.py --source webcam"
echo ""
echo "# Process video file:"
echo "python real_time_safety_monitor.py --source video1.mp4"
echo ""
echo "# Process image:"
echo "python real_time_safety_monitor.py --source construction*.jpeg"
echo ""
echo "# With custom confidence threshold:"
echo "python real_time_safety_monitor.py --source webcam --conf 0.6"
echo ""
echo "=========================================="

