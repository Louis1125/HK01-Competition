"""
YOLOv4 + Medication System Integration
When YOLOv4 detects a person, automatically get their medications and show appropriate drugs
Works for Person 1, 2, 3, ... (any number of persons)
"""

import sqlite3
from datetime import datetime
from elder_medication_system import setup_medication_database, MedicationManager, MedicationReminder
from personalized_medications import setup_personalized_medications
"""
Duplicate module stub. The canonical yoloV4 integration lives at root `yoloV4/`.
Remove this nested copy to avoid import confusion.
"""

raise SystemExit("Duplicate module - use project root yoloV4 package")
def example_2_detect_person_2():
    """YOLOv4 detects Person 2 and shows their medications."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: YOLOV4 DETECTS PERSON 2")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    system.detect_and_get_medications(person_id=2)


# ============================================================================
# EXAMPLE 3: YOLOv4 Detects Person 3
# ============================================================================

def example_3_detect_person_3():
    """YOLOv4 detects Person 3 and shows their medications."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: YOLOV4 DETECTS PERSON 3")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    system.detect_and_get_medications(person_id=3)


# ============================================================================
# EXAMPLE 4: YOLOv4 Detects Multiple Persons
# ============================================================================

def example_4_detect_multiple_persons():
    """YOLOv4 detects multiple persons in sequence."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 4: YOLOV4 DETECTS MULTIPLE PERSONS (1, 2, 3)")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    system.detect_multiple_persons([1, 2, 3])


# ============================================================================
# EXAMPLE 5: Simulate Real-time YOLOv4 Detection
# ============================================================================

def example_5_realtime_detection_simulation():
    """Simulate real-time camera detection of persons."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 5: REAL-TIME YOLOV4 CAMERA SIMULATION")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    
    # Simulate camera frames detecting different persons
    detected_persons = [1, 2, 1, 3, 2]  # Camera detects these persons in sequence
    
    print("\n[CAMERA] Running real-time detection simulation...")
    print(f"[CAMERA] Detected persons: {detected_persons}\n")
    
    for i, person_id in enumerate(detected_persons, 1):
        print(f"\n{'=' * 80}")
        print(f"[FRAME {i}] Detected Person {person_id}")
        print("=" * 80)
        system.detect_and_get_medications(person_id)
        print(f"\n[ACTION] Show medications to Person {person_id}")


# ============================================================================
# EXAMPLE 6: YOLOv4 + Show Alert if Medication Due
# ============================================================================

def example_6_detection_with_medication_alert():
    """Detect person and alert if they have due medications."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 6: YOLOV4 + MEDICATION ALERT")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    
    # Test all persons
    for person_id in [1, 2, 3]:
        print(f"\n{'=' * 80}")
        print(f"Checking Person {person_id}...")
        print("=" * 80)
        
        data = system.detect_and_get_medications(person_id)
        
        if data and data['due_medications']:
            print(f"\n[URGENT] Person {person_id} has medications due!")
            print("[ACTION] ALERT: Show medications to caregiver")
        else:
            print(f"\n[INFO] Person {person_id} has no medications due now")


# ============================================================================
# EXAMPLE 7: Database Lookup with Person Name
# ============================================================================

def example_7_lookup_by_name_then_show_meds():
    """Look up person by name, then show their medications."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 7: LOOKUP BY NAME -> SHOW MEDICATIONS")
    print("=" * 80)
    
    db, manager = setup_personalized_medications()
    
    # Get all persons and show their medications
    all_persons = manager.get_all_elders()
    
    for person in all_persons:
        person_id = person['elder_id']
        print(f"\n[SEARCH] Found person: {person['name']}")
        
        meds = manager.get_medications(person_id)
        print(f"[MEDS] {len(meds)} medication(s):")
        for med in meds:
            print(f"  - {med['name']} ({med['dosage']})")


# ============================================================================
# EXAMPLE 8: Dynamic Person ID (User Input)
# ============================================================================

