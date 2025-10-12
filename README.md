# Edge Safety Monitor 🦺

**AI-powered real-time safety monitoring system for construction sites and industrial environments**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Project Overview

Edge Safety Monitor is an advanced computer vision system designed to enhance workplace safety by detecting:
- **PPE Compliance**: Hard hats, safety vests
- **Safety Violations**: Mobile phone usage in restricted areas
- **Worker Alertness**: Drowsiness detection
- **Real-time Alerts**: Instant notifications for safety violations

## 🌟 Features

- ✅ Real-time object detection using YOLOv8
- ✅ Multi-class safety detection (helmet, vest, phone, drowsiness)
- ✅ Edge deployment ready (optimized for Raspberry Pi/Jetson Nano)
- ✅ Alert system for safety violations
- ✅ Video and image processing support
- ✅ Performance metrics and logging

## 📁 Project Structure

```
Edge_Safety_Monitor/
├── data/
│   ├── raw/              # Raw dataset images
│   ├── processed/        # Preprocessed images
│   ├── annotations/      # YOLO format annotations
│   └── datasets.yaml     # Dataset configuration
├── models/
│   ├── pretrained/       # Pre-trained YOLOv8 models
│   ├── trained/          # Custom trained models
│   └── exports/          # Exported models (ONNX, TFLite)
├── src/
│   ├── detection/        # Detection modules
│   ├── preprocessing/    # Data preprocessing
│   ├── training/         # Training scripts
│   ├── inference/        # Inference engine
│   └── utils/            # Utility functions
├── tests/
│   ├── test_detection.py
│   └── test_model.py
├── scripts/
│   ├── download_datasets.py
│   ├── train_model.py
│   └── run_inference.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── config/
│   └── config.yaml       # Configuration settings
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- CUDA toolkit (optional, for GPU acceleration)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/siddiqueakber/Edge_Safety_Monitor.git
cd Edge_Safety_Monitor
```

2. **Create and activate virtual environment**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Download datasets**
```bash
python scripts/download_datasets.py
```

### 🧪 Test YOLOv8 Baseline

Run the baseline test to confirm your environment is working:

```bash
python scripts/test_baseline.py
```

This will:
- Download YOLOv8 pre-trained model
- Run inference on sample images
- Display detection results
- Save outputs to `outputs/` folder

## 📊 Datasets

The project uses the following datasets:

1. **Hard Hat Detection Dataset**
   - Source: Roboflow/Kaggle
   - Classes: helmet, no_helmet, person
   - Images: ~7,000+

2. **Safety Vest Detection Dataset**
   - Source: Roboflow/Kaggle
   - Classes: vest, no_vest, person
   - Images: ~5,000+

3. **Phone Usage Detection Dataset**
   - Source: Custom collected/Kaggle
   - Classes: person_with_phone, person
   - Images: ~3,000+

4. **Drowsiness Detection Dataset**
   - Source: Kaggle (YawDD, Drowsiness Detection)
   - Classes: alert, drowsy, yawning
   - Images: ~2,500+

## 🎓 Training

Train a custom model:

```bash
python scripts/train_model.py --data config/data.yaml --epochs 100 --batch 16
```

## 🔍 Inference

Run inference on images or video:

```bash
# On image
python scripts/run_inference.py --source path/to/image.jpg --model models/trained/best.pt

# On video
python scripts/run_inference.py --source path/to/video.mp4 --model models/trained/best.pt

# On webcam
python scripts/run_inference.py --source 0 --model models/trained/best.pt
```

## 📈 Performance Metrics

Target metrics for production:
- **mAP@0.5**: > 0.85
- **Inference Speed**: < 50ms per frame (on edge device)
- **Model Size**: < 100MB (for edge deployment)

## 🛠️ Development Roadmap

### Phase 1: Setup & Baseline (Week 1)
- [x] Create repository structure
- [ ] Setup virtual environment
- [ ] Gather and organize datasets
- [ ] Run YOLOv8 baseline tests
- [ ] Document initial results

### Phase 2: Data Preparation (Week 2)
- [ ] Data cleaning and preprocessing
- [ ] Data augmentation pipeline
- [ ] Train/validation/test split
- [ ] Create YOLO format annotations

### Phase 3: Model Training (Week 3-4)
- [ ] Train individual models (helmet, vest, phone, drowsiness)
- [ ] Train multi-class unified model
- [ ] Hyperparameter tuning
- [ ] Model evaluation and validation

### Phase 4: Optimization (Week 5)
- [ ] Model compression (pruning, quantization)
- [ ] Export to ONNX/TFLite
- [ ] Edge device testing
- [ ] Performance benchmarking

### Phase 5: Deployment (Week 6)
- [ ] Alert system integration
- [ ] UI/Dashboard development
- [ ] Edge deployment (Raspberry Pi/Jetson)
- [ ] Final testing and documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Siddique Akber**
- GitHub: [@siddiqueakber](https://github.com/siddiqueakber)

## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- Roboflow for dataset hosting
- Open-source community for various datasets

## 📧 Contact

For questions or collaboration, please open an issue or reach out via GitHub.

---

**⚠️ Safety First!** This project aims to make workplaces safer through AI technology.

