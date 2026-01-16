"""
YOLOv4 Usage Examples
Practical examples showing how to use the YOLOv4 detector in different scenarios.
"""

from yolov4_demo import YOLOv4Detector, YOLOv4withML


# ============================================================================
# EXAMPLE 1: Simple object detection in a single image
# ============================================================================

def example_1_basic_detection():
    """Detect all objects in an image."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Object Detection")
    print("="*70)
    
    detector = YOLOv4Detector()
    results = detector.detect("your_image.jpg")
    
    print(f"\nFound {results['count']} objects:")
    for obj in results['objects']:
        print(f"  • {obj['class']}: confidence {obj['confidence']:.1%}")
    
    """
    Duplicate usage examples - canonical copies live at root `yoloV4/`.
    Remove this nested copy to avoid confusion.
    """

    raise SystemExit("Duplicate module - use project root yoloV4 package")
    print("\n" + "="*70)
    print("EXAMPLE 3: Detect → Identify → Database Lookup")
    print("="*70)
    
    detector = YOLOv4Detector()
    pipeline = YOLOv4withML(detector)
    
    results = pipeline.detect_and_identify("your_image.jpg")
    
    print(f"\n{results['summary']}")
    print(f"\nDatabase Information:")
    
    for person in results['identified_persons']:
        db_info = person['database_info']
        print(f"\n  Name: {db_info['name']}")
        print(f"  Email: {db_info['email']}")
        print(f"  Department: {db_info['department']}")
        print(f"  Age: {db_info['age']}")


# ============================================================================
# EXAMPLE 4: Process multiple images in a folder
# ============================================================================

def example_4_batch_processing():
    """Process all images in a folder."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Batch Processing Multiple Images")
    print("="*70)
    
    import os
    from pathlib import Path
    
    detector = YOLOv4Detector()
    image_folder = "images/"  # Replace with your folder
    
    # Supported image formats
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    image_files = [
        f for f in os.listdir(image_folder)
        if Path(f).suffix.lower() in image_extensions
    ]
    
    print(f"\nProcessing {len(image_files)} images...")
    
    all_results = {}
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        results = detector.detect(image_path)
        all_results[image_file] = results
        print(f"  ✓ {image_file}: {results['count']} objects detected")
    
    return all_results


# ============================================================================
# EXAMPLE 5: Filter detections by confidence
# ============================================================================

def example_5_high_confidence_only():
    """Detect objects but filter for high confidence results only."""
    print("\n" + "="*70)
    print("EXAMPLE 5: High Confidence Detections Only")
    print("="*70)
    
    detector = YOLOv4Detector()
    results = detector.detect("your_image.jpg", confidence_threshold=0.8)
    
    # Further filter
    high_confidence = [obj for obj in results['objects'] if obj['confidence'] >= 0.9]
    
    print(f"\nDetections with confidence >= 90%:")
    for obj in high_confidence:
        print(f"  • {obj['class']}: {obj['confidence']:.1%}")


# ============================================================================
# EXAMPLE 6: Count objects by type
# ============================================================================

def example_6_count_objects_by_type():
    """Count how many of each object type is detected."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Count Objects by Type")
    print("="*70)
    
    detector = YOLOv4Detector()
    results = detector.detect("your_image.jpg")
    
    # Count by class
    from collections import Counter
    class_counts = Counter(obj['class'] for obj in results['objects'])
    
    print(f"\nObject counts:")
    for class_name, count in class_counts.most_common():
        print(f"  • {class_name}: {count}")


# ============================================================================
# EXAMPLE 7: Find object positions and centers
# ============================================================================

def example_7_object_positions():
    """Get precise positions of all detected objects."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Object Positions and Centers")
    print("="*70)
    
    detector = YOLOv4Detector()
    results = detector.detect("your_image.jpg")
    
    print(f"\nObject locations:")
    for i, obj in enumerate(results['objects'], 1):
        print(f"\n  {i}. {obj['class'].upper()}")
        print(f"     Top-left: ({obj['x']}, {obj['y']})")
        print(f"     Size: {obj['width']}x{obj['height']}")
        print(f"     Center: ({obj['center_x']}, {obj['center_y']})")