def example_8_get_person_by_user_input():
    """Allow user to input person ID and get their medications."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 8: USER INPUT -> GET MEDICATIONS")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    
    # Simulate user input
    person_ids_to_check = [1, 2, 3, 999]  # 999 doesn't exist
    
    for person_id in person_ids_to_check:
        print(f"\n[INPUT] User entered: {person_id}")
        data = system.detect_and_get_medications(person_id)
        
        if data:
            print(f"[OUTPUT] Showing medications for {data['person']['name']}")
        else:
            print(f"[OUTPUT] Person {person_id} not found - please try again")


# ============================================================================
# EXAMPLE 9: Medication Dispenser Integration
# ============================================================================

def example_9_medication_dispenser():
    """Integrate with medication dispenser - dispense correct drugs for detected person."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 9: MEDICATION DISPENSER INTEGRATION")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    
    print("\n[SYSTEM] Medication Dispenser Ready")
    print("[SYSTEM] Waiting for person detection...\n")
    
    # Simulate detection and dispensing
    detected_persons = [1, 2, 3]
    
    for person_id in detected_persons:
        print("=" * 80)
        print(f"[CAMERA] Person {person_id} detected at dispenser")
        print("=" * 80)
        
        data = system.detect_and_get_medications(person_id)
        
        if data:
            print(f"\n[DISPENSER] Preparing medications for {data['person']['name']}...")
            
            for med in data['medications']:
                print(f"  [DISPENSE] {med['name']} - {med['dosage']}")
            
            print(f"\n[COMPLETE] Medications ready for {data['person']['name']}")
        
        print()


# ============================================================================
# EXAMPLE 10: Complete Workflow - Detection to Reminder
# ============================================================================

def example_10_complete_workflow():
    """Complete workflow: detect -> get data -> check schedule -> set reminder."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 10: COMPLETE WORKFLOW")
    print("=" * 80)
    
    system = YOLOv4WithMedicationLookup()
    
    print("\n[WORKFLOW] Person enters medication management area...")
    
    # Step 1: Detect person
    person_id = 1
    print(f"\n[STEP 1] YOLOv4 Detection: Person {person_id}")
    
    # Step 2: Get person data
    data = system.detect_and_get_medications(person_id)
    
    if data is None:
        print("[ERROR] Person not found")
        return
    
    person = data['person']
    medications = data['medications']
    due_meds = data['due_medications']
    
    # Step 3: Check if medication is due
    print(f"\n[STEP 3] Checking medication schedule for {person['name']}...")
    
    if due_meds:
        print(f"\n[STEP 4] MEDICATIONS DUE - Show alert to caregiver:")
        for med in due_meds:
            print(f"  [REMINDER] {med['name']} at {med['time']}")
            print(f"  [ACTION] Give to {person['name']}")
    else:
        print(f"\n[STEP 4] No medications due right now")
        print(f"         Next scheduled medication:")
        if medications:
            next_med = medications[0]
            schedules = data['schedules']
            if schedules:
                next_time = schedules[0]['time']
                print(f"         {next_med['name']} at {next_time}")
    
    # Step 5: Log interaction
    print(f"\n[STEP 5] Logging interaction with {person['name']}")
    print(f"[LOG] Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[LOG] Person: {person['name']}")
    print(f"[LOG] Action: Medication check and reminder")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("YOLOV4 + MEDICATION SYSTEM INTEGRATION")
    print("=" * 80)
    print("\nRunning all examples...\n")
    
    # Run all examples
    example_1_detect_person_1()
    example_2_detect_person_2()
    example_3_detect_person_3()
    example_4_detect_multiple_persons()
    example_5_realtime_detection_simulation()
    example_6_detection_with_medication_alert()
    example_7_lookup_by_name_then_show_meds()
    example_8_get_person_by_user_input()
    example_9_medication_dispenser()
    example_10_complete_workflow()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)
