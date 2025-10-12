"""
Unit tests for Edge Safety Monitor models
"""

import pytest
import torch
from ultralytics import YOLO


def test_yolo_import():
    """Test that YOLOv8 can be imported."""
    assert YOLO is not None


def test_torch_available():
    """Test that PyTorch is available."""
    assert torch is not None
    assert torch.__version__ is not None


def test_cuda_check():
    """Test CUDA availability (informational)."""
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {cuda_available}")
    if cuda_available:
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")


def test_model_loading():
    """Test that YOLOv8 model can be loaded."""
    model = YOLO('yolov8n.pt')
    assert model is not None
    assert len(model.names) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

