"""
Practical Examples: How to Use Elder Medication System
Shows real-world scenarios for managing elderly care medications.
"""

from elder_medication_system import (
    setup_medication_database, 
    MedicationManager, 
    MedicationReminder
)


# ============================================================================
# EXAMPLE 1: Add a New Elder
# ============================================================================

def example_1_add_new_elder():
    """Add a new elderly person to the system."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Add a New Elder")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    # Add new elder
    elder_id = manager.add_elder(
        name="Patricia Wilson",
        age=80,
        phone="555-0104",
        emergency_contact="Tom Wilson (son)",
        address="321 Elm Street"
    )
    
    print(f"\n✓ Added new elder: Patricia Wilson")
    print(f"  Elder ID: {elder_id}")
    
    db.close()


# ============================================================================
# EXAMPLE 2: Add Medications to an Elder
# ============================================================================

def example_2_add_medications():
    """Add multiple medications for an elder."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Add Medications to Elder")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    elder_id = 1  # John Smith
    
    # Add medication 1
    med1_id = manager.add_medication(
        elder_id=elder_id,
        med_name="Atorvastatin",
        dosage="20mg",
        reason="High Cholesterol",
        side_effects="Muscle pain",
        notes="Take with food in evening"
    )
    print(f"✓ Added: Atorvastatin (ID: {med1_id})")
    
    # Add medication 2
    med2_id = manager.add_medication(
        elder_id=elder_id,
        med_name="Vitamin D",
        dosage="1000 IU",
        reason="Bone Health",
        side_effects="None",
        notes="Take with breakfast"
    )
    print(f"✓ Added: Vitamin D (ID: {med2_id})")
    
    db.close()


# ============================================================================
# EXAMPLE 3: Set Medication Schedule
# ============================================================================

def example_3_create_schedule():
    """Create a medication schedule."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Create Medication Schedule")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    med_id = 1  # Metformin
    
    # Add schedule
    schedule_id = manager.add_schedule(
        med_id=med_id,
        time_of_day="08:00",  # 8:00 AM
        frequency="Once daily",
        days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
        start_date="2025-01-01",
        end_date="2025-12-31"
    )
    
    print(f"✓ Created schedule for Metformin")
    print(f"  Time: 08:00 (every day)")
    print(f"  Schedule ID: {schedule_id}")
    
    db.close()


# ============================================================================
# EXAMPLE 4: Check Due Medications
# ============================================================================

def example_4_check_due_meds():
    """Check which medications are due soon."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Check Due Medications")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    reminder = MedicationReminder(manager)
    
    elder_id = 1
    elder = manager.get_elder(elder_id)
    
    # Check medications due in next 4 hours
    due_meds = reminder.get_due_medications(elder_id, within_hours=4)
    
    print(f"\nChecking medications for {elder['name']}...")
    print(f"Due in next 4 hours:")
    
    if due_meds:
        for med in due_meds:
            print(f"\n  🔴 {med['name']} ({med['dosage']})")
            print(f"     Time: {med['time']}")
            print(f"     Status: {med['status']}")
    else:
        print("  ✓ No medications due in the next 4 hours")
    
    db.close()


# ============================================================================
# EXAMPLE 5: Mark Dose as Taken
# ============================================================================

def example_5_mark_dose_taken():
    """Record that an elder took their medication."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Mark Dose as Taken")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    reminder = MedicationReminder(manager)
    
    schedule_id = 1  # First schedule
    
    # Mark dose as taken
    reminder.mark_dose_taken(
        schedule_id=schedule_id,
        notes="Taken with breakfast"
    )
    
    print(f"✓ Dose marked as taken")
    print(f"  Schedule ID: {schedule_id}")
    print(f"  Time: {reminder.manager.conn.cursor().execute('SELECT CURRENT_TIME').fetchone()[0]}")
    
    db.close()


# ============================================================================
# EXAMPLE 6: Update Medication Details
# ============================================================================

def example_6_update_medication():
    """Update medication information."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Update Medication Details")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    med_id = 1  # Metformin
    
    # Update medication
    manager.update_medication(
        med_id=med_id,
        dosage="750mg",  # Increase dose
        notes="Increased dose due to blood sugar levels"
    )
    
    print(f"✓ Updated medication ID {med_id}")
    print(f"  New dosage: 750mg")
    print(f"  Notes: Increased dose due to blood sugar levels")
    
    db.close()


