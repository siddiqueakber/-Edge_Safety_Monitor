@echo off
REM Edge Safety Monitor - Docker Deployment

echo ======================================================================
echo Building Docker Image...
echo ======================================================================
docker build -t edge-safety-monitor .

echo.
echo ======================================================================
echo Starting Safety Monitor with Docker...
echo ======================================================================
docker run -it --rm ^
  --device=/dev/video0:/dev/video0 ^
  -v "%cd%\outputs:/app/outputs" ^
  -v "%cd%\models:/app/models" ^
  edge-safety-monitor

pause

