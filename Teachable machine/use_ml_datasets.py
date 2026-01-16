"""
ML DATASET USAGE - TRAINING EXAMPLE
How to use your datasets for machine learning
"""

import csv
import json
import sqlite3
from datetime import datetime


print("\n" + "=" * 80)
print("HOW TO USE ML DATASETS FOR TRAINING")
print("=" * 80)


# ============================================================================
# EXAMPLE 1: LOAD CSV AND PREPARE FOR ML
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Load CSV and Prepare Data")
print("=" * 80)

print("\nCode to type in VS Code:\n")
print("""
import csv

# STEP 1: Load data from CSV
def load_csv_data(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# STEP 2: Use the data
dataset = load_csv_data('medication_dataset.csv')

# STEP 3: Print each record
for record in dataset:
    print(f"{record['name']}: {record['medication']}")

# STEP 4: Extract features for ML
names = [row['name'] for row in dataset]
ages = [int(row['age']) for row in dataset]
medications = [row['medication'] for row in dataset]

print(f"Names: {names}")
print(f"Ages: {ages}")
print(f"Medications: {medications}")
""")

# Actually run this example
print("\n--- RUNNING THE CODE ---\n")

def load_csv_data(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

dataset = load_csv_data('medication_dataset.csv')

print("[OUTPUT]:\n")
for record in dataset:
    print(f"{record['name']}: {record['medication']}")

# Extract features for ML
names = [row['name'] for row in dataset]
ages = [int(row['age']) for row in dataset]
medications = [row['medication'] for row in dataset]

print(f"\nNames: {names}")
print(f"Ages: {ages}")
print(f"Medications: {medications}")


# ============================================================================
# EXAMPLE 2: LOAD JSON AND PREPARE FOR ML
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Load JSON and Prepare Data")
print("=" * 80)

print("\nCode to type in VS Code:\n")
print("""
import json

# STEP 1: Load data from JSON
def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# STEP 2: Use the data
dataset = load_json_data('medication_dataset.json')

# STEP 3: Loop through persons
for person in dataset['persons']:
    print(f"{person['name']}, Age {person['age']}")
    for med in person['medications']:
        print(f"  - {med['name']}: {med['frequency']}")

# STEP 4: Extract features for ML
features = []
for person in dataset['persons']:
    features.append({
        'name': person['name'],
        'age': person['age'],
        'medication_count': len(person['medications']),
        'medications': [m['name'] for m in person['medications']]
    })

print(f"\\nTotal persons: {len(features)}")
""")

# Actually run this example
print("\n--- RUNNING THE CODE ---\n")

def load_json_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

dataset = load_json_data('medication_dataset.json')

print("[OUTPUT]:\n")
for person in dataset['persons']:
    print(f"{person['name']}, Age {person['age']}")
    for med in person['medications']:
        print(f"  - {med['name']}: {med['frequency']}")

features = []
for person in dataset['persons']:
    features.append({
        'name': person['name'],
        'age': person['age'],
        'medication_count': len(person['medications']),
        'medications': [m['name'] for m in person['medications']]
    })

print(f"\nTotal persons: {len(features)}")


# ============================================================================
# EXAMPLE 3: LOAD FROM SQLITE AND PREPARE FOR ML
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Load from SQLite and Prepare Data")
print("=" * 80)

print("\nCode to type in VS Code:\n")
print("""
import sqlite3

# STEP 1: Connect to database
conn = sqlite3.connect('medication_dataset.db')
cursor = conn.cursor()

# STEP 2: Query data
cursor.execute('SELECT * FROM persons')
persons = cursor.fetchall()

# STEP 3: Print persons
print("Persons in database:")
for person in persons:
    person_id, name, age, phone = person
    print(f"  ID: {person_id}, Name: {name}, Age: {age}")

# STEP 4: Query medications
cursor.execute('''
    SELECT p.name, m.name, m.dosage
    FROM persons p
    JOIN medications m ON p.id = m.person_id
''')
results = cursor.fetchall()

print("\\nMedication pairs:")
for row in results:
    print(f"  {row[0]}: {row[1]} ({row[2]})")

conn.close()
""")

# Actually run this example
print("\n--- RUNNING THE CODE ---\n")

conn = sqlite3.connect('medication_dataset.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM persons')
persons = cursor.fetchall()

print("[OUTPUT]:\n")
print("Persons in database:")
for person in persons:
    person_id, name, age, phone = person
    print(f"  ID: {person_id}, Name: {name}, Age: {age}")

cursor.execute('''
    SELECT p.name, m.name, m.dosage
    FROM persons p
    JOIN medications m ON p.id = m.person_id
''')
results = cursor.fetchall()

print("\nMedication pairs:")
for row in results:
    print(f"  {row[0]}: {row[1]} ({row[2]})")

conn.close()


# ============================================================================
# EXAMPLE 4: PREPARE DATA FOR ML TRAINING
# ============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Prepare Data for ML Training")
print("=" * 80)

print("\nCode to type in VS Code:\n")
print("""
# Simple ML dataset preparation

# STEP 1: Create training data (features and labels)
training_data = [
    # Features: [age, medication_count] -> Label: [risk_level]
    ([78, 1], 'low'),      # John: 78 years old, 1 medication -> low risk
    ([82, 2], 'high'),     # Mary: 82 years old, 2 medications -> high risk
    ([75, 2], 'medium'),   # Robert: 75 years old, 2 medications -> medium risk
]

# STEP 2: Extract features and labels
X = [data[0] for data in training_data]  # Features
y = [data[1] for data in training_data]  # Labels

print("Features (X):")
for i, features in enumerate(X):
    print(f"  Person {i+1}: age={features[0]}, med_count={features[1]}")

print("\\nLabels (y):")
for i, label in enumerate(y):
    print(f"  Person {i+1}: {label} risk")

# STEP 3: Simple prediction (example)
def predict_risk(age, medication_count):
    if age >= 80 and medication_count >= 2:
        return 'high'
    elif age >= 75 and medication_count >= 2:
        return 'medium'
    else:
        return 'low'

# Test predictions
print("\\nTest predictions:")
test_ages = [78, 82, 75]
test_med_counts = [1, 2, 2]
for age, med_count in zip(test_ages, test_med_counts):
    risk = predict_risk(age, med_count)
    print(f"  Age {age}, {med_count} meds -> {risk} risk")
""")

# Actually run this example
print("\n--- RUNNING THE CODE ---\n")

training_data = [
    ([78, 1], 'low'),
    ([82, 2], 'high'),
    ([75, 2], 'medium'),
]

X = [data[0] for data in training_data]
y = [data[1] for data in training_data]

print("[OUTPUT]:\n")
print("Features (X):")
for i, features in enumerate(X):
    print(f"  Person {i+1}: age={features[0]}, med_count={features[1]}")

print("\nLabels (y):")
for i, label in enumerate(y):
    print(f"  Person {i+1}: {label} risk")

def predict_risk(age, medication_count):
    if age >= 80 and medication_count >= 2:
        return 'high'
    elif age >= 75 and medication_count >= 2:
        return 'medium'
    else:
        return 'low'

print("\nTest predictions:")
test_ages = [78, 82, 75]
test_med_counts = [1, 2, 2]
for age, med_count in zip(test_ages, test_med_counts):
    risk = predict_risk(age, med_count)
    print(f"  Age {age}, {med_count} meds -> {risk} risk")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY: STEPS TO BUILD AND USE ML DATASETS")
print("=" * 80)

print("""
STEP 1: CREATE YOUR DATASET
  Option A: CSV (simple, Excel-compatible)
  Option B: JSON (flexible, structured)
  Option C: SQLite (queryable, relational)
  Option D: Python code (native, fast)

STEP 2: LOAD THE DATA
  CSV:    csv.DictReader()
  JSON:   json.load()
  SQLite: sqlite3.connect() + cursor.execute()
  Python: Direct list/dictionary

STEP 3: EXPLORE THE DATA
  Print records
  Check data types
  Look for patterns

STEP 4: EXTRACT FEATURES
  Features = Input values (age, symptoms, etc)
  Labels = Output values (diagnosis, medication, etc)
  Create [features] -> label pairs

STEP 5: PREPARE FOR ML
  Normalize data (scale values 0-1)
  Split into training/testing sets
  Remove missing values

STEP 6: TRAIN MODEL
  Use features and labels
  Train ML algorithm (decision tree, neural network, etc)

STEP 7: TEST AND PREDICT
  Test on new data
  Make predictions

SAMPLE CODE TEMPLATE:
  
  import csv/json/sqlite3
  
  # Load
  data = load_data('file')
  
  # Extract features
  X = [features for each record]
  y = [labels for each record]
  
  # Train
  model = train(X, y)
  
  # Predict
  prediction = model.predict(new_data)
""")

print("\n" + "=" * 80)
print("YOUR DATASET IS READY TO USE!")
print("=" * 80)
