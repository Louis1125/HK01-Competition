"""
HOW TO BUILD ML DATASETS IN VS CODE
Outcome: Complete step-by-step guide with practical examples
"""

import csv
import json
import os
from datetime import datetime
import sqlite3


print("\n" + "=" * 80)
print("BUILDING ML DATASETS IN VS CODE - COMPLETE GUIDE")
print("=" * 80)


# ============================================================================
# PART 1: WHAT IS AN ML DATASET?
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: WHAT IS AN ML DATASET?")
print("=" * 80)

print("""
An ML Dataset is:
- Collection of data (examples)
- Input features + expected output
- Used to train machine learning models

EXAMPLE:
Person's age + symptoms → Diagnosis
Input: age=78, headache=yes, fever=no
Output: "mild_pain"

DATABASE EXAMPLE:
Person 1: John Smith, Age 78, Medications: Paracetamol
Person 2: Mary Johnson, Age 82, Medications: Cold & Flu
Person 3: Robert Brown, Age 75, Medications: Aspirin
""")


# ============================================================================
# PART 2: CREATE DATASET AS CSV FILE
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: CREATE DATASET AS CSV FILE")
print("=" * 80)

# Create a simple medication dataset as CSV
dataset_csv = [
    ['person_id', 'name', 'age', 'medication', 'dosage', 'frequency'],
    [1, 'John Smith', 78, 'Paracetamol', '500mg', '3_times_daily'],
    [2, 'Mary Johnson', 82, 'Cold & Flu Pills', '1_capsule', '3_times_daily'],
    [2, 'Mary Johnson', 82, 'Cough Syrup', '2_teaspoons', 'bedtime'],
    [3, 'Robert Brown', 75, 'Aspirin', '81mg', 'once_daily'],
    [3, 'Robert Brown', 75, 'Vitamin D3', '1000_IU', 'once_daily'],
]

print("\nSTEP 1: Create CSV dataset file")
print("-" * 80)

csv_filename = "medication_dataset.csv"
print(f"Creating: {csv_filename}\n")

with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(dataset_csv)

print("[OK] File created!")
print(f"Location: {os.path.abspath(csv_filename)}\n")

print("HOW TO VIEW IN VS CODE:")
print("1. Open VS Code")
print("2. File → Open File → medication_dataset.csv")
print("3. You'll see table format:\n")

# Display the CSV content
print("person_id | name           | age | medication       | dosage      | frequency")
print("-" * 80)
for row in dataset_csv[1:]:
    print(f"{row[0]:<9} | {row[1]:<14} | {row[2]:<3} | {row[3]:<16} | {row[4]:<11} | {row[5]}")


# ============================================================================
# PART 3: CREATE DATASET AS JSON FILE
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: CREATE DATASET AS JSON FILE")
print("=" * 80)

print("\nSTEP 2: Create JSON dataset file")
print("-" * 80)

dataset_json = {
    "metadata": {
        "name": "Medication Dataset",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "total_persons": 3,
        "total_medications": 5
    },
    "persons": [
        {
            "id": 1,
            "name": "John Smith",
            "age": 78,
            "phone": "555-0101",
            "medications": [
                {
                    "name": "Paracetamol",
                    "dosage": "500mg",
                    "frequency": "3 times daily",
                    "reason": "Pain relief"
                }
            ]
        },
        {
            "id": 2,
            "name": "Mary Johnson",
            "age": 82,
            "phone": "555-0102",
            "medications": [
                {
                    "name": "Cold & Flu Pills",
                    "dosage": "1 capsule",
                    "frequency": "3 times daily",
                    "reason": "Cold symptoms"
                },
                {
                    "name": "Cough Syrup",
                    "dosage": "2 teaspoons",
                    "frequency": "bedtime",
                    "reason": "Cough relief"
                }
            ]
        },
        {
            "id": 3,
            "name": "Robert Brown",
            "age": 75,
            "phone": "555-0103",
            "medications": [
                {
                    "name": "Aspirin",
                    "dosage": "81mg",
                    "frequency": "once daily",
                    "reason": "Heart prevention"
                },
                {
                    "name": "Vitamin D3",
                    "dosage": "1000 IU",
                    "frequency": "once daily",
                    "reason": "Bone health"
                }
            ]
        }
    ]
}

json_filename = "medication_dataset.json"
print(f"Creating: {json_filename}\n")

with open(json_filename, 'w') as f:
    json.dump(dataset_json, f, indent=2)

print("[OK] File created!")
print(f"Location: {os.path.abspath(json_filename)}\n")

