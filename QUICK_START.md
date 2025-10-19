# 🚀 Edge Safety Monitor - Quick Start

Get up and running in 5 minutes!

---

## ✅ Option 1: Run Immediately (Windows)

```cmd
REM 1. Run the automated deployment script
deploy_local.bat

REM 2. Start monitoring
python real_time_safety_monitor.py --source webcam
```

---

## ✅ Option 2: Run Immediately (Linux/Mac)

```bash
# 1. Run the automated deployment script
chmod +x deploy_local.sh
./deploy_local.sh

# 2. Start monitoring  
python real_time_safety_monitor.py --source webcam
```

---

## ✅ Option 3: Manual Setup (3 Steps)

### Windows
```cmd
REM Step 1: Activate virtual environment
venv\Scripts\activate

REM Step 2: Install dependencies (if not already done)
pip install -r requirements.txt

REM Step 3: Run the application
python real_time_safety_monitor.py --source webcam
```

### Linux/Mac
```bash
# Step 1: Activate virtual environment
source venv/bin/activate

# Step 2: Install dependencies (if not already done)
pip install -r requirements.txt

# Step 3: Run the application
python real_time_safety_monitor.py --source webcam
```

---

## 🎯 Common Use Cases

### 1. Monitor Construction Site (Webcam)
```bash
python real_time_safety_monitor.py --source webcam --conf 0.5
```
**Controls:** Press 'q' to quit, 's' to save snapshot

### 2. Analyze Existing Video
```bash
python real_time_safety_monitor.py --source video1.mp4
```
**Output:** Annotated video saved to `outputs/safety_monitoring/`

### 3. Check Safety in Image
```bash
python real_time_safety_monitor.py --source "construction workers_on site.jpeg"
```
**Output:** Analyzed image saved to `outputs/safety_monitoring/`

### 4. Stricter Detection (Higher Confidence)
```bash
python real_time_safety_monitor.py --source webcam --conf 0.7
```

### 5. More Sensitive Detection (Lower Confidence)
```bash
python real_time_safety_monitor.py --source webcam --conf 0.3
```

---

## 📊 What You'll See

### Real-time Display
```
┌──────────────────────────────────────────────┐
│  ⚠️ VIOLATION DETECTED  or  ✅ SAFETY COMPLIANT │
│                                              │
│  Workers: 3 | Hardhats: 2 | Masks: 1 | Vests: 2 │
│  Violations: No-Hat(1) | No-Mask(2) | No-Vest(1) │
│                                              │
│     [Live video feed with bounding boxes]    │
│                                              │
│  🚧 Cones: 2 | ⚙️ Machinery: 1 | 🚗 Vehicles: 0  │
│  2025-10-19 14:30:45                         │
└──────────────────────────────────────────────┘
```

### Console Output
```
📊 MONITORING SESSION SUMMARY
═══════════════════════════
Total Frames Processed: 1250
Violation Frames: 45
Safety Compliance Rate: 96.40%

PPE Detections Summary:
  👷 Hardhats: 234
  😷 Masks: 189
  🦺 Safety Vests: 245

Violations Detected:
  ❌ No-Hardhat: 12
  ❌ No-Mask: 28
  ❌ No-Safety Vest: 15
```

---

## 🐳 Docker Deployment (Alternative)

### Quick Docker Start
```bash
# Build image
docker build -t edge-safety-monitor .

# Run with docker-compose
docker-compose up safety-monitor

# Or run directly
docker run -it --rm \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/models:/app/models \
  edge-safety-monitor \
  python real_time_safety_monitor.py --source webcam
```

---

## ❓ Troubleshooting

### Model Not Found?
```bash
# Make sure Git LFS pulled the model
git lfs pull

# Verify model exists (5.2 MB)
# Windows: dir models\ppe_detection_4classes\best.pt
# Linux/Mac: ls -lh models/ppe_detection_4classes/best.pt
```

### Webcam Not Working?
```bash
# Test webcam access
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'ERROR')"

# Try different camera index
python real_time_safety_monitor.py --source 1  # or 2, 3, etc.
```

### Dependencies Issue?
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Slow Performance?
```bash
# Use lower confidence for faster processing
python real_time_safety_monitor.py --source webcam --conf 0.3

# Or process fewer frames (edit code)
```

---

## 📁 Output Files Location

All outputs are saved to:
```
outputs/safety_monitoring/
├── monitored_20251019_143045.mp4    # Processed videos
├── result_20251019_143112.jpg        # Processed images  
└── snapshot_20251019_143158.jpg      # Saved snapshots
```

---

## 🎓 Next Steps

1. **Customize Detection:**
   - Adjust confidence threshold (`--conf`)
   - Modify detection classes in code
   - Train on custom dataset

2. **Integration:**
   - Add email/SMS alerts
   - Connect to dashboard
   - Stream to cloud storage

3. **Scaling:**
   - Deploy to cloud (AWS, GCP, Azure)
   - Run on edge devices (Raspberry Pi, Jetson)
   - Process multiple camera feeds

4. **Read Full Documentation:**
   - [README.md](README.md) - Complete documentation
   - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed deployment
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

---

## 🆘 Need Help?

1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed troubleshooting
2. Review [README.md](README.md) for complete documentation
3. Check GitHub issues
4. Verify all prerequisites are installed

---

## ⚡ Performance Tips

- **CPU Only**: ~10-20 FPS
- **With GPU**: ~30-60 FPS
- **Best Practice**: conf=0.5 for balanced detection
- **For Speed**: conf=0.3, process fewer frames
- **For Accuracy**: conf=0.7, process all frames

---

**Ready to deploy? Run:**
```bash
# Windows
deploy_local.bat

# Linux/Mac
./deploy_local.sh
```

**Last Updated**: October 19, 2025  
**Version**: 1.0.0

