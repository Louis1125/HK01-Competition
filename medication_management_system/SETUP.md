# SETUP INSTRUCTIONS

## Quick Start (5 minutes)

### Step 1: Install Dependencies
```
python setup/install.py
```

### Step 2: Set Up Data
```
python setup/setup_data.py
```

### Step 3: Run Main Program
```
python code/Second_Program_with_Teachable_Machine.py
```

## What's Included

- Core medication management system
- YOLOv4 real person detection
- Teachable Machine integration (optional)
- Complete documentation
- Setup scripts

## System Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy
- SQLite3 (included)

## File Structure

```
medication_management_system/
├── code/                     (Python scripts)
│   ├── elder_medication_system.py
│   ├── personalized_medications.py
│   ├── yolov4_detector.py
│   └── Second_Program_with_Teachable_Machine.py
├── data/                     (Sample data)
├── models/                   (ML models - add your files here)
├── config/                   (Configuration files)
├── docs/                     (Documentation)
├── setup/                    (Installation scripts)
│   ├── install.py
│   ├── setup_data.py
│   └── requirements.txt
└── README.md
```

## Features

✓ Real YOLOv4 person detection (not hardcoded)
✓ Automatic medication lookup
✓ Due medication alerts
✓ Side effects tracking
✓ Multiple person support
✓ Compliance reporting

## Adding Your Models

1. YOLOv4: Place weights in `models/yolov4/`
2. Teachable Machine: Place model in `models/teachable_machine/`
3. Custom models: Add to `models/custom/`

## Troubleshooting

Q: OpenCV import error?
A: Run: pip install opencv-python

Q: No module named 'X'?
A: Run: python setup/install.py

Q: Detection not working?
A: Check models in `models/` folder

## Support

See `docs/` folder for detailed guides
