"""
Edge Safety Monitor - Test with Sample Construction Images
=========================================================
This script downloads sample construction images from the web
and tests YOLOv8 detection to see what it currently detects.

This helps you understand what the model sees before training
on custom safety datasets.

Author: Siddique Akber
Date: October 2025
"""

import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
import requests
from io import BytesIO
from PIL import Image
import numpy as np

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def download_image(url, save_path):
    """Download image from URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        img.save(save_path)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False


def test_construction_images():
    """Test YOLOv8 on construction-related images."""
    print("=" * 70)
    print("🏗️ Testing YOLOv8 on Construction Site Images")
    print("=" * 70)
    
    # Create output directory
    output_dir = PROJECT_ROOT / "outputs" / "construction_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample construction images (public domain/free to use)
    sample_images = [
        {
            'url': 'https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800',
            'name': 'construction_workers_1.jpg',
            'description': 'Construction workers on site'
        },
        {
            'url': 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800',
            'name': 'construction_site_2.jpg',
            'description': 'Construction site overview'
        },
    ]
    
    print("\n📥 Downloading sample construction images...")
    downloaded = []
    
    for img_info in sample_images:
        save_path = output_dir / img_info['name']
        print(f"\n  Downloading: {img_info['description']}")
        if download_image(img_info['url'], save_path):
            print(f"  ✓ Saved to: {save_path}")
            downloaded.append(save_path)
        else:
            print(f"  ✗ Failed to download")
    
    if not downloaded:
        print("\n❌ No images downloaded. Please check your internet connection.")
        return
    
    # Load YOLOv8 model
    print("\n\n📦 Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt')
    print("✓ Model loaded!")
    
    # Run detection on downloaded images
    print("\n\n🔎 Running detection on construction images...\n")
    
    for img_path in downloaded:
        print(f"\n{'='*70}")
        print(f"📸 Processing: {img_path.name}")
        print(f"{'='*70}")
        
        # Run inference
        results = model(str(img_path), conf=0.25, save=True, 
                       project=str(output_dir), name=img_path.stem)
        
        result = results[0]
        
        print(f"✓ Detections found: {len(result.boxes)}")
        
        if len(result.boxes) > 0:
            print(f"\n📋 Detected Objects:")
            for i, box in enumerate(result.boxes):
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = model.names[cls_id]
                print(f"  {i+1}. {cls_name} (confidence: {conf:.2f})")
        else:
            print("  No objects detected")
        
        print(f"💾 Results saved to: {output_dir / img_path.stem}")
    
    print("\n\n" + "=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)
    print(f"\n📁 All results saved in: {output_dir}")
    print("\n💡 OBSERVATIONS:")
    print("   - YOLOv8 can detect 'person' (workers)")
    print("   - But it CANNOT detect helmets, vests specifically yet")
    print("   - This is why we need to train a CUSTOM model!")
    print("   - After training, it will detect: helmet, no_helmet, vest, etc.")
    
    print("\n📚 NEXT STEPS:")
    print("   1. Gather full safety datasets (helmet, vest, phone)")
    print("   2. Train custom model on safety-specific data")
    print("   3. Test again - you'll see helmet/vest detection!")


def main():
    """Main function."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + " " * 10 + "Edge Safety Monitor - Construction Test" + " " * 18 + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    test_construction_images()
    
    print("\n\n🎯 Understanding the Results:")
    print("   Current YOLOv8 (pre-trained on COCO dataset):")
    print("   ✓ CAN detect: person, car, truck, bicycle, etc.")
    print("   ✗ CANNOT detect: helmet, vest, phone usage, drowsiness")
    print()
    print("   After training on YOUR safety dataset:")
    print("   ✓ WILL detect: helmet, no_helmet, vest, no_vest, phone, drowsy, alert")
    print()
    print("   That's why we need custom training data! 🎓")
    print("\n")


if __name__ == "__main__":
    sys.exit(main())

