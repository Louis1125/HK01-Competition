# Configuration File

## Person Mapping
# Maps person IDs to names for detection
PERSON_MAPPING = {
    1: 'John Smith',
    2: 'Mary Johnson',
    3: 'Robert Brown'
}

## YOLOv4 Settings
YOLO_WEIGHTS = 'models/yolov4/yolov4.weights'
YOLO_CONFIG = 'models/yolov4/yolov4.cfg'
YOLO_NAMES = 'models/yolov4/coco.names'
YOLO_CONFIDENCE_THRESHOLD = 0.5
YOLO_NMS_THRESHOLD = 0.4

## Database Settings
DATABASE_PATH = 'data/medications.db'
DATABASE_TYPE = 'sqlite'

## Detection Settings
DETECTION_METHOD = 'yolov4'  # or 'cascade' or 'teachable_machine'
CONFIDENCE_THRESHOLD = 0.80  # 80% minimum confidence

## Feature Flags
USE_YOLOV4 = True
USE_TEACHABLE_MACHINE = False
USE_CASCADE = True  # Fallback method

## Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/app.log'
