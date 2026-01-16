# 🏥 Elder Medication Management System

## Overview
A complete medication reminder and tracking system for elderly care. Manages medication schedules, sends reminders, tracks compliance, and integrates with YOLOv4 person detection.

---

## ✨ Features

✅ **Elder Management** - Add/manage elderly individuals with contact info
✅ **Medication Tracking** - Store all medications, dosages, reasons, side effects
✅ **Scheduling** - Set medication times, frequency, and duration
✅ **Reminders** - Get alerts when medications are due
✅ **Compliance Tracking** - Record when doses are actually taken
✅ **Compliance Reports** - View medication adherence statistics
✅ **YOLOv4 Integration** - Detect elders in camera + auto-show their meds
✅ **Database Persistence** - Store all data in SQLite

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `elder_medication_system.py` | Core system with database and logic |
| `elder_medication_examples.py` | 10 practical usage examples |
| `README_ELDER_MED.md` | This quick reference guide |

---

## 🚀 Quick Start

### Installation
```python
# No external dependencies needed! Uses only built-in sqlite3
```

### Basic Setup
```python
from elder_medication_system import (
    setup_medication_database,
    MedicationManager,
    MedicationReminder
)

# Initialize
db = setup_medication_database()
manager = MedicationManager(db)
reminder = MedicationReminder(manager)
```

---

## 📚 Common Tasks

### 1. Add an Elder
```python
elder_id = manager.add_elder(
    name="John Smith",
    age=78,
    phone="555-0101",
    emergency_contact="Alice Smith (daughter)",
    address="123 Main St"
)
```

### 2. Add a Medication
```python
med_id = manager.add_medication(
    elder_id=1,
    med_name="Metformin",
    dosage="500mg",
    reason="Type 2 Diabetes",
    side_effects="Nausea, dizziness",
    notes="Take with food"
)
```

### 3. Create a Schedule
```python
schedule_id = manager.add_schedule(
    med_id=1,
    time_of_day="08:00",  # 8:00 AM
    frequency="Once daily",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-01",
    end_date="2025-12-31"
)
```

### 4. Check Due Medications
```python
# Get medications due in next 2 hours
due_meds = reminder.get_due_medications(elder_id=1, within_hours=2)

for med in due_meds:
    print(f"⏰ {med['name']} ({med['dosage']})")
    print(f"   Time: {med['time']}")
    print(f"   Status: {med['status']}")
```

### 5. Mark Dose as Taken
```python
reminder.mark_dose_taken(
    schedule_id=1,
    notes="Taken with breakfast"
)
```

### 6. Get Compliance Report
```python
# Get medication compliance for last 7 days
report = reminder.get_compliance_report(elder_id=1, days=7)

for med in report['medications']:
    print(f"{med['name']}: {med['compliance_percent']}%")
```

### 7. Update Medication Details
```python
manager.update_medication(
    med_id=1,
    dosage="750mg",  # New dosage
    notes="Increased dose per doctor"
)
```

### 8. Update Schedule
```python
manager.update_schedule(
    schedule_id=1,
    time_of_day="09:00",  # Change time
    end_date="2025-06-30"  # New expiration
)
```

### 9. View All Data
```python
# Get all elders
elders = manager.get_all_elders()

# Get elder's medications
meds = manager.get_medications(elder_id=1)

# Get medication schedules
schedules = manager.get_schedules(elder_id=1)
```

### 10. Delete Medication
```python
manager.delete_medication(med_id=1)
```

---

## 🔗 Integration with YOLOv4

Combine person detection with medication management:

```python
from yolov4_demo import YOLOv4Detector, YOLOv4withML
from elder_medication_system import MedicationManager, MedicationReminder

# 1. Detect person in camera
detector = YOLOv4Detector()
pipeline = YOLOv4withML(detector)
results = pipeline.detect_and_identify("camera_feed.jpg")

# 2. For each identified person, get their medications
db = setup_medication_database()
manager = MedicationManager(db)
reminder = MedicationReminder(manager)

for person in results['identified_persons']:
    elder_id = person['database_info']['person_id']
    
    # 3. Check if they need medication
    due_meds = reminder.get_due_medications(elder_id, within_hours=1)
    
    if due_meds:
        print(f"🔔 ALERT: {person['database_info']['name']}")
        print(f"   Medication due: {due_meds[0]['name']}")
        print(f"   Time: {due_meds[0]['time']}")
```

---

## 📊 Database Structure

### Elders Table
```
elder_id: Unique ID
name: Elder's name
age: Age in years
phone: Contact number
emergency_contact: Person to call in emergency
address: Home address
```

### Medications Table
```
med_id: Unique ID
elder_id: Reference to elder
med_name: Name of medication
dosage: Dose amount (e.g., 500mg)
reason: Why prescribed (e.g., Diabetes)
side_effects: Possible side effects
notes: Additional notes
```

### Schedules Table
```
schedule_id: Unique ID
med_id: Reference to medication
time_of_day: When to take (HH:MM format)
frequency: How often (e.g., "Once daily")
days_of_week: Which days (e.g., "Mon,Tue,Wed...")
start_date: When to start (YYYY-MM-DD)
end_date: When to stop (YYYY-MM-DD)
```

### Doses Taken Table
```
dose_id: Unique ID
schedule_id: Reference to schedule
date: Date taken (YYYY-MM-DD)
time_taken: Time actually taken (HH:MM:SS)
taken: 1 if taken, 0 if missed
notes: Any notes about the dose
```

---

## 💡 Real-World Examples

