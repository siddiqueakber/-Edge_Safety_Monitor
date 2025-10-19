@echo off
REM Edge Safety Monitor - Quick Launch Script
REM Double-click this file to start monitoring

title Edge Safety Monitor - Construction Site Safety Detection

cd /d "C:\Users\abub7\OneDrive\Desktop\Main project"

echo ======================================================================
echo 🦺 EDGE SAFETY MONITOR - Starting...
echo ======================================================================
echo.
echo System: Local PC Deployment
echo Source: Webcam
echo Confidence: 0.5 (50%%)
echo.
echo Controls:
echo   - Press 'q' to quit
echo   - Press 's' to save snapshot
echo.
echo ======================================================================
echo.

venv\Scripts\python.exe real_time_safety_monitor.py --source webcam --conf 0.5

echo.
echo ======================================================================
echo Monitoring session ended.
echo Check outputs in: outputs\safety_monitoring\
echo ======================================================================
pause