print("HOW TO VIEW IN VS CODE:")
print("1. File → Open File → medication_dataset.json")
print("2. VS Code shows JSON tree structure")
print("3. Click arrows to expand/collapse\n")


# ============================================================================
# PART 4: CREATE DATASET AS SQLITE DATABASE
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: CREATE DATASET AS SQLITE DATABASE")
print("=" * 80)

print("\nSTEP 3: Create SQLite database file")
print("-" * 80)

db_filename = "medication_dataset.db"
print(f"Creating: {db_filename}\n")

# Create database
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        phone TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY,
        person_id INTEGER,
        name TEXT,
        dosage TEXT,
        frequency TEXT,
        reason TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id)
    )
''')

# Insert data
persons_data = [
    (1, 'John Smith', 78, '555-0101'),
    (2, 'Mary Johnson', 82, '555-0102'),
    (3, 'Robert Brown', 75, '555-0103'),
]

medications_data = [
    (1, 1, 'Paracetamol', '500mg', '3 times daily', 'Pain relief'),
    (2, 2, 'Cold & Flu Pills', '1 capsule', '3 times daily', 'Cold symptoms'),
    (3, 2, 'Cough Syrup', '2 teaspoons', 'bedtime', 'Cough relief'),
    (4, 3, 'Aspirin', '81mg', 'once daily', 'Heart prevention'),
    (5, 3, 'Vitamin D3', '1000 IU', 'once daily', 'Bone health'),
]

cursor.executemany('INSERT INTO persons VALUES (?, ?, ?, ?)', persons_data)
cursor.executemany('INSERT INTO medications VALUES (?, ?, ?, ?, ?, ?)', medications_data)
conn.commit()

print("[OK] Database created!")
print(f"Location: {os.path.abspath(db_filename)}\n")

print("HOW TO VIEW IN VS CODE:")
print("1. Install extension: 'SQLite' (by alexcvzz)")
print("2. Open Command Palette (Ctrl+Shift+P)")
print("3. Type: 'SQLite: Open Database'")
print("4. Select: medication_dataset.db")
print("5. See tables and data\n")

# Query and display
cursor.execute('''
    SELECT p.name, p.age, m.name as medication, m.dosage, m.frequency
    FROM persons p
    JOIN medications m ON p.id = m.person_id
