# 💊 Personalized Medication Guide

## How to Set Up Different Medications for Different Elders

---

## Example Setup

### Person 1: John Smith - Paracetamol (Pain Relief)
```python
# Add medication
paracetamol_id = manager.add_medication(
    elder_id=1,
    med_name="Paracetamol",
    dosage="500mg",
    reason="Pain relief & headaches",
    side_effects="Rare: liver damage if overdosed",
    notes="Maximum 3 doses per day, space 4-6 hours apart"
)

# Add schedule - Morning (required)
manager.add_schedule(
    med_id=paracetamol_id,
    time_of_day="08:00",  # 8:00 AM
    frequency="Once daily",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# Add schedule - Afternoon (optional, as needed)
manager.add_schedule(
    med_id=paracetamol_id,
    time_of_day="14:00",  # 2:00 PM
    frequency="As needed",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# Add schedule - Evening (optional, as needed)
manager.add_schedule(
    med_id=paracetamol_id,
    time_of_day="20:00",  # 8:00 PM
    frequency="As needed",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)
```

**Result:** John Smith takes Paracetamol 3 times a day (morning required, afternoon & evening as needed)

---

### Person 2: Mary Johnson - Cold & Flu Pills (Multiple Medications)
```python
# Medication 1: Cold & Flu Relief Capsules
cold_flu_id = manager.add_medication(
    elder_id=2,
    med_name="Cold & Flu Relief Capsules",
    dosage="1 capsule (contains Paracetamol 500mg + Caffeine 65mg)",
    reason="Treatment of cold and flu symptoms (headache, fever, body ache)",
    side_effects="Mild: insomnia (due to caffeine), dizziness",
    notes="Take with water. Do not take more than 4 capsules in 24 hours"
)

# Schedule 1: Morning
manager.add_schedule(
    med_id=cold_flu_id,
    time_of_day="08:00",
    frequency="Once every 4-6 hours as needed",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# Schedule 2: Midday
manager.add_schedule(
    med_id=cold_flu_id,
    time_of_day="12:00",
    frequency="Once every 4-6 hours as needed",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# Schedule 3: Evening
manager.add_schedule(
    med_id=cold_flu_id,
    time_of_day="18:00",
    frequency="Once every 4-6 hours as needed",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# Medication 2: Cough Suppressant Syrup
cough_syrup_id = manager.add_medication(
    elder_id=2,
    med_name="Cough Suppressant Syrup",
    dosage="2 teaspoons (10ml)",
    reason="Relief from persistent cough",
    side_effects="Drowsiness, dizziness",
    notes="Take at bedtime if cough is severe"
)

# Schedule: Bedtime
manager.add_schedule(
    med_id=cough_syrup_id,
    time_of_day="21:00",
    frequency="Once at bedtime as needed",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)
```

**Result:** Mary Johnson takes Cold & Flu pills 3x daily (8:00, 12:00, 18:00) + Cough syrup at bedtime

---

### Person 3: Robert Brown - Regular Daily Medications
```python
# Medication 1: Aspirin (daily)
aspirin_id = manager.add_medication(
    elder_id=3,
    med_name="Aspirin",
    dosage="81mg (Low-dose)",
    reason="Heart disease prevention & blood thinner",
    side_effects="Mild stomach upset, increased bleeding risk",
    notes="Take with food or after meals"
)

manager.add_schedule(
    med_id=aspirin_id,
    time_of_day="07:00",
    frequency="Once daily",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# Medication 2: Vitamin D (daily)
vitamin_d_id = manager.add_medication(
    elder_id=3,
    med_name="Vitamin D3",
    dosage="1000 IU",
    reason="Bone health & calcium absorption",
    side_effects="None (at this dose)",
    notes="Take with breakfast for better absorption"
)

manager.add_schedule(
    med_id=vitamin_d_id,
    time_of_day="08:00",
    frequency="Once daily",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)
```

**Result:** Robert Brown takes Aspirin at 7:00 AM and Vitamin D at 8:00 AM (both daily)

---

## Quick Commands

### View All Medications for a Person
```python
meds = manager.get_medications(elder_id=1)

for med in meds:
    print(f"• {med['name']} ({med['dosage']})")
    print(f"  Reason: {med['reason']}")
    print(f"  Notes: {med['notes']}")
```

### View All Schedules for a Person
```python
schedules = manager.get_schedules(elder_id=1)

for sched in schedules:
    print(f"• {sched['time']} - Take medication")
    print(f"  Frequency: {sched['frequency']}")
```

### Mark Medication as Taken
```python
reminder.mark_dose_taken(
    schedule_id=1,
    notes="Taken with breakfast"
)
```

