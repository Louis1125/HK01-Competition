"""
YOLOv4 + Medication System Integration
When YOLOv4 detects a person, automatically get their medications and show appropriate drugs
Works for Person 1, 2, 3, ... (any number of persons)
"""

import sqlite3
import logging
from datetime import datetime
from elder_medication_system import setup_medication_database, MedicationManager, MedicationReminder
from personalized_medications import setup_personalized_medications


class YOLOv4WithMedicationLookup:
    """
    YOLOv4 detects person -> Gets their medication data automatically
    """
    
    def __init__(self):
        """Initialize database and manager."""
        self.db, self.manager = setup_personalized_medications()
        self.reminder = MedicationReminder(self.manager)
    
    def detect_and_get_medications(self, person_id):
        """
        Simulates YOLOv4 detecting a person and retrieving their medications.
        
        Args:
            person_id: The ID of the detected person (1, 2, 3, ...)
        
        Returns:
            dict: Person's info + medications + schedules, or None if not found
        """
        
        logging.getLogger(__name__).info("[YOLOV4] DETECTED PERSON ID: %s", person_id)
        
        # Step 1: Check if person exists
        person = self.manager.get_elder(person_id)
        
        if person is None:
            logging.getLogger(__name__).warning("Person %s not found in database", person_id)
            return None
        
        # Step 2: Get person's data
        logging.getLogger(__name__).info("Found Person: %s (Age: %s, Phone: %s)", person['name'], person['age'], person['phone'])
        
        # Step 3: Get medications for this person
        medications = self.manager.get_medications(person_id)
        logging.getLogger(__name__).debug("Found %d medications for person_id=%s", len(medications), person_id)
        # Medication details are sensitive; do not print by default.
        
        # Step 4: Get schedules
        schedules = self.manager.get_schedules(elder_id=person_id)
        logging.getLogger(__name__).debug("Found %d schedules for person_id=%s", len(schedules), person_id)
        
        # Step 5: Get due medications (next 4 hours)
        due_meds = self.reminder.get_due_medications(person_id, within_hours=4)
        
        if due_meds:
            logging.getLogger(__name__).warning("Medications DUE in next 4 hours for person_id=%s: %s", person_id, [d['name'] for d in due_meds])
        else:
            logging.getLogger(__name__).info("No medications due in next 4 hours for person_id=%s", person_id)
        
        # Step 6: Get compliance
        compliance = self.reminder.get_compliance_report(person_id, days=7)
        logging.getLogger(__name__).debug("Compliance for person_id=%s: %s", person_id, compliance)
        
        # Return complete data
        return {
            'person': person,
            'medications': medications,
            'schedules': schedules,
            'due_medications': due_meds,
            'compliance': compliance
        }
    
    def detect_multiple_persons(self, person_ids):
        """
        Detect multiple persons and get their medications.
        
        Args:
            person_ids: List of person IDs to detect (e.g., [1, 2, 3])
        """
        
        print("\n" + "=" * 80)
        print("[YOLOV4] MULTIPLE PERSON DETECTION")
        print("=" * 80)
        
        results = {}
        for person_id in person_ids:
            data = self.detect_and_get_medications(person_id)
            if data:
                results[person_id] = data
        
        return results


# EXAMPLES omitted for brevity in this helper module

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("YOLOV4 + MEDICATION SYSTEM INTEGRATION")
    print("=" * 80)
    print("\nRunning a small example...\n")
    system = YOLOv4WithMedicationLookup()
    system.detect_and_get_medications(1)
