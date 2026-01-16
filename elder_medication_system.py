"""
Elder Medication Reminder System
Tracks medication schedules for elderly people and provides timely reminders.
"""

import sqlite3
import json
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# ============================================================================
# DATABASE SETUP
# ============================================================================

def setup_medication_database():
    """Create database for elder care medication tracking."""
    # Allow the DB connection to be used from other threads (the camera server
    # runs request handlers in separate threads that may need DB access).
    # For an in-memory database the same connection object must be shared;
    # setting check_same_thread=False permits cross-thread usage.
    conn = sqlite3.connect(':memory:', check_same_thread=False)  # Use file path for persistence
    cursor = conn.cursor()
    
    # Elders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elders (
            elder_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            phone TEXT,
            emergency_contact TEXT,
            address TEXT,
            external_id TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            med_id INTEGER PRIMARY KEY,
            elder_id INTEGER NOT NULL,
            med_name TEXT NOT NULL,
            dosage TEXT,
            reason TEXT,
            side_effects TEXT,
            notes TEXT,
            FOREIGN KEY (elder_id) REFERENCES elders(elder_id)
        )
    ''')
    
    # Medication schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            schedule_id INTEGER PRIMARY KEY,
            med_id INTEGER NOT NULL,
            time_of_day TEXT,
            frequency TEXT,
            days_of_week TEXT,
            start_date DATE,
            end_date DATE,
            FOREIGN KEY (med_id) REFERENCES medications(med_id)
        )
    ''')
    
    # Doses taken table (for tracking compliance)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doses_taken (
            dose_id INTEGER PRIMARY KEY,
            schedule_id INTEGER NOT NULL,
            date DATE,
            time_taken TIME,
            taken INTEGER,
            notes TEXT,
            FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id)
        )
    ''')
    
    # Insert sample data
    sample_elders = [
        (1, "John Smith", 78, "555-0101", "Alice Smith (daughter)", "123 Main St", '12345678'),
        (2, "Mary Johnson", 82, "555-0102", "Bob Johnson (son)", "456 Oak Ave", '98765432'),
        (3, "Robert Brown", 75, "555-0103", "Carol Brown (wife)", "789 Pine Rd", '13572468'),
    ]
    
    cursor.executemany(
        'INSERT INTO elders (elder_id, name, age, phone, emergency_contact, address, external_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        sample_elders
    )
    
    # Sample medications for elder 1 (John Smith)
    sample_meds = [
        (1, 1, "Metformin", "500mg", "Type 2 Diabetes", "Nausea, dizziness", "Take with food"),
        (2, 1, "Lisinopril", "10mg", "High Blood Pressure", "Dry cough", "Take in morning"),
        (3, 1, "Aspirin", "81mg", "Heart Disease Prevention", "None", "Take daily"),
        (4, 2, "Amlodipine", "5mg", "Hypertension", "Swelling in legs", ""),
        (5, 2, "Omeprazole", "20mg", "Acid Reflux", "Headache", "Take 30 min before food"),
    ]
    
    cursor.executemany(
        'INSERT INTO medications (med_id, elder_id, med_name, dosage, reason, side_effects, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
        sample_meds
    )
    
    # Sample schedules
    sample_schedules = [
        (1, 1, "08:00", "Once daily", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "2025-01-01", "2025-12-31"),
        (2, 1, "07:00", "Once daily", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "2025-01-01", "2025-12-31"),
        (3, 1, "20:00", "Once daily", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "2025-01-01", "2025-12-31"),
        (4, 2, "09:00", "Once daily", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "2025-01-01", "2025-12-31"),
        (5, 2, "07:30", "Once daily", "Mon,Tue,Wed,Thu,Fri,Sat,Sun", "2025-01-01", "2025-12-31"),
    ]
    
    cursor.executemany(
        'INSERT INTO schedules (schedule_id, med_id, time_of_day, frequency, days_of_week, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
        sample_schedules
    )
    
    conn.commit()
    return conn


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Medication:
    """Represents a single medication."""
    med_id: int
    med_name: str
    dosage: str
    reason: str
    side_effects: str
    notes: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'med_id': self.med_id,
            'name': self.med_name,
            'dosage': self.dosage,
            'reason': self.reason,
            'side_effects': self.side_effects,
            'notes': self.notes
        }


@dataclass
class Schedule:
    """Represents a medication schedule."""
    schedule_id: int
    med_id: int
    time_of_day: str
    frequency: str
    days_of_week: str
    start_date: str
    end_date: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'schedule_id': self.schedule_id,
            'med_id': self.med_id,
            'time': self.time_of_day,
            'frequency': self.frequency,
            'days': self.days_of_week,
            'start': self.start_date,
            'end': self.end_date
        }


@dataclass
class Elder:
    """Represents an elderly person."""
    elder_id: int
    name: str
    age: int
    phone: str
    emergency_contact: str
    address: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'elder_id': self.elder_id,
            'name': self.name,
            'age': self.age,
            'phone': self.phone,
            'emergency_contact': self.emergency_contact,
            'address': self.address
        }


# ============================================================================
# MEDICATION MANAGER
# ============================================================================

class MedicationManager:
    """Manages medications and schedules for elders."""
    
    def __init__(self, db_conn):
        self.conn = db_conn
        # Lock to serialize DB access across threads
        self._lock = threading.Lock()

    @contextmanager
    def locked_cursor(self):
        """Context manager that yields a DB cursor while holding the lock.

        Use this to ensure all DB reads/writes are serialized when the same
        sqlite3 connection is shared across threads.
        """
        self._lock.acquire()
        try:
            cur = self.conn.cursor()
            yield cur
        finally:
            self._lock.release()
    
    def get_elder(self, elder_id: int) -> Optional[Dict[str, Any]]:
        """Get elder information."""
        with self.locked_cursor() as cursor:
            cursor.execute('SELECT * FROM elders WHERE elder_id = ?', (elder_id,))
            row = cursor.fetchone()
        
        if row:
            return {
                'elder_id': row[0],
                'name': row[1],
                'age': row[2],
                'phone': row[3],
                'emergency_contact': row[4],
                'address': row[5],
                'external_id': row[6]
            }
        return None
    
    def get_all_elders(self) -> List[Dict[str, Any]]:
        """Get all elders."""
        with self.locked_cursor() as cursor:
            cursor.execute('SELECT * FROM elders')
            
            elders = []
            for row in cursor.fetchall():
                elders.append({
                    'elder_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'phone': row[3],
                    'emergency_contact': row[4],
                    'address': row[5],
                    'external_id': row[6]
                })
        return elders
    
    def add_elder(self, name: str, age: int, phone: str, emergency_contact: str, address: str) -> int:
        """Add a new elder to the database."""
        with self.locked_cursor() as cursor:
            cursor.execute(
                'INSERT INTO elders (name, age, phone, emergency_contact, address) VALUES (?, ?, ?, ?, ?)',
                (name, age, phone, emergency_contact, address)
            )
            self.conn.commit()
            return cursor.lastrowid
    
    def get_medications(self, elder_id: int) -> List[Dict[str, Any]]:
        """Get all medications for an elder."""
        with self.locked_cursor() as cursor:
            cursor.execute(
                'SELECT * FROM medications WHERE elder_id = ?',
                (elder_id,)
            )
            
            meds = []
            for row in cursor.fetchall():
                meds.append({
                    'med_id': row[0],
                    'elder_id': row[1],
                    'name': row[2],
                    'dosage': row[3],
                    'reason': row[4],
                    'side_effects': row[5],
                    'notes': row[6]
                })
        return meds

    def get_elder_by_external_id(self, external_id: str) -> Optional[Dict[str, Any]]:
        """Lookup an elder by their external ID (8-digit unique ID)."""
        with self.locked_cursor() as cursor:
            cursor.execute('SELECT * FROM elders WHERE external_id = ?', (str(external_id),))
            row = cursor.fetchone()
        if row:
            return {
                'elder_id': row[0],
                'name': row[1],
                'age': row[2],
                'phone': row[3],
                'emergency_contact': row[4],
                'address': row[5],
                'external_id': row[6]
            }
        return None

    def get_elder_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Lookup an elder by their name (case-insensitive, exact or partial match)."""
        with self.locked_cursor() as cursor:
            # Try exact match first
            cursor.execute('SELECT * FROM elders WHERE name = ?', (name,))
            row = cursor.fetchone()
        if row:
            return {
                'elder_id': row[0],
                'name': row[1],
                'age': row[2],
                'phone': row[3],
                'emergency_contact': row[4],
                'address': row[5],
                'external_id': row[6]
            }
        # Fallback to partial case-insensitive match
            cursor.execute('SELECT * FROM elders WHERE lower(name) LIKE lower(?)', (f"%{name}%",))
            row = cursor.fetchone()
            if row:
                return {
                    'elder_id': row[0],
                    'name': row[1],
                    'age': row[2],
                    'phone': row[3],
                    'emergency_contact': row[4],
                    'address': row[5],
                    'external_id': row[6]
                }
        return None
    
    def add_medication(self, elder_id: int, med_name: str, dosage: str, reason: str, 
                      side_effects: str = "", notes: str = "") -> int:
        """Add a medication for an elder."""
        with self.locked_cursor() as cursor:
            cursor.execute(
                'INSERT INTO medications (elder_id, med_name, dosage, reason, side_effects, notes) VALUES (?, ?, ?, ?, ?, ?)',
                (elder_id, med_name, dosage, reason, side_effects, notes)
            )
            self.conn.commit()
            return cursor.lastrowid
    
    def update_medication(self, med_id: int, dosage: str = None, reason: str = None, 
                         side_effects: str = None, notes: str = None):
        """Update a medication."""
        with self.locked_cursor() as cursor:
            
            updates = []
            values = []
        
        if dosage is not None:
            updates.append("dosage = ?")
            values.append(dosage)
        if reason is not None:
            updates.append("reason = ?")
            values.append(reason)
        if side_effects is not None:
            updates.append("side_effects = ?")
            values.append(side_effects)
        if notes is not None:
            updates.append("notes = ?")
            values.append(notes)
        
            if updates:
                values.append(med_id)
                query = f"UPDATE medications SET {', '.join(updates)} WHERE med_id = ?"
                cursor.execute(query, values)
                self.conn.commit()
    
    def get_schedules(self, med_id: int = None, elder_id: int = None) -> List[Dict[str, Any]]:
        """Get schedules. Can filter by med_id or elder_id."""
        with self.locked_cursor() as cursor:
            
            if med_id:
                cursor.execute('SELECT * FROM schedules WHERE med_id = ?', (med_id,))
            elif elder_id:
                cursor.execute('''
                    SELECT s.* FROM schedules s
                    JOIN medications m ON s.med_id = m.med_id
                    WHERE m.elder_id = ?
                ''', (elder_id,))
            else:
                cursor.execute('SELECT * FROM schedules')
            
            schedules = []
            for row in cursor.fetchall():
                schedules.append({
                    'schedule_id': row[0],
                    'med_id': row[1],
                    'time': row[2],
                    'frequency': row[3],
                    'days': row[4],
                    'start_date': row[5],
                    'end_date': row[6]
                })
        return schedules
    
    def add_schedule(self, med_id: int, time_of_day: str, frequency: str, days_of_week: str,
                    start_date: str, end_date: str) -> int:
        """Add a medication schedule."""
        with self.locked_cursor() as cursor:
            cursor.execute(
                'INSERT INTO schedules (med_id, time_of_day, frequency, days_of_week, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)',
                (med_id, time_of_day, frequency, days_of_week, start_date, end_date)
            )
            self.conn.commit()
            return cursor.lastrowid
    
    def update_schedule(self, schedule_id: int, time_of_day: str = None, frequency: str = None, 
                       days_of_week: str = None, end_date: str = None):
        """Update a schedule."""
        with self.locked_cursor() as cursor:
            
            updates = []
            values = []
            
            if time_of_day is not None:
                updates.append("time_of_day = ?")
                values.append(time_of_day)
            if frequency is not None:
                updates.append("frequency = ?")
                values.append(frequency)
            if days_of_week is not None:
                updates.append("days_of_week = ?")
                values.append(days_of_week)
            if end_date is not None:
                updates.append("end_date = ?")
                values.append(end_date)
            
            if updates:
                values.append(schedule_id)
                query = f"UPDATE schedules SET {', '.join(updates)} WHERE schedule_id = ?"
                cursor.execute(query, values)
                self.conn.commit()
    
    def delete_medication(self, med_id: int):
        """Delete a medication (and its schedules)."""
        with self.locked_cursor() as cursor:
            cursor.execute('DELETE FROM schedules WHERE med_id = ?', (med_id,))
            cursor.execute('DELETE FROM medications WHERE med_id = ?', (med_id,))
            self.conn.commit()


# ============================================================================
# REMINDER SYSTEM
# ============================================================================

class MedicationReminder:
    """Generates reminders for upcoming medications."""
    
    def __init__(self, manager: MedicationManager):
        self.manager = manager
    
    def get_due_medications(self, elder_id: int, within_hours: int = 2) -> List[Dict[str, Any]]:
        """
        Get medications due within X hours for an elder.
        Returns list of medications that need to be taken.
        """
        with self.manager.locked_cursor() as cursor:
            # Get all medications and schedules for this elder
            cursor.execute('''
                SELECT m.med_id, m.med_name, m.dosage, s.time_of_day, s.schedule_id
                FROM medications m
                JOIN schedules s ON m.med_id = s.med_id
                WHERE m.elder_id = ?
                AND DATE(s.start_date) <= DATE('now')
                AND DATE(s.end_date) >= DATE('now')
            ''', (elder_id,))
        
        due_meds = []
        current_time = datetime.now()
        
        for row in cursor.fetchall():
            med_id, med_name, dosage, time_str, schedule_id = row
            
            # Parse time
            med_time = datetime.strptime(time_str, "%H:%M")
            med_time = med_time.replace(
                year=current_time.year,
                month=current_time.month,
                day=current_time.day
            )
            
            # Check if due within timeframe
            time_diff = (med_time - current_time).total_seconds() / 3600
            
            if 0 <= time_diff <= within_hours:
                due_meds.append({
                    'med_id': med_id,
                    'name': med_name,
                    'dosage': dosage,
                    'time': time_str,
                    'schedule_id': schedule_id,
                    'hours_until': time_diff,
                    'status': 'DUE NOW' if time_diff < 1 else f'DUE IN {int(time_diff)} HOURS'
                })
        
        # Sort by time due
        due_meds.sort(key=lambda x: x['hours_until'])
        return due_meds
    
    def mark_dose_taken(self, schedule_id: int, date: str = None, time_taken: str = None, notes: str = ""):
        """Record that a dose was taken."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if time_taken is None:
            time_taken = datetime.now().strftime("%H:%M:%S")
        
        with self.manager.locked_cursor() as cursor:
            cursor.execute(
                'INSERT INTO doses_taken (schedule_id, date, time_taken, taken, notes) VALUES (?, ?, ?, 1, ?)',
                (schedule_id, date, time_taken, notes)
            )
            self.manager.conn.commit()
    
    def get_compliance_report(self, elder_id: int, days: int = 7) -> Dict[str, Any]:
        """Get medication compliance report for past X days."""
        with self.manager.locked_cursor() as cursor:
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            cursor.execute('''
                SELECT m.med_name, COUNT(*) as scheduled, 
                       SUM(CASE WHEN dt.taken = 1 THEN 1 ELSE 0 END) as taken
                FROM medications m
                JOIN schedules s ON m.med_id = s.med_id
                LEFT JOIN doses_taken dt ON s.schedule_id = dt.schedule_id AND dt.date >= ?
                WHERE m.elder_id = ?
                GROUP BY m.med_id, m.med_name
            ''', (start_date, elder_id))

            report = {
                'elder_id': elder_id,
                'period_days': days,
                'medications': []
            }

            for row in cursor.fetchall():
                med_name, scheduled, taken = row
                compliance = (taken / scheduled * 100) if scheduled > 0 else 0

                report['medications'].append({
                    'name': med_name,
                    'scheduled': scheduled,
                    'taken': taken or 0,
                    'compliance_percent': round(compliance, 1)
                })

        return report


# ============================================================================
# DEMO
# ============================================================================

def main():
    print("=" * 70)
    print("🏥 ELDER MEDICATION REMINDER SYSTEM")
    print("=" * 70)
    
    # Setup database
    print("\n1️⃣  Setting up medication database...")
    db = setup_medication_database()
    manager = MedicationManager(db)
    reminder = MedicationReminder(manager)
    
    # Show all elders
    print("\n2️⃣  Registered Elders:")
    print("-" * 70)
    elders = manager.get_all_elders()
    for elder in elders:
        print(f"  {elder['elder_id']}. {elder['name']}, Age {elder['age']}")
        print(f"     Phone: {elder['phone']}")
        print(f"     Emergency: {elder['emergency_contact']}")
    
    # Show medications for first elder
    elder_id = 1
    print(f"\n3️⃣  Medications for {elders[0]['name']}:")
    print("-" * 70)
    meds = manager.get_medications(elder_id)
    for med in meds:
        print(f"  • {med['name']} ({med['dosage']})")
        print(f"    Reason: {med['reason']}")
        print(f"    Side effects: {med['side_effects']}")
    
    # Show schedules
    print(f"\n4️⃣  Medication Schedule for {elders[0]['name']}:")
    print("-" * 70)
    schedules = manager.get_schedules(elder_id=elder_id)
    
    # Get medication names for reference
    med_dict = {med['med_id']: med['name'] for med in meds}
    
    for schedule in schedules:
        med_name = med_dict.get(schedule['med_id'], 'Unknown')
        print(f"  • {med_name}")
        print(f"    Time: {schedule['time']}")
        print(f"    Frequency: {schedule['frequency']}")
        print(f"    Days: {schedule['days']}")
    
    # Show due medications
    print(f"\n5️⃣  Due Medications for {elders[0]['name']} (Next 2 Hours):")
    print("-" * 70)
    due_meds = reminder.get_due_medications(elder_id, within_hours=2)
    
    if due_meds:
        for med in due_meds:
            print(f"  ⏰ {med['name']} ({med['dosage']})")
            print(f"     Time: {med['time']}")
            print(f"     Status: {med['status']}")
    else:
        print("  ✓ No medications due in the next 2 hours")
    
    # Mark a dose as taken
    if due_meds:
        print(f"\n6️⃣  Marking dose as taken:")
        print("-" * 70)
        first_due = due_meds[0]
        reminder.mark_dose_taken(first_due['schedule_id'], notes="Taken as scheduled")
        print(f"  ✓ {first_due['name']} marked as taken")
    
    # Show compliance report
    print(f"\n7️⃣  Compliance Report (Last 7 Days) for {elders[0]['name']}:")
    print("-" * 70)
    report = reminder.get_compliance_report(elder_id, days=7)
    
    total_scheduled = sum(m['scheduled'] for m in report['medications'])
    total_taken = sum(m['taken'] for m in report['medications'])
    
    for med_report in report['medications']:
        print(f"  • {med_report['name']}")
        print(f"    Scheduled: {med_report['scheduled']}, Taken: {med_report['taken']}, Compliance: {med_report['compliance_percent']}%")
    
    print(f"\n  Overall Compliance: {total_taken}/{total_scheduled} ({(total_taken/total_scheduled*100):.1f}%)" if total_scheduled > 0 else "  No data")
    
    print("\n" + "=" * 70)
    print("✓ Demo Complete!")
    print("=" * 70)
    
    db.close()


if __name__ == "__main__":
    main()
