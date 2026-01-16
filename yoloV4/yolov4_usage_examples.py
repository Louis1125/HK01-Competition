"""
YOLOv4 Usage Examples
Practical examples showing how to use the YOLOv4 detector in different scenarios.
"""

from yoloV4.yolov4_demo import YOLOv4Detector, YOLOv4withML


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
    
    return results

# ... (other examples omitted) 


def run_all_examples():
    print("\n" + "="*70)
    print("YOLOv4 USAGE EXAMPLES - QUICK START")
    print("="*70)
    try:
        example_1_basic_detection()
        print("\n" + "="*70)
        print("✓ Examples ran (shortened output)")
    except Exception as e:
        print(f"Example run failed: {e}")


if __name__ == "__main__":
    run_all_examples()
