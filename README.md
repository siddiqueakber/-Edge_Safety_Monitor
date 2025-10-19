# 🦺 Edge Safety Monitor - Construction Site Safety Detection

**Real-time PPE compliance monitoring system using YOLOv8 for construction site safety**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-brightgreen.svg)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Overview

The **Edge Safety Monitor** is a production-ready computer vision system that detects Personal Protective Equipment (PPE) compliance in real-time on construction sites. It monitors workers for proper safety equipment usage and generates alerts for violations.

### Key Features

- 🎥 **Real-time Detection** - Live webcam monitoring with instant feedback
- 📹 **Video Analysis** - Process construction site videos frame-by-frame
- 📸 **Image Processing** - Analyze static images for PPE compliance
- 🧢 **Multi-class Detection** - Detects 10 different PPE and equipment classes
- 📊 **Compliance Reporting** - Detailed statistics and violation tracking
- 🟢🔴 **Status Indicators** - Visual feedback (Green = Safe, Red = Violation)
- 💾 **Output Generation** - Annotated videos and snapshots
- ⚡ **CPU/GPU Ready** - Works on any device (optimized for edge deployment)

---

## 📋 Detection Classes

The model detects **10 different classes**:

| Class | Type | Purpose |
|-------|------|---------|
| 🧢 **Hardhat** | Safe | Safety hard hat detected |
| 😷 **Mask** | Safe | Face mask detected |
| 🦺 **Safety Vest** | Safe | High-visibility vest detected |
| ❌ **NO-Hardhat** | Violation | Worker without hard hat |
| ❌ **NO-Mask** | Violation | Worker without mask |
| ❌ **NO-Safety Vest** | Violation | Worker without vest |
| 👤 **Person** | Context | Worker/person detected |
| 🚧 **Safety Cone** | Equipment | Safety cone detected |
| ⚙️ **Machinery** | Equipment | Heavy machinery detected |
| 🚗 **Vehicle** | Equipment | Vehicle detected |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip
- Webcam (for live monitoring) or video files
- 4GB+ RAM recommended

### Installation

```bash
# 1. Clone the repository (includes model via Git LFS)
git clone https://github.com/siddiqueakber/-Edge_Safety_Monitor.git
cd -Edge_Safety_Monitor

# 2. Install Git LFS (if not already installed)
# Download from: https://git-lfs.github.com/
# The trained model files are stored with Git LFS

# 3. Pull LFS files (model weights)
git lfs pull

# 4. Create virtual environment
python -m venv venv

# 5. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt
```

**📦 Model Download**: The trained model (`models/ppe_detection_4classes/best.pt` - 5.2 MB) is included via **Git LFS**. Make sure Git LFS is installed before cloning.

### Usage

#### 1. Real-time Webcam Monitoring
```bash
python real_time_safety_monitor.py --source webcam
```

#### 2. Analyze Video File
```bash
python real_time_safety_monitor.py --source path/to/video.mp4
```

#### 3. Process Single Image
```bash
python real_time_safety_monitor.py --source path/to/image.jpg
```

#### 4. Adjust Confidence Threshold
```bash
# Lower confidence = more detections (may have false positives)
python real_time_safety_monitor.py --source webcam --conf 0.3

# Higher confidence = fewer detections (stricter)
python real_time_safety_monitor.py --source webcam --conf 0.7
```

---

## 🎮 Controls

While monitoring:
- **'q'** - Quit monitoring
- **'s'** - Save current frame as snapshot

Snapshots are saved to: `outputs/safety_monitoring/`

---

## 📊 Output

### Display Elements

**Top Banner (Status Bar):**
- Status: "✅ SAFETY COMPLIANT" (Green) or "⚠️ VIOLATION DETECTED" (Red)
- Real-time counts: Workers, Hardhats, Masks, Vests
- Violation breakdown: Missing hardhats, masks, vests

**Center:**
- Live detection bounding boxes
- Object labels with confidence scores

**Bottom Info Bar:**
- Equipment detected: Safety Cones, Machinery, Vehicles
- Timestamp

### Generated Files

- **Videos**: `outputs/safety_monitoring/monitored_[timestamp].mp4`
- **Images**: `outputs/safety_monitoring/result_[timestamp].jpg`
- **Snapshots**: `outputs/safety_monitoring/snapshot_[timestamp].jpg`

---

## 📈 Model Performance

**Model Information:**
- **Architecture**: YOLOv8n (Nano - optimized for edge devices)
- **Model File**: `models/ppe_detection_4classes/best.pt` (5.2 MB, via Git LFS)
- **Training Epochs**: 100
- **Dataset**: Construction site PPE compliance dataset
- **Classes**: 10 detection classes

**Performance Metrics:**

| Metric | Value |
|--------|-------|
| **Model Size** | 5.2 MB |
| **Inference Speed (CPU)** | 50-100ms per frame |
| **Inference Speed (GPU)** | 15-30ms per frame |
| **FPS (CPU)** | 10-20 FPS |
| **FPS (GPU)** | 30-60 FPS |

**Training Results** available in `run/train/helmet_detection_100epochs/`:
- Confusion matrices
- Precision-Recall curves
- F1 score curves
- Training loss curves
- Validation results
- Model checkpoints (best.pt, last.pt)

---

## 🗂️ Project Structure