### Example 1: Morning Routine
```python
# Morning checklist
print("🌅 Morning Medications (7:00-9:00 AM)")
morning_meds = reminder.get_due_medications(elder_id=1, within_hours=2)

for med in morning_meds:
    print(f"  □ {med['name']} ({med['dosage']})")
    # Caregiver marks it taken
    reminder.mark_dose_taken(med['schedule_id'])
```

### Example 2: Compliance Alert
```python
# Check if elder is taking medications regularly
report = reminder.get_compliance_report(elder_id=1, days=30)

for med_report in report['medications']:
    if med_report['compliance_percent'] < 80:
        print(f"⚠️ LOW COMPLIANCE: {med_report['name']}")
        print(f"   Only {med_report['taken']}/{med_report['scheduled']} doses taken")
        # Send alert to caregiver
```

### Example 3: Medication Change
```python
# Doctor changed prescription
manager.update_schedule(
    schedule_id=5,
    end_date="2025-01-15"  # Stop old medication
)

# Add new medication with new schedule
new_med_id = manager.add_medication(
    elder_id=1,
    med_name="New Medication",
    dosage="10mg",
    reason="Prescribed by Dr. Smith"
)

manager.add_schedule(
    med_id=new_med_id,
    time_of_day="08:00",
    frequency="Once daily",
    days_of_week="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
    start_date="2025-01-16",
    end_date="2025-12-31"
)
```

---

## ⏰ Reminder System

The reminder system checks medications due in a specified time window:

```python
# Get medications due in next 2 hours
due = reminder.get_due_medications(elder_id=1, within_hours=2)

# Each medication has:
# - name: Medication name
# - dosage: Dose amount
# - time: Scheduled time
# - status: "DUE NOW" or "DUE IN X HOURS"
# - hours_until: Exact hours until due
```

---

## 📈 Compliance Tracking

Monitor how well elders take their medications:

```python
report = reminder.get_compliance_report(elder_id=1, days=7)

# Shows for each medication:
# - scheduled: How many times it should be taken
# - taken: How many times it was actually taken
# - compliance_percent: Percentage (0-100%)
```

Example output:
```
Metformin: 7 scheduled, 7 taken → 100% ✓
Lisinopril: 7 scheduled, 6 taken → 85.7% ⚠
Aspirin: 7 scheduled, 5 taken → 71.4% 🔴
```

---

## 🎯 Workflow Example

**Complete workflow for daily medication management:**

```python
# Morning: Check who needs medication
print("🌅 MORNING CHECK")
for elder in manager.get_all_elders():
    due = reminder.get_due_medications(elder['elder_id'], within_hours=1)
    if due:
        print(f"{elder['name']}: {len(due)} medication(s) due")

# Afternoon: Update medication taken
print("\n🌤 MARK DOSES")
reminder.mark_dose_taken(schedule_id=1, notes="Taken at 8:15 AM")
reminder.mark_dose_taken(schedule_id=2, notes="Taken at 8:30 AM")

# Evening: Generate compliance report
print("\n🌙 DAILY REPORT")
report = reminder.get_compliance_report(elder_id=1, days=1)
for med in report['medications']:
    status = "✓" if med['compliance_percent'] == 100 else "✗"
    print(f"{status} {med['name']}: {med['compliance_percent']}%")
```

---

## 🔧 Customization

### Change Time Format
Currently uses 24-hour format (08:00, 20:00). To use 12-hour:
```python
# In get_due_medications, convert:
time_12h = datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p")
```

### Add Reminders via Email/SMS
```python
def send_reminder(elder_name, med_name):
    # Integrate with email/SMS service
    message = f"{elder_name}, time for {med_name}"
    # send_sms(elder_phone, message)
```

### Database Persistence
Change from in-memory to file:
```python
# In setup_medication_database()
conn = sqlite3.connect('medications.db')  # File-based
```

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Medications not showing as due | Check time format (use 24-hour: "08:00") |
| Compliance shows 0% | Need to mark doses with `mark_dose_taken()` |
| Schedule expires too early | Update end_date: `manager.update_schedule(..., end_date="2025-12-31")` |
| Can't find elder | Verify elder_id with `manager.get_all_elders()` |

---

## 📝 Examples Files

Run the examples to see all features in action:

```bash
python elder_medication_examples.py
```

This runs 10 complete examples:
1. Add new elder
2. Add medications
3. Create schedule
4. Check due medications
5. Mark dose as taken
6. Update medication
7. Update schedule
8. Compliance report
9. Daily routine
10. YOLOv4 integration

---

## 🎓 Learning Path

1. **Start here:** `elder_medication_system.py` - See the core classes
2. **Try examples:** `elder_medication_examples.py` - Learn by doing
3. **Integrate:** Combine with YOLOv4 for complete solution
4. **Extend:** Add email/SMS reminders, web interface, mobile app

---

## 💾 Saving to File (Optional)

To persist data to disk instead of memory:

```python
# Change in setup_medication_database():
# FROM:
conn = sqlite3.connect(':memory:')

# TO:
conn = sqlite3.connect('elders_medications.db')
```

Then all data survives program restarts!

---

## ✅ Checklist for Implementation

- [ ] Set up medication database
- [ ] Add elders to system
- [ ] Add medications for each elder
- [ ] Create medication schedules
- [ ] Set up reminder notifications
- [ ] Track doses taken daily
- [ ] Review compliance reports weekly
- [ ] Integrate with YOLOv4 camera system
- [ ] Set up automatic alerts (email/SMS)
- [ ] Train caregivers on system

---

**System ready to use! Start with the examples and customize as needed. 🎯**
