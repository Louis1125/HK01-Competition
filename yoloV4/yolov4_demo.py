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
        
        # For real YOLOv4, you would load:
        # self.net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
        # For now, this demo shows the structure
        self.net = None  # Placeholder
        self.initialized = True
    
    def detect(self, image_path: str, confidence_threshold: float = 0.5) -> Dict[str, Any]:
        """
        Detect objects in an image using YOLOv4.
        
        Args:
            image_path: Path to input image
            confidence_threshold: Minimum confidence (0-1)
        
        Returns:
            Dict with detected objects and metadata
        """
        print(f"\n🔍 Detecting objects in: {Path(image_path).name}")
        
        # In real implementation:
        # 1. Load image with cv2.imread()
        # 2. Create blob: cv2.dnn.blobFromImage(image, 1/255.0, (416, 416))
        # 3. Forward pass: self.net.forward(output_layers)
        # 4. Post-process: filter by confidence, NMS
        
        # For demo, return mock detections
        mock_detections = [
            Detection('person', 0.94, 50, 100, 150, 300),
            Detection('car', 0.87, 300, 250, 200, 180),
            Detection('person', 0.91, 400, 80, 140, 280),
        ]
        
        detections = [d.to_dict() for d in mock_detections]
        
        return {
            'image_path': image_path,
            'objects': detections,
            'count': len(detections),
            'confidence_threshold': confidence_threshold
        }
    
    def detect_persons(self, image_path: str) -> List[Dict[str, Any]]:
        """Detect only people in image."""
        results = self.detect(image_path)
        persons = [obj for obj in results['objects'] if obj['class'] == 'person']
        print(f"   ✓ Found {len(persons)} person(s)")
        return persons
    
    def detect_vehicles(self, image_path: str) -> List[Dict[str, Any]]:
        """Detect vehicles (cars, trucks, buses, bikes)."""
        results = self.detect(image_path)
        vehicles = ['car', 'truck', 'bus', 'motorbike', 'bicycle']
        vehicles_found = [obj for obj in results['objects'] if obj['class'] in vehicles]
        print(f"   ✓ Found {len(vehicles_found)} vehicle(s)")
        return vehicles_found


class YOLOv4withML:
    """
    Combines YOLOv4 detection with ML-based identification and SQL lookup.
    """
    
    def __init__(self, detector: YOLOv4Detector):
        """Initialize with YOLOv4 detector."""
        self.detector = detector
        print("🔗 Integrated YOLOv4 + ML + SQL Lookup")
    
    def detect_and_identify(self, image_path: str) -> Dict[str, Any]:
        """
        1. Detect objects with YOLOv4
        2. Use ML to identify specific people
        3. Auto-query database for their information
        """
        print(f"\n{'='*70}")
        print("🎯 DETECT → IDENTIFY → DATABASE LOOKUP")
        print(f"{'='*70}")
        
        # Step 1: YOLOv4 Detection
        print("\n[Step 1/3] 🔍 Running YOLOv4 object detection...")
        results = self.detector.detect(image_path)
        print(f"   ✓ Detected {results['count']} objects")
        
        # Step 2: Extract persons (mock ML identification)
        print("\n[Step 2/3] 🤖 ML-based person identification...")
        persons = [obj for obj in results['objects'] if obj['class'] == 'person']
        print(f"   ✓ Identified {len(persons)} person(s)")
        
        # Step 3: Auto-query database
        print("\n[Step 3/3] 💾 Auto-fetching person data from database...")
        enhanced_results = []
        for i, person in enumerate(persons, 1):
            # Mock database lookup (in real scenario, would use PersonLookup class)
            db_record = {
                'person_id': 1000 + i,
                'name': f'Person {i}',
                'age': 25 + i * 5,
                'department': 'Sales',
                'email': f'person{i}@company.com'
            }
            
            enhanced_results.append({
                'detection': person,
                'database_info': db_record
            })
            print(f"   ✓ Found in DB: {db_record['name']} ({db_record['department']})")
        
        return {
            'all_detections': results['objects'],
            'identified_persons': enhanced_results,
            'summary': f"Detected {results['count']} objects, identified {len(persons)} persons"
        }
    
    def export_results(self, results: Dict[str, Any], output_file: str = "detection_results.json"):
        """Export results to JSON."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n📁 Results saved to: {output_file}")


def main():
    print("=" * 70)
    print("🎯 YOLOv4 OBJECT DETECTION DEMO")
    print("=" * 70)
    
    # Initialize detector
    print("\n1️⃣  Initialize YOLOv4 Detector")
    detector = YOLOv4Detector()
    
    # Test different detection scenarios
    print("\n2️⃣  Scenario: Detect all objects")
    print("-" * 70)
    results_all = detector.detect("test_image.jpg")
    print(f"✓ Found {results_all['count']} objects:")
    for obj in results_all['objects']:
        print(f"   • {obj['class'].upper()} (confidence: {obj['confidence']:.1%})")
    
    print("\n3️⃣  Scenario: Detect only persons")
    print("-" * 70)
    persons = detector.detect_persons("test_image.jpg")
    
    print("\n4️⃣  Scenario: Detect only vehicles")
    print("-" * 70)
    vehicles = detector.detect_vehicles("test_image.jpg")
    
    # Integrated ML + SQL demo
    print("\n5️⃣  Advanced: YOLOv4 + ML + Database Integration")
    print("-" * 70)
    pipeline = YOLOv4withML(detector)
    integrated_results = pipeline.detect_and_identify("test_image.jpg")
    
    # Show combined results
    print("\n📊 FINAL RESULTS:")
    print(f"   {integrated_results['summary']}")
    
    if integrated_results['identified_persons']:
        print("\n   Identified Persons with Database Info:")
        for i, item in enumerate(integrated_results['identified_persons'], 1):
            db_info = item['database_info']
            det = item['detection']
            print(f"\n   {i}. {db_info['name']}")
            print(f"      Email: {db_info['email']}")
            print(f"      Department: {db_info['department']}")
            print(f"      Detection Confidence: {det['confidence']:.1%}")
            print(f"      Position: ({det['x']}, {det['y']})")
    
    # Export results
    pipeline.export_results(integrated_results)
    
    print("\n" + "=" * 70)
    print("✓ YOLOv4 Demo Complete!")
    print("=" * 70)
    print("\n📝 To use real YOLOv4 (not mock):")
    print("   1. pip install opencv-python")
    print("   2. Download YOLOv4 weights from: https://github.com/AlexeyAB/darknet")
    print("   3. Replace mock detection with real cv2.dnn.readNet() calls")


if __name__ == "__main__":
    main()
