"""
SECOND PROGRAM WITH TEACHABLE MACHINE INTEGRATION
Complete main program with person detection via Teachable Machine
"""

from teachable_machine_integration import TeachableMachinePersonDetector
from personalized_medications import setup_personalized_medications
from elder_medication_system import MedicationManager


def display_person(person_id, detector):
    """Display complete person information with medications"""
    result = detector.detect_and_lookup(f"person_{person_id}.jpg")
    
    if result['status'] != 'success':
        print(f"\n[ERROR] Could not find person {person_id}")
        return
    
    print("\n" + "=" * 80)
    print(f"PERSON: {result['detected']}")
    print("=" * 80)
    
    info = result['person_info']
    print(f"\nName: {info['name']}")
    print(f"Age: {info['age']}")
    print(f"Phone: {info['phone']}")
    
    print(f"\nDetection Confidence: {result['confidence']*100:.1f}%")
    
    print(f"\n[MEDICATIONS] ({len(result['medications'])} total):")
    print("-" * 80)
    for med in result['medications']:
        print(f"\nMedication: {med['name']}")
        print(f"  Dosage: {med['dosage']}")
        print(f"  Reason: {med['reason']}")
        if med['side_effects']:
            print(f"  Side Effects: {med['side_effects']}")
        if med['notes']:
            print(f"  Notes: {med['notes']}")
    
    if result['due_medications']:
        print(f"\n[DUE MEDICATIONS] ({len(result['due_medications'])} due now):")
        print("-" * 80)
        for med in result['due_medications']:
            print(f"  - {med['name']} ({med['dosage']}) at {med.get('time', 'TBD')}")
    else:
        print(f"\n[DUE MEDICATIONS] None due now")
    
    print("\n" + "=" * 80)


def display_all(detector, manager):
    """Display all persons in database"""
    print("\n" + "=" * 80)
    print("ALL PERSONS IN DATABASE")
    print("=" * 80)
    
    elders = manager.get_all_elders()
    
    print(f"\nTotal Persons: {len(elders)}\n")
    
    for elder in elders:
        person_id = elder['elder_id']
        meds = manager.get_medications(person_id)
        
        print(f"Person {person_id}: {elder['name']}")
        print(f"  Age: {elder['age']}")
        print(f"  Phone: {elder['phone']}")
        print(f"  Medications: {len(meds)}")
        print()
    
    print("=" * 80)


def main():
    """Main interactive program with Teachable Machine"""
    
    print("\n" + "=" * 80)
    print("ELDERLY MEDICATION MANAGEMENT SYSTEM")
    print("Powered by Teachable Machine Person Detection")
    print("=" * 80)
    
    # Setup database
    print("\n[INITIALIZING] Setting up medication database...")
    setup_personalized_medications()
    
    # Create detector
    print("[INITIALIZING] Loading Teachable Machine model...")
    try:
        detector = TeachableMachinePersonDetector()
    except Exception as e:
        print(f"[ERROR] Could not load Teachable Machine model: {e}")
        print("[INFO] Make sure model files are in ./my_model/ folder")
        return
    
    # Create medication manager
    db = detector.db
    manager = MedicationManager(db)
    
    print("[READY] System initialized and ready\n")
    
    # Interactive menu
    while True:
        print("\n" + "-" * 80)
        print("COMMANDS:")
        print("  person 1       - Detect Person 1 (John Smith)")
        print("  person 2       - Detect Person 2 (Mary Johnson)")
        print("  person 3       - Detect Person 3 (Robert Brown)")
        print("  detect <file>  - Detect person from image file")
        print("  all            - Show all persons in database")
        print("  exit           - Exit program")
        print("-" * 80)
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "exit":
            print("\n[EXIT] Goodbye!")
            break
        
        elif command == "person 1":
            display_person(1, detector)
        
        elif command == "person 2":
            display_person(2, detector)
        
        elif command == "person 3":
            display_person(3, detector)
        
        elif command.startswith("detect "):
            image_file = command.replace("detect ", "").strip()
            try:
                result = detector.detect_and_lookup(image_file)
                if result['status'] == 'success':
                    print(f"\n[DETECTED] {result['detected']}")
                    print(f"[CONFIDENCE] {result['confidence']*100:.1f}%")
                    print(f"[MEDICATIONS] {len(result['medications'])} found")
                else:
                    print(f"\n[ERROR] {result['status']}")
            except Exception as e:
                print(f"\n[ERROR] Could not process image: {e}")
        
        elif command == "all":
            display_all(detector, manager)
        
        else:
            print(f"\n[ERROR] Unknown command: {command}")
            print("Try: person 1, person 2, person 3, detect <file>, all, or exit")


if __name__ == "__main__":
    main()
