"""
MAIN STARTUP SCRIPT
Run this to start the medication management system
"""

import sys
import os
from pathlib import Path

# Add code directory to path
code_dir = Path(__file__).parent.parent / 'code'
sys.path.insert(0, str(code_dir))

# Check if code files exist
required_files = [
    'elder_medication_system.py',
    'personalized_medications.py',
    'Second_Program_with_Teachable_Machine.py'
]

missing = []
for file in required_files:
    if not (code_dir / file).exists():
        missing.append(file)

if missing:
    print("[ERROR] Missing files:")
    for f in missing:
        print(f"  - {f}")
    sys.exit(1)

print("[STARTING] Medication Management System")
print("[PATH] Using code directory:", code_dir)

# Import and run main program
from Second_Program_with_Teachable_Machine import main

try:
    main()
except KeyboardInterrupt:
    print("\n[EXIT] Program terminated by user")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
