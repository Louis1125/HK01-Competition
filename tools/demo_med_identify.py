"""
Demo medication identification (simulated)
This script forces the YOLO detector into simulated mode and runs
`YOLOv4MedicationDetector.detect_and_identify` to show detected medications.
"""
import importlib.util
import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from yoloV4.yolov4_detector import YOLOv4MedicationDetector

# Create detector
det = YOLOv4MedicationDetector()
# Force simulated mode to avoid needing model files or images
det.yolo.use_simulated = True

# Inject a simple demo manager if the detector's manager is not present
class DemoManager:
    def get_elder(self, elder_id):
        return {'elder_id': elder_id, 'name': 'Demo Elder', 'phone': '+10000000000', 'age': 75}
    def get_medications(self, elder_id):
        return [{'med_id': 1, 'elder_id': elder_id, 'name': 'DemoMed', 'dosage': '1 tablet'}]
    def get_all_elders(self):
        return [self.get_elder(1)]


class SimpleReminder:
    def __init__(self, manager):
        self.manager = manager

    def get_due_medications(self, elder_id, within_hours=4):
        # return the meds as if due now for demo
        return self.manager.get_medications(elder_id)

    def get_compliance_report(self, elder_id, days=7):
        return {"medications": []}

# Replace manager and reminder with demo objects
det.manager = DemoManager()
det.reminder = SimpleReminder(det.manager)

print('Running simulated detect_and_identify...')
results = det.detect_and_identify('dummy.jpg')
print('\nRESULTS:')
print(json.dumps(results, indent=2, ensure_ascii=False))
