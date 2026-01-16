# HOW TO BUILD ML DATASETS IN VS CODE - COMPLETE SUMMARY

## What You Just Created

You now have a complete ML dataset system with 4 Python files and 3 dataset formats:

### Files Created:
1. **build_ml_datasets.py** - Creates all 3 dataset formats
2. **use_ml_datasets.py** - Shows how to load and use datasets
3. **view_datasets_in_vscode.py** - Guide to viewing datasets in VS Code
4. **medication_dataset.csv** - Tabular format (6 columns, 5 data rows)
5. **medication_dataset.json** - Structured format (3 persons, 5 medications)
6. **medication_dataset.db** - SQLite database (2 tables, 8 records)

---

## Quick Start: 3 Steps

### STEP 1: Run to Create Datasets
```bash
cd "d:\Github python\my_first_project"
python build_ml_datasets.py
```

Result: 3 dataset files created ✓

### STEP 2: Run to Learn How to Use
```bash
python use_ml_datasets.py
```

Result: 4 examples showing how to load and prepare data ✓

### STEP 3: Run to Learn How to View
```bash
python view_datasets_in_vscode.py
```

Result: Guide to viewing in VS Code ✓

---

## Dataset Formats Explained

### CSV Format (medication_dataset.csv)
**Best for:** Simple tabular data, Excel compatibility

```
person_id,name,age,medication,dosage,frequency
1,John Smith,78,Paracetamol,500mg,3_times_daily
2,Mary Johnson,82,Cold & Flu Pills,1_capsule,3_times_daily
2,Mary Johnson,82,Cough Syrup,2_teaspoons,bedtime
3,Robert Brown,75,Aspirin,81mg,once_daily
3,Robert Brown,75,Vitamin D3,1000_IU,once_daily
```

### JSON Format (medication_dataset.json)
**Best for:** Flexible structure, nested data

```json
{
  "metadata": {...},
  "persons": [
    {
      "id": 1,
      "name": "John Smith",
      "age": 78,
      "medications": [...]
    }
  ]
}
```

### SQLite Database (medication_dataset.db)
**Best for:** Large datasets, relational data, queries

```
Tables:
- persons (id, name, age, phone)
- medications (id, person_id, name, dosage, frequency, reason)
```

---

## How to Use in Your Code

### Load from CSV:
```python
import csv

with open('medication_dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']}: {row['medication']}")
```

### Load from JSON:
```python
import json

with open('medication_dataset.json', 'r') as f:
    data = json.load(f)
    for person in data['persons']:
        print(f"{person['name']}: {len(person['medications'])} meds")
```

### Load from SQLite:
```python
import sqlite3

conn = sqlite3.connect('medication_dataset.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM persons')
for person in cursor.fetchall():
    print(person)

conn.close()
```

---

## How to View in VS Code

### View CSV:
1. Open folder: File → Open Folder → d:\Github python\my_first_project
2. Click on medication_dataset.csv in left sidebar
3. See data in text or table format

### View JSON:
1. Click on medication_dataset.json
2. Click arrows to expand/collapse sections
3. See structured data with syntax highlighting

### View SQLite:
1. Install "SQLite" extension (left sidebar)
2. Ctrl+Shift+P → "SQLite: Open Database"
3. Click medication_dataset.db
4. See tables and run queries

---

## For ML Training

### Step-by-Step Process:

```python
# 1. Load data
data = load_from_csv_or_json_or_sqlite()

# 2. Extract features (inputs) and labels (outputs)
features = [[person['age'], len(person['medications'])] for person in data]
labels = ['low_risk', 'high_risk', 'medium_risk']

# 3. Prepare data
X = features  # Input features
y = labels    # Output labels

# 4. Train model (example: simple rule-based)
def predict(age, med_count):
    if age >= 80 and med_count >= 2:
        return 'high_risk'
    return 'low_risk'

# 5. Test predictions
print(predict(82, 2))  # Output: high_risk
```

---

## Dataset Contents

### Persons:
- **John Smith**, 78 years old, 1 medication
- **Mary Johnson**, 82 years old, 2 medications
- **Robert Brown**, 75 years old, 2 medications

### Medications:
- Paracetamol (500mg, 3x daily)
- Cold & Flu Pills (1 capsule, 3x daily)
- Cough Syrup (2 teaspoons, bedtime)
- Aspirin (81mg, once daily)
- Vitamin D3 (1000 IU, once daily)

---

## Common Tasks

### Q: How do I add more data?
A: Edit the files:
- CSV: Add new rows
- JSON: Add to "persons" array
- SQLite: Use INSERT statements

### Q: How do I query the data?
A: Use the format that suits your need:
- CSV: Simple with csv.DictReader()
- JSON: Flexible with json.load()
- SQLite: Powerful with SQL queries

### Q: How do I prepare for ML?
A: Run use_ml_datasets.py to see 4 examples

### Q: How do I expand the dataset?
A: 
- Add more persons
- Add more medications
- Add labels for supervised learning
- Add features for prediction

---

## Keyboard Shortcuts in VS Code

| Shortcut | Action |
|----------|--------|
| Ctrl+P | Open file quickly |
| Ctrl+Shift+P | Command Palette |
| Ctrl+S | Save |
| Ctrl+/ | Toggle comment |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |

---

## Next Steps

1. **Explore the datasets**: Open each file in VS Code
2. **Run the examples**: Execute use_ml_datasets.py
3. **Load into your code**: Copy examples and modify
4. **Expand the data**: Add more persons/medications
5. **Build ML model**: Use features and labels to train
6. **Make predictions**: Test your model

---

## Files Location

```
d:\Github python\my_first_project\
├── build_ml_datasets.py           (creates datasets)
├── use_ml_datasets.py             (usage examples)
├── view_datasets_in_vscode.py     (viewing guide)
├── medication_dataset.csv         (tabular data)
├── medication_dataset.json        (structured data)
└── medication_dataset.db          (database)
```

---

## Summary

✅ Created 3 ML datasets in different formats
✅ Learned how to view in VS Code
✅ Learned how to load in Python code
✅ Learned how to prepare for ML training
✅ Ready to build your ML model!

Your ML dataset infrastructure is complete and ready to use!