# ============================================================================
# EXAMPLE 8: Create a real-world application
# ============================================================================

class SecurityMonitor:
    """Real-world example: Monitor for persons entering a restricted area."""
    
    def __init__(self):
        self.detector = YOLOv4Detector()
        self.restricted_zone = {'x1': 200, 'y1': 150, 'x2': 500, 'y2': 400}
    
    def check_intrusion(self, image_path):
        """Check if any person is in the restricted zone."""
        persons = self.detector.detect_persons(image_path)
        
        intruders = []
        for person in persons:
            # Check if person's center is in restricted zone
            cx, cy = person['center_x'], person['center_y']
            zone = self.restricted_zone
            
            if zone['x1'] <= cx <= zone['x2'] and zone['y1'] <= cy <= zone['y2']:
                intruders.append(person)
        
        return intruders


def example_8_security_application():
    """Real-world security monitoring example."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Security Monitoring Application")
    print("="*70)
    
    monitor = SecurityMonitor()
    intruders = monitor.check_intrusion("your_image.jpg")
    
    if intruders:
        print(f"\n⚠️  ALERT! {len(intruders)} person(s) in restricted zone!")
        for i, intruder in enumerate(intruders, 1):
            print(f"   {i}. Position: ({intruder['center_x']}, {intruder['center_y']})")
    else:
        print("\n✓ No intrusions detected. Restricted zone is clear.")


# ============================================================================
# QUICK START: Run all examples
# ============================================================================

def run_all_examples():
    """Run all examples at once."""
    print("\n" + "="*70)
    print("YOLOv4 USAGE EXAMPLES - QUICK START")
    print("="*70)
    
    print("\n📝 NOTE: Replace 'your_image.jpg' with your actual image file!")
    
    try:
        # Example 1
        example_1_basic_detection()
        
        # Example 2
        example_2_detect_persons_only()
        example_2b_detect_vehicles_only()
        
        # Example 3
        example_3_detect_and_identify()
        
        # Example 5
        example_5_high_confidence_only()
        
        # Example 6
        example_6_count_objects_by_type()
        
        # Example 7
        example_7_object_positions()
        
        # Example 8
        example_8_security_application()
        
        print("\n" + "="*70)
        print("✓ All examples completed!")
        print("="*70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n📝 Instructions:")
        print("   1. Replace 'your_image.jpg' with your actual image file")
        print("   2. Or use example_4_batch_processing() to process a folder")


# ============================================================================
# COMMON USE CASES
# ============================================================================

COMMON_USE_CASES = """

COMMON USE CASES:
================

1. Detect people in a room:
   >>> detector = YOLOv4Detector()
   >>> persons = detector.detect_persons("office.jpg")

2. Count cars in a parking lot:
   >>> from collections import Counter
   >>> results = detector.detect("parking_lot.jpg")
   >>> cars = [o for o in results['objects'] if o['class'] == 'car']

3. Find a specific person and get their database info:
   >>> pipeline = YOLOv4withML(detector)
   >>> results = pipeline.detect_and_identify("conference.jpg")
   
4. Export detections to JSON:
   >>> pipeline.export_results(results, "detections.json")

5. Monitor a security camera:
   >>> monitor = SecurityMonitor()
   >>> intruders = monitor.check_intrusion("camera_feed.jpg")
   >>> if intruders:
   ...     print("ALERT! Unauthorized entry!")

6. Process all images in a folder:
   >>> results = example_4_batch_processing()


NEXT STEPS:
===========

1. Install OpenCV for real YOLOv4:
   pip install opencv-python

2. Download YOLOv4 weights (first run will auto-download):
   - Weights: https://github.com/AlexeyAB/darknet/releases
   - Config: https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov4.cfg
   - Names: https://github.com/AlexeyAB/darknet/blob/master/data/coco.names

3. Use with your own images:
   - Replace file paths in examples
   - Adjust confidence thresholds as needed
   - Add custom post-processing for your use case
"""

print(COMMON_USE_CASES)


if __name__ == "__main__":
    run_all_examples()
