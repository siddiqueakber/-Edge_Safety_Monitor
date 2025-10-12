#!/usr/bin/env python3
"""
Edge Safety Monitor - Dataset Download Script
============================================
Downloads and organizes datasets for safety detection tasks:
- Hard hat detection
- Safety vest detection
- Phone usage detection
- Drowsiness detection

Author: Siddique Akber
Date: October 2025
"""

import os
import sys
from pathlib import Path
import requests
from tqdm import tqdm
import zipfile
import shutil

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def create_directory_structure():
    """Create the necessary directory structure for datasets."""
    directories = [
        DATA_DIR / "raw" / "helmet",
        DATA_DIR / "raw" / "vest",
        DATA_DIR / "raw" / "phone",
        DATA_DIR / "raw" / "drowsiness",
        DATA_DIR / "processed",
        DATA_DIR / "annotations",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("✓ Directory structure created")


def download_file(url, destination):
    """Download a file with progress bar."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as file, tqdm(
            desc=destination.name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
        
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def print_dataset_instructions():
    """Print instructions for manually downloading datasets."""
    print("\n" + "=" * 70)
    print("📊 DATASET DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    
    print("""
Since many datasets require API keys or manual download, please follow
these steps to gather the datasets:

1️⃣  HARD HAT DETECTION DATASET
   ----------------------------
   Source: Roboflow Universe
   Link: https://universe.roboflow.com/search?q=hard%20hat
   
   Recommended datasets:
   - "Hard Hat Detection" by Roboflow (7000+ images)
   - "Construction Site Safety" dataset
   
   Steps:
   a) Visit the link above
   b) Sign up for a free Roboflow account
   c) Download in YOLOv8 format
   d) Extract to: data/raw/helmet/

2️⃣  SAFETY VEST DETECTION DATASET
   ------------------------------
   Source: Roboflow Universe / Kaggle
   
   Option A - Roboflow:
   Link: https://universe.roboflow.com/search?q=safety%20vest
   
   Option B - Kaggle:
   Link: https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection
   
   Steps:
   a) Download dataset in YOLOv8 format
   b) Extract to: data/raw/vest/

3️⃣  PHONE USAGE DETECTION DATASET
   -------------------------------
   Source: Kaggle / Custom collection
   
   Option A - Kaggle Cell Phone Detection:
   Link: https://www.kaggle.com/datasets/saisandeepk/cell-phone-detection
   
   Option B - Create custom dataset:
   - Collect images of people using phones
   - Use LabelImg or Roboflow to annotate
   
   Steps:
   a) Download dataset
   b) Extract to: data/raw/phone/

4️⃣  DROWSINESS DETECTION DATASET
   ------------------------------
   Source: Kaggle
   
   Recommended datasets:
   - "Drowsiness Dataset" (YawDD)
     Link: https://www.kaggle.com/datasets/ismailnasri20/driver-drowsiness-dataset-ddd
   
   - "Drowsy Driver Detection"
     Link: https://www.kaggle.com/datasets/dharunprakash/drowsy-driver-detection
   
   Steps:
   a) Download dataset from Kaggle
   b) Extract to: data/raw/drowsiness/

📝 SETTING UP KAGGLE API (Recommended)
   ----------------------------------
   1. Create Kaggle account: https://www.kaggle.com/
   2. Go to Account → Create New API Token
   3. Download kaggle.json
   4. Place kaggle.json in:
      Windows: C:\\Users\\<username>\\.kaggle\\kaggle.json
      Linux/Mac: ~/.kaggle/kaggle.json
   
   5. Install Kaggle CLI:
      pip install kaggle
   
   6. Download datasets using:
      kaggle datasets download -d <dataset-path>

📝 SETTING UP ROBOFLOW API (Recommended)
   -------------------------------------
   1. Create Roboflow account: https://roboflow.com/
   2. Get API key from workspace settings
   3. Install Roboflow:
      pip install roboflow
   
   4. Use in Python:
      from roboflow import Roboflow
      rf = Roboflow(api_key="YOUR_API_KEY")
      project = rf.workspace().project("PROJECT_NAME")
      dataset = project.version(1).download("yolov8")

