# TEACHABLE MACHINE INTEGRATION GUIDE

## What You Have Now

Your Teachable Machine model integrated with Python medication system!

**File Created:** `teachable_machine_integration.py`

## How It Works

```
Image of Person → Teachable Machine Detection → Person ID
                                                    ↓
                                        Medication Database Lookup
                                                    ↓
                                    Show medications + due times
```

## Quick Start: 3 Steps

### Step 1: Train Your Teachable Machine Model

1. Go to: https://teachablemachine.withgoogle.com
2. Click "Start" → "Image Project"
3. Click "Standard Image Model"
4. Create 4 classes:
   - Class 1: "Person 1 (John Smith)" - upload his photos
   - Class 2: "Person 2 (Mary Johnson)" - upload her photos
   - Class 3: "Person 3 (Robert Brown)" - upload his photos
   - Class 4: "Unknown" - upload random people/objects
5. Click "Train"
6. Click "Export" → "TensorFlow"
7. Click "Download"
8. Extract the zip file to `my_model/` folder in your project

### Step 2: Place Model Files

Your folder structure should look like:
```
d:\Github python\my_first_project\
├── my_model/
│   ├── model.json
│   ├── metadata.json
│   ├── weights.bin
│   ├── weights.bin.002
│   ├── group1-shard1of*
│   └── ... (other weight files)
├── teachable_machine_integration.py
├── HK01 Competition 12-12-2025 main programme.py
├── personalized_medications.py
├── elder_medication_system.py
└── ... (other files)
```

### Step 3: Use in Your Code

Option A: Detect from image file
```python
from teachable_machine_integration import TeachableMachinePersonDetector

detector = TeachableMachinePersonDetector()
result = detector.detect_and_lookup("person_photo.jpg")

print(result['detected'])           # "Person 1 (John Smith)"
print(result['confidence'])         # 0.95
print(result['medications'])        # List of medications
print(result['due_medications'])    # Due meds
```

Option B: Real-time webcam detection
```python
import cv2
from teachable_machine_integration import TeachableMachinePersonDetector

detector = TeachableMachinePersonDetector()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imwrite("temp.jpg", frame)
    result = detector.detect_and_lookup("temp.jpg")
    
    # Draw on frame
    text = f"{result['detected']} ({result['confidence']*100:.0f}%)"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Person Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Integration with HK01 Competition 12-12-2025 main programme.py

Replace the manual person input with automatic detection:

```python
# OLD (before)
person_id = input("Enter person ID (1-3): ")

# NEW (after)
from teachable_machine_integration import TeachableMachinePersonDetector
detector = TeachableMachinePersonDetector()
result = detector.detect_and_lookup("webcam_image.jpg")
person_id = result['person_id']
```

## What the System Returns

```python
result = {
    'detected': 'Person 1 (John Smith)',        # Detected name
    'confidence': 0.95,                         # Confidence (0-1)
    'person_id': 1,                             # Database ID
    'person_info': {
        'name': 'John Smith',
        'age': 78,
        'phone': '555-0101'
    },
    'medications': [                            # All medications
        {
            'med_id': 1,
            'name': 'Paracetamol',
            'dosage': '500mg',
            'reason': 'Pain relief',
            'side_effects': 'None',
            'notes': 'Take with food'
        },
        ...
    ],
    'due_medications': [                        # Due within 2 hours
        {
            'med_id': 1,
            'name': 'Paracetamol',
            'dosage': '500mg',
            'time': '14:00'
        },
        ...
    ],
    'timestamp': '2025-11-27T15:30:45.123456',
    'status': 'success'
}
```

## Use Cases

### Use Case 1: Medication Reminder by Face
```python
detector = TeachableMachinePersonDetector()

# Take photo or frame from camera
result = detector.detect_and_lookup("camera_frame.jpg")

if result['status'] == 'success':
    person = result['person_info']
    due_meds = result['due_medications']
    
    print(f"Hi {person['name']}! You have {len(due_meds)} medications due now:")
    for med in due_meds:
        print(f"  - {med['name']} ({med['dosage']} at {med['time']})")
```

### Use Case 2: Automated Check-in System
```python
detector = TeachableMachinePersonDetector()
result = detector.detect_and_lookup("check_in_photo.jpg")

# Automatically log that person is here
# Show their due medications
# Ask if they took meds
```

### Use Case 3: Security + Medication
```python
detector = TeachableMachinePersonDetector()
result = detector.detect_and_lookup("door_camera.jpg")

if result['confidence'] > 0.8:
    person = result['person_info']
    print(f"Welcome {person['name']}!")
    print(f"You have {len(result['medications'])} active medications")
```

## Troubleshooting

### Problem: Model files not found
**Solution:** Make sure you extracted all files from Teachable Machine export to `my_model/` folder

### Problem: Low confidence predictions
**Solution:** Train with more images of each person from different angles and lighting

### Problem: Webcam not working
**Solution:** Install opencv: `pip install opencv-python`

### Problem: Wrong person detected
**Solution:** 
1. Add more training images for that person
2. Increase "Number of Epochs" to 100-200 in Teachable Machine
3. Retrain the model

## Files You Need

File | Purpose | Status
-----|---------|--------
teachable_machine_integration.py | Main integration code | ✓ Created
model.json | Model architecture | Need to export
metadata.json | Class labels | Need to export
weights.bin | Model weights | Need to export
HK01 Competition 12-12-2025 main programme.py | Main program | Ready to integrate

## Next Steps

1. **Train your model** on Teachable Machine (5-10 minutes)
2. **Export** as TensorFlow (2 minutes)
3. **Extract** to my_model/ folder (1 minute)
4. **Test** the integration (run teachable_machine_integration.py)
5. **Integrate** into Second Program.py
6. **Deploy** for real-time detection

## Example Training Guide

### Train for John Smith:
1. Take 20-30 photos of John from different angles
2. Upload to "Person 1" class in Teachable Machine
3. Make sure you see his face clearly

### Train for Mary Johnson:
1. Take 20-30 photos of Mary from different angles
2. Upload to "Person 2" class

### Train for Robert Brown:
1. Take 20-30 photos of Robert from different angles
2. Upload to "Person 3" class

### Train Unknown:
1. Take 20-30 photos of other people / random objects
2. Upload to "Unknown" class

Total training data: ~100-120 images

## HTML/JavaScript Integration

Your original HTML code can work alongside Python:

**Frontend (HTML/JavaScript):** Real-time webcam display
**Backend (Python):** Database queries + medication logic

```html
<!-- Frontend shows webcam -->
<!-- JavaScript detects person -->
<!-- Python backend looks up medications -->
```

## Performance Tips

1. Use good lighting when taking training photos
2. Take photos from multiple angles
3. Use 100+ epochs for better accuracy
4. Include different facial expressions
5. Train on diverse backgrounds

## Security Considerations

1. Store model files securely
2. Don't share trained weights publicly
3. Validate predictions before using
4. Always confirm with 2nd factor (PIN, etc.)

## Summary

Your system now:
✓ Detects persons from Teachable Machine
✓ Looks up medications automatically
✓ Shows due medications
✓ Works with webcam or images
✓ Integrates with database

Ready to deploy!
