"""
TEST: Interactive Person Finder (automated demo)
Simulates typing commands in the terminal
"""

from personalized_medications import setup_personalized_medications
from elder_medication_system import MedicationReminder


def show_person_info(person_id, manager, reminder):
    """Show complete information for a person."""
    
    # Find the person
    person = manager.get_elder(person_id)
    
    if person is None:
        print(f"\n[ERROR] Person {person_id} not found")
        return
    
    # Get medications
    medications = manager.get_medications(person_id)
    
    # Get schedules
    schedules = manager.get_schedules(elder_id=person_id)
    
    # Get due medications
    due_meds = reminder.get_due_medications(person_id, within_hours=4)
    
    # Get compliance
    compliance = reminder.get_compliance_report(person_id, days=7)
    
    # Print formatted output
    print("\n" + "=" * 80)
    print(f"PERSON {person_id}: {person['name'].upper()}")
    print("=" * 80)
    
    print(f"\n[INFO] Basic Information:")
    print(f"  ID:                 {person['elder_id']}")
    print(f"  Name:               {person['name']}")
    print(f"  Age:                {person['age']} years old")
    print(f"  Phone:              {person['phone']}")
    print(f"  Emergency Contact:  {person['emergency_contact']}")
    print(f"  Address:            {person['address']}")
    
    print(f"\n[MEDICATIONS] ({len(medications)} medication(s)):")
    if medications:
        for med in medications:
            print(f"\n  - {med['name']}")
            print(f"    Dosage:      {med['dosage']}")
            print(f"    Reason:      {med['reason']}")
            print(f"    Side Effects: {med['side_effects']}")
    else:
        print("  (No medications)")
    
    print(f"\n[SCHEDULE] ({len(schedules)} time(s) per day):")
    if schedules:
        for schedule in schedules:
            print(f"  - {schedule['time']}: {schedule['frequency']}")
    else:
        print("  (No schedules)")
    
    print(f"\n[DUE NOW] (Next 4 hours):")
    if due_meds:
        for med in due_meds:
            print(f"  - {med['name']} at {med['time']}")
    else:
        print("  (No medications due)")
    
    print(f"\n[COMPLIANCE] (Last 7 days):")
    if compliance['medications']:
        for med_comp in compliance['medications']:
            percentage = med_comp['compliance_percent']
            status = "Good" if percentage > 75 else "Poor" if percentage < 25 else "Fair"
            print(f"  - {med_comp['name']}: {med_comp['taken']}/{med_comp['scheduled']} ({percentage:.1f}%) [{status}]")
    else:
        print("  (No compliance data)")
    
    print("\n" + "=" * 80)


def show_all_persons(manager):
    """Show all persons in database."""
    
    all_persons = manager.get_all_elders()
    
    print("\n" + "=" * 80)
    print("ALL PERSONS IN DATABASE")
    print("=" * 80)
    
    print(f"\nTotal: {len(all_persons)} persons\n")
    
    for person in all_persons:
        print(f"  [{person['elder_id']}] {person['name']} (Age {person['age']})")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("INTERACTIVE PERSON FINDER - DEMONSTRATION")
    print("=" * 80)
    
    print("\nLoading database...")
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)
    print("[OK] Database loaded\n")
    
    # Simulate commands
    commands = [
        ("person 1", "Show Person 1"),
        ("person 2", "Show Person 2"),
        ("person 3", "Show Person 3"),
        ("all", "Show all persons"),
    ]
    
    for command, description in commands:
        print(f"\n{'=' * 80}")
        print(f"[COMMAND] > {command}")
        print(f"[ACTION]  {description}")
        print(f"{'=' * 80}")
        
        if command.startswith("person "):
            try:
                person_id = int(command.split()[1])
                show_person_info(person_id, manager, reminder)
            except (IndexError, ValueError):
                print("[ERROR] Invalid format")
        elif command == "all":
            show_all_persons(manager)
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("""
YOU CAN NOW:
1. Run: python interactive_person_finder.py
2. Type: person 1          (See Person 1's info)
3. Type: person 2          (See Person 2's info)
4. Type: person 3          (See Person 3's info)
5. Type: all               (See all persons)
6. Type: exit              (Quit)
""")
