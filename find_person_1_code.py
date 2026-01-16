"""
HOW TO TYPE THE CODE - FIND PERSON 1
Copy-paste ready examples
"""

from elder_medication_system import setup_medication_database, MedicationManager, MedicationReminder
from personalized_medications import setup_personalized_medications


# ============================================================================
# EXAMPLE 1: SIMPLEST WAY - Get Person 1's Info
# ============================================================================

def example_1_get_person_1_info():
    """Simplest: Just get Person 1's basic information."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 1: GET PERSON 1 INFO")
    print("=" * 80)
    
    # Step 1: Setup database
    db, manager = setup_personalized_medications()
    
    # Step 2: Get Person 1 (elder_id = 1)
    person_1 = manager.get_elder(1)
    
    # Step 3: Display the info
    print(f"\nPerson 1 found:")
    print(f"  Name: {person_1['name']}")
    print(f"  Age: {person_1['age']}")
    print(f"  Phone: {person_1['phone']}")
    print(f"  Emergency Contact: {person_1['emergency_contact']}")
    print(f"  Address: {person_1['address']}")


# ============================================================================
# EXAMPLE 2: GET PERSON 1 + MEDICATIONS
# ============================================================================

def example_2_get_person_1_and_medications():
    """Get Person 1 and all their medications."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: GET PERSON 1 + MEDICATIONS")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Get Person 1
    person_1 = manager.get_elder(1)
    print(f"\nPerson: {person_1['name']} (Age {person_1['age']})")
    
    # Get Person 1's medications
    medications = manager.get_medications(1)
    
    print(f"\nMedications ({len(medications)}):")
    for med in medications:
        print(f"  - {med['name']}")
        print(f"    Dosage: {med['dosage']}")
        print(f"    Reason: {med['reason']}")


# ============================================================================
# EXAMPLE 3: GET PERSON 1 + MEDICATIONS + SCHEDULES
# ============================================================================

def example_3_get_person_1_complete():
    """Get Person 1 with all medications and schedules."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: GET PERSON 1 COMPLETE PROFILE")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Get Person 1
    person_1 = manager.get_elder(1)
    print(f"\nPerson: {person_1['name']}")
    
    # Get medications
    medications = manager.get_medications(1)
    print(f"\nMedications: {len(medications)}")
    for med in medications:
        print(f"  - {med['name']} ({med['dosage']})")
    
    # Get schedules
    schedules = manager.get_schedules(elder_id=1)
    print(f"\nSchedules: {len(schedules)}")
    for schedule in schedules:
        print(f"  - {schedule['time']}: {schedule['frequency']}")


# ============================================================================
# EXAMPLE 4: GET ALL PERSONS (1, 2, 3)
# ============================================================================

def example_4_get_all_persons():
    """Get all persons in the database."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 4: GET ALL PERSONS")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Get all elders
    all_persons = manager.get_all_elders()
    
    print(f"\nTotal persons: {len(all_persons)}\n")
    
    for person in all_persons:
        print(f"Person {person['elder_id']}: {person['name']}")
        print(f"  Age: {person['age']}")
        print(f"  Phone: {person['phone']}\n")


# ============================================================================
# EXAMPLE 5: SEARCH - FIND PERSON BY NAME
# ============================================================================

def example_5_find_person_by_name():
    """Search for a person by their name."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 5: FIND PERSON BY NAME")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Get all persons
    all_persons = manager.get_all_elders()
    
    # Search for "John Smith"
    search_name = "John Smith"
    found = None
    
    for person in all_persons:
        if person['name'] == search_name:
            found = person
            break
    
    if found:
        print(f"\nFound: {found['name']}")
        print(f"  ID: {found['elder_id']}")
        print(f"  Age: {found['age']}")
    else:
        print(f"\n{search_name} not found")


# ============================================================================
# EXAMPLE 6: SEARCH - FIND PERSON BY ID
# ============================================================================

def example_6_find_person_by_id():
    """Search for a person by their ID."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 6: FIND PERSON BY ID")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Search for elder_id = 1
    person_id = 1
    person = manager.get_elder(person_id)
    
    if person:
        print(f"\nFound Person {person_id}:")
        print(f"  Name: {person['name']}")
        print(f"  Age: {person['age']}")
    else:
        print(f"\nPerson {person_id} not found")


# ============================================================================
# EXAMPLE 7: CHECK IF PERSON EXISTS
# ============================================================================

