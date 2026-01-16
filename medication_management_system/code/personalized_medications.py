"""
Personalized Elder Medication System
Each elder has their own specific medications and schedules.
Example: Person 1 takes Paracetamol daily, Person 2 takes Cold & Flu pills
"""

from elder_medication_system import (
    setup_medication_database,
    MedicationManager,
    MedicationReminder
)


def setup_personalized_medications():
    """
    Set up medications for specific elders.
    Person 1: Paracetamol (pain relief)
    Person 2: Cold & Flu pills (cold symptoms)
    Person 3: Multiple medications
    """
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    print("=" * 70)
    print("[HOSPITAL] SETTING UP PERSONALIZED MEDICATIONS")
    print("=" * 70)
    
    # ========================================================================
    # PERSON 1: John Smith - Takes Paracetamol daily
    # ========================================================================
    
    print("\n[PERSON] Person 1: John Smith (Age 78)")
    print("-" * 70)
    
    person1_id = 1  # Already exists in sample data
    
    # Clear existing meds for person 1 (optional)
    existing_meds = manager.get_medications(person1_id)
    for med in existing_meds:
        manager.delete_medication(med['med_id'])
    
    # Add Paracetamol for Person 1
    print("\nAdding medications for John Smith:")
    
    paracetamol_id = manager.add_medication(
        elder_id=person1_id,
        med_name="Paracetamol",
        dosage="500mg",
        reason="Pain relief & headaches",
        side_effects="Rare: liver damage if overdosed",
        notes="Maximum 3 doses per day, space 4-6 hours apart"
    )
    print(f"  [OK] Added: Paracetamol 500mg (ID: {paracetamol_id})")
    
    # Schedule Paracetamol - Morning
    schedule1 = manager.add_schedule(
        med_id=paracetamol_id,
        time_of_day="08:00",
        frequency="Once daily",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule 1: 08:00 AM (Morning)")
    
    # Schedule Paracetamol - Afternoon (optional second dose)
    schedule2 = manager.add_schedule(
        med_id=paracetamol_id,
        time_of_day="14:00",
        frequency="As needed",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule 2: 14:00 (2:00 PM) - As needed")
    
    # Schedule Paracetamol - Evening (optional third dose)
    schedule3 = manager.add_schedule(
        med_id=paracetamol_id,
        time_of_day="20:00",
        frequency="As needed",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule 3: 20:00 (8:00 PM) - As needed")
    
    print(f"\n[OK] Person 1 Setup Complete!")
    print(f"  Medications: 1 (Paracetamol)")
    print(f"  Schedules: 3 (morning, afternoon, evening)")
    
    # ========================================================================
    # PERSON 2: Mary Johnson - Takes Cold & Flu pills regularly
    # ========================================================================
    
    print("\n[PERSON] Person 2: Mary Johnson (Age 82)")
    print("-" * 70)
    
    person2_id = 2  # Already exists in sample data
    
    # Clear existing meds for person 2
    existing_meds = manager.get_medications(person2_id)
    for med in existing_meds:
        manager.delete_medication(med['med_id'])
    
    print("\nAdding medications for Mary Johnson:")
    
    # Add Cold & Flu pills for Person 2
    cold_flu_id = manager.add_medication(
        elder_id=person2_id,
        med_name="Cold & Flu Relief Capsules",
        dosage="1 capsule (contains Paracetamol 500mg + Caffeine 65mg)",
        reason="Treatment of cold and flu symptoms (headache, fever, body ache)",
        side_effects="Mild: insomnia (due to caffeine), dizziness",
        notes="Take with water. Do not take more than 4 capsules in 24 hours"
    )
    print(f"  [OK] Added: Cold & Flu Relief Capsules (ID: {cold_flu_id})")
    
    # Schedule Cold & Flu - Morning
    schedule1 = manager.add_schedule(
        med_id=cold_flu_id,
        time_of_day="08:00",
        frequency="Once every 4-6 hours as needed",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule 1: 08:00 AM (Morning)")
    
    # Schedule Cold & Flu - Midday
    schedule2 = manager.add_schedule(
        med_id=cold_flu_id,
        time_of_day="12:00",
        frequency="Once every 4-6 hours as needed",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule 2: 12:00 PM (Midday)")
    
    # Schedule Cold & Flu - Evening
    schedule3 = manager.add_schedule(
        med_id=cold_flu_id,
        time_of_day="18:00",
        frequency="Once every 4-6 hours as needed",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule 3: 18:00 (6:00 PM)")
    
    # Optional: Add Cough Syrup
    cough_syrup_id = manager.add_medication(
        elder_id=person2_id,
        med_name="Cough Suppressant Syrup",
        dosage="2 teaspoons (10ml)",
        reason="Relief from persistent cough",
        side_effects="Drowsiness, dizziness",
        notes="Take at bedtime if cough is severe"
    )
    print(f"  [OK] Added: Cough Suppressant Syrup (ID: {cough_syrup_id})")
    
    schedule_cough = manager.add_schedule(
        med_id=cough_syrup_id,
        time_of_day="21:00",
        frequency="Once at bedtime as needed",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule: 21:00 (9:00 PM) - Bedtime")
    
    print(f"\n[OK] Person 2 Setup Complete!")
    print(f"  Medications: 2 (Cold & Flu Pills, Cough Syrup)")
    print(f"  Schedules: 4 (morning, midday, evening, bedtime)")
    
    # ========================================================================
    # PERSON 3: Robert Brown - Multiple regular medications
    # ========================================================================
    
    print("\n[PERSON] Person 3: Robert Brown (Age 75)")
    print("-" * 70)
    
    person3_id = 3
    
    # Clear existing meds
    existing_meds = manager.get_medications(person3_id)
    for med in existing_meds:
        manager.delete_medication(med['med_id'])
    
    print("\nAdding medications for Robert Brown:")
    
    # Medication 1: Aspirin (daily)
    aspirin_id = manager.add_medication(
        elder_id=person3_id,
        med_name="Aspirin",
        dosage="81mg (Low-dose)",
        reason="Heart disease prevention & blood thinner",
        side_effects="Mild stomach upset, increased bleeding risk",
        notes="Take with food or after meals"
    )
    print(f"  [OK] Added: Aspirin 81mg (ID: {aspirin_id})")
    
    schedule_aspirin = manager.add_schedule(
        med_id=aspirin_id,
        time_of_day="07:00",
        frequency="Once daily",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule: 07:00 AM (Every day)")
    
    # Medication 2: Vitamin D (daily)
    vitamin_d_id = manager.add_medication(
        elder_id=person3_id,
        med_name="Vitamin D3",
        dosage="1000 IU",
        reason="Bone health & calcium absorption",
        side_effects="None (at this dose)",
        notes="Take with breakfast for better absorption"
    )
    print(f"  [OK] Added: Vitamin D3 1000 IU (ID: {vitamin_d_id})")
    
    schedule_vitamin = manager.add_schedule(
        med_id=vitamin_d_id,
        time_of_day="08:00",
        frequency="Once daily",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    print(f"    Schedule: 08:00 AM (Every day)")
    
    print(f"\n[OK] Person 3 Setup Complete!")
    print(f"  Medications: 2 (Aspirin, Vitamin D)")
    print(f"  Schedules: 2 (morning)")
    
    return db, manager


def show_medication_summary(manager):
    """Show summary of all elders and their medications."""
    
    print("\n" + "=" * 70)
    print("[INFO] MEDICATION SUMMARY")
    print("=" * 70)
    
    elders = manager.get_all_elders()
    
    for elder in elders:
        elder_id = elder['elder_id']
        meds = manager.get_medications(elder_id)
        schedules = manager.get_schedules(elder_id=elder_id)
        
        print(f"\n[PERSON] {elder['name']} (ID: {elder_id}, Age: {elder['age']})")
        print(f"   Phone: {elder['phone']}")
        print(f"   Emergency: {elder['emergency_contact']}")
        
        print(f"   [MEDS] Medications ({len(meds)}):")
        for med in meds:
            print(f"      • {med['name']} ({med['dosage']})")
            print(f"        Reason: {med['reason']}")
        
        print(f"   [SCHEDULE] Schedule ({len(schedules)} times):")
        
        # Get med names
        med_dict = {med['med_id']: med['name'] for med in meds}
        
        # Sort schedules by time
        schedules_sorted = sorted(schedules, key=lambda x: x['time'])
        
        for sched in schedules_sorted:
            med_name = med_dict.get(sched['med_id'], 'Unknown')
            print(f"      • {sched['time']} - {med_name}")
            print(f"        Frequency: {sched['frequency']}")
        
        print()


def show_daily_medication_plan(manager, elder_id):
    """Show detailed daily medication plan for an elder."""
    
    elder = manager.get_elder(elder_id)
    if not elder:
        print(f"Elder with ID {elder_id} not found")
        return
    
    print("\n" + "=" * 70)
    print(f"📅 DAILY MEDICATION PLAN FOR {elder['name'].upper()}")
    print("=" * 70)
    
    meds = manager.get_medications(elder_id)
    schedules = manager.get_schedules(elder_id=elder_id)
    
    # Create medication lookup
    med_dict = {med['med_id']: med for med in meds}
    
    # Sort by time
    schedules_sorted = sorted(schedules, key=lambda x: x['time'])
    
    current_time = None
    for sched in schedules_sorted:
        time_str = sched['time']
        med = med_dict.get(sched['med_id'])
        
        if med:
            # Time header (only show once per hour)
            if current_time != time_str:
                hour, minute = time_str.split(':')
                hour_int = int(hour)
                
                # Determine time of day
                if hour_int < 12:
                    period = "[MORNING]"
                elif hour_int < 17:
                    period = "[AFTERNOON]"
                else:
                    period = "[EVENING]"
                
                print(f"\n{period} - {time_str}")
                current_time = time_str
            
            # Medication details
            print(f"\n  [MED] {med['name']}")
            print(f"     Dosage: {med['dosage']}")
            print(f"     Reason: {med['reason']}")
            print(f"     Frequency: {sched['frequency']}")
            
            if med['notes']:
                print(f"     Notes: {med['notes']}")
            
            if med['side_effects']:
                print(f"     Side effects: {med['side_effects']}")


def simulate_daily_routine(manager, reminder, elder_id, day_name="Today"):
    """Simulate a daily medication routine for an elder."""
    
    elder = manager.get_elder(elder_id)
    if not elder:
        print(f"Elder with ID {elder_id} not found")
        return
    
    print("\n" + "=" * 70)
    print(f"[SCHEDULE] DAILY ROUTINE - {day_name.upper()}")
    print(f"[PERSON] {elder['name']}")
    print("=" * 70)
    
    meds = manager.get_medications(elder_id)
    schedules = manager.get_schedules(elder_id=elder_id)
    
    med_dict = {med['med_id']: med for med in meds}
    schedules_sorted = sorted(schedules, key=lambda x: x['time'])
    
    print("\n📋 Medication Schedule:")
    
    for i, sched in enumerate(schedules_sorted, 1):
        med = med_dict.get(sched['med_id'])
        if med:
            time_str = sched['time']
            print(f"\n  [{i}] {time_str} - {med['name']} ({med['dosage']})")
            print(f"      Status: ⬜ NOT TAKEN")
            print(f"      Instructions: {med['notes'] if med['notes'] else 'Take with water'}")
    
    print("\n" + "-" * 70)
    print("📊 SIMULATION: Marking all doses as taken...")
    print("-" * 70)
    
    for sched in schedules_sorted:
        med = med_dict.get(sched['med_id'])
        if med:
            # Record dose taken
            reminder.mark_dose_taken(
                sched['schedule_id'],
                notes=f"Taken as scheduled on {day_name}"
            )
            print(f"✓ {med['name']} - Marked as taken at {sched['time']}")
    
    # Show compliance
    print("\n📈 COMPLIANCE STATUS:")
    report = reminder.get_compliance_report(elder_id, days=1)
    
    for med_report in report['medications']:
        compliance = med_report['compliance_percent']
        if compliance == 100:
            status = "✓ 100% - Perfect!"
        elif compliance >= 50:
            status = f"⚠ {compliance:.0f}% - Partial"
        else:
            status = f"🔴 {compliance:.0f}% - Missed"
        
        print(f"  {med_report['name']}: {status}")


def main():
    print("\n" + "🏥" * 35)
    print("PERSONALIZED ELDER MEDICATION MANAGEMENT SYSTEM")
    print("🏥" * 35)
    
    # Setup personalized medications
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)
    
    # Show summary
    show_medication_summary(manager)
    
    # Show daily plans for each elder
    print("\n" + "=" * 70)
    print("DETAILED DAILY PLANS")
    print("=" * 70)
    
    show_daily_medication_plan(manager, elder_id=1)
    show_daily_medication_plan(manager, elder_id=2)
    show_daily_medication_plan(manager, elder_id=3)
    
    # Simulate daily routine for Person 1
    print("\n" + "=" * 70)
    print("SIMULATING DAILY ROUTINE")
    print("=" * 70)
    
    simulate_daily_routine(manager, reminder, elder_id=1, day_name="Tuesday, November 27, 2025")
    
    # Show compliance
    print("\n" + "=" * 70)
    print("COMPLIANCE REPORT")
    print("=" * 70)
    
    for elder_id in [1, 2, 3]:
        elder = manager.get_elder(elder_id)
        report = reminder.get_compliance_report(elder_id, days=7)
        
        print(f"\n[PERSON] {elder['name']} - 7-Day Compliance:")
        total_scheduled = sum(m['scheduled'] for m in report['medications'])
        total_taken = sum(m['taken'] for m in report['medications'])
        
        for med_report in report['medications']:
            print(f"   {med_report['name']}: {med_report['taken']}/{med_report['scheduled']} ({med_report['compliance_percent']:.1f}%)")
        
        if total_scheduled > 0:
            overall = (total_taken / total_scheduled) * 100
            print(f"   OVERALL: {total_taken}/{total_scheduled} ({overall:.1f}%)")
    
    print("\n" + "=" * 70)
    print("✓ Personalized Medication System Setup Complete!")
    print("=" * 70)
    
    db.close()


if __name__ == "__main__":
    main()
