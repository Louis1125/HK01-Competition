"""
HOW THE CODE KNOWS THE CONSTRUCTION - SELECT PERSON 1
Demonstrates how to retrieve and SELECT Person 1's complete data
"""

from elder_medication_system import setup_medication_database, MedicationManager, MedicationReminder
from personalized_medications import setup_personalized_medications


def show_sql_construction():
    """Show the SQL construction behind the scenes."""
    
    print("=" * 80)
    print("HOW THE CODE SELECTS PERSON 1 - SQL CONSTRUCTION")
    print("=" * 80)
    
    # ========================================================================
    # STEP 1: Setup database
    # ========================================================================
    print("\n[STEP 1] DATABASE SETUP")
    print("-" * 80)
    
    db, manager = setup_personalized_medications()
    reminder = MedicationReminder(manager)
    
    print("[OK] Database created with tables:")
    print("     - elders (elder_id, name, age, phone, emergency_contact, address)")
    print("     - medications (med_id, elder_id, med_name, dosage, reason, side_effects)")
    print("     - schedules (schedule_id, med_id, time_of_day, frequency, days_of_week)")
    print("     - doses_taken (dose_id, schedule_id, date, time_taken, taken)")
    
    # ========================================================================
    # STEP 2: SELECT Person 1 (John Smith)
    # ========================================================================
    print("\n" + "=" * 80)
    print("[STEP 2] SELECT PERSON 1 - THE CODE CONSTRUCTION")
    print("=" * 80)
    
    elder_id = 1
    print(f"\nGoal: Find Person 1 (elder_id = {elder_id})")
    
    # ====== Method 1: Get Elder ======
    print("\n[METHOD 1] get_elder(1) - SELECT FROM elders")
    print("-" * 80)
    print("SQL QUERY:")
    print("  SELECT * FROM elders WHERE elder_id = 1")
    print("\nPython Code:")
    print("  cursor.execute('SELECT * FROM elders WHERE elder_id = ?', (1,))")
    print("  elder = cursor.fetchone()")
    
    elder = manager.get_elder(elder_id)
    
    print("\nResult (the construction/components returned):")
    print(f"  {elder}")
    print("\nComponents:")
    for key, value in elder.items():
        print(f"    - {key}: {value}")
    
    # ====== Method 2: Get Medications ======
    print("\n" + "-" * 80)
    print("[METHOD 2] get_medications(1) - SELECT FROM medications")
    print("-" * 80)
    print("SQL QUERY:")
    print("  SELECT * FROM medications WHERE elder_id = 1")
    print("\nPython Code:")
    print("  cursor.execute('SELECT * FROM medications WHERE elder_id = ?', (1,))")
    print("  medications = cursor.fetchall()")
    
    medications = manager.get_medications(elder_id)
    
    print(f"\nResult ({len(medications)} medications found):")
    for med in medications:
        print(f"\n  Medication Record:")
        for key, value in med.items():
            print(f"    - {key}: {value}")
    
    # ====== Method 3: Get Schedules ======
    print("\n" + "-" * 80)
    print("[METHOD 3] get_schedules(elder_id=1) - SELECT FROM schedules")
    print("-" * 80)
    print("SQL QUERY:")
    print("  SELECT s.* FROM schedules s")
    print("  JOIN medications m ON s.med_id = m.med_id")
    print("  WHERE m.elder_id = 1")
    print("\nPython Code:")
    print("  cursor.execute('''")
    print("      SELECT s.* FROM schedules s")
    print("      JOIN medications m ON s.med_id = m.med_id")
    print("      WHERE m.elder_id = ?", (1,))
    print("  ''', (1,))")
    
    schedules = manager.get_schedules(elder_id=elder_id)
    
    print(f"\nResult ({len(schedules)} schedules found):")
    for schedule in schedules:
        print(f"\n  Schedule Record:")
        for key, value in schedule.items():
            print(f"    - {key}: {value}")
    
    # ========================================================================
    # STEP 3: COMPLETE PERSON 1 PROFILE
    # ========================================================================
    print("\n" + "=" * 80)
    print("[STEP 3] COMPLETE PERSON 1 PROFILE - ALL COMPONENTS COMBINED")
    print("=" * 80)
    
    print(f"\n[PERSON 1] {elder['name']}")
    print("-" * 80)
    print(f"Elder ID:           {elder['elder_id']}")
    print(f"Name:               {elder['name']}")
    print(f"Age:                {elder['age']} years old")
    print(f"Phone:              {elder['phone']}")
    print(f"Emergency Contact:  {elder['emergency_contact']}")
    print(f"Address:            {elder['address']}")
    
    print(f"\nMEDICATIONS ({len(medications)}):")
    for med in medications:
        print(f"\n  [Medication {med['med_id']}] {med['name']}")
        print(f"    Dosage:      {med['dosage']}")
        print(f"    Reason:      {med['reason']}")
        print(f"    Side Effects: {med['side_effects']}")
        print(f"    Notes:       {med['notes']}")
    
    print(f"\nSCHEDULES ({len(schedules)}):")
    for schedule in schedules:
        med_name = next((m['name'] for m in medications if m['med_id'] == schedule['med_id']), 'Unknown')
        print(f"\n  [Schedule {schedule['schedule_id']}] {med_name}")
        print(f"    Time:       {schedule['time']}")
        print(f"    Frequency:  {schedule['frequency']}")
        print(f"    Days:       {schedule['days']}")
        print(f"    Start:      {schedule['start_date']}")
        print(f"    End:        {schedule['end_date']}")
    
    # ========================================================================
    # STEP 4: HOW TO QUERY DIRECTLY (Raw SQL)
    # ========================================================================
    print("\n" + "=" * 80)
    print("[STEP 4] DIRECT SQL QUERIES (If you want to write your own SQL)")
    print("=" * 80)
    
    print("\n[QUERY 1] Get Person 1's basic info:")
    print("""
    SELECT elder_id, name, age, phone, emergency_contact, address
    FROM elders
    WHERE elder_id = 1;
    """)
    
    print("[QUERY 2] Get all medications for Person 1:")
    print("""
    SELECT med_id, med_name, dosage, reason, side_effects, notes
    FROM medications
    WHERE elder_id = 1;
    """)
    
    print("[QUERY 3] Get all schedules for Person 1's medications:")
    print("""
    SELECT s.schedule_id, m.med_name, s.time_of_day, s.frequency, s.days_of_week
    FROM schedules s
    JOIN medications m ON s.med_id = m.med_id
    WHERE m.elder_id = 1
    ORDER BY s.time_of_day;
    """)
    
    print("[QUERY 4] Get Person 1's complete profile (everything):")
    print("""
    SELECT 
        e.elder_id, e.name, e.age, e.phone, e.emergency_contact, e.address,
        m.med_id, m.med_name, m.dosage, m.reason,
        s.schedule_id, s.time_of_day, s.frequency, s.days_of_week
    FROM elders e
    LEFT JOIN medications m ON e.elder_id = m.elder_id
    LEFT JOIN schedules s ON m.med_id = s.med_id
    WHERE e.elder_id = 1
    ORDER BY s.time_of_day;
    """)
    
    # ========================================================================
    # STEP 5: PYTHON METHODS (No SQL needed - we do it for you)
    # ========================================================================
    print("\n" + "=" * 80)
    print("[STEP 5] PYTHON METHODS (Easy Way - No SQL Coding)")
    print("=" * 80)
    
    print("""
    # Get Person 1
    manager = MedicationManager(db)
    
    # 1. Get elder info
    elder = manager.get_elder(elder_id=1)
    
    # 2. Get medications
    meds = manager.get_medications(elder_id=1)
    
    # 3. Get schedules
    schedules = manager.get_schedules(elder_id=1)
    
    # 4. Get due medications (next 4 hours)
    reminder = MedicationReminder(manager)
    due_meds = reminder.get_due_medications(elder_id=1, within_hours=4)
    
    # 5. Get compliance (7 days)
    compliance = reminder.get_compliance_report(elder_id=1, days=7)
    """)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
The code KNOWS the construction by:

1. DATABASE SCHEMA:
   - Each table has columns (components)
   - elder_id is the key to find Person 1
   
2. FOREIGN KEYS:
   - elder_id links: elders -> medications -> schedules
   - This creates the relationship chain
   
3. MANAGER METHODS:
   - get_elder(1) finds Person 1
   - get_medications(1) finds Person 1's drugs
   - get_schedules(1) finds Person 1's medication times
   
4. PYTHON CODE AUTOMATICALLY BUILDS THE SQL:
   - You call: manager.get_elder(1)
   - It runs: SELECT * FROM elders WHERE elder_id = 1
   - You get back: dict with all person 1 components
   
5. NO MANUAL SQL NEEDED:
   - The system handles all SELECT statements
   - You just call the Python methods
   - It retrieves the complete construction/components
    """)


if __name__ == "__main__":
    show_sql_construction()