def example_7_check_if_person_exists():
    """Check if a person exists before using their data."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 7: CHECK IF PERSON EXISTS")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Check if person 1 exists
    person_id = 1
    person = manager.get_elder(person_id)
    
    if person is not None:
        print(f"\n[OK] Person {person_id} exists: {person['name']}")
    else:
        print(f"\n[ERROR] Person {person_id} does not exist")
    
    # Check if person 999 exists (should not exist)
    person_id_invalid = 999
    person_invalid = manager.get_elder(person_id_invalid)
    
    if person_invalid is not None:
        print(f"[OK] Person {person_id_invalid} exists")
    else:
        print(f"[ERROR] Person {person_id_invalid} does not exist")


# ============================================================================
# EXAMPLE 8: GET PERSON 1 + DUE MEDICATIONS
# ============================================================================

def example_8_get_person_1_due_medications():
    """Get Person 1 and their due medications in next 4 hours."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 8: GET PERSON 1 + DUE MEDICATIONS")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)
    
    # Get Person 1
    person_1 = manager.get_elder(1)
    print(f"\nPerson: {person_1['name']}")
    
    # Get due medications (next 4 hours)
    due = reminder.get_due_medications(1, within_hours=4)
    
    print(f"\nMedications due in next 4 hours: {len(due)}")
    for med in due:
        print(f"  - {med['name']} at {med['time']}")


# ============================================================================
# EXAMPLE 9: FORMATTED OUTPUT - PERSON 1 REPORT
# ============================================================================

def example_9_person_1_formatted_report():
    """Create a nice formatted report for Person 1."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 9: FORMATTED REPORT FOR PERSON 1")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)
    
    # Get Person 1
    person_id = 1
    person = manager.get_elder(person_id)
    
    if person is None:
        print(f"Person {person_id} not found")
        return
    
    # Get data
    medications = manager.get_medications(person_id)
    schedules = manager.get_schedules(elder_id=person_id)
    compliance = reminder.get_compliance_report(person_id, days=7)
    
    # Print formatted report
    print(f"\n{'=' * 60}")
    print(f"MEDICATION REPORT - {person['name'].upper()}")
    print(f"{'=' * 60}")
    
    print(f"\nPerson Information:")
    print(f"  Name:               {person['name']}")
    print(f"  Age:                {person['age']} years")
    print(f"  Phone:              {person['phone']}")
    print(f"  Emergency Contact:  {person['emergency_contact']}")
    
    print(f"\nMedications ({len(medications)}):")
    for med in medications:
        print(f"  {med['name']:<30} {med['dosage']:<15} {med['reason']}")
    
    print(f"\nDaily Schedule ({len(schedules)} times):")
    for schedule in schedules:
        print(f"  {schedule['time']:<10} {schedule['frequency']:<20}")
    
    print(f"\n7-Day Compliance:")
    for med_comp in compliance['medications']:
        percentage = med_comp['compliance_percent']
        print(f"  {med_comp['name']:<30} {med_comp['taken']}/{med_comp['scheduled']} ({percentage:.1f}%)")
    
    print(f"\n{'=' * 60}")


# ============================================================================
# EXAMPLE 10: LOOP THROUGH ALL PERSONS
# ============================================================================

def example_10_loop_all_persons():
    """Loop through all persons and get their info."""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 10: LOOP THROUGH ALL PERSONS")
    print("=" * 80)
    
    # Setup
    db, manager = setup_personalized_medications()
    
    # Get all persons
    all_persons = manager.get_all_elders()
    
    print(f"\nTotal persons in database: {len(all_persons)}\n")
    
    for person in all_persons:
        person_id = person['elder_id']
        
        # For each person, get their medications
        medications = manager.get_medications(person_id)
        
        print(f"Person {person_id}: {person['name']}")
        print(f"  Medications: {len(medications)}")
        for med in medications:
            print(f"    - {med['name']}")
        print()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("HOW TO TYPE THE CODE - EXAMPLES")
    print("=" * 80)
    print("\nChoose which example to run:\n")
    print("1. example_1_get_person_1_info()")
    print("2. example_2_get_person_1_and_medications()")
    print("3. example_3_get_person_1_complete()")
    print("4. example_4_get_all_persons()")
    print("5. example_5_find_person_by_name()")
    print("6. example_6_find_person_by_id()")
    print("7. example_7_check_if_person_exists()")
    print("8. example_8_get_person_1_due_medications()")
    print("9. example_9_person_1_formatted_report()")
    print("10. example_10_loop_all_persons()")
    
    # Run all examples
    example_1_get_person_1_info()
    example_2_get_person_1_and_medications()
    example_3_get_person_1_complete()
    example_4_get_all_persons()
    example_5_find_person_by_name()
    example_6_find_person_by_id()
    example_7_check_if_person_exists()
    example_8_get_person_1_due_medications()
    example_9_person_1_formatted_report()
    example_10_loop_all_persons()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)