### Check Due Medications (Next 2 Hours)
```python
due_meds = reminder.get_due_medications(elder_id=1, within_hours=2)

for med in due_meds:
    print(f"🔔 {med['name']} ({med['dosage']})")
    print(f"   Time: {med['time']}")
    print(f"   Status: {med['status']}")
```

### Get Compliance Report (Last 7 Days)
```python
report = reminder.get_compliance_report(elder_id=1, days=7)

for med_report in report['medications']:
    print(f"{med_report['name']}: {med_report['compliance_percent']}%")
```

### Update Medication Dosage
```python
manager.update_medication(
    med_id=1,
    dosage="750mg"  # New dosage
)
```

### Update Schedule Time
```python
manager.update_schedule(
    schedule_id=1,
    time_of_day="09:00"  # New time
)
```

### Delete a Medication
```python
manager.delete_medication(med_id=1)
```

---

## Time Format Reference

```
Time Format: HH:MM (24-hour)

Examples:
  "07:00" = 7:00 AM
  "08:00" = 8:00 AM
  "12:00" = 12:00 PM (noon)
  "14:00" = 2:00 PM
  "18:00" = 6:00 PM
  "20:00" = 8:00 PM
  "21:00" = 9:00 PM
```

---

## Frequency Options

```
"Once daily"              - Once per day
"Once every 4-6 hours"    - Multiple times spaced out
"Twice daily"             - Morning and evening
"Three times daily"       - Morning, afternoon, evening
"As needed"               - Patient takes when needed
"Once at bedtime"         - Before sleeping
"Weekly"                  - Once per week
```

---

## Days of Week Format

```
"Mon,Tue,Wed,Thu,Fri,Sat,Sun"  - Every day
"Mon,Tue,Wed,Thu,Fri"           - Weekdays only
"Sat,Sun"                        - Weekends only
"Mon,Wed,Fri"                    - Every other day pattern
```

---

## Complete Workflow Example

```python
from elder_medication_system import (
    setup_medication_database,
    MedicationManager,
    MedicationReminder
)

# 1. Initialize
db = setup_medication_database()
manager = MedicationManager(db)
reminder = MedicationReminder(manager)

# 2. Add elder (if not already added)
elder_id = manager.add_elder(
    name="Jane Doe",
    age=70,
    phone="555-0105",
    emergency_contact="John Doe (son)",
    address="456 Church St"
)

# 3. Add medication
med_id = manager.add_medication(
    elder_id=elder_id,
    med_name="Blood Pressure Medicine",
    dosage="10mg",
    reason="High blood pressure",
    side_effects="Dizziness",
    notes="Take with breakfast"
)

# 4. Add schedule
schedule_id = manager.add_schedule(
    med_id=med_id,
    time_of_day="08:00",
    frequency="Once daily",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)

# 5. Check due medications
due = reminder.get_due_medications(elder_id, within_hours=2)
print(f"Due medications: {len(due)}")

# 6. Mark as taken
if due:
    reminder.mark_dose_taken(due[0]['schedule_id'])

# 7. Get compliance
report = reminder.get_compliance_report(elder_id, days=7)
print(f"Compliance: {report}")

db.close()
```

---

## Common Medications for Elders

### Pain Relief
- **Paracetamol (Acetaminophen)** 500-1000mg, 3-4 times daily
- **Ibuprofen** 200-400mg, 3-4 times daily
- **Aspirin** 81-325mg daily

### Cold & Flu
- **Cold & Flu Relief Capsules** 1-2 capsules every 4-6 hours
- **Cough Suppressant Syrup** 10-20ml at bedtime
- **Decongestant** As directed

### Chronic Conditions
- **Blood Pressure Medicine** 1 tablet daily (morning)
- **Diabetes Medicine** 1-2 tablets with meals
- **Heart Medicine** As prescribed
- **Arthritis Medicine** 1-2 tablets with meals

### Supplements
- **Vitamin D** 1000 IU daily
- **Vitamin B12** As prescribed
- **Calcium** With meals
- **Iron** With orange juice

---

## Tips

1. **Use consistent times** - Makes it easier for caregivers to remember
2. **Group morning meds** - Most medications taken in morning
3. **Note side effects** - Helps identify medication interactions
4. **Mark as taken immediately** - Don't wait until end of day
5. **Review monthly** - Check if medications need adjustment
6. **Keep notes** - Document any issues or changes

---

## Files to Use

- `personalized_medications.py` - See complete examples
- `elder_medication_system.py` - Core system
- `elder_medication_examples.py` - More usage examples

Run: `python personalized_medications.py`

---

**Start managing medications for your elders today! 💊**
