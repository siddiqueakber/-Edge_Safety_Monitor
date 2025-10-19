# 🚀 Edge Safety Monitor - Deployment Guide

Complete guide for deploying the Edge Safety Monitor system locally and on various platforms.

---

## 📋 Table of Contents

1. [Local Deployment (Recommended)](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Troubleshooting](#troubleshooting)

---

## 🏠 Local Deployment

### Windows Deployment

**Quick Start (Automated):**
```cmd
# Run the deployment script
deploy_local.bat
```

**Manual Steps:**
```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify model exists
dir models\ppe_detection_4classes\best.pt

# 5. Run the application
python real_time_safety_monitor.py --source webcam
```

### Linux/Mac Deployment

**Quick Start (Automated):**
```bash
# Make script executable
chmod +x deploy_local.sh

# Run deployment
./deploy_local.sh
```

**Manual Steps:**
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify model exists
ls -lh models/ppe_detection_4classes/best.pt

# 5. Run the application
python real_time_safety_monitor.py --source webcam
```

---

## 🐳 Docker Deployment

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)

### Build Docker Image

```bash
# Build the image
docker build -t edge-safety-monitor:latest .

# Verify build
docker images edge-safety-monitor
```

### Run with Docker Compose

**1. Webcam Monitoring:**
```bash
docker-compose up safety-monitor
```

**2. Process Video File:**
```bash
# Place video in ./videos/ directory
docker-compose --profile batch up video-processor
```

**3. Process Image:**
```bash
# Place image in ./images/ directory
docker-compose --profile batch up image-processor
```

### Run with Docker CLI

**Basic webcam monitoring (Linux/Mac):**
```bash
docker run -it --rm \
  --device /dev/video0:/dev/video0 \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/models:/app/models \
  edge-safety-monitor:latest \
  python real_time_safety_monitor.py --source webcam
```

**Windows (no webcam access in Docker):**
```bash
# Process video file instead
docker run -it --rm \
  -v %cd%/outputs:/app/outputs \
  -v %cd%/models:/app/models \
  -v %cd%/video1.mp4:/app/input.mp4 \
  edge-safety-monitor:latest \
  python real_time_safety_monitor.py --source /app/input.mp4
```

---

## ☁️ Cloud Deployment

### Option 1: AWS EC2

**Instance Requirements:**
- Instance Type: t3.large or better
- OS: Ubuntu 22.04 LTS
- Storage: 20GB+
- Security Group: Allow SSH (22)

**Setup Steps:**
```bash
# SSH to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Git and Git LFS
sudo apt install -y git git-lfs

# Clone repository
git clone https://github.com/siddiqueakber/-Edge_Safety_Monitor.git
cd -Edge_Safety_Monitor

# Pull LFS files
git lfs pull

# Run deployment script
chmod +x deploy_local.sh
./deploy_local.sh

# Run application
source venv/bin/activate
python real_time_safety_monitor.py --source webcam
```

### Option 2: Google Cloud

**VM Requirements:**
- Machine Type: n1-standard-2
- OS: Ubuntu 22.04
- Boot Disk: 20GB

**Setup Steps:**
```bash
# Create VM
gcloud compute instances create safety-monitor \
    --zone=us-central1-a \
    --machine-type=n1-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud

# SSH to VM
gcloud compute ssh safety-monitor

# Follow same steps as AWS
```

### Option 3: Azure

**VM Requirements:**
- VM Size: Standard_D2s_v3
- OS: Ubuntu 22.04

**Setup Steps:**
```bash
# Create VM
az vm create \
    --resource-group SafetyMonitorRG \
    --name SafetyMonitorVM \
    --image UbuntuLTS \
    --size Standard_D2s_v3

# SSH and follow AWS steps
```

---

## 🔧 Usage Examples

### Real-time Webcam Monitoring
```bash
python real_time_safety_monitor.py --source webcam --conf 0.5
```

### Process Video Files
```bash
# Single video
python real_time_safety_monitor.py --source video1.mp4

# Custom confidence
python real_time_safety_monitor.py --source video2.mp4 --conf 0.6
```

### Process Images
```bash
python real_time_safety_monitor.py --source "construction workers_on site.jpeg"
```

### Batch Processing
```bash
# Process all videos in directory
for video in *.mp4; do
    python real_time_safety_monitor.py --source "$video" --conf 0.5
done
```

---

## 🛠️ Troubleshooting

### Issue: Model Not Found

**Solution:**
```bash
# Check if Git LFS is installed
git lfs version

# If not installed, install it
# Windows: Download from https://git-lfs.github.com/
# Linux: sudo apt install git-lfs
# Mac: brew install git-lfs

# Pull LFS files
git lfs install
git lfs pull
```

### Issue: Webcam Not Detected

**Solution:**
```bash
# Linux/Mac - Check webcam
ls /dev/video*

# Test with OpenCV
python -c "import cv2; cap = cv2.VideoCapture(0); print('Webcam OK' if cap.isOpened() else 'Webcam Error')"

# Windows - Use Device Manager to verify camera
```

### Issue: Slow Performance

**Solutions:**
1. **Lower Confidence Threshold:**
   ```bash
   python real_time_safety_monitor.py --source webcam --conf 0.3
   ```

2. **Use GPU (if available):**
   - CUDA should be automatically detected
   - Verify: `python -c "import torch; print(torch.cuda.is_available())"`

3. **Process at lower resolution:**
   - Edit `real_time_safety_monitor.py`
   - Resize frames before processing

### Issue: Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Permission Denied (Linux/Mac)

**Solution:**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Logout and login again
```

---

## 📊 Performance Optimization

### For CPU-Only Systems
```bash
# Use smaller model (if available)
python real_time_safety_monitor.py --source webcam --conf 0.5

# Process every Nth frame
# Edit code to skip frames
```

### For GPU Systems
```bash
# Verify GPU is being used
python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"Not available\"}')"

# Monitor GPU usage
nvidia-smi -l 1
```

---

## 🔒 Production Deployment Checklist

- [ ] Model file downloaded (via Git LFS)
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Webcam/video source tested
- [ ] Output directories created
- [ ] Application runs without errors
- [ ] Performance is acceptable
- [ ] Logs are being generated
- [ ] Output files are saving correctly

---

## 📞 Support

For deployment issues:
1. Check logs in `logs/` directory
2. Verify all prerequisites are installed
3. Review this troubleshooting section
4. Check GitHub repository for updates

---

## 🎯 Quick Commands Reference

```bash
# Start monitoring
python real_time_safety_monitor.py --source webcam

# Stop monitoring
# Press 'q' in the application window

# View outputs
cd outputs/safety_monitoring
ls -lh

# View logs
tail -f logs/*.log

# Clean outputs
rm -rf outputs/safety_monitoring/*

# Update application
git pull
git lfs pull
pip install -r requirements.txt
```

---

**Last Updated**: October 19, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

