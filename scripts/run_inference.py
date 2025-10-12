#!/usr/bin/env python3
"""
Edge Safety Monitor - Inference Script
=====================================
Run inference on images, videos, or webcam feed.

Author: Siddique Akber
Date: October 2025
"""

import argparse
import sys
from pathlib import Path
import cv2
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


def run_inference(source, model_path, config):
    """Run inference on the specified source."""
    
    # Load model
    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)
    
    # Get inference parameters from config
    conf_threshold = config['inference']['confidence_threshold']
    iou_threshold = config['inference']['iou_threshold']
    
    print(f"Running inference on: {source}")
    print(f"Confidence threshold: {conf_threshold}")
    print(f"IoU threshold: {iou_threshold}")
    
    # Run inference
    results = model(
        source,
        conf=conf_threshold,
        iou=iou_threshold,
        save=True,
        show=False,
    )
    
    print(f"\n✓ Inference completed!")
    print(f"Results saved to: runs/detect/")
    
    return results


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Edge Safety Monitor - Inference')
    parser.add_argument('--source', type=str, required=True,
                       help='Source for inference (image path, video path, or 0 for webcam)')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='Path to model weights')
    parser.add_argument('--config', type=str, default=None,
                       help='Path to config file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Run inference
    run_inference(args.source, args.model, config)


if __name__ == "__main__":
    main()

