# Dataset Directory

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