```
edge-safety-monitor/
├── real_time_safety_monitor.py   # Main monitoring application
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── PROJECT_SUMMARY.md            # Project overview and roadmap
├── LICENSE                        # MIT License
├── INDEX.md                       # Project index
│
├── config/
│   ├── data.yaml                 # Dataset configuration
│   └── config.yaml               # System configuration
│
├── data/
│   ├── raw/                      # Raw datasets
│   │   ├── helmet/               # Helmet detection dataset
│   │   ├── vest/                 # Safety vest dataset
│   │   ├── phone/                # Phone usage dataset
│   │   └── drowsiness/           # Drowsiness detection dataset
│   ├── processed/                # Processed datasets
│   ├── annotations/              # Annotation files
│   └── README.md                 # Dataset documentation
│
├── models/
│   └── ppe_detection_4classes/   # Trained PPE detection model
│       └── best.pt               # YOLOv8 trained weights
│
├── scripts/
│   ├── train_model.py            # Model training script
│   ├── run_inference.py          # Inference script
│   ├── test_baseline.py          # Baseline testing
│   ├── test_with_sample_images.py # Sample image testing
│   └── download_datasets.py      # Dataset downloader
│
├── outputs/
│   ├── safety_monitoring/        # Generated outputs
│   │   ├── monitored_*.mp4       # Processed videos
│   │   ├── result_*.jpg          # Processed images
│   │   └── snapshot_*.jpg        # Captured snapshots
│   ├── baseline_test/            # Baseline test results
│   ├── construction_test/        # Construction site tests
│   └── test_samples/             # Sample test outputs
│
├── run/
│   └── train/                    # Training runs and metrics
│       └── helmet_detection_100epochs/
│           ├── weights/          # Model checkpoints
│           ├── results.csv       # Training metrics
│           └── *.png             # Training visualizations
│
├── src/
│   ├── detection/                # Detection modules
│   ├── inference/                # Inference utilities
│   ├── preprocessing/            # Data preprocessing
│   ├── training/                 # Training utilities
│   └── utils/                    # Helper functions
│       └── logger.py             # Logging utilities
│
├── tests/
│   └── test_model.py             # Unit tests
│
└── notebooks/
    └── example_notebook.ipynb    # Jupyter notebooks for experiments
```

---

## 🔧 Configuration

### Model Path
Default model: `models/ppe_detection_4classes/best.pt`

To use a different model:
```bash
python real_time_safety_monitor.py --model /path/to/model.pt --source webcam
```

### Confidence Threshold
- Default: 0.5 (50%)
- Range: 0.0 - 1.0
- Lower = more detections, higher = fewer detections

---

## 📚 Advanced Usage

### Custom Training

To retrain the model on your own dataset:

```bash
python scripts/train_model.py --data config/data.yaml --epochs 100 --batch 16
```

Training results will be saved in the `run/train/` directory with metrics, visualizations, and model checkpoints.

### Video Processing with Custom Settings

```bash
# High confidence (strict detection)
python real_time_safety_monitor.py \
    --model models/ppe_detection_4classes/best.pt \
    --source video.mp4 \
    --conf 0.6

# Low confidence (sensitive detection)
python real_time_safety_monitor.py \
    --model models/ppe_detection_4classes/best.pt \
    --source video.mp4 \
    --conf 0.3
```

---

## 💻 System Requirements

### Minimum Requirements
- CPU: Intel i5 or equivalent
- RAM: 4GB
- Storage: 500MB
- Python 3.12+

### Recommended Requirements
- GPU: NVIDIA GeForce GTX 1650 or better (for faster processing)
- RAM: 8GB+
- Storage: 1GB
- Bandwidth: 10Mbps (if using cloud deployment)

### Tested On
- Windows 10/11
- Ubuntu 20.04+
- MacOS 12+

---

## 🛠️ Troubleshooting

### Webcam Not Working
```bash
# Check if webcam is available
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"
```

### GPU Not Being Used
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

### Slow Performance
- Reduce video resolution
- Lower confidence threshold
- Use GPU instead of CPU
- Close other applications

---

## 📊 Performance Metrics

- **Inference Speed**: ~50-100ms per frame (CPU), ~15-30ms per frame (GPU)
- **Model Size**: ~10.5 MB
- **FPS**: 10-30 FPS depending on hardware
- **Accuracy**: ~82% average precision

---

## 🚀 Deployment

### Cloud Deployment
Compatible with:
- AWS EC2
- Google Cloud
- Azure
- Docker containers

### Edge Devices
Optimized for:
- Raspberry Pi 4
- NVIDIA Jetson Nano
- Intel NUC

---

## 📝 Development Roadmap

- [x] 10-class PPE detection model
- [x] Real-time webcam monitoring
- [x] Video analysis with output generation
- [x] Image processing
- [x] Professional UI/UX with status indicators
- [x] Model training pipeline
- [x] Comprehensive testing suite
- [x] Dataset management and organization
- [ ] Email/SMS alerts
- [ ] Web dashboard
- [ ] Mobile app
- [ ] Cloud integration
- [ ] Multi-camera support
- [ ] Analytics and reporting dashboard

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Siddique Akber**
- GitHub: [@siddiqueakber](https://github.com/siddiqueakber)
- Email: contact@example.com

---

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection framework
- [OpenCV](https://opencv.org/) - Computer vision library
- [PyTorch](https://pytorch.org/) - Deep learning framework

---

## 📞 Support

For issues, questions, or suggestions:
1. Open an issue on GitHub
2. Check existing documentation
3. Review troubleshooting section

---

## ⭐ Give it a Star!

If this project helped you, please give it a star! ⭐

---

**Last Updated**: October 19, 2025  
**Status**: ✅ Production Ready  
**Version**: 1.0.0

