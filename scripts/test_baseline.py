#!/usr/bin/env python3
"""
Edge Safety Monitor - YOLOv8 Baseline Test
=========================================
This script tests the YOLOv8 installation and runs baseline detection
on sample images to confirm the environment is working correctly.

Author: Siddique Akber
Date: October 2025
"""

import os
import sys
from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO
import torch

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_environment():
    """Check if the environment is set up correctly."""
    print("=" * 60)
    print("🔍 Environment Check")
    print("=" * 60)
    
    # Python version
    print(f"✓ Python Version: {sys.version.split()[0]}")
    
    # PyTorch version
    print(f"✓ PyTorch Version: {torch.__version__}")
    
    # CUDA availability
    if torch.cuda.is_available():
        print(f"✓ CUDA Available: Yes (Device: {torch.cuda.get_device_name(0)})")
        print(f"  CUDA Version: {torch.version.cuda}")
    else:
        print("⚠ CUDA Available: No (Using CPU)")
    
    # OpenCV version
    print(f"✓ OpenCV Version: {cv2.__version__}")
    
    print("=" * 60)
    print()


def create_sample_image():
    """Create a simple test image if no sample images are available."""
    print("📝 Creating sample test image...")
    
    # Create a simple colored image with text
    img = np.ones((640, 640, 3), dtype=np.uint8) * 255
    
    # Add colored rectangles (simulating objects)
    cv2.rectangle(img, (100, 100), (300, 400), (255, 0, 0), -1)
    cv2.rectangle(img, (350, 150), (550, 450), (0, 255, 0), -1)
    
    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Safety Test Image', (150, 50), font, 1, (0, 0, 0), 2)
    cv2.putText(img, 'Person 1', (130, 250), font, 0.7, (255, 255, 255), 2)
    cv2.putText(img, 'Person 2', (380, 300), font, 0.7, (255, 255, 255), 2)
    
    return img


def test_yolov8_detection():
    """Test YOLOv8 detection on a sample image."""
    print("=" * 60)
    print("🚀 Testing YOLOv8 Detection")
    print("=" * 60)
    
    # Create output directory
    output_dir = PROJECT_ROOT / "outputs" / "baseline_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {output_dir}")
    
    try:
        # Load YOLOv8 pre-trained model (will download if not present)
        print("\n📦 Loading YOLOv8 model (this may take a moment on first run)...")
        model = YOLO('yolov8n.pt')  # yolov8n = nano (smallest/fastest)
        print("✓ Model loaded successfully!")
        
        # Print model info
        print(f"\n📊 Model Information:")
        print(f"  Model Type: YOLOv8n (Nano)")
        print(f"  Classes: {len(model.names)}")
        print(f"  Sample Classes: {list(model.names.values())[:10]}...")
        
        # Create or load test image
        print("\n🖼️ Preparing test image...")
        sample_image = create_sample_image()
        sample_path = output_dir / "sample_input.jpg"
        cv2.imwrite(str(sample_path), sample_image)
        print(f"✓ Sample image saved: {sample_path}")
        
        # Run inference
        print("\n🔎 Running inference...")
        results = model(sample_image, conf=0.25, iou=0.45)
        
        # Process results
        result = results[0]
        print(f"✓ Inference completed!")
        print(f"  Detections: {len(result.boxes)}")
        
        # Draw and save results
        annotated_image = result.plot()
        output_path = output_dir / "detection_result.jpg"
        cv2.imwrite(str(output_path), annotated_image)
        print(f"✓ Result saved: {output_path}")
        
        # Print detection details
        if len(result.boxes) > 0:
            print(f"\n📋 Detection Details:")
            for i, box in enumerate(result.boxes):
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = model.names[cls_id]
                print(f"  {i+1}. {cls_name} (confidence: {conf:.2f})")
        else:
            print("\n⚠ No objects detected in sample image")
        
        # Test on a real image URL (optional)
        print("\n🌐 Testing on sample image from URL...")
        test_url = "https://ultralytics.com/images/bus.jpg"
        try:
            results_url = model(test_url, conf=0.25)
            result_url = results_url[0]
            annotated_url = result_url.plot()
            output_url_path = output_dir / "detection_bus.jpg"
            cv2.imwrite(str(output_url_path), annotated_url)
            print(f"✓ URL test completed: {output_url_path}")
            print(f"  Detections: {len(result_url.boxes)}")
        except Exception as e:
            print(f"⚠ URL test skipped: {e}")
        
        print("\n" + "=" * 60)
        print("✅ YOLOv8 Baseline Test PASSED!")
        print("=" * 60)
        print(f"\n📁 Results saved in: {output_dir}")
        print("\nNext steps:")
        print("  1. Download safety-specific datasets")
        print("  2. Prepare training data")
        print("  3. Train custom models")
        print("  4. Deploy to edge devices")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


def print_next_steps():
    """Print next steps for the project."""
    print("\n" + "=" * 60)
    print("📚 Next Steps")
    print("=" * 60)
    print("""
1. Download Datasets:
   python scripts/download_datasets.py

2. Prepare Data:
   python scripts/prepare_data.py

3. Train Custom Model:
   python scripts/train_model.py --data config/data.yaml --epochs 100

4. Run Inference:
   python scripts/run_inference.py --source path/to/image.jpg

For more information, check the README.md file.
    """)


def main():
    """Main function to run baseline tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + " " * 10 + "Edge Safety Monitor - Baseline Test" + " " * 13 + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Check environment
    check_environment()
    
    # Test YOLOv8
    success = test_yolov8_detection()
    
    if success:
        print_next_steps()
        return 0
    else:
        print("\n⚠️ Please fix the errors above and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

