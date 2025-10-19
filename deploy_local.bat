@echo off
REM Edge Safety Monitor - Local Deployment Script for Windows
REM This script helps deploy the system locally

echo ==========================================
echo Edge Safety Monitor - Local Deployment
echo ==========================================
echo.

REM Check Python installation
echo Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo SUCCESS: Python %PYTHON_VERSION% found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo SUCCESS: Virtual environment created
) else (
    echo SUCCESS: Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo SUCCESS: Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo SUCCESS: Dependencies installed
echo.

REM Check model file
echo Checking model file...
if exist "models\ppe_detection_4classes\best.pt" (
    for %%A in (models\ppe_detection_4classes\best.pt) do set MODEL_SIZE=%%~zA
    echo SUCCESS: Model found
) else (
    echo WARNING: Model not found!
    echo Please ensure Git LFS is installed and run: git lfs pull
    pause
    exit /b 1
)
echo.

REM Create output directories
echo Creating output directories...
if not exist "outputs\safety_monitoring\" mkdir outputs\safety_monitoring
if not exist "logs\" mkdir logs
echo SUCCESS: Directories ready
echo.

REM Test imports
echo Testing Python imports...
python -c "import cv2; import torch; from ultralytics import YOLO; print('SUCCESS: All imports successful')"
if errorlevel 1 (
    echo ERROR: Import test failed
    pause
    exit /b 1
)
echo.

echo ==========================================
echo SUCCESS: Local Deployment Complete!
echo ==========================================
echo.
echo Quick Start Commands:
echo.
echo 1. Real-time webcam monitoring:
echo    python real_time_safety_monitor.py --source webcam
echo.
echo 2. Process video file:
echo    python real_time_safety_monitor.py --source video1.mp4
echo.
echo 3. Process image:
echo    python real_time_safety_monitor.py --source "construction workers_on site.jpeg"
echo.
echo 4. With custom confidence threshold:
echo    python real_time_safety_monitor.py --source webcam --conf 0.6
echo.
echo ==========================================
echo.
echo Virtual environment is activated. You can now run the commands above.
echo.
pause