💡 QUICK START WITH SAMPLE DATA
   ----------------------------
   For testing purposes, you can start with a few images:
   
   1. Google "construction worker with helmet" - save 10-20 images
   2. Google "worker without helmet" - save 10-20 images
   3. Repeat for vest, phone usage, drowsy driver
   4. Place in respective folders in data/raw/
   
   This gives you a small dataset to test the pipeline before
   downloading larger datasets.

📁 EXPECTED FOLDER STRUCTURE
   ------------------------
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
   └── processed/

🎯 MINIMUM DATASET SIZES (for good results)
   ---------------------------------------
   - Training: 1000+ images per class
   - Validation: 200+ images per class
   - Testing: 100+ images per class
   
   Total recommended: 1500+ images per detection task

    """)
    
    print("=" * 70)


def create_sample_data_yaml():
    """Create a sample data.yaml configuration file for YOLOv8."""
    yaml_content = """# Edge Safety Monitor - Dataset Configuration
# YOLOv8 format

# Paths (relative to this file)
path: ../data  # dataset root dir
train: processed/train/images  # train images
val: processed/val/images  # validation images
test: processed/test/images  # test images (optional)

# Classes
names:
  0: person
  1: helmet
  2: no_helmet
  3: vest
  4: no_vest
  5: phone
  6: drowsy
  7: alert

# Number of classes
nc: 8

# Dataset info
dataset_name: Edge Safety Monitor Dataset
version: 1.0
created: 2025-10-12
author: Siddique Akber

# Training parameters (recommended)
epochs: 100
batch: 16
imgsz: 640
patience: 50
"""
    
    config_dir = PROJECT_ROOT / "config"
    config_dir.mkdir(exist_ok=True)
    
    yaml_path = config_dir / "data.yaml"
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)
    
    print(f"✓ Created sample data.yaml: {yaml_path}")


def create_readme_for_data():
    """Create README in data directory with instructions."""
    readme_content = """# Dataset Directory

This directory contains all datasets for the Edge Safety Monitor project.

## Structure

- `raw/` - Raw, unprocessed datasets downloaded from sources
  - `helmet/` - Hard hat detection images and labels
  - `vest/` - Safety vest detection images and labels
  - `phone/` - Phone usage detection images and labels
  - `drowsiness/` - Drowsiness detection images and labels

- `processed/` - Preprocessed and augmented data ready for training
  - `train/` - Training set
  - `val/` - Validation set
  - `test/` - Test set

- `annotations/` - Annotation files and metadata

## Download Instructions

Run the dataset download script:
```bash
python scripts/download_datasets.py
```

Follow the on-screen instructions to download datasets from Roboflow and Kaggle.

## Data Format

All datasets should be in YOLO format:
- Images: .jpg or .png
- Labels: .txt files with same name as image
- Label format: `class_id x_center y_center width height` (normalized 0-1)

## Data Preparation

After downloading raw data, run:
```bash
python scripts/prepare_data.py
```

This will:
1. Clean and validate data
2. Split into train/val/test sets
3. Apply data augmentation
4. Generate processed dataset ready for training
"""
    
    readme_path = DATA_DIR / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Created data README: {readme_path}")


def main():
    """Main function to download datasets."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + " " * 15 + "Edge Safety Monitor - Dataset Setup" + " " * 18 + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Create directory structure
    print("📁 Creating directory structure...")
    create_directory_structure()
    
    # Create configuration files
    print("\n📝 Creating configuration files...")
    create_sample_data_yaml()
    create_readme_for_data()
    
    # Print download instructions
    print_dataset_instructions()
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("   1. Follow the instructions above to download datasets")
    print("   2. Organize datasets in data/raw/ folders")
    print("   3. Run: python scripts/prepare_data.py")
    print("   4. Start training: python scripts/train_model.py")


if __name__ == "__main__":
    main()

