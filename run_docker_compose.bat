@echo off
REM Edge Safety Monitor - Docker Compose Deployment

echo ======================================================================
echo Starting with Docker Compose...
echo ======================================================================

REM For webcam monitoring
docker-compose up safety-monitor

REM Or for video processing
REM docker-compose --profile batch up video-processor

pause

