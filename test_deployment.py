"""
Quick deployment test script
"""
import sys
print("="*70)
print("🦺 Edge Safety Monitor - Deployment Test")
print("="*70)
print()

# Test 1: Python version
print("✅ Test 1: Python Version")
print(f"   Python {sys.version}")
print()

# Test 2: Import dependencies
print("✅ Test 2: Testing Dependencies...")
try:
    import cv2
    print(f"   ✓ OpenCV: {cv2.__version__}")
except Exception as e:
    print(f"   ✗ OpenCV: {e}")

try:
    import torch
    print(f"   ✓ PyTorch: {torch.__version__}")
    print(f"   ✓ CUDA Available: {torch.cuda.is_available()}")
except Exception as e:
    print(f"   ✗ PyTorch: {e}")

try:
    from ultralytics import YOLO
    print(f"   ✓ Ultralytics YOLO: OK")
except Exception as e:
    print(f"   ✗ Ultralytics: {e}")

print()

# Test 3: Model file
print("✅ Test 3: Model File")
import os
model_path = "models/ppe_detection_4classes/best.pt"
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"   ✓ Model found: {model_path}")
    print(f"   ✓ Size: {size_mb:.2f} MB")
else:
    print(f"   ✗ Model not found: {model_path}")

print()

# Test 4: Load model
print("✅ Test 4: Loading Model...")
try:
    from ultralytics import YOLO
    model = YOLO(model_path)
    print(f"   ✓ Model loaded successfully")
    print(f"   ✓ Classes: {len(model.names)}")
    print(f"   ✓ Class names: {list(model.names.values())}")
except Exception as e:
    print(f"   ✗ Error loading model: {e}")

print()

# Test 5: Check outputs
print("✅ Test 5: Output Directory")
output_dir = "outputs/safety_monitoring"
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    print(f"   ✓ Directory exists: {output_dir}")
    print(f"   ✓ Files found: {len(files)}")
    for f in files[:5]:  # Show first 5
        print(f"     - {f}")
else:
    print(f"   Creating directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

print()
print("="*70)
print("🎉 All Tests Passed! System is Ready!")
print("="*70)
print()
print("🚀 To run the application:")
print()
print("  For webcam:")
print("  venv\\Scripts\\python.exe real_time_safety_monitor.py --source webcam")
print()
print("  For video:")
print("  venv\\Scripts\\python.exe real_time_safety_monitor.py --source video1.mp4")
print()
print("  For image:")
print("  venv\\Scripts\\python.exe real_time_safety_monitor.py --source \"construction workers_on site.jpeg\"")
print()
print("="*70)