# ============================================================================
# EXAMPLE 7: Update Schedule
# ============================================================================

def example_7_update_schedule():
    """Modify medication schedule."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Update Medication Schedule")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    schedule_id = 1
    
    # Update schedule time
    manager.update_schedule(
        schedule_id=schedule_id,
        time_of_day="07:00",  # Change from 08:00 to 07:00
        end_date="2025-06-30"  # Expire prescription on June 30
    )
    
    print(f"✓ Updated schedule ID {schedule_id}")
    print(f"  New time: 07:00")
    print(f"  Expires: 2025-06-30")
    
    db.close()


# ============================================================================
# EXAMPLE 8: Compliance Report
# ============================================================================

def example_8_compliance_report():
    """Generate medication compliance report."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Medication Compliance Report")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    reminder = MedicationReminder(manager)
    
    elder_id = 1
    elder = manager.get_elder(elder_id)
    
    # Get compliance for last 7 days
    report = reminder.get_compliance_report(elder_id, days=7)
    
    print(f"\nCompliance Report for {elder['name']} (Last 7 Days)")
    print("-" * 70)
    
    for med_report in report['medications']:
        print(f"\n{med_report['name']}:")
        print(f"  Scheduled: {med_report['scheduled']}")
        print(f"  Taken: {med_report['taken']}")
        print(f"  Compliance: {med_report['compliance_percent']}%")
        
        # Color code the compliance
        if med_report['compliance_percent'] >= 90:
            status = "✓ Excellent"
        elif med_report['compliance_percent'] >= 70:
            status = "⚠ Good"
        else:
            status = "Poor"
        
        print(f"  Status: {status}")
    
    db.close()


# ============================================================================
# EXAMPLE 9: Real-World Scenario - Daily Routine
# ============================================================================

def example_9_daily_routine():
    """Simulate a daily medication routine."""
    print("\n" + "="*70)
    print("EXAMPLE 9: Daily Medication Routine")
    print("="*70)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    reminder = MedicationReminder(manager)
    
    elder_id = 1
    elder = manager.get_elder(elder_id)
    
    print(f"\n📅 Daily Routine for {elder['name']}")
    print("-" * 70)
    
    # Morning medications
    print(f"\n🌅 Morning (7:00 - 9:00 AM):")
    schedules = manager.get_schedules(elder_id=elder_id)
    morning_meds = [s for s in schedules if s['time'] <= '09:00']
    
    for sched in morning_meds[:2]:
        print(f"  • {sched['time']} - Check medication")
        reminder.mark_dose_taken(sched['schedule_id'], notes="Taken during morning routine")
    
    # Afternoon medications
    print(f"\n🌤 Afternoon (12:00 - 5:00 PM):")
    afternoon_meds = [s for s in schedules if '12:00' <= s['time'] < '17:00']
    print(f"  ✓ No afternoon medications scheduled")
    
    # Evening medications
    print(f"\n🌙 Evening (6:00 PM+):")
    evening_meds = [s for s in schedules if s['time'] >= '18:00']
    for sched in evening_meds[:1]:
        print(f"  • {sched['time']} - Check medication")
    
    db.close()


# ============================================================================
# EXAMPLE 10: Integration with YOLOv4
# ============================================================================

