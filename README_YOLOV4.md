# YOLOv4 Quick Reference Guide

## Quick Start (3 lines of code)

```python
from yolov4_demo import YOLOv4Detector

detector = YOLOv4Detector()
results = detector.detect("your_image.jpg")
```

---

## Common Tasks

### 1. Detect All Objects
```python
detector = YOLOv4Detector()
results = detector.detect("image.jpg")

for obj in results['objects']:
    print(f"{obj['class']}: {obj['confidence']:.1%}")
```

### 2. Detect Only People
```python
detector = YOLOv4Detector()
persons = detector.detect_persons("image.jpg")
print(f"Found {len(persons)} persons")
```

### 3. Detect Only Vehicles
```python
detector = YOLOv4Detector()
vehicles = detector.detect_vehicles("image.jpg")
print(f"Found {len(vehicles)} vehicles")
```

### 4. Detect & Get Database Info
```python
from yolov4_demo import YOLOv4Detector, YOLOv4withML

detector = YOLOv4Detector()
pipeline = YOLOv4withML(detector)
results = pipeline.detect_and_identify("image.jpg")

# Each person has detection + database info
for person in results['identified_persons']:
    print(person['database_info']['name'])
```

### 5. Filter by Confidence
```python
detector = YOLOv4Detector()
results = detector.detect("image.jpg", confidence_threshold=0.9)
```

### 6. Get Object Positions
```python
detector = YOLOv4Detector()
results = detector.detect("image.jpg")

for obj in results['objects']:
    print(f"{obj['class']} at ({obj['center_x']}, {obj['center_y']})")
```

### 7. Count Objects by Type
```python
from collections import Counter

detector = YOLOv4Detector()
results = detector.detect("image.jpg")
counts = Counter(obj['class'] for obj in results['objects'])

print(counts)  # {'person': 2, 'car': 1}
```

### 8. Find Objects in a Region
```python
detector = YOLOv4Detector()
results = detector.detect("image.jpg")

# Find objects in box (x: 100-400, y: 150-350)
region_objects = [
    obj for obj in results['objects']
    if 100 <= obj['center_x'] <= 400 and 150 <= obj['center_y'] <= 350
]
```

### 9. Process Multiple Images
```python
import os
from pathlib import Path

detector = YOLOv4Detector()
image_folder = "images/"

for filename in os.listdir(image_folder):
    if Path(filename).suffix.lower() in ['.jpg', '.png']:
        results = detector.detect(os.path.join(image_folder, filename))
        print(f"{filename}: {results['count']} objects")
```

### 10. Export Results to JSON
```python
from yolov4_demo import YOLOv4withML
import json

detector = YOLOv4Detector()
pipeline = YOLOv4withML(detector)
results = pipeline.detect_and_identify("image.jpg")
pipeline.export_results(results, "output.json")
```

---

## Detectable Objects (80 COCO Classes)

**People & Animals:**
person, dog, cat, horse, sheep, cow, elephant, bear, zebra, giraffe

**Vehicles:**
car, bicycle, motorbike, aeroplane, bus, train, truck, boat

**Sports & Outdoor:**
sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket

**Kitchen & Food:**
bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

**Furniture & Indoor:**
chair, sofa, bed, diningtable, toilet, tvmonitor, laptop, keyboard, mouse, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

**Other:**
backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, fire hydrant, stop sign, parking meter, bench

---

## Response Format

Every detection returns:
```python
{
    'class': 'person',          # Object type
    'confidence': 0.94,         # Detection confidence (0-1)
    'x': 50,                    # Top-left x coordinate
    'y': 100,                   # Top-left y coordinate
    'width': 150,               # Bounding box width
    'height': 300,              # Bounding box height
    'center_x': 125,            # Center x coordinate
    'center_y': 250             # Center y coordinate
}
```

---

## Real-World Examples

### Security Monitoring
```python
from yolov4_usage_examples import SecurityMonitor

monitor = SecurityMonitor()
intruders = monitor.check_intrusion("camera_feed.jpg")
if intruders:
    print("🚨 ALERT! Unauthorized entry detected!")
```

### Parking Lot Analysis
```python
detector = YOLOv4Detector()
results = detector.detect("parking_lot.jpg")
cars = [o for o in results['objects'] if o['class'] == 'car']
available_spaces = 50 - len(cars)
```

### Office Occupancy
```python
detector = YOLOv4Detector()
persons = detector.detect_persons("office_camera.jpg")
print(f"Office occupancy: {len(persons)} people")
```

---

## Tips & Tricks

1. **Adjust Confidence:** Lower threshold = more detections (but more false positives)
   ```python
   results = detector.detect("image.jpg", confidence_threshold=0.5)
   ```

2. **Speed vs Accuracy:** For faster detection, use lower confidence threshold

3. **Processing Images in Bulk:**
   ```python
   from yolov4_usage_examples import example_4_batch_processing
   results = example_4_batch_processing()
   ```

4. **Combine with ML for identification:**
   - YOLOv4 finds people
   - ML identifies which person
   - Database auto-fetches their info

5. **Chain Multiple Detections:**
   ```python
   results = detector.detect("image.jpg")
   persons = [o for o in results['objects'] if o['class'] == 'person']
   vehicles = [o for o in results['objects'] if o['class'] in ['car', 'truck']]
   ```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError: cv2 | Install: `pip install opencv-python` |
| FileNotFoundError: yolov4.weights | First run auto-downloads (~200MB), check internet |
| Slow detection | Use lower confidence threshold or crop image |
| False positives | Increase confidence_threshold to 0.8+ |
| Out of memory | Process smaller images or lower resolution |

---

## Next Steps

1. ✅ Run the demo: `python yolov4_demo.py`
2. ✅ Try examples: `python yolov4_usage_examples.py`
3. 📁 Use with your images: Replace filenames in code
4. 🔧 Integrate with real OpenCV: `pip install opencv-python`
5. 📊 Build your application: Chain detections with ML and database

---

## Files Created

| File | Purpose |
|------|---------|
| `yolov4_demo.py` | Core YOLOv4 detector + ML integration |
| `yolov4_usage_examples.py` | 8+ practical usage examples |
| `detection_results.json` | Sample output from demo |
| `README_YOLOV4.md` | This quick reference |

---

**Happy detecting! 🎯**
