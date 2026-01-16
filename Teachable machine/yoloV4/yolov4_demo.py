"""
YOLOv4 Object Detection Demo (Lightweight Version)
Demonstrates YOLOv4 integration for detecting people, cars, and other objects.
Uses mock detection for demo purposes (can upgrade to real YOLOv4 later).
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path


@dataclass
class Detection:
    """Represents a single object detection."""
    class_name: str
    confidence: float
    x: int
    y: int
    width: int
    height: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'class': self.class_name,
            'confidence': self.confidence,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'center_x': self.x + self.width // 2,
            'center_y': self.y + self.height // 2
        }


class YOLOv4Detector:
    """
    YOLOv4 Object Detection Wrapper
    
    Usage:
        detector = YOLOv4Detector()
        results = detector.detect("image.jpg")
    """
    
    # YOLOv4 COCO dataset classes (80 classes total)
    COCO_CLASSES = [
        'person', 'bicycle', 'car', 'motorbike', 'aeroplane',
        'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'cat',
        'dog', 'horse', 'sheep', 'cow', 'elephant',
        'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
        'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
        'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
        'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli',
        'carrot', 'hot dog', 'pizza', 'donut', 'cake',
        'chair', 'sofa', 'pottedplant', 'bed', 'diningtable',
        'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote',
        'keyboard', 'microwave', 'oven', 'toaster', 'sink',
        'refrigerator', 'book', 'clock', 'vase', 'scissors',
        'teddy bear', 'hair drier', 'toothbrush'
    ]
    
    def __init__(self):
        """Initialize YOLOv4 detector."""
        print("📦 Initializing YOLOv4 Detector...")
        print(f"   ✓ Available object classes: {len(self.COCO_CLASSES)}")
        print(f"   ✓ Supported classes: person, car, dog, cat, bicycle, etc.")
        
        """
        This file was moved to the project root `yoloV4/` and is intentionally left
        as a duplicate placeholder to avoid accidental imports from the nested
        Teachable machine copy. Use the root package `yoloV4` instead.

        If you see this file, remove the copy under `Teachable machine/yoloV4`.
        """

        raise SystemExit("Duplicate module - use project root yoloV4 package")
        
