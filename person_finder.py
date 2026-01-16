"""
SIMPLE PERSON FINDER - INTERACTIVE TERMINAL
Type "person 1", "person 2", "person 3", "all", or "exit"
"""

from personalized_medications import setup_personalized_medications
from elder_medication_system import MedicationReminder
import logging


def display_person(person_id, manager, reminder):
    """Display person's complete information."""
    person = manager.get_elder(person_id)
    
    if person is None:
        print(f"\n[ERROR] Person {person_id} not found\n")
        return
    
    # Show only basic info by default. Prompt the operator to reveal medications.
    logging.getLogger(__name__).info("PERSON %s: %s", person_id, person['name'].upper())

    print("\n" + "=" * 80)
    print(f"PERSON {person_id}: {person['name'].upper()}")
    print("=" * 80)

    print(f"\n[BASIC INFO]")
    print(f"  Name:    {person['name']}")
    print(f"  Age:     {person['age']}")
    print(f"  Phone:   {person['phone']}")
    print(f"  Contact: {person['emergency_contact']}")
    print(f"  Address: {person['address']}")

    # Ask whether to show medications (sensitive data)
    ans = input("Show medications and schedule for this person? (yes/no) > ").strip().lower()
    if ans in ('y', 'yes'):
        medications = manager.get_medications(person_id)
        schedules = manager.get_schedules(elder_id=person_id)
        due_meds = reminder.get_due_medications(person_id, within_hours=4)
        compliance = reminder.get_compliance_report(person_id, days=7)

        print(f"\n[MEDICATIONS] ({len(medications)}):")
        for med in medications:
            print(f"  - {med['name']} ({med['dosage']})")
            print(f"    Reason: {med['reason']}")

        print(f"\n[SCHEDULE] ({len(schedules)} times/day):")
        for sched in schedules:
            print(f"  - {sched['time']}: {sched['frequency']}")

        print(f"\n[DUE NOW]:")
        if due_meds:
            for med in due_meds:
                print(f"  - {med['name']} at {med['time']}")
        else:
            print("  (None)")

        print(f"\n[7-DAY COMPLIANCE]:")
        for comp in compliance['medications']:
            pct = comp['compliance_percent']
            print(f"  - {comp['name']}: {comp['taken']}/{comp['scheduled']} ({pct:.1f}%)")

    print("\n" + "=" * 80 + "\n")


def display_all(manager):
    """Display all persons."""
    all_persons = manager.get_all_elders()
    
    print("\n" + "=" * 80)
    print("ALL PERSONS IN DATABASE")
    print("=" * 80)
    print(f"\nTotal: {len(all_persons)} persons\n")
    
    for p in all_persons:
        print(f"  [{p['elder_id']}] {p['name']} - Age {p['age']}")
    
    print("\n" + "=" * 80 + "\n")


def main():
    """Main program."""
    print("\n" + "=" * 80)
    print("PERSON FINDER - INTERACTIVE TERMINAL")
    print("=" * 80)
    
    print("\nLoading database...")
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)
    print("[OK] Ready\n")
    
    print("COMMANDS:")
    print("  person 1  - Show Person 1 (John Smith)")
    print("  person 2  - Show Person 2 (Mary Johnson)")
    print("  person 3  - Show Person 3 (Robert Brown)")
    print("  all       - Show all persons")
    print("  exit      - Exit\n")
    
    while True:
        cmd = input("Enter command > ").strip().lower()
        
        if not cmd:
            continue
        
        if cmd == "exit" or cmd == "quit":
            print("\n[OK] Goodbye!\n")
            break
        
        if cmd == "all":
            display_all(manager)
            continue
        
        if cmd.startswith("person "):
            try:
                person_id = int(cmd.split()[1])
                display_person(person_id, manager, reminder)
            except (IndexError, ValueError):
                print("[ERROR] Use: person 1, person 2, person 3\n")
            continue
        
        print(f"[ERROR] Unknown command: {cmd}\n")


if __name__ == "__main__":
    main()
