"""
DATA SETUP SCRIPT
Initialize sample data and database for the medication management system
"""

import sys
import os
from pathlib import Path
import sqlite3

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir / 'code'))

print("\n" + "="*70)
print("DATA SETUP - Medication Management System")
print("="*70)

# Create data directory
data_dir = parent_dir / 'data'
data_dir.mkdir(exist_ok=True)
print(f"\n[CREATE] Data directory: {data_dir}")

# Database file path
db_file = data_dir / 'medications.db'
print(f"[DATABASE] {db_file}")

# Create database connection
try:
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    print("[OK] Database connected")
except Exception as e:
    print(f"[ERROR] Database connection failed: {e}")
    sys.exit(1)

# Create tables
print("\n[CREATE] Database tables...")

try:
    # Persons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            notes TEXT
        )
    ''')
    print("  ✓ persons")

    # Medications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT,
            side_effects TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id)
        )
    ''')
    print("  ✓ medications")

    # Schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY,
            medication_id INTEGER,
            time_of_day TEXT,
            FOREIGN KEY(medication_id) REFERENCES medications(id)
        )
    ''')
    print("  ✓ schedules")

    # Doses taken table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doses_taken (
            id INTEGER PRIMARY KEY,
            medication_id INTEGER,
            date_taken TEXT,
            FOREIGN KEY(medication_id) REFERENCES medications(id)
        )
    ''')
    print("  ✓ doses_taken")

    conn.commit()
    print("[OK] Tables created")

except Exception as e:
    print(f"[ERROR] Table creation failed: {e}")
    conn.close()
    sys.exit(1)

# Insert sample data
print("\n[INSERT] Sample data...")

try:
    # Sample persons
    persons_data = [
        (1, 'John Smith', 75, 'Hypertension, Diabetes Type 2'),
        (2, 'Mary Johnson', 82, 'Arthritis, High Cholesterol'),
        (3, 'Robert Brown', 68, 'Heart Disease, Atrial Fibrillation')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO persons (id, name, age, notes)
        VALUES (?, ?, ?, ?)
    ''', persons_data)
    print("  ✓ Persons (3 elders)")

    # Sample medications
    medications_data = [
        # John Smith (id=1)
        (1, 1, 'Lisinopril', '10mg', 'Daily', 'Dizziness, Dry cough'),
        (2, 1, 'Metformin', '500mg', 'Twice daily', 'Nausea, Stomach upset'),
        
        # Mary Johnson (id=2)
        (3, 2, 'Ibuprofen', '200mg', 'As needed', 'Stomach pain, Heartburn'),
        (4, 2, 'Atorvastatin', '20mg', 'Daily', 'Muscle pain, Weakness'),
        
        # Robert Brown (id=3)
        (5, 3, 'Warfarin', '5mg', 'Daily', 'Bleeding risk, Bruising'),
        (6, 3, 'Digoxin', '0.25mg', 'Daily', 'Nausea, Vision changes'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO medications (id, person_id, name, dosage, frequency, side_effects)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', medications_data)
    print("  ✓ Medications (6 total)")

    # Sample schedules
    schedules_data = [
        (1, 1, 'Morning'),     # Lisinopril - Morning
        (2, 2, 'Morning'),     # Metformin - Morning
        (3, 2, 'Evening'),     # Metformin - Evening
        (4, 3, 'As needed'),   # Ibuprofen - As needed
        (5, 4, 'Evening'),     # Atorvastatin - Evening
        (6, 5, 'Morning'),     # Warfarin - Morning
        (7, 6, 'Morning'),     # Digoxin - Morning
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO schedules (id, medication_id, time_of_day)
        VALUES (?, ?, ?)
    ''', schedules_data)
    print("  ✓ Schedules (7 total)")

    conn.commit()
    print("[OK] Sample data inserted")

except Exception as e:
    print(f"[ERROR] Data insertion failed: {e}")
    conn.close()
    sys.exit(1)

finally:
    conn.close()

# Create models directory structure
print("\n[CREATE] Model directories...")

model_dirs = [
    'models/yolov4',
    'models/teachable_machine',
    'models/custom',
    'logs'
]

for dir_path in model_dirs:
    full_path = parent_dir / dir_path
    full_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {dir_path}")

# Create .gitkeep files to preserve empty directories
for dir_path in model_dirs:
    gitkeep = parent_dir / dir_path / '.gitkeep'
    gitkeep.touch()

print("\n" + "="*70)
print("DATA SETUP COMPLETE")
print("="*70)
print("""
Database initialized with sample data:
  - 3 elderly persons (John, Mary, Robert)
  - 6 medications with dosages and side effects
  - Medication schedules and compliance tracking

Database location: data/medications.db

Next steps:
  1. Add YOLOv4 weights to models/yolov4/
  2. Configure person mapping in config/settings.py
  3. Run the main program: python run.py

To view the database:
  - Open data/medications.db with SQLite viewer
  - Or run: sqlite3 data/medications.db

""")