''')

results = cursor.fetchall()
print("DATABASE CONTENTS:")
print("name           | age | medication        | dosage      | frequency")
print("-" * 80)
for row in results:
    print(f"{row[0]:<14} | {row[1]:<3} | {row[2]:<17} | {row[3]:<11} | {row[4]}")

conn.close()


# ============================================================================
# PART 5: CREATE DATASET AS PYTHON LIST/DICTIONARY
# ============================================================================

print("\n" + "=" * 80)
print("PART 5: CREATE DATASET AS PYTHON DATA STRUCTURE")
print("=" * 80)

print("\nSTEP 4: Create dataset as Python code\n")

print("HOW TO TYPE IN VS CODE:")
print("""
# Option 1: List of dictionaries
dataset = [
    {
        'id': 1,
        'name': 'John Smith',
        'age': 78,
        'medications': ['Paracetamol']
    },
    {
        'id': 2,
        'name': 'Mary Johnson',
        'age': 82,
        'medications': ['Cold & Flu Pills', 'Cough Syrup']
    },
    {
        'id': 3,
        'name': 'Robert Brown',
        'age': 75,
        'medications': ['Aspirin', 'Vitamin D3']
    }
]

# Option 2: Dictionary of lists
dataset = {
    'persons': [
        {'id': 1, 'name': 'John Smith', 'age': 78},
        {'id': 2, 'name': 'Mary Johnson', 'age': 82},
        {'id': 3, 'name': 'Robert Brown', 'age': 75},
    ],
    'medications': [
        {'person_id': 1, 'name': 'Paracetamol', 'dosage': '500mg'},
        {'person_id': 2, 'name': 'Cold & Flu Pills', 'dosage': '1 capsule'},
        {'person_id': 2, 'name': 'Cough Syrup', 'dosage': '2 teaspoons'},
        {'person_id': 3, 'name': 'Aspirin', 'dosage': '81mg'},
        {'person_id': 3, 'name': 'Vitamin D3', 'dosage': '1000 IU'},
    ]
}
""")


# ============================================================================
# PART 6: DATASET COMPARISON
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: WHICH FORMAT TO USE?")
print("=" * 80)

print("""
CSV Format:
  Pros: Simple, Excel-compatible, easy to read
  Cons: Limited structure, no nested data
  Use for: Simple tabular data, Excel export
  File: medication_dataset.csv

JSON Format:
  Pros: Flexible, nested structure, human-readable
  Cons: Can be verbose, slower to parse
  Use for: APIs, web data, complex structures
  File: medication_dataset.json

SQLite Database:
  Pros: Queryable, relational, efficient
  Cons: Need database knowledge
  Use for: Large datasets, relationships, production
  File: medication_dataset.db

Python Data Structure:
  Pros: Native to Python, fast
  Cons: Not shareable, needs serialization
  Use for: In-memory data, temporary use
  File: your_script.py
""")


# ============================================================================
# PART 7: LOAD AND USE DATASET
# ============================================================================

print("\n" + "=" * 80)
print("PART 7: HOW TO LOAD AND USE DATASETS")
print("=" * 80)

print("\nOPTION 1: Load from CSV")
print("-" * 80)
print("""
import csv

with open('medication_dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']}: {row['medication']}")
""")

print("\nOPTION 2: Load from JSON")
print("-" * 80)
print("""
import json

with open('medication_dataset.json', 'r') as f:
    dataset = json.load(f)
    for person in dataset['persons']:
        print(f"{person['name']}: {len(person['medications'])} medications")
""")

print("\nOPTION 3: Load from SQLite")
print("-" * 80)
print("""
import sqlite3

conn = sqlite3.connect('medication_dataset.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM persons')
for person in cursor.fetchall():
    print(person)

conn.close()
""")


# ============================================================================
# PART 8: DATASET STATS
# ============================================================================

print("\n" + "=" * 80)
print("PART 8: YOUR DATASET STATISTICS")
print("=" * 80)

print(f"""
CSV Dataset:
  - File: {csv_filename}
  - Rows: 6 (1 header + 5 data)
  - Columns: 6
  - Size: ~300 bytes
  
JSON Dataset:
  - File: {json_filename}
  - Persons: 3
  - Medications: 5
  - Size: ~1.5 KB
  
SQLite Database:
  - File: {db_filename}
  - Tables: 2 (persons, medications)
  - Records: 3 persons + 5 medications
  - Size: ~4 KB
""")


# ============================================================================
# PART 9: NEXT STEPS
# ============================================================================

print("\n" + "=" * 80)
print("PART 9: NEXT STEPS IN VS CODE")
print("=" * 80)

print("""
1. OPEN THE FILES:
   - File → Open Folder → your_project_folder
   - You'll see the 3 dataset files created:
     * medication_dataset.csv
     * medication_dataset.json
     * medication_dataset.db

2. INSTALL EXTENSIONS:
   - Click Extensions (left sidebar)
   - Search and install:
     * "SQLite" (alexcvzz) - for database viewing
     * "JSON" (esbenp.prettier-vscode) - for JSON formatting

3. VIEW DATASET:
   - CSV: Right-click → Open Preview (or Ctrl+K V)
   - JSON: Click file to open and view structure
   - SQLite: Use 'SQLite: Open Database' command

4. USE IN YOUR CODE:
   - Import the dataset files
   - Load data
   - Train ML models
   - Make predictions

5. EXPAND DATASET:
   - Add more persons
   - Add more medications
   - Add labels for ML training
   - Add features for prediction
""")


# ============================================================================
# PART 10: QUICK REFERENCE
# ============================================================================

print("\n" + "=" * 80)
print("PART 10: QUICK REFERENCE")
print("=" * 80)

print("""
FILES CREATED:
1. medication_dataset.csv      (Tabular format)
2. medication_dataset.json     (Structured format)
3. medication_dataset.db       (Database format)

HOW TO CREATE EACH FORMAT:

CSV:
  import csv
  data = [['name', 'age'], ['John', 78]]
  with open('file.csv', 'w') as f:
      csv.writer(f).writerows(data)

JSON:
  import json
  data = {'persons': [{'name': 'John', 'age': 78}]}
  with open('file.json', 'w') as f:
      json.dump(data, f)

SQLite:
  import sqlite3
  conn = sqlite3.connect('file.db')
  cursor = conn.cursor()
  cursor.execute('CREATE TABLE people (name TEXT, age INT)')
  cursor.execute('INSERT INTO people VALUES (?, ?)', ('John', 78))
  conn.commit()
""")

print("\n" + "=" * 80)
print("DATASETS CREATED SUCCESSFULLY!")
print("=" * 80)
print(f"""
All dataset files are saved in:
{os.getcwd()}

Files created:
✓ {csv_filename}
✓ {json_filename}
✓ {db_filename}

Next: Open these files in VS Code and explore!
""")
