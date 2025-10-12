# Edge Safety Monitor - Setup Guide

## 🚀 Quick Start Guide

Follow these steps to get the Edge Safety Monitor project up and running.

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/siddiqueakber/Edge_Safety_Monitor.git
cd Edge_Safety_Monitor
```

---

## Step 2: Create Virtual Environment

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- YOLOv8 (ultralytics)
- PyTorch
- OpenCV
- And other required packages

**Installation time:** 5-10 minutes depending on your internet speed.

---

## Step 4: Test YOLOv8 Baseline

Verify your environment is working correctly:

```bash
python scripts/test_baseline.py
```

**Expected output:**
- ✓ Environment check (Python, PyTorch, CUDA)
- ✓ YOLOv8 model download and load
- ✓ Sample inference on test images
- ✓ Results saved to `outputs/baseline_test/`

**Time:** 2-5 minutes (first run downloads YOLOv8 model ~6MB)

---

## Step 5: Download Datasets

Run the dataset setup script:

```bash
python scripts/download_datasets.py
```

This will:
- Create data directory structure
- Display instructions for downloading datasets
- Create sample configuration files

**Follow the on-screen instructions** to download datasets from:
- Roboflow (for helmet, vest datasets)
- Kaggle (for phone, drowsiness datasets)

### Dataset Checklist:
- [ ] Hard hat detection dataset (~7000 images)
- [ ] Safety vest detection dataset (~5000 images)
- [ ] Phone usage detection dataset (~3000 images)
- [ ] Drowsiness detection dataset (~2500 images)

---

## Step 6: Organize Your Data

After downloading, organize datasets like this:

```
data/
├── raw/
│   ├── helmet/
│   │   ├── images/
│   │   └── labels/
│   ├── vest/
│   │   ├── images/
│   │   └── labels/
│   ├── phone/
│   │   ├── images/
│   │   └── labels/
│   └── drowsiness/
│       ├── images/
│       └── labels/
```

---

## Step 7: Start Training (Optional)

Once you have datasets prepared, start training:

```bash
python scripts/train_model.py --data config/data.yaml --epochs 100
```

**Training time:** Several hours depending on:
- Dataset size
- Hardware (GPU recommended)
- Number of epochs

---

## Quick Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Test environment
python scripts/test_baseline.py

# Download datasets
python scripts/download_datasets.py

# Train model
python scripts/train_model.py --data config/data.yaml --epochs 100

# Run inference on image
python scripts/run_inference.py --source path/to/image.jpg --model yolov8n.pt

# Run inference on video
python scripts/run_inference.py --source path/to/video.mp4 --model yolov8n.pt

# Run inference on webcam
python scripts/run_inference.py --source 0 --model yolov8n.pt
```

---

## Troubleshooting

### Issue: CUDA not available
**Solution:** Install CUDA toolkit or use CPU mode (slower)

### Issue: Module not found
**Solution:** Ensure virtual environment is activated and dependencies are installed

### Issue: Out of memory during training
**Solution:** Reduce batch size in `config/config.yaml`

### Issue: Dataset download fails
**Solution:** Check internet connection, API keys for Roboflow/Kaggle

---

## Hardware Requirements

### Minimum:
- CPU: Intel i5 or equivalent
- RAM: 8GB
- Storage: 50GB
- OS: Windows/Linux/Mac

### Recommended:
- CPU: Intel i7 or better
- RAM: 16GB+
- GPU: NVIDIA GPU with 6GB+ VRAM (for training)
- Storage: 100GB SSD
- OS: Windows 10/11 or Ubuntu 20.04+

### For Edge Deployment:
- Raspberry Pi 4 (4GB+ RAM) or
- NVIDIA Jetson Nano or
- Similar edge computing device

---

## Next Steps

After completing setup:

1. **Explore notebooks:** Check `notebooks/` for data exploration
2. **Customize config:** Edit `config/config.yaml` for your needs
3. **Train models:** Use `scripts/train_model.py`
4. **Test inference:** Use `scripts/run_inference.py`
5. **Deploy:** Follow deployment guides for edge devices

---

## Support

- **Issues:** Open an issue on GitHub
- **Questions:** Check README.md for detailed information
- **Contributions:** Pull requests welcome!

---

**Happy Coding! 🚀**

