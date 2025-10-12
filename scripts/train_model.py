#!/usr/bin/env python3
"""
Edge Safety Monitor - Training Script
====================================
Train custom YOLOv8 model for safety detection.

Author: Siddique Akber
Date: October 2025
"""

import argparse
import sys
from pathlib import Path
import yaml
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def load_config(config_path=None):
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = PROJECT_ROOT / "config" / "config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def train_model(data_yaml, config, model_variant='yolov8n.pt'):
    """Train YOLOv8 model."""
    
    print("=" * 60)
    print("🚀 Starting Model Training")
    print("=" * 60)
    
    # Load model
    print(f"\nLoading model: {model_variant}")
    model = YOLO(model_variant)
    
    # Get training parameters from config
    epochs = config['training']['epochs']
    batch_size = config['training']['batch_size']
    lr = config['training']['learning_rate']
    patience = config['training']['patience']
    device = config['training']['device']
    
    print(f"\nTraining Parameters:")
    print(f"  Epochs: {epochs}")
    print(f"  Batch Size: {batch_size}")
    print(f"  Learning Rate: {lr}")
    print(f"  Patience: {patience}")
    print(f"  Device: {device}")
    
    # Train the model
    print("\n" + "=" * 60)
    print("📚 Training Started...")
    print("=" * 60 + "\n")
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        lr0=lr,
        patience=patience,
        device=device,
        save=True,
        save_period=config['training']['save_period'],
        workers=config['training']['workers'],
        project=str(PROJECT_ROOT / "runs" / "train"),
        name="edge_safety_monitor",
        exist_ok=True,
    )
    
    print("\n" + "=" * 60)
    print("✅ Training Completed!")
    print("=" * 60)
    
    # Validate the model
    print("\n📊 Running validation...")
    metrics = model.val()
    
    print(f"\nValidation Results:")
    print(f"  mAP50: {metrics.box.map50:.4f}")
    print(f"  mAP50-95: {metrics.box.map:.4f}")
    
    # Save best model info
    best_model_path = PROJECT_ROOT / "runs" / "train" / "edge_safety_monitor" / "weights" / "best.pt"
    print(f"\n🏆 Best model saved to: {best_model_path}")
    
    return results, metrics


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Edge Safety Monitor - Training')
    parser.add_argument('--data', type=str, default='config/data.yaml',
                       help='Path to data.yaml file')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='Model variant (yolov8n.pt, yolov8s.pt, etc.)')
    parser.add_argument('--config', type=str, default=None,
                       help='Path to config file')
    parser.add_argument('--epochs', type=int, default=None,
                       help='Number of epochs (override config)')
    parser.add_argument('--batch', type=int, default=None,
                       help='Batch size (override config)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command-line arguments if provided
    if args.epochs:
        config['training']['epochs'] = args.epochs
    if args.batch:
        config['training']['batch_size'] = args.batch
    
    # Resolve data.yaml path
    data_yaml = PROJECT_ROOT / args.data
    if not data_yaml.exists():
        print(f"❌ Error: Data file not found: {data_yaml}")
        print("\nPlease ensure you have:")
        print("  1. Downloaded datasets")
        print("  2. Prepared data using scripts/prepare_data.py")
        print("  3. Created data.yaml configuration")
        sys.exit(1)
    
    # Train model
    train_model(str(data_yaml), config, args.model)


if __name__ == "__main__":
    main()

