"""
INTERACTIVE TERMINAL - TYPE "person 1" AND GET OUTPUT
User-friendly interface to find persons and their medications
"""

from personalized_medications import setup_personalized_medications


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


def interactive_terminal():
    """Interactive terminal interface."""
    
    print("\n" + "=" * 80)
    print("INTERACTIVE PERSON FINDER")
    print("=" * 80)
    
    print("\nSetup: Loading database...")
    db, manager = setup_personalized_medications()
    from elder_medication_system import MedicationReminder
    reminder = MedicationReminder(manager)
    
    print("[OK] Database loaded\n")
    
    print("AVAILABLE COMMANDS:")
    print("  - Type: person 1          (Show Person 1)")
    print("  - Type: person 2          (Show Person 2)")
    print("  - Type: person 3          (Show Person 3)")
    print("  - Type: all               (Show all persons)")
    print("  - Type: help              (Show help)")
    print("  - Type: exit              (Exit program)")
    print("\n" + "=" * 80 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\nEnter command > ").strip().lower()
            
            # Check if empty
            if not user_input:
                continue
            
            # Help command
            if user_input == "help":
                print("\nAVAILABLE COMMANDS:")
                print("  - person 1, person 2, person 3  -> Show person info")
                print("  - all                          -> Show all persons")
                print("  - help                         -> Show this help")
                print("  - exit                         -> Exit program")
                continue
            
            # Exit command
            if user_input == "exit" or user_input == "quit":
                print("\n[INFO] Goodbye!")
                break
            
            # All persons command
            if user_input == "all":
                show_all_persons(manager)
                continue
            
            # Person command (e.g., "person 1", "person 2")
            if user_input.startswith("person "):
                try:
                    person_id = int(user_input.split()[1])
                    show_person_info(person_id, manager, reminder)
                except (IndexError, ValueError):
                    print("[ERROR] Invalid format. Use: person 1, person 2, etc.")
                continue
            
            # Unknown command
            print(f"[ERROR] Unknown command: '{user_input}'")
            print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\n[INFO] Goodbye!")
            break
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    # Show introduction
    print("\n" + "=" * 80)
    print("WELCOME TO PERSON FINDER")
    print("=" * 80)
    print("""
This program allows you to:
1. Type "person 1" to see Person 1's information
2. Type "person 2" to see Person 2's information
3. Type "person 3" to see Person 3's information
4. Type "all" to see all persons
5. Type "exit" to quit

The system will show:
- Person's basic info (name, age, phone, address)
- All medications
- Medication schedule (what time each day)
- Due medications (next 4 hours)
- Compliance report (7-day history)

Let's start!
""")
    
    interactive_terminal()
