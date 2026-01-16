"""
VIEWING YOUR ML DATASETS IN VS CODE
Step-by-step guide with screenshots explained
"""

print("\n" + "=" * 80)
print("VIEWING YOUR ML DATASETS IN VS CODE")
print("=" * 80)

print("""
You now have 3 ML datasets created:
1. medication_dataset.csv      (Tabular format)
2. medication_dataset.json     (Structured format)
3. medication_dataset.db       (Database format)

All files are in: d:\\Github python\\my_first_project\\

============================================================================
METHOD 1: VIEW CSV FILE IN VS CODE
============================================================================

STEP 1: Open VS Code
  - Click VS Code icon on desktop or taskbar

STEP 2: Open the folder
  - File → Open Folder
  - Select: d:\\Github python\\my_first_project
  - Click Select Folder

STEP 3: Find the CSV file
  - Look at the left sidebar (Explorer)
  - Find: medication_dataset.csv
  - Click on it

STEP 4: View the data
  - CSV opens in text format
  - You'll see:
    person_id,name,age,medication,dosage,frequency
    1,John Smith,78,Paracetamol,500mg,3_times_daily
    2,Mary Johnson,82,Cold & Flu Pills,1_capsule,3_times_daily
    etc.

STEP 5 (OPTIONAL): View as table
  - Right-click on the CSV file
  - Select "Open With..."
  - Look for "CSV Preview" or similar
  - OR: Ctrl+Shift+P → "CSV: Open Preview"
  - You'll see it formatted as a nice table

WHAT YOU'LL SEE:
┌────────────┬──────────────┬─────┬──────────────┬────────┬────────────────┐
│ person_id  │ name         │ age │ medication   │ dosage │ frequency      │
├────────────┼──────────────┼─────┼──────────────┼────────┼────────────────┤
│ 1          │ John Smith   │ 78  │ Paracetamol  │ 500mg  │ 3_times_daily  │
│ 2          │ Mary Johnson │ 82  │ Cold & Flu   │ 1_cap  │ 3_times_daily  │
│ 2          │ Mary Johnson │ 82  │ Cough Syrup  │ 2_tsp  │ bedtime        │
│ 3          │ Robert Brown │ 75  │ Aspirin      │ 81mg   │ once_daily     │
│ 3          │ Robert Brown │ 75  │ Vitamin D3   │ 1000IU │ once_daily     │
└────────────┴──────────────┴─────┴──────────────┴────────┴────────────────┘

============================================================================
METHOD 2: VIEW JSON FILE IN VS CODE
============================================================================

STEP 1: In left sidebar, find: medication_dataset.json
STEP 2: Click on it to open
STEP 3: You'll see the JSON structure:

{
  "metadata": {
    "name": "Medication Dataset",
    "version": "1.0",
    "created": "2025-11-27T...",
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
    ... more persons ...
  ]
}

STEP 4: Click arrows to expand/collapse sections
  - Click arrow next to "metadata" to show/hide
  - Click arrow next to "persons" to show/hide
  - Click arrow next to each person to expand details

FEATURES:
✓ Syntax highlighting (colors different parts)
✓ Collapsible sections (arrows to hide/show)
✓ Line numbers (on left side)
✓ Error detection (red squiggles if invalid)

============================================================================
METHOD 3: VIEW SQLITE DATABASE IN VS CODE
============================================================================

STEP 1: Install SQLite extension
  - Click Extensions icon (left sidebar, looks like squares)
  - Search for: "SQLite"
  - Install: "SQLite" by alexcvzz (has many downloads)

STEP 2: Open the database
  - Open Command Palette: Ctrl+Shift+P
  - Type: "SQLite: Open Database"
  - Press Enter
  - Find: medication_dataset.db
  - Click on it

STEP 3: View the schema
  - A new panel appears on the left
  - You'll see:
    medication_dataset.db
    ├── persons (table)
    │   ├── id (INTEGER)
    │   ├── name (TEXT)
    │   ├── age (INTEGER)
    │   └── phone (TEXT)
    └── medications (table)
        ├── id (INTEGER)
        ├── person_id (INTEGER)
        ├── name (TEXT)
        ├── dosage (TEXT)
        ├── frequency (TEXT)
        └── reason (TEXT)

STEP 4: View table data
  - Right-click on "persons" table
  - Click "Show Table"
  - A new tab opens showing all rows:

    id | name           | age | phone
    ---|----------------|-----|----------
    1  | John Smith     | 78  | 555-0101
    2  | Mary Johnson   | 82  | 555-0102
    3  | Robert Brown   | 75  | 555-0103

STEP 5: Run SQL queries
  - Right-click on the database name
  - Click "Run Query"
  - Type SQL:
    SELECT * FROM medications
    WHERE person_id = 2;
  - Results show below

WHAT YOU'LL SEE:
id | person_id | name            | dosage      | frequency | reason
---|-----------|-----------------|-------------|-----------|--------
2  | 2         | Cold & Flu Pills| 1 capsule   | 3 times   | Symptoms
3  | 2         | Cough Syrup     | 2 teaspoons | bedtime   | Cough

============================================================================
METHOD 4: VIEW ALL TOGETHER
============================================================================

In VS Code you can open all 3 at once:

TAB 1: medication_dataset.csv (left side shows table format)
TAB 2: medication_dataset.json (left side shows tree structure)
TAB 3: medication_dataset.db (left side shows SQLite explorer)

Click between tabs to switch views!

============================================================================
QUICK KEYBOARD SHORTCUTS
============================================================================

Ctrl+P                → Open file quickly (type filename)
Ctrl+Shift+P          → Open Command Palette (type command)
Ctrl+K Ctrl+V         → Preview markdown file
Ctrl+/                → Toggle comment
Ctrl+S                → Save file
Ctrl+Z                → Undo
Ctrl+Y                → Redo

For CSV:
  Right-click → "Open Preview" (if extension installed)

For JSON:
  Ctrl+Shift+P → "JSON: Format Document"

For SQLite:
  Ctrl+Shift+P → "SQLite: Open Database"
  Ctrl+Shift+P → "SQLite: Run Query"

============================================================================
TROUBLESHOOTING
============================================================================

CSV not showing as table?
  → Right-click → "Open With..." → Select CSV extension
  → Or: Ctrl+Shift+P → "CSV: Open Preview"

JSON has red squiggles?
  → Check for missing commas or brackets
  → Ctrl+Shift+P → "JSON: Format Document"

SQLite database won't open?
  → Make sure extension "SQLite" is installed
  → Ctrl+Shift+P → "Extensions: Show Installed"
  → Search for SQLite

Files not visible in explorer?
  → Check: File → Open Folder → correct path
  → Verify files are in d:\\Github python\\my_first_project\\

============================================================================
PRACTICE TASKS
============================================================================

TASK 1: View CSV
  1. Open medication_dataset.csv
  2. Find how many medications John Smith has
  3. What dosage does Mary Johnson take for Cough Syrup?

TASK 2: View JSON
  1. Open medication_dataset.json
  2. Expand "persons" → click person "Mary Johnson"
  3. How many medications does she have?
  4. What's the reason for each medication?

TASK 3: View SQLite
  1. Install SQLite extension
  2. Open medication_dataset.db
  3. Click "persons" table → "Show Table"
  4. Click "medications" table → "Show Table"
  5. Right-click database → "Run Query"
  6. Type: SELECT * FROM medications WHERE person_id = 1;
  7. How many results?

============================================================================
NEXT STEPS
============================================================================

✓ Datasets created in 3 formats
✓ You know how to view each format
✓ You can explore the data

Next: Use these datasets for your ML project!

1. Load the data in Python
2. Extract features and labels
3. Train your ML model
4. Make predictions

See use_ml_datasets.py for examples!
""")

print("\n" + "=" * 80)
print("YOUR DATASETS ARE READY!")
print("=" * 80)