def example_10_yolov4_integration():
    """Show how to integrate with YOLOv4 person detection."""
    print("\n" + "="*70)
    print("EXAMPLE 10: Integration with YOLOv4")
    print("="*70)
    
    print("""
Workflow:
  1. YOLOv4 detects a person in camera feed
  2. ML model identifies which elder it is
  3. Database automatically shows their medication schedule
  4. System alerts if it's time for medication
  5. Caregiver administers medication
  6. System records dose as taken
  
Code Example:
  
  from yolov4_demo import YOLOv4Detector, YOLOv4withML
  from elder_medication_system import MedicationManager, MedicationReminder
  
  # Detect person
  detector = YOLOv4Detector()
  pipeline = YOLOv4withML(detector)
  results = pipeline.detect_and_identify("camera_feed.jpg")
  
  # For each identified person
  for person in results['identified_persons']:
      elder_id = person['database_info']['person_id']
      
      # Get their medication schedule
      manager = MedicationManager(db)
      reminder = MedicationReminder(manager)
      
      due_meds = reminder.get_due_medications(elder_id, within_hours=1)
      
      if due_meds:
          alert(f"🔔 {elder['name']} needs medication: {due_meds[0]['name']}")
    """)
    
    db = setup_medication_database()
    manager = MedicationManager(db)
    
    print("\nSimulated Integration:")
    elder = manager.get_elder(1)
    print(f"  Detected: {elder['name']}")
    print(f"  Age: {elder['age']}")
    print(f"  Medications: {len(manager.get_medications(1))}")
    
    db.close()


# ============================================================================
# QUICK START GUIDE
# ============================================================================

QUICK_START = """

QUICK START GUIDE
=================

1. ADD AN ELDER:
   >>> manager.add_elder("John Smith", 78, "555-0101", "Alice Smith", "123 Main St")

2. ADD MEDICATION:
   >>> manager.add_medication(
   ...     elder_id=1,
   ...     med_name="Metformin",
   ...     dosage="500mg",
   ...     reason="Diabetes",
   ...     side_effects="Nausea"
   ... )

3. CREATE SCHEDULE:
   >>> manager.add_schedule(
   ...     med_id=1,
   ...     time_of_day="08:00",
   ...     frequency="Once daily",
   ...     days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
   ...     start_date="2025-01-01",
   ...     end_date="2025-12-31"
   ... )

4. CHECK DUE MEDICATIONS:
   >>> due = reminder.get_due_medications(elder_id=1, within_hours=2)
   >>> for med in due:
   ...     print(f"{med['name']}: {med['status']}")

5. MARK DOSE AS TAKEN:
   >>> reminder.mark_dose_taken(schedule_id=1, notes="Taken with breakfast")

6. GET COMPLIANCE REPORT:
   >>> report = reminder.get_compliance_report(elder_id=1, days=7)

DATABASE STRUCTURE:
  - elders: Elder information (name, age, contact)
  - medications: Individual medications (name, dosage, reason)
  - schedules: When to take medications (time, frequency, days)
  - doses_taken: Track compliance (when doses were actually taken)

COMMON OPERATIONS:

View all elders:
  >>> manager.get_all_elders()

View elder's medications:
  >>> manager.get_medications(elder_id=1)

View medication schedule:
  >>> manager.get_schedules(elder_id=1)

Update medication dosage:
  >>> manager.update_medication(med_id=1, dosage="750mg")

Update schedule time:
  >>> manager.update_schedule(schedule_id=1, time_of_day="09:00")

Delete medication:
  >>> manager.delete_medication(med_id=1)

"""

print(QUICK_START)


if __name__ == "__main__":
    # Run examples
    example_1_add_new_elder()
    example_2_add_medications()
    example_3_create_schedule()
    example_4_check_due_meds()
    example_5_mark_dose_taken()
    example_6_update_medication()
    example_7_update_schedule()
    example_8_compliance_report()
    example_9_daily_routine()
    example_10_yolov4_integration()
    
    print("\n" + "="*70)
    print("✓ All examples completed!")
    print("="*70)
